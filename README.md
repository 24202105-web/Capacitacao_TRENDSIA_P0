# 🇬🇧 English Tutor Assistant — P0 (TRENDS+IA)

Aplicação CLI em Python que atua como tutor de inglês para estudantes brasileiros utilizando a API do Google Gemini, oferecendo correções gramaticais, elogios e continuidade de diálogo de forma bilíngue (inglês e português).

Entrega consolidada do **P0 — Nível Avançado (`p0-avancado`)**.

---

## 🏗️ Estrutura do Projeto

```text
Capacitacao_TRENDSIA/
├── tests/
│   └── test_tutor.py      # Testes unitários offline (sem chamadas reais à API)
├── .env.example           # Modelo de variáveis de ambiente e parâmetros do LLM
├── .gitignore             # Ignora .env, ambientes virtuais e arquivos .log
├── app.py                 # Interface de linha de comando (CLI)
├── config.py              # Carregamento e validação das configurações externas
├── tutor.py               # Núcleo de comunicação com o Gemini, logs e tratamento de erros
├── requirements.txt       # Dependências do projeto
└── README.md              # Documentação do projeto
```

---

## 🛠️ Stack e Versões

- **Python:** `3.12` *(compatível com Python 3.10+)*
- **Bibliotecas principais:**
  - `google-genai` (SDK oficial do Google Gemini)
  - `python-dotenv` (gerenciamento de variáveis de ambiente)
  - `unittest` / `unittest.mock` (biblioteca padrão do Python para testes offline)
- **Modelo padrão:** `gemini-3.5-flash-lite`

---

## 🚀 Instalação e Configuração

### 1. Clonar o repositório
```bash
git clone https://github.com/24202105-web/Capacitacao_TRENDSIA.git
cd Capacitacao_TRENDSIA
```

### 2. Criar e ativar o ambiente virtual
```bash
python -m venv .venv
```
* **Windows (PowerShell):**
  ```powershell
  .\.venv\Scripts\Activate.ps1
  ```
* **Linux / macOS:**
  ```bash
  source .venv/bin/activate
  ```

### 3. Instalar as dependências
```bash
pip install -r requirements.txt
```

### 4. Configurar variáveis de ambiente
Copie o arquivo de exemplo para `.env`:
* **Windows (PowerShell):** `Copy-Item .env.example .env`
* **Linux / macOS:** `cp .env.example .env`

Edite o `.env` e preencha sua chave obtida no [Google AI Studio](https://aistudio.google.com/). Os parâmetros do LLM podem ser ajustados nesse arquivo sem alterar o código-fonte:

| Variável | Obrigatória | Padrão | Descrição |
| :--- | :---: | :--- | :--- |
| `GEMINI_API_KEY` | Sim | — | Chave de autenticação da API do Google Gemini |
| `GEMINI_MODEL` | Não | `gemini-3.5-flash-lite` | Modelo utilizado na geração de respostas |
| `GEMINI_TEMPERATURE` | Não | `0.7` | Criatividade das respostas (`0.0` a `2.0`) |
| `GEMINI_MAX_OUTPUT_TOKENS` | Não | `500` | Limite máximo de tokens por resposta |
| `TUTOR_SYSTEM_PROMPT` | Não | *Prompt bilíngue* | Instrução de comportamento do tutor |
| `LOG_LEVEL` | Não | `INFO` | Nível de registro (`INFO`, `WARNING`, `ERROR`) |
| `LOG_FILE` | Não | `execucao.log` | Arquivo local de logs operacionais |

---

## ▶️ Execução e Testes

### Executar a aplicação
```bash
python app.py
```
Digite suas frases em inglês no terminal. Para encerrar, digite `sair`, `exit` ou `quit`.

### Executar os testes unitários (offline)
Os testes validam configuração, entradas inválidas, preparação de parâmetros, resposta simulada, erro simulado e sanitização de logs sem consumir cota da API:
```bash
python -m unittest discover -s tests -v
```

---

## 🛡️ Resiliência, Segurança e Logs

- **Validação preventiva:** bloqueia entradas vazias no terminal e valida parâmetros antes de chamar a API.
- **Tratamento de falhas:** exibe mensagens claras em português para chave ausente/inválida (`400/401/403`), limite de cota ou indisponibilidade (`429/503`) e falhas de rede/timeout, sem expor *stacktraces*.
- **Logs seguros (`execucao.log`):** registra apenas metadados técnicos (modelo, quantidade de caracteres, latência em ms e códigos de erro). Chaves de API, mensagens do usuário e respostas do LLM **nunca** são armazenadas.

---

## ✅ Validação em Ambiente Limpo

Teste realizado em um novo ambiente virtual (`.venv_teste`) seguindo exclusivamente os passos deste README:

- **Ambiente testado:** Windows / Python 3.12
- **Instalação (`pip install -r requirements.txt`):** concluída sem conflitos.
- **Testes offline (`unittest`):** todos os testes passaram sem acesso à API.
- **Execução (`python app.py`):** inicialização, resposta bilíngue, geração de `execucao.log` sem dados sensíveis e encerramento controlado validados.
- **Problemas encontrados e correções:** *Nenhum problema encontrado durante a instalação e execução limpa.* *(Caso ocorra algum ajuste durante seu teste, registre aqui o ocorrido e a solução aplicada.)*

---

## 🤖 Desenvolvimento Assistido por IA

Projeto desenvolvido com o apoio do **Gemini (Google AI)** para modularização da arquitetura, definição do esquema de logs seguros, estruturação dos testes com *mocks* e revisão da documentação.
