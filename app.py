import streamlit as st
import pandas as pd

st.set_page_config(page_title="DevTask Pro", page_icon="🚀", layout="wide")

# -------------------------
# LOGIN
# -------------------------

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
            st.error("Usuário ou senha incorretos")


if "logado" not in st.session_state:
    st.session_state["logado"] = False

if not st.session_state["logado"]:
    login()
    st.stop()

# -------------------------
# BANCO DE TAREFAS (FAKE)
# -------------------------

if "tasks" not in st.session_state:
    st.session_state.tasks = [
        {
            "titulo": "Implementar sistema de autenticação",
            "descricao": "Criar login seguro com validação de usuário e senha.",
            "done": True
        },
        {
            "titulo": "Desenvolver dashboard de métricas",
            "descricao": "Adicionar gráficos de produtividade.",
            "done": True
        },
        {
            "titulo": "Criar API REST",
            "descricao": "Integração com serviços externos.",
            "done": False
        },
        {
            "titulo": "Implementar exportação de dados",
            "descricao": "Exportar tarefas para CSV.",
            "done": False
        },
        {
            "titulo": "Sistema de notificações",
            "descricao": "Alertar usuários sobre prazos.",
            "done": False
        },
        {
            "titulo": "Melhorar UI",
            "descricao": "Aplicar melhorias visuais.",
            "done": True
        },
        {
            "titulo": "Otimização de performance",
            "descricao": "Reduzir tempo de carregamento.",
            "done": False
        }
    ]

# -------------------------
# SIDEBAR
# -------------------------

st.sidebar.title("🚀 DevTask Pro")

menu = st.sidebar.radio(
    "Menu",
    ["Dashboard","Criar tarefa","Lista de tarefas","Exportar"]
)

if st.sidebar.button("Sair"):
    st.session_state["logado"] = False
    st.rerun()

# -------------------------
# DASHBOARD
# -------------------------

if menu == "Dashboard":

    st.title("📊 Dashboard")

    total = len(st.session_state.tasks)
    done = sum(task["done"] for task in st.session_state.tasks)

    col1,col2 = st.columns(2)

    col1.metric("Total de tarefas", total)
    col2.metric("Concluídas", done)

    if total > 0:

        progresso = done / total

        st.progress(progresso)

    st.subheader("Progresso do projeto")

    data = {
        "Status":["Concluídas","Pendentes"],
        "Quantidade":[done,total-done]
    }

    df = pd.DataFrame(data)

    st.bar_chart(df.set_index("Status"))

# -------------------------
# CRIAR TAREFA
# -------------------------

if menu == "Criar tarefa":

    st.title("➕ Nova tarefa")

    titulo = st.text_input("Título da tarefa")

    descricao = st.text_area("Descrição")

    if st.button("Salvar tarefa"):

        if titulo:

            st.session_state.tasks.append({
                "titulo":titulo,
                "descricao":descricao,
                "done":False
            })

            st.success("Tarefa criada com sucesso!")

        else:
            st.warning("Digite um título")

# -------------------------
# LISTA
# -------------------------

if menu == "Lista de tarefas":

    st.title("📋 Lista de tarefas")

    for i,task in enumerate(st.session_state.tasks):

        col1,col2 = st.columns([5,1])

        with col1:

            if task["done"]:
                st.write(f"✅ **{task['titulo']}**")
            else:
                st.write(f"⬜ **{task['titulo']}**")

            st.write(task["descricao"])

        with col2:

            if not task["done"]:

                if st.button("Concluir", key=i):

                    st.session_state.tasks[i]["done"] = True
                    st.rerun()

# -------------------------
# EXPORTAR
# -------------------------

if menu == "Exportar":

    st.title("📥 Exportar tarefas")

    df = pd.DataFrame(st.session_state.tasks)

    csv = df.to_csv(index=False)

    st.download_button(
        label="Baixar CSV",
        data=csv,
        file_name="tarefas.csv",
        mime="text/csv"
    )