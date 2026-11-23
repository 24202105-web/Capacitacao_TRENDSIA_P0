import logging
import os
import tempfile
import unittest
from unittest.mock import MagicMock, patch
from google.genai.errors import APIError
from config import ConfiguracaoError, TutorConfig, carregar_configuracao
from tutor import preparar_config_geracao, processar_mensagem


class TestTutorOffline(unittest.TestCase):
    def setUp(self):
        self.config_valida = TutorConfig(
            api_key="CHAVE_SECRETA_TESTE_999",
            model="gemini-3.5-flash-lite",
            temperature=0.4,
            max_output_tokens=300,
            system_prompt="You are an English tutor.",
        )

    @patch.dict(os.environ, {}, clear=True)
    def test_carregar_configuracao_sem_api_key_falha(self):
        with self.assertRaises(ConfiguracaoError):
            carregar_configuracao(carregar_dotenv=False)

    @patch.dict(os.environ, {"GEMINI_API_KEY": "sua_chave_aqui"}, clear=True)
    def test_carregar_configuracao_placeholder_falha(self):
        with self.assertRaises(ConfiguracaoError):
            carregar_configuracao(carregar_dotenv=False)

    @patch.dict(
        os.environ,
        {
            "GEMINI_API_KEY": "chave_valida_teste",
            "GEMINI_MODEL": "gemini-2.5-flash",
            "GEMINI_TEMPERATURE": "0.2",
            "GEMINI_MAX_OUTPUT_TOKENS": "150",
            "TUTOR_SYSTEM_PROMPT": "Custom prompt",
        },
        clear=True,
    )
    def test_carregar_configuracao_customizada(self):
        cfg = carregar_configuracao(carregar_dotenv=False)
        self.assertEqual(cfg.model, "gemini-2.5-flash")
        self.assertEqual(cfg.temperature, 0.2)
        self.assertEqual(cfg.max_output_tokens, 150)
        self.assertEqual(cfg.system_prompt, "Custom prompt")

    def test_preparacao_config_geracao(self):
        gen_cfg = preparar_config_geracao(self.config_valida)
        self.assertEqual(gen_cfg.temperature, 0.4)
        self.assertEqual(gen_cfg.max_output_tokens, 300)
        self.assertEqual(gen_cfg.system_instruction, "You are an English tutor.")

    def test_validacao_entrada_vazia_nao_chama_llm(self):
        client_mock = MagicMock()
        resultado = processar_mensagem(client_mock, self.config_valida, "    ")
        self.assertIsNone(resultado)
        client_mock.models.generate_content.assert_not_called()

    def test_processar_mensagem_resposta_simulada(self):
        client_mock = MagicMock()
        client_mock.models.generate_content.return_value.text = (
            "Great sentence! What did you do yesterday?"
        )

        resposta = processar_mensagem(client_mock, self.config_valida, "I like studying Python.")
        self.assertEqual(resposta, "Great sentence! What did you do yesterday?")
        client_mock.models.generate_content.assert_called_once()

    def test_tratamento_erro_api_simulado(self):
        client_mock = MagicMock()
        client_mock.models.generate_content.side_effect = APIError(
            code=503,
            response_json={"error": {"message": "Model overloaded", "status": "UNAVAILABLE"}},
        )

        resposta = processar_mensagem(client_mock, self.config_valida, "Hello!")
        self.assertIsNone(resposta)

    def test_logs_nao_armazenam_chave_ou_conteudo_sensivel(self):
        client_mock = MagicMock()
        client_mock.models.generate_content.return_value.text = "Secret response content"

        with tempfile.NamedTemporaryFile(mode="r+", delete=False, encoding="utf-8") as tmp:
            caminho_log = tmp.name

        logger_tutor = logging.getLogger("tutor_ingles")
        handlers_originais = list(logger_tutor.handlers)
        logger_tutor.handlers.clear()

        try:
            handler = logging.FileHandler(caminho_log, encoding="utf-8")
            logger_tutor.addHandler(handler)
            logger_tutor.setLevel(logging.INFO)

            processar_mensagem(
                client_mock, self.config_valida, "My personal secret message 12345"
            )
            handler.flush()
            handler.close()

            with open(caminho_log, "r", encoding="utf-8") as f:
                conteudo_log = f.read()

            self.assertNotIn("CHAVE_SECRETA_TESTE_999", conteudo_log)
            self.assertNotIn("My personal secret message 12345", conteudo_log)
            self.assertNotIn("Secret response content", conteudo_log)
            self.assertIn("chars_entrada=31", conteudo_log)
        finally:
            logger_tutor.handlers.clear()
            logger_tutor.handlers.extend(handlers_originais)
            if os.path.exists(caminho_log):
                os.remove(caminho_log)


if __name__ == "__main__":
    unittest.main()