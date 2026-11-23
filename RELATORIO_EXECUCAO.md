# 📋 Relatório de Execução — P0 (TRENDS+IA)

- **Projeto:** English Tutor Assistant (CLI bilíngue com Google Gemini)
- **Repositório:** https://github.com/24202105-web/Capacitacao_TRENDSIA_P0
- **Vídeo de Demonstração:** [INSERIR_LINK_DO_VIDEO_AQUI]

---

## 1. Evolução por Nível

- **Nível Básico (`p0-basico`):** Construção da menor chamada funcional à API do Google Gemini (`google-genai`) via terminal, enviando uma frase em inglês com instrução fixa para receber correção gramatical e resposta bilíngue (inglês e português).
- **Nível Intermediário (`p0-intermediario`):** Separação entre interface de terminal (`app.py`) e regras de negócio (`tutor.py`), proteção de credenciais com `.env`, `.env.example` e `.gitignore`, validação de entradas vazias e tratamento amigável de erros de autenticação, cota/indisponibilidade (`503`) e falhas de rede.
- **Nível Avançado (`p0-avancado`):** Externalização de parâmetros do LLM e comportamento do tutor (`config.py` + `.env`), adição de logs operacionais seguros sem dados sensíveis (`execucao.log`), criação de suíte de testes unitários offline com *mocks* (`tests/test_tutor.py`), documentação reproduzível e validação em ambiente virtual limpo.

---

## 2. Decisões Principais

| Decisão Tomada | Alternativa Considerada | Justificativa |
| :--- | :--- | :--- |
| **Desacoplar parâmetros do LLM em `config.py` e `.env`** | Manter `SYSTEM_PROMPT`, modelo, temperatura e limite de tokens fixos no código (`tutor.py`). | Permite alterar comportamento e hiperparâmetros sem modificar o núcleo da aplicação, facilitando testes e reprodutibilidade por terceiros. |
| **Substituir `sys.exit(1)` na configuração por exceção `ConfiguracaoError`** | Encerrar o processo diretamente dentro da função de carregamento de configuração. | Encerrar o processo abruptamente dificulta testes automatizados; lançar exceção permite que `app.py` trate o erro na CLI e que o `unittest` valide cenários de falha isoladamente. |
| **Registrar apenas metadados técnicos no `execucao.log`** | Gravar o texto completo das mensagens, respostas do modelo ou stacktraces brutos no log. | Protege credenciais, dados pessoais e conteúdo do usuário contra exposição acidental, mantendo métricas úteis para diagnóstico (modelo, tamanho do texto, latência em ms e código de erro). |
| **Usar `unittest` e `unittest.mock` nativos para testes offline** | Adicionar frameworks externos (como `pytest`) ou depender apenas de chamadas reais à API. | Evita dependências adicionais e permite validar configuração, entradas, respostas simuladas, erros de API e sanitização de logs sem internet ou gasto de cota. |

---

## 3. Testes e Resultados

| Teste | Entrada ou situação | Resultado esperado | Resultado obtido |
| :--- | :--- | :--- | :--- |
| **Configuração válida (Simulado)** | Variáveis `GEMINI_API_KEY`, `GEMINI_MODEL`, `GEMINI_TEMPERATURE=0.2` e `GEMINI_MAX_OUTPUT_TOKENS=150` definidas no ambiente | Carregar `TutorConfig` com os valores customizados sem erro | **Passou** (`test_carregar_configuracao_customizada` — OK) |
| **Credencial ausente ou placeholder (Simulado e Real)** | `GEMINI_API_KEY` vazia ou igual a `sua_chave_aqui` | Lançar `ConfiguracaoError` e exibir orientação clara sem chamar a API | **Passou** (`test_carregar_configuracao_sem_api_key_falha` e `placeholder_falha` — OK) |
| **Parâmetro fora do intervalo (Simulado)** | `GEMINI_TEMPERATURE=5.0` | Rejeitar configuração inválida com `ConfiguracaoError` | **Passou** (`test_carregar_configuracao_temperatura_invalida_falha` — OK) |
| **Entrada vazia no terminal (Simulado e Real)** | Usuário pressiona `Enter` ou envia apenas espaços (`"   "`) | Bloquear envio antes de chamar o LLM e alertar no terminal | **Passou** (`test_validacao_entrada_vazia_nao_chama_llm` — OK) |
| **Correção gramatical bilíngue (Real)** | `"I goes to store yesterday"` com API real ativa | Corrigir tempo verbal (`went`), explicar em inglês/português e fazer nova pergunta | **Passou** (resposta bilíngue retornada no terminal) |
| **Resposta simulada de sucesso (Simulado)** | Mock retornando `"Great sentence! What did you do yesterday?"` | Retornar string tratada e registrar métricas no log | **Passou** (`test_processar_mensagem_resposta_simulada` — OK) |
| **Indisponibilidade da API (Simulado)** | Mock lançando `APIError` com código `503` (`UNAVAILABLE`) | Exibir aviso amigável de indisponibilidade sem stacktrace e retornar `None` | **Passou** (`test_tratamento_erro_api_simulado` — OK) |
| **Sanitização de logs (Simulado e Real)** | Envio de mensagem com chave secreta configurada | `execucao.log` registra apenas `chars_entrada` e latência, sem chave ou textos | **Passou** (`test_logs_nao_armazenam_chave_ou_conteudo_sensivel` — OK) |

