import streamlit as st
import pandas as pd

st.set_page_config(page_title="DevTask Pro", page_icon="🚀", layout="wide")

# LOGIN

def login():

    st.title("🚀 DevTask Pro")
    st.subheader("Gerenciador de tarefas para desenvolvedores")

    user = st.text_input("Usuário")
    password = st.text_input("Senha", type="password")

    if st.button("Entrar"):

        if user == "admin" and password == "123":

            st.session_state["logado"] = True
            st.rerun()

        else:
            st.error("Credenciais inválidas")


if "logado" not in st.session_state:
    st.session_state["logado"] = False


if not st.session_state["logado"]:
    login()
    st.stop()


# BANCO DE TAREFAS

if "tasks" not in st.session_state:
    st.session_state.tasks = []


st.sidebar.title("DevTask Pro")

menu = st.sidebar.radio(
    "Menu",
    ["Dashboard","Criar tarefa","Lista de tarefas"]
)

if st.sidebar.button("Sair"):
    st.session_state["logado"] = False
    st.rerun()


# DASHBOARD

if menu == "Dashboard":

    st.title("📊 Dashboard")

    total = len(st.session_state.tasks)
    done = sum(task["done"] for task in st.session_state.tasks)

    col1,col2 = st.columns(2)

    col1.metric("Total de tarefas", total)
    col2.metric("Concluídas", done)

    if total > 0:
        progress = done / total
        st.progress(progress)

# CRIAR TAREFA

if menu == "Criar tarefa":

    st.title("➕ Nova tarefa")

    titulo = st.text_input("Título")
    descricao = st.text_area("Descrição")

    if st.button("Salvar"):

        st.session_state.tasks.append({
            "titulo":titulo,
            "descricao":descricao,
            "done":False
        })

        st.success("Tarefa criada!")

# LISTA

if menu == "Lista de tarefas":

    st.title("📋 Tarefas")

    for i,task in enumerate(st.session_state.tasks):

        col1,col2 = st.columns([4,1])

        with col1:
            st.write(f"**{task['titulo']}**")
            st.write(task["descricao"])

        with col2:

            if not task["done"]:

                if st.button("✔", key=i):

                    st.session_state.tasks[i]["done"] = True
                    st.rerun()

    if st.session_state.tasks:

        df = pd.DataFrame(st.session_state.tasks)

        csv = df.to_csv(index=False)

        st.download_button(
            "Exportar tarefas",
            csv,
            "tarefas.csv",
            "text/csv"
        )