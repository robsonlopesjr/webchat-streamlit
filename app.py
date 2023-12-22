from pathlib import Path
from unidecode import unidecode
import pickle
import streamlit as st
import time


PASTA_MENSAGENS = Path(__file__).parent / "mensagens"
PASTA_MENSAGENS.mkdir(exist_ok=True)

PASTA_USUARIOS = Path(__file__).parent / "usuarios"
PASTA_USUARIOS.mkdir(exist_ok=True)


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


def pagina_login():
    st.header("📨 Bem-vindo ao WebChat", divider=True)

    tab1, tab2 = st.tabs(["Entrar", "Cadastrar"])

    with tab1.form(key="login"):
        nome = st.text_input("Digite seu nome de usuario")
        senha = st.text_input("Digite sua senha")
        if st.form_submit_button("Entrar"):
            _login_usuario(nome, senha)

    with tab2.form(key="cadastrar"):
        nome = st.text_input("Cadastre seu nome de usuario")
        senha = st.text_input("Cadastre sua senha")
        if st.form_submit_button("Cadastrar"):
            _cadastrar_usuario(nome, senha)


def _login_usuario(nome, senha):
    if validacao_de_senha(nome, senha):
        st.success("Login efetuado com sucesso!")
        time.sleep(2)
        st.session_state["usuario_logado"] = nome.upper()
        mudar_pagina("chat")
        st.rerun()
    else:
        st.error("Erro ao logar")


def _cadastrar_usuario(nome, senha):
    if salvar_novo_usuario(nome, senha):
        st.success("Usuário cadastrado com sucesso!")
        time.sleep(2)
        st.session_state["usuario_logado"] = nome.upper()
        mudar_pagina("chat")
        st.rerun()
    else:
        st.error("Erro ao cadastrar usuário")


def mudar_pagina(nome_pagina):
    st.session_state["pagina_atual"] = nome_pagina


def salvar_novo_usuario(nome, senha):
    nome_arquivo = unidecode(nome.replace(" ", "_").lower())

    if (PASTA_USUARIOS / nome_arquivo).exists():
        return False
    else:
        with open(PASTA_USUARIOS / nome_arquivo, "wb") as f:
            pickle.dump({"nome_usuario": nome, "senha": senha}, f)
        return True


def validacao_de_senha(nome, senha):
    nome_arquivo = unidecode(nome.replace(" ", "_").lower())

    if not (PASTA_USUARIOS / nome_arquivo).exists():
        return False
    else:
        with open(PASTA_USUARIOS / nome_arquivo, "rb") as f:
            arquivo_senha = pickle.load(f)

        if arquivo_senha["senha"] == senha:
            return True
        else:
            return False


def pagina_chat():
    """
    Função principal para mostrar as mensagens
    """
    st.title("📨 WebChat - Streamlit Messenger")
    st.divider()

    usuario_logado = st.session_state["usuario_logado"]
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


def inicializacao():
    if not "pagina_atual" in st.session_state:
        mudar_pagina("login")

    if not "usuario_logado" in st.session_state:
        st.session_state["usuario_logado"] = ""


def main():
    inicializacao()

    if st.session_state["pagina_atual"] == "login":
        pagina_login()
    elif st.session_state["pagina_atual"] == "chat":
        pagina_chat()


if __name__ == "__main__":
    main()
