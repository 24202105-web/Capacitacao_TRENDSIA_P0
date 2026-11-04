# 🇬🇧 English Tutor Assistant — P0 (TRENDS+IA)

Uma aplicação em Python de interface via terminal que atua como um tutor de inglês para brasileiros. O sistema utiliza a API do Google Gemini para oferecer correções gramaticais gentis, elogios e manter o diálogo ativo com o usuário.

Projeto desenvolvido para cumprir os requisitos do projeto **P0 - Nível Básico** do curso **TRENDS+IA**.

---

## 🎯 Problema e Escopo

* **Problema Resolvido:** A dificuldade que estudantes brasileiros de nível básico/intermediário têm em praticar a escrita em inglês e receber correções imediatas de forma contextual e sem julgamentos.
* **Público-Alvo:** Estudantes de inglês que desejam praticar a escrita e manter conversações curtas no dia a dia.
* **Por que um LLM?** A correção gramatical adaptativa e a manutenção de um diálogo contínuo exigem processamento de linguagem natural (PLN) contextual, o que torna inviável o uso de regras estáticas ou hardcoded.

---

## 🛠️ Tecnologias e Stack

* **Linguagem:** Python 3.10+
* **LLM / SDK:** Google Gemini API (`google-genai` SDK)
* **Modelo Utilizado:** `gemini-3.5-flash-lite` (escolhido pelo equilíbrio de velocidade, disponibilidade e cota de requisições)
* **Gerenciamento de Variáveis de Ambiente:** `python-dotenv`
* **Versionamento:** Git e GitHub (Tag de entrega: `p0-basico`)

---

## 📋 Arquitetura de Entradas, Saídas e Segurança

* **Entrada:** Frases e mensagens digitadas pelo usuário diretamente no terminal em inglês ou português.
* **Solicitação Derivada (System Prompt):** A mensagem do usuário é combinada a um prompt de sistema que instrui a IA a agir como um tutor amigável, corrigindo erros gentilmente e formulando uma nova pergunta simples.
* **Saída:** Feedback textual formatado e exibido diretamente no terminal.
* **Segurança de Credenciais:** A chave de acesso `GEMINI_API_KEY` é armazenada estritamente no arquivo local `.env`, que está listado no `.gitignore` e mantido fora do controle de versão.

---

## 🚀 Como Executar o Projeto Localmente

### Pré-requisitos
* Python 3.10 ou superior instalado.
* Uma chave de API do Google Gemini ([obtenha aqui no Google AI Studio](https://aistudio.google.com/)). obs.: utilize uma conta pessoal

### Passo a Passo

1. **Clonar o repositório:**
   ```bash
        git clone https://github.com/24202105-web/Capacitacao_TRENDSIA.git
        cd Capacitacao_TRENDSIA

 2. **Criar e ativar o ambiente virtual:**
 
    python -m venv venv
    # No Windows:
    .\venv\Scripts\activate
    # No Linux/Mac:
    source venv/bin/activate
3. **Instalar as dependências:**

    pip install -r requirements.txt 

4. **Configurar as variáveis de ambiente:**

    Crie um arquivo .env na raiz do projeto com a sua chave da API do Gemini:

    GEMINI_API_KEY=sua_chave_aqui 

5. **Executar a aplicação:**

    python app.py    

### Casos de Teste Utilizados

Entrada Simples/Correta: hi

Resultado Esperado: Cumprimento curto em inglês ou português seguido de uma pergunta para continuar a conversa.

Entrada com Erro Gramatical: I goes to store yesterday

Resultado Esperado: Correção gentil apontando o uso correto do tempo verbal ("I went to the store yesterday") e uma nova pergunta em inglês.

Encerrar Aplicação: Digitar sair, exit ou quit.

Resultado Esperado: Exibição da mensagem de despedida e encerramento do script.    

### Entregável (Tag)

    Este projeto cumpre integralmente todas as competências previstas no Nível Básico (C01, C02, C03 e C04). A entrega oficial desta fase está registrada no Git sob a tag:

    p0-basico