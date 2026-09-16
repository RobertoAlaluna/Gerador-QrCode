# Gerador de QR Code

Aplicativo desktop para gerar QR Codes personalizados com logo opcional, preview em tempo real e exportação em PNG. Desenvolvido em Python com interface gráfica moderna via CustomTkinter.

---

## Funcionalidades

* **Qualquer entrada**: Geração de QR Codes a partir de textos simples ou URLs.
* **Logo centralizado**: Inserção opcional de imagem no centro com fundo branco automático.
* **Preview responsivo**: Pré-visualização em tempo real ajustável ao tamanho da janela.
* **Exportação PNG**: Salvamento do arquivo gerado com nome personalizável.
* **Interface moderna**: Layout adaptável a diferentes resoluções de tela.

---

## Tecnologias Utilizadas

| Ferramenta | Uso no Projeto |
| :--- | :--- |
| **Python 3.10+** | Linguagem base do projeto |
| **CustomTkinter** | Construção da interface gráfica |
| **qrcode** | Geração da matriz do QR Code |
| **Pillow (PIL)** | Composição e manipulação de imagens |
| **PyInstaller** | Criação de executável portável |

---

## Como Rodar o Projeto

### Pré-requisitos
Certifique-se de ter o **Python 3.10 ou superior** instalado na máquina.

### 1. Clonar o repositório
```bash
git clone [https://github.com/RobertoAlaluna/Gerador-QrCode.git](https://github.com/RobertoAlaluna/Gerador-QrCode.git)
cd Gerador-QrCode
```

### 2. Instalar as dependências
```bash
pip install -r requirements.txt
```

### 3. Executar o aplicativo
```bash
python main.py
```

> Caso alguma dependência falte, o próprio aplicativo detecta e exibe o comando exato no terminal para correção.

---

## Como Usar

1. Digite a URL ou texto desejado no campo de entrada.
2. *(Opcional)* Clique em **Selecionar imagem** para carregar um logo central.
3. Insira o nome desejado para o arquivo final.
4. Clique em **Gerar QR Code** para visualizar a prévia na tela.
5. Clique em **Salvar QR Code** e selecione a pasta de destino no computador.

---

## Estrutura do Projeto

```text
Gerador-QrCode/
├── src/
│   ├── qrcode_gen.py   # Regra de geração do QR Code (core)
│   └── app.py          # Interface gráfica (CustomTkinter)
├── assets/
│   └── logo.ico        # Ícone da janela do programa
├── main.py             # Ponto de entrada do sistema
├── requirements.txt    # Dependências do projeto
└── README.md           # Documentação
```

---

## Licença

Distribuído sob a licença **MIT**. Consulte o arquivo `LICENSE` para mais detalhes.

---

## Autor

* **Roberto Alaluna Ferreira**
* GitHub: [@RobertoAlaluna](https://github.com/RobertoAlaluna)