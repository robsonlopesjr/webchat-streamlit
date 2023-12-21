import streamlit as st


MENSSAGEM_FICT = [
    {
        "nome_usuario": "ROBSON",
        "conteudo": "Olá, Junior"
    },
    {
        "nome_usuario": "JUNIOR",
        "conteudo": "Olá, Robson"
    }
]


def pagina_chat():
    st.title("📨 WebChat - Streamlit")
    st.divider()

    if not "mensagens" in st.session_state:
        st.session_state["mensagens"] = MENSSAGEM_FICT

    mensagens = st.session_state["mensagens"]
    usuario_logado = "ROBSON"

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

        st.session_state["mensagens"] = mensagens


def main():
    pagina_chat()


if __name__ == "__main__":
    main()
