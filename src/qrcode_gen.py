from pathlib import Path

import qrcode
from PIL import Image

# Nível de correção de erro "H" (~30% de redundância).
# Necessário para o QR continuar legível com o logo sobreposto.
_NIVEL_CORRECAO = qrcode.constants.ERROR_CORRECT_H

# Proporção do QR que o logo ocupa (20% da largura).
_PROPORCAO_LOGO = 0.20

# Margem branca ao redor do logo, em pixels, para destacá-lo do QR.
_MARGEM_LOGO = 10


def gerar_qrcode(
    conteudo: str,
    caminho_logo: str | Path | None = None,
) -> Image.Image:
    """Gera um QR Code e devolve a imagem pronta em memória.

    Se um caminho de logo for informado, ele é centralizado sobre o QR Code.
    Quem chamar decide se salva, mostra em tela ou converte para outro formato.
    """
    if not conteudo or not conteudo.strip():
        raise ValueError("O conteúdo do QR Code não pode ficar vazio.")

    imagem = _criar_qr_base(conteudo)

    if caminho_logo:
        caminho_logo = Path(caminho_logo)
        if caminho_logo.exists():
            _aplicar_logo(imagem, caminho_logo)

    return imagem


def _criar_qr_base(conteudo: str) -> Image.Image:
    qr = qrcode.QRCode(
        version=1,
        error_correction=_NIVEL_CORRECAO,
        box_size=10,
        border=4,
    )
    qr.add_data(conteudo)
    qr.make(fit=True)

    return qr.make_image(
        fill_color="black",
        back_color="white",
    ).convert("RGB")


def _aplicar_logo(imagem: Image.Image, caminho_logo: Path) -> None:
    logo = Image.open(caminho_logo).convert("RGBA")

    tamanho_logo = int(imagem.width * _PROPORCAO_LOGO)
    logo.thumbnail((tamanho_logo, tamanho_logo), Image.LANCZOS)

    fundo = Image.new(
        "RGB",
        (logo.width + _MARGEM_LOGO * 2, logo.height + _MARGEM_LOGO * 2),
        "white",
    )

    posicao_no_fundo = (
        (fundo.width - logo.width) // 2,
        (fundo.height - logo.height) // 2,
    )
    fundo.paste(logo, posicao_no_fundo, logo)

    posicao_na_imagem = (
        (imagem.width - fundo.width) // 2,
        (imagem.height - fundo.height) // 2,
    )
    imagem.paste(fundo, posicao_na_imagem)


if __name__ == "__main__":
    conteudo = input("Digite o conteúdo do QR Code: ").strip()
    caminho_logo = input("Caminho do logo (ou ENTER para nenhum): ").strip() or None

    qr = gerar_qrcode(conteudo, caminho_logo)
    qr.save("qr_code.png")
    print("QR Code salvo em qr_code.png")