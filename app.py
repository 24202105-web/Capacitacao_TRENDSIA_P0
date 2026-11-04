from tutor import carregar_configuracao, processar_mensagem

def main():
    """Gerencia a captura de dados e exibição do fluxo no terminal."""
    client = carregar_configuracao()

    print("🇬🇧 English Tutor Assistant - Nível Intermediário")
    print("Escreva suas mensagens em inglês! Digite 'sair' para encerrar.\n")
    print("-" * 50)

    while True:
        try:
            entrada = input("Você (em inglês): ")
        except (KeyboardInterrupt, EOFError):
            print("\n\nGoodbye! 👋")
            break

        # Impedir o envio de entradas vazias ou compostas apenas por espaços
        entrada_limpa = entrada.strip()
        if not entrada_limpa:
            print("⚠️ Entrada vazia! Por favor, digite uma frase em inglês ou 'sair' para encerrar.\n")
            continue

        if entrada_limpa.lower() in ['sair', 'exit', 'quit']:
            print("Goodbye! 👋")
            break

        resposta = processar_mensagem(client, entrada_limpa)
        if resposta:
            print(f"\n🤖 Tutor:\n{resposta}\n")
            print("-" * 50)

if __name__ == "__main__":
    main()