from pathlib import Path
from unidecode import unidecode
import pickle
import streamlit as st


PASTA_MENSAGENS = Path(__file__).parent / "mensagens"
PASTA_MENSAGENS.mkdir(exist_ok=True)


def ler_mensagens_armazenadas(usuario_logado, conversando_com):
    """
    Função para ler as mensagens
    :param usuario_logado: Str
    :param conversando_com: Str
    :return: List
    """
    nome_arquivo = nome_arquivo_armazenado(usuario_logado, conversando_com)
    if (PASTA_MENSAGENS / nome_arquivo).exists():
        with open(PASTA_MENSAGENS / nome_arquivo, 'rb') as f:
            return pickle.load(f)
    else:
        return []


def armazenar_mensagens(usuario_logado, conversando_com, mensagens):
    """
    Função que irá armazenar o arquivo
    :param usuario_logado: Str
    :param conversando_com: Str
    :param mensagens: list
    """
    nome_arquivo = nome_arquivo_armazenado(usuario_logado, conversando_com)
    with open(PASTA_MENSAGENS / nome_arquivo, 'wb') as f:
        pickle.dump(mensagens, f)


def nome_arquivo_armazenado(usuario_logado, conversando_com):
    """
    Função para gerar o nome do arquivo a ser armazenado
    :param usuario_logado: Str
    :param conversando_com: Str
    :return: Str
    """

    nome_arquivo = [usuario_logado, conversando_com]
    nome_arquivo.sort()

    # Substituir os espaços em branco por undeline
    nome_arquivo = [u.replace(" ", "_") for u in nome_arquivo]

    # Remover as acentuações
    nome_arquivo = [unidecode(u) for u in nome_arquivo]

    nome_arquivo = "&".join(nome_arquivo).lower()

    return nome_arquivo

def pagina_chat():
    """
    Função principal para mostrar as mensagens
    """
    st.title("📨 WebChat - Streamlit")
    st.divider()

    usuario_logado = "ROBSON"
    conversando_com = "JUNIOR"
    mensagens = ler_mensagens_armazenadas(usuario_logado, conversando_com)

    for mensagem in mensagens:
        nome_usuario = "user" if mensagem["nome_usuario"] == usuario_logado else mensagem["nome_usuario"]

        avatar = None if mensagem["nome_usuario"] == usuario_logado else '😎'

        chat = st.chat_message(nome_usuario, avatar=avatar)
        chat.markdown(mensagem["conteudo"])

    nova_mensagem = st.chat_input("Digite uma mensagem")

    if nova_mensagem:
        mensagem = {
            "nome_usuario": usuario_logado,
            "conteudo": nova_mensagem
        }

        chat = st.chat_message("user")
        chat.markdown(mensagem["conteudo"])

        mensagens.append(mensagem)

        armazenar_mensagens(usuario_logado, conversando_com, mensagens)


def main():
    pagina_chat()


if __name__ == "__main__":
    main()
