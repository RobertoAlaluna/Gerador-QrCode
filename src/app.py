import os
import platform
import subprocess
from pathlib import Path

import customtkinter as ctk
from PIL import Image
from tkinter import filedialog, messagebox

from src.qrcode_gen import gerar_qrcode


ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("green")


COR_PRIMARIA = "#0d9488"
COR_PRIMARIA_HOVER = "#0f766e"
COR_ACENTO = "#10b981"
COR_ACENTO_HOVER = "#059669"
COR_TEXTO = "#0f172a"
COR_TEXTO_SUAVE = "#64748b"
COR_SUCESSO = "#10b981"
COR_ERRO = "#ef4444"
COR_FUNDO_PREVIEW = "#ecfdf5"
COR_BARRA_ACENTO = "#0d9488"
COR_INPUT_BG = "#ffffff"


def _fonte_padrao() -> str:
    sistema = platform.system()
    if sistema == "Windows":
        return "Segoe UI"
    if sistema == "Darwin":
        return "Helvetica Neue"
    return "DejaVu Sans"


def _abrir_arquivo(caminho: Path) -> None:
    sistema = platform.system()
    if sistema == "Windows":
        os.startfile(caminho)
    elif sistema == "Darwin":
        subprocess.run(["open", caminho])
    else:
        subprocess.run(["xdg-open", caminho])


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Gerador de QR Code")
        self.geometry("1000x640")
        self.minsize(880, 620)

        self.fonte = _fonte_padrao()
        self.caminho_logo = ""
        self.imagem_qr: Image.Image | None = None
        self._imagem_preview: ctk.CTkImage | None = None
        self._ultimo_tamanho_preview = (0, 0)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        self._criar_barra_acento()
        self._criar_cabecalho()
        self._criar_corpo()

    # ------------------------------------------------------------------
    # Estrutura visual
    # ------------------------------------------------------------------

    def _criar_barra_acento(self):
        barra = ctk.CTkFrame(self, height=4, fg_color=COR_BARRA_ACENTO, corner_radius=0)
        barra.grid(row=0, column=0, sticky="ew")
        barra.grid_propagate(False)

    def _criar_cabecalho(self):
        cabecalho = ctk.CTkFrame(self, fg_color="transparent")
        cabecalho.grid(row=1, column=0, sticky="ew", padx=36, pady=(24, 12))

        textos = ctk.CTkFrame(cabecalho, fg_color="transparent")
        textos.pack(anchor="w")

        ctk.CTkLabel(
            textos,
            text="Gerador de QR Code",
            font=ctk.CTkFont(family=self.fonte, size=26, weight="bold"),
            text_color=COR_TEXTO,
        ).pack(anchor="w")

        ctk.CTkLabel(
            textos,
            text="Crie QR Codes personalizados com logo em poucos cliques",
            font=ctk.CTkFont(family=self.fonte, size=12),
            text_color=COR_TEXTO_SUAVE,
        ).pack(anchor="w", pady=(4, 0))

    def _criar_corpo(self):
        corpo = ctk.CTkFrame(self, fg_color="transparent")
        corpo.grid(row=2, column=0, sticky="nsew", padx=36, pady=(0, 28))
        corpo.grid_columnconfigure(0, weight=35, uniform="col")
        corpo.grid_columnconfigure(1, weight=65, uniform="col")
        corpo.grid_rowconfigure(0, weight=1)

        self._criar_painel_config(corpo)
        self._criar_painel_preview(corpo)

    def _criar_painel_config(self, pai):
        painel = ctk.CTkFrame(pai, fg_color="transparent")
        painel.grid(row=0, column=0, sticky="nsew", padx=(0, 20))
        painel.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            painel,
            text="Link ou texto",
            font=ctk.CTkFont(family=self.fonte, size=11, weight="bold"),
            text_color=COR_TEXTO_SUAVE,
        ).grid(row=0, column=0, sticky="w", pady=(0, 4))

        self.txt_conteudo = ctk.CTkEntry(
            painel,
            height=40,
            corner_radius=0,
            border_width=0,
            fg_color=COR_INPUT_BG,
            font=ctk.CTkFont(family=self.fonte, size=13),
            placeholder_text="Ex.: https://exemplo.com",
        )
        self.txt_conteudo.grid(row=1, column=0, sticky="ew", pady=(0, 4))

        linha = ctk.CTkFrame(painel, height=2, fg_color=COR_ACENTO, corner_radius=1)
        linha.grid(row=2, column=0, sticky="ew", pady=(0, 26))
        linha.grid_propagate(False)

        ctk.CTkLabel(
            painel,
            text="Logo (opcional)",
            font=ctk.CTkFont(family=self.fonte, size=11, weight="bold"),
            text_color=COR_TEXTO_SUAVE,
        ).grid(row=3, column=0, sticky="w", pady=(0, 6))

        self.btn_logo = ctk.CTkButton(
            painel,
            text="Selecionar imagem",
            height=38,
            corner_radius=19,
            font=ctk.CTkFont(family=self.fonte, size=12),
            fg_color=COR_PRIMARIA,
            hover_color=COR_PRIMARIA_HOVER,
            text_color="white",
            command=self._selecionar_logo,
        )
        self.btn_logo.grid(row=4, column=0, sticky="ew")

        self.lbl_status_logo = ctk.CTkLabel(
            painel,
            text="Nenhum logo selecionado",
            font=ctk.CTkFont(family=self.fonte, size=11),
            text_color=COR_TEXTO_SUAVE,
        )
        self.lbl_status_logo.grid(row=5, column=0, sticky="w", pady=(6, 26))

        ctk.CTkLabel(
            painel,
            text="Nome do arquivo",
            font=ctk.CTkFont(family=self.fonte, size=11, weight="bold"),
            text_color=COR_TEXTO_SUAVE,
        ).grid(row=6, column=0, sticky="w", pady=(0, 4))

        self.txt_nome = ctk.CTkEntry(
            painel,
            height=40,
            corner_radius=0,
            border_width=0,
            fg_color=COR_INPUT_BG,
            font=ctk.CTkFont(family=self.fonte, size=13),
            placeholder_text="nome_do_arquivo",
        )
        self.txt_nome.grid(row=7, column=0, sticky="ew", pady=(0, 4))

        linha2 = ctk.CTkFrame(painel, height=2, fg_color=COR_ACENTO, corner_radius=1)
        linha2.grid(row=8, column=0, sticky="ew", pady=(0, 30))
        linha2.grid_propagate(False)

        self.btn_gerar = ctk.CTkButton(
            painel,
            text="Gerar QR Code",
            height=46,
            corner_radius=23,
            font=ctk.CTkFont(family=self.fonte, size=14, weight="bold"),
            fg_color=COR_ACENTO,
            hover_color=COR_ACENTO_HOVER,
            text_color="white",
            command=self._gerar,
        )
        self.btn_gerar.grid(row=9, column=0, sticky="ew")

        self.btn_salvar = ctk.CTkButton(
            painel,
            text="Salvar QR Code",
            height=42,
            corner_radius=21,
            font=ctk.CTkFont(family=self.fonte, size=12, weight="bold"),
            fg_color="transparent",
            border_width=2,
            border_color=COR_PRIMARIA,
            text_color=COR_PRIMARIA,
            hover_color="#d1fae5",
            state="disabled",
            command=self._salvar,
        )
        self.btn_salvar.grid(row=10, column=0, sticky="ew", pady=(12, 0))

        self.btn_limpar = ctk.CTkButton(
            painel,
            text="Limpar campos",
            height=32,
            corner_radius=16,
            font=ctk.CTkFont(family=self.fonte, size=11),
            fg_color="transparent",
            text_color=COR_TEXTO_SUAVE,
            hover_color="#e2e8f0",
            command=self._limpar,
        )
        self.btn_limpar.grid(row=11, column=0, sticky="ew", pady=(14, 0))

    def _criar_painel_preview(self, pai):
        painel = ctk.CTkFrame(
            pai,
            corner_radius=20,
            fg_color=COR_FUNDO_PREVIEW,
        )
        painel.grid(row=0, column=1, sticky="nsew")
        painel.grid_columnconfigure(0, weight=1)
        painel.grid_rowconfigure(1, weight=1)

        ctk.CTkLabel(
            painel,
            text="Pré-visualização",
            font=ctk.CTkFont(family=self.fonte, size=13, weight="bold"),
            text_color=COR_PRIMARIA,
        ).grid(row=0, column=0, pady=(22, 10))

        self.frame_imagem = ctk.CTkFrame(
            painel,
            corner_radius=12,
            fg_color="transparent",
        )
        self.frame_imagem.grid(row=1, column=0, padx=40, pady=(0, 12), sticky="nsew")
        self.frame_imagem.grid_columnconfigure(0, weight=1)
        self.frame_imagem.grid_rowconfigure(0, weight=1)
        self.frame_imagem.bind("<Configure>", self._ao_redimensionar_preview)

        self.lbl_preview = ctk.CTkLabel(
            self.frame_imagem,
            text="Seu QR Code\naparecerá aqui",
            font=ctk.CTkFont(family=self.fonte, size=13),
            text_color=COR_TEXTO_SUAVE,
        )
        self.lbl_preview.grid(row=0, column=0)

        self.lbl_status = ctk.CTkLabel(
            painel,
            text="",
            font=ctk.CTkFont(family=self.fonte, size=12),
            text_color=COR_TEXTO_SUAVE,
            wraplength=420,
            justify="center",
        )
        self.lbl_status.grid(row=2, column=0, pady=(0, 22), padx=20)

    # ------------------------------------------------------------------
    # Ações
    # ------------------------------------------------------------------

    def _selecionar_logo(self):
        arquivo = filedialog.askopenfilename(
            title="Selecione o logo",
            filetypes=[
                ("Imagens", "*.png *.jpg *.jpeg"),
                ("Todos os arquivos", "*.*"),
            ],
        )
        if arquivo:
            self.caminho_logo = arquivo
            self.lbl_status_logo.configure(
                text=f"✓ {Path(arquivo).name}",
                text_color=COR_ACENTO,
            )

    def _gerar(self):
        conteudo = self.txt_conteudo.get().strip()

        if not conteudo:
            messagebox.showwarning(
                "Falta o conteúdo",
                "Digite um link ou texto antes de gerar o QR Code.",
            )
            self.txt_conteudo.focus()
            return

        try:
            self.imagem_qr = gerar_qrcode(conteudo, self.caminho_logo or None)
        except Exception as erro:
            messagebox.showerror(
                "Erro ao gerar",
                f"Não foi possível gerar o QR Code.\n\nDetalhes: {erro}",
            )
            return

        self._renderizar_preview()
        self.btn_salvar.configure(state="normal")
        self._definir_status(
            "✓ QR Code gerado. Clique em Salvar para escolher onde guardar.",
            COR_SUCESSO,
        )

    def _salvar(self):
        if self.imagem_qr is None:
            return

        nome = self.txt_nome.get().strip() or "qr_code"
        if not nome.lower().endswith(".png"):
            nome += ".png"

        destino = filedialog.asksaveasfilename(
            title="Salvar QR Code",
            defaultextension=".png",
            initialfile=nome,
            filetypes=[("Imagem PNG", "*.png")],
        )
        if not destino:
            return

        try:
            self.imagem_qr.save(destino)
        except Exception as erro:
            messagebox.showerror(
                "Erro ao salvar",
                f"Não foi possível salvar o arquivo.\n\nDetalhes: {erro}",
            )
            return

        if messagebox.askyesno(
            "QR Code salvo",
            "Arquivo salvo com sucesso!\n\nDeseja abrir agora?",
        ):
            _abrir_arquivo(Path(destino))

    def _limpar(self):
        self.txt_conteudo.delete(0, "end")
        self.txt_nome.delete(0, "end")

        self.caminho_logo = ""
        self.imagem_qr = None
        self._imagem_preview = None
        self._ultimo_tamanho_preview = (0, 0)

        self.lbl_status_logo.configure(
            text="Nenhum logo selecionado",
            text_color=COR_TEXTO_SUAVE,
        )

        self.lbl_preview.configure(image=None, text="Seu QR Code\naparecerá aqui")
        self._definir_status("", COR_TEXTO_SUAVE)
        self.btn_salvar.configure(state="disabled")
        self.txt_conteudo.focus()

    # ------------------------------------------------------------------
    # Helpers de UI
    # ------------------------------------------------------------------

    def _definir_status(self, texto: str, cor: str):
        self.lbl_status.configure(text=texto, text_color=cor)

    def _ao_redimensionar_preview(self, evento):
        tamanho = (evento.width, evento.height)
        if tamanho == self._ultimo_tamanho_preview:
            return
        self._ultimo_tamanho_preview = tamanho
        self._renderizar_preview()

    def _renderizar_preview(self):
        if self.imagem_qr is None:
            return

        largura = self.frame_imagem.winfo_width()
        altura = self.frame_imagem.winfo_height()
        if largura < 40 or altura < 40:
            return

        margem = 40
        lado_max = max(80, min(largura, altura) - margem)

        preview = self.imagem_qr.copy()
        preview.thumbnail((lado_max, lado_max), Image.LANCZOS)

        self._imagem_preview = ctk.CTkImage(
            light_image=preview,
            dark_image=preview,
            size=preview.size,
        )
        self.lbl_preview.configure(image=self._imagem_preview, text="")


if __name__ == "__main__":
    app = App()
    app.mainloop()