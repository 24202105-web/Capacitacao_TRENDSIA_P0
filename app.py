from tutor import carregar_configuracao, processar_mensagem

def main():
    client = carregar_configuracao()

    print("🇬🇧 English Tutor Assistant - Nível Intermediário")
    print("Escreva suas mensagens em inglês! Digite 'sair' para encerrar.\n")
    print("-" * 50)

    while True:
        entrada = input("Você (em inglês): ")
        
        if entrada.lower().strip() in ['sair', 'exit', 'quit']:
            print("Goodbye! 👋")
            break

        if not entrada.strip():
            continue

        resposta = processar_mensagem(client, entrada)
        if resposta:
            print(f"\n🤖 Tutor:\n{resposta}\n")
            print("-" * 50)

if __name__ == "__main__":
    main()