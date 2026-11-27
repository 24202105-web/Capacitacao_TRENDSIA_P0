# 🇬🇧 English Tutor Assistant — P0 (TRENDS+IA)

Aplicação CLI em Python que atua como tutor de inglês para estudantes brasileiros utilizando a API do Google Gemini, oferecendo correções gramaticais, elogios e continuidade de diálogo de forma bilíngue (inglês e português).

Entrega consolidada do **P0 — Níveis Básico (`p0-basico`), Intermediário (`p0-intermediario`) e Avançado (`p0-avancado`)**.

- **Vídeo de Demonstração:**: https://youtu.be/zmy1PpTWWis

---

## 🎯 Problema, Público-Alvo e Justificativa do LLM

- **Problema Escolhido:** Uma pessoa que estuda inglês por conta própria precisa transformar frases escritas em inglês em correções gramaticais comentadas e perguntas de continuação em português e inglês, porque atualmente enfrenta a falta de feedback imediato e acessível para praticar conversação escrita sem receio de errar.
- **Público-Alvo:** Estudantes brasileiros de inglês em nível básico ou intermediário que buscam praticar escrita no dia a dia.
- **Justificativa para Utilizar um LLM:** Regras fixas ou expressões regulares não conseguem interpretar variações livres de vocabulário, identificar erros contextuais de gramática e gerar respostas naturais em dois idiomas mantendo o diálogo ativo.

---

## 🏗️ Funcionamento e Estrutura do Projeto

O fluxo da aplicação separa a interface de terminal, o carregamento de configurações externas, o núcleo de comunicação com o LLM e os testes automatizados:

```text
Capacitacao_TRENDSIA_P0/
├── tests/
│   ├── __init__.py
│   └── test_tutor.py          # Testes unitários offline (simulados, sem chamadas reais à API)
├── .env.example               # Modelo público de variáveis de ambiente e parâmetros do LLM
├── .gitignore                 # Ignora .env, ambientes virtuais e arquivos .log
├── app.py                     # Interface de linha de comando (CLI) e loop de interação
├── config.py                  # Carregamento e validação das configurações externas
├── tutor.py                   # Núcleo de chamadas ao Gemini, logs seguros e tratamento de erros
├── requirements.txt           # Dependências do projeto
├── RELATORIO_EXECUCAO.md      # Relatório técnico de evolução, decisões, testes e reflexão
└── README.md                  # Documentação principal do projeto
```

### Stack e Versões
- **Python:** `3.12` *(compatível com Python 3.10+)*
- **Bibliotecas principais:**
  - `google-genai` (SDK oficial do Google Gemini)
  - `python-dotenv` (carregamento de variáveis de ambiente a partir do `.env`)
  - `unittest` / `unittest.mock` (biblioteca padrão do Python para testes offline)
- **Modelo padrão:** `gemini-3.5-flash-lite`

---

## 🚀 Instalação e Configuração

### 1. Clonar o repositório
```bash
git clone https://github.com/24202105-web/Capacitacao_TRENDSIA_P0.git
cd Capacitacao_TRENDSIA_P0
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

### 4. Configurar o acesso ao LLM (`.env`)
Copie o arquivo de modelo para `.env`:
* **Windows (PowerShell):** `Copy-Item .env.example .env`
* **Linux / macOS:** `cp .env.example .env`

Edite o `.env` e adicione sua chave obtida no [Google AI Studio](https://aistudio.google.com/). Todos os parâmetros de geração e comportamento do tutor podem ser ajustados nesse arquivo sem alterar o código-fonte:

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

## ▶️ Execução e Exemplos de Uso

### Executar a aplicação (uso real com a API)
```bash
python app.py
```
Digite suas frases em inglês no terminal. Para encerrar a sessão com segurança, digite `sair`, `exit` ou `quit`.

### Exemplos de Entrada e Saída

**1. Entrada com erro gramatical:**
```text
Você (em inglês): I goes to store yesterday

🤖 Tutor:
Almost there! A small correction: "I went to the store yesterday." ("goes" is present tense, and "went" is the past tense of "go").

Quase lá! Uma pequena correção: "I went to the store yesterday." ("goes" está no presente, e "went" é o passado de "go").
What did you buy at the store? (O que você comprou na loja?)
```

**2. Entrada gramaticalmente correta:**
```text
Você (em inglês): I like studying Python in the morning.

🤖 Tutor:
Great job! Your sentence is completely correct and very natural.

Ótimo trabalho! Sua frase está totalmente correta e muito natural.
How long have you been studying Python? (Há quanto tempo você estuda Python?)
```

**3. Entrada vazia (bloqueada localmente antes de chamar a API):**
```text
Você (em inglês):    
⚠️ Entrada vazia! Por favor, digite uma frase em inglês ou 'sair' para encerrar.
```

---

## 🧪 Testes Reais e Simulados

O projeto combina **testes simulados (offline)** para validar a lógica local sem custo de API e **testes reais** para verificar a integração ponta a ponta:

### 1. Testes Simulados (Offline — sem chamada à API)
Implementados em `tests/test_tutor.py` com `unittest.mock`. Validam carregamento de credenciais, bloqueio de placeholders, parâmetros inválidos, montagem de `GenerateContentConfig`, entrada vazia, resposta simulada, erro simulado de API (`503`), falha de rede (`TimeoutError`) e sanitização de logs:
```bash
python -m unittest discover -s tests -v
```

### 2. Testes Reais (Integração com Google Gemini)
Executados diretamente via `python app.py` com chave válida no `.env` para validar:
- Resposta bilíngue real do modelo `gemini-3.5-flash-lite`;
- Tratamento amigável ao testar chave inválida (`400/403`);
- Geração do arquivo `execucao.log` contendo apenas metadados técnicos (modelo, contagem de caracteres, latência em ms e códigos de status), sem expor chaves ou textos do usuário.

---

## ⚠️ Limites do Projeto e Limitações Conhecidas

- **Sem memória entre turnos:** Cada mensagem é enviada de forma independente (`generate_content`), portanto o tutor não mantém histórico das frases anteriores da mesma sessão.
- **Somente texto via terminal:** A aplicação não processa áudio, pronúncia ou compreensão auditiva.
- **Dependência de conexão e cota externa:** O uso real exige acesso à internet e está sujeito aos limites de requisições e disponibilidade da API gratuita do Google Gemini.

---

## ✅ Validação em Ambiente Limpo

Teste realizado em um novo ambiente virtual seguindo exclusivamente os passos deste `README.md`:

- **Ambiente testado:** Windows / Python 3.12
- **Instalação (`pip install -r requirements.txt`):** concluída sem conflitos.
- **Testes offline (`unittest`):** 8/8 testes aprovados sem acesso à API.
- **Execução real (`python app.py`):** inicialização, resposta bilíngue, gravação segura em `execucao.log` e encerramento controlado validados.
