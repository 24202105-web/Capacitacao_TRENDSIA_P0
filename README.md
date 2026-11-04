# 🇬🇧 English Tutor Assistant — P0 (TRENDS+IA)

Uma aplicação em Python de interface via terminal que atua como um tutor de inglês para estudantes brasileiros. O sistema utiliza a API do Google Gemini para oferecer correções gramaticais gentis, elogios e manter o diálogo ativo com o usuário de forma bilíngue (inglês e português).

Projeto desenvolvido para cumprir os requisitos do **P0 (Níveis Básico e Intermediário)** do curso **TRENDS+IA**.

---

## 🤖 Desenvolvimento Assistido por IA

Este projeto foi construído de forma colaborativa com o auxílio do **Gemini (Google AI)** como parceiro de desenvolvimento (*thought partner* e suporte técnico). A IA foi utilizada para:
- Estruturação e refatoração da arquitetura do código (modularização entre interface e regras de negócio);
- Implementação e mapeamento de tratamento resiliente de exceções de API e ambiente;
- Auxílio na criação de documentação e roteiros de comandos do Git/GitHub.

---

## 🎯 Problema e Escopo

- **Problema Resolvido:** A dificuldade de estudantes brasileiros em praticar a escrita em inglês de forma contínua, sem julgamentos e com feedbacks gramaticais imediatos.
- **Público-Alvo:** Estudantes de inglês em nível básico/intermediário.
- **Por que um LLM?** A correção gramatical adaptativa, o suporte bilíngue e a manutenção da fluidez em um diálogo dependem de processamento de linguagem natural (PLN) contextual, inviabilizando abordagens estáticas (*hardcoded*).

---

## 🏗️ Arquitetura e Modularização (Nível Intermediário)

O código foi refatorado para garantir a **separação clara de responsabilidades** em componentes distintos:

- **`tutor.py`**: Módulo de regras de negócio. Responsável por carregar variáveis de ambiente, preparar prompts derivados, realizar chamadas à API da Google e tratar erros de autenticação, rede e indisponibilidade.
- **`app.py`**: Módulo de interface de usuário (CLI). Responsável pela captura de entrada no terminal, validação de entradas vazias, chamadas às funções do tutor e exibição formatada da resposta.
- **`.env.example`**: Modelo público de configuração para indicação da chave de API sem expor credenciais reais.
- **`.gitignore`**: Proteção de credenciais locais (`.env`) e ambiente virtual (`venv/`).

---

## 🛡️ Tratamento de Erros e Resiliência

A aplicação foi projetada para encerrar ou reagir de maneira amigável em situações adversas:

1. **Entradas Vazias:** Impede mensagens em branco ou compostas apenas por espaços no terminal.
2. **Credencial Ausente:** Identifica a falta da variável `GEMINI_API_KEY` no arquivo `.env` e exibe orientações de configuração.
3. **Credencial Inválida:** Captura tentativas com chaves no formato padrão (*placeholder*) ou recusadas pelo servidor do Google (erros `400/403/UNAUTHENTICATED`).
4. **Indisponibilidade / Alta Demanda:** Trata picos de consumo da API (erros `503` / `RESOURCE_EXHAUSTED`), notificando o usuário sem expor *stacktraces* técnicos.
5. **Falhas de Conexão e Timeout:** Trata interrupções de rede com mensagens claras em português.

---

## 🛠️ Tecnologias e Stack

- **Linguagem:** Python 3.10+
- **LLM / SDK:** Google Gemini API (`google-genai` SDK)
- **Modelo Utilizado:** `gemini-3.5-flash-lite` (equilíbrio entre velocidade, cota gratuita e baixa latência)
- **Gerenciamento de Variáveis de Ambiente:** `python-dotenv`
- **Versionamento:** Git e GitHub (Fluxo por *Branch*, *Pull Request* e *Tags*)

---

## 🚀 Como Executar o Projeto Localmente

### Pré-requisitos
- Python 3.10 ou superior instalado.
- Uma chave de API do Google Gemini ([obtenha aqui no Google AI Studio](https://aistudio.google.com/)). *Obs.: Recomenda-se utilizar uma conta pessoal do Google.*

### Passo a Passo

1. **Clonar o repositório:**
   ```bash
   git clone [https://github.com/24202105-web/Capacitacao_TRENDSIA.git](https://github.com/24202105-web/Capacitacao_TRENDSIA.git)
   cd Capacitacao_TRENDSIA

Criar e ativar o ambiente virtual:

Bash
python -m venv venv
# No Windows:
.\venv\Scripts\activate
# No Linux/Mac:
source venv/bin/activate

python -m venv venv

Criar e ativar o ambiente virtual:

# No Windows (PowerShell):
.\venv\Scripts\activate

# No Linux/Mac:
source venv/bin/activate

**Instalar as dependências:**

    ```bash
    pip install -r requirements.txt

**Configurar as variáveis de ambiente:**

    Copie o arquivo .env.example para .env:

    ```bash
    cp .env.example .env

**Edite o arquivo .env e insira sua chave válida:**

    Snippet de código
    GEMINI_API_KEY=sua_chave_real_aqui

**Executar a aplicação:**

    ```bash
    python app.py



Cenários de Teste Demonstrados
Entrada Simples/Correta:

Input: hi

Resultado: Feedback amigável em inglês/português e pergunta para prosseguir.

Entrada com Erro Gramatical:

Input: I goes to store yesterday

Resultado: Correção gentil apontando o tempo verbal correto (I went to the store yesterday) e continuidade da conversa.

Teste de Entrada Vazia:

Input: Teclar Enter sem conteúdo.

Resultado: Alerta no terminal solicitando digitação válida.

Teste de Credencial Ausente/Inválida:

Procedimento: Executar sem .env ou com chave alterada para teste.

Resultado: Exibição de mensagem informativa orientando o ajuste do .env.

Encerramento Controlado:

Input: Digitar sair, exit ou quit.

Resultado: Mensagem de despedida e finalização do script.