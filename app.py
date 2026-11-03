import ollama

# Configuração da IA
SYSTEM_PROMPT = """
Você é um tutor de inglês amigável e paciente ajudando um estudante brasileiro.
Para cada mensagem que o usuário enviar em inglês ou português:
1. Se houver erros gramaticais ou de vocabulário, mostre a correção de forma gentil. Se estiver correto, elogie rapidamente.
2. Responda em inglês ou português de forma natural e faça UMA nova pergunta simples para dar continuidade à conversa.
Mantenha suas respostas curtas e diretas.
"""

print("🇬🇧 English Tutor Assistant - Nível Básico")
print("Escreva suas mensagens em inglês ou Portugês! Digite 'sair' para encerrar.\n")
print("-" * 50)

while True:
    # 1. Recebe a entrada textual pelo terminal
    entrada = input("Você (em inglês): ")
    
    if entrada.lower().strip() in ['sair', 'exit', 'quit']:
        print("Goodbye! See you next time! 👋")
        break

    if not entrada.strip():
        continue

    # 2. Envia a entrada com a solicitação derivada (contexto de estudo de inglês)
    prompt_derivado = f"{SYSTEM_PROMPT}\n\nMensagem do aluno: {entrada}"

    resposta = ollama.chat(
        model='llama3',
        messages=[{'role': 'user', 'content': prompt_derivado}]
    )

    # 3. Apresenta a resposta ao usuário
    print(f"\n🤖 Tutor:\n{resposta['message']['content']}\n")
    print("-" * 50)