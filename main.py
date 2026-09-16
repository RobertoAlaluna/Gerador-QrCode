import sys

try:
    from src.app import App
except ImportError as erro:
    faltando = str(erro).split("'")[1] if "'" in str(erro) else "desconhecida"
    print("=" * 60)
    print("  ERRO: dependências não instaladas")
    print("=" * 60)
    print(f"\nA biblioteca '{faltando}' não foi encontrada.\n")
    print("Instale as dependências com:")
    print("    pip install -r requirements.txt\n")
    print("Ou, se preferir instalar individualmente:")
    print("    pip install qrcode pillow customtkinter")
    print("=" * 60)
    sys.exit(1)

if __name__ == "__main__":
    app = App()
    app.mainloop()