---

## 4. Falhas e Limitações

### Dificuldades encontradas e tratadas
1. **Acoplamento inicial com `sys.exit(1)` e falha em asserção de teste:**
   - **O que aconteceu:** Na versão intermediária, `carregar_configuracao()` encerrava o programa diretamente com `sys.exit(1)`, impedindo testes unitários diretos. Além disso, durante a criação dos testes de log, uma asserção esperava `chars_entrada=31` para uma frase de 32 caracteres.
   - **Como foi identificado:** Durante a refatoração para testes automatizados e na execução de `python -m unittest discover -s tests -v`.
   - **Como foi tratado:** A validação de configuração passou a lançar `ConfiguracaoError` (tratada no `app.py`) e a asserção do teste foi corrigida para `chars_entrada=32`, atingindo 100% de aprovação (8/8 testes).

### Limitações conhecidas (permanecem no escopo atual)
1. **Ausência de memória entre turnos:** Cada frase enviada é tratada como uma requisição independente, sem histórico das mensagens anteriores da sessão. Permanece assim para manter a arquitetura simples, previsível e dentro de um orçamento fixo de tokens por chamada.
2. **Interação restrita a texto via CLI e dependência de API externa:** A aplicação não avalia pronúncia/áudio e depende de conexão com a internet e disponibilidade da API do Google Gemini.

---

## 5. Uso de IA no Desenvolvimento

- **Ferramenta utilizada:** Google Gemini.
- **Tarefa delegada:** Apoio na modularização da arquitetura (`config.py`, `tutor.py`, `app.py`), definição do formato de logs seguros sem dados sensíveis, estruturação dos testes offline com `unittest.mock` e revisão da documentação (`README.md` e `RELATORIO_EXECUCAO.md`).
- **Resultado aproveitado:** Estrutura de configuração tipada com `@dataclass`, isolamento das chamadas de API para permitir *mocks* e organização clara dos artefatos de entrega.
- **Correções e alterações realizadas:** Ajuste na contagem esperada de caracteres no teste de sanitização de logs (`32` caracteres), atualização da URL do repositório remoto no GitHub (`Capacitacao_TRENDSIA_P0`) e revisão das mensagens de erro para refletir o comportamento real do CLI.
- **Forma de verificação:** Execução da suíte completa de testes offline (`python -m unittest discover -s tests -v`), validação da instalação em ambiente virtual limpo seguindo o `README.md` e testes reais no terminal inspecionando o conteúdo gerado em `execucao.log`.

---

## 6. Reflexão Final

- **Principal aprendizado:** Construir uma solução com LLM pronta para entrega exige muito mais do que ajustar um prompt: é indispensável separar configurações do núcleo do código, proteger credenciais, evitar vazamento de informações sensíveis nos registros de execução e documentar o ambiente para que qualquer pessoa consiga reproduzir o projeto sem auxílio.
- **Competência mais desenvolvida:** Organização modular em Python combinada à criação de testes unitários offline com *mocks* para simular respostas e falhas da API, além do uso disciplinado do histórico do Git com commits incrementais e tags de versão.
- **Aspecto que ainda precisa ser aprimorado:** Adicionar gerenciamento controlado de histórico conversacional (memória de curto prazo entre turnos com limite de contexto) e ampliar os testes de ponta a ponta.
