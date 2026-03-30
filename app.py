
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="DevBoard AI",
    page_icon="🚀",
    layout="wide"
)

# -----------------------
# CSS / VISUAL
# -----------------------

st.markdown("""
<style>
.stApp {
    background-color: #0e1117;
    color: white;
}

button {
    border-radius: 8px !important;
}

.block-container {
    padding-top: 2rem;
}
</style>
""", unsafe_allow_html=True)

# -----------------------
# LOGIN
# -----------------------

def login():

    col1, col2, col3 = st.columns([1,2,1])

    with col2:

        st.title("🚀 DevBoard AI")
        st.write("Kanban para equipes de desenvolvimento")

        user = st.text_input("Usuário")
        password = st.text_input("Senha", type="password")

        if st.button("Entrar", use_container_width=True):

            if user == "admin" and password == "123":

                st.session_state["logado"] = True
                st.rerun()

            else:

                st.error("Usuário ou senha inválidos")


if "logado" not in st.session_state:
    st.session_state["logado"] = False


if not st.session_state["logado"]:
    login()
    st.stop()


# -----------------------
# BANCO DE TAREFAS
# -----------------------

if "tasks" not in st.session_state:

    st.session_state.tasks = [

        {"titulo":"Criar sistema de login","descricao":"Implementar autenticação","status":"todo"},
        {"titulo":"Criar dashboard","descricao":"Adicionar métricas","status":"progress"},
        {"titulo":"Criar API REST","descricao":"Integração backend","status":"todo"},
        {"titulo":"Deploy cloud","descricao":"Publicar aplicação","status":"done"},
        {"titulo":"Melhorar UI","descricao":"Aplicar design moderno","status":"progress"}

    ]


# -----------------------
# HEADER / PROGRESSO
# -----------------------

st.markdown("## 🚀 DevBoard AI")

total_tasks = len(st.session_state.tasks)
done_tasks = len([t for t in st.session_state.tasks if t["status"]=="done"])

progress = int((done_tasks/total_tasks)*100) if total_tasks > 0 else 0

st.progress(progress)
st.caption(f"Progresso do projeto: {progress}% concluído")


# -----------------------
# SIDEBAR
# -----------------------

st.sidebar.title("🚀 DevBoard AI")

menu = st.sidebar.radio(
    "Menu",
    ["Dashboard","Kanban","Nova tarefa"]
)

if st.sidebar.button("Sair"):

    st.session_state["logado"] = False
    st.rerun()


# -----------------------
# DASHBOARD
# -----------------------

if menu == "Dashboard":

    st.title("📊 Dashboard")

    df = pd.DataFrame(st.session_state.tasks)

    total = len(df)
    todo = len(df[df["status"]=="todo"])
    progress_count = len(df[df["status"]=="progress"])
    done = len(df[df["status"]=="done"])

    col1,col2,col3,col4 = st.columns(4)

    col1.metric("Total", total)
    col2.metric("A Fazer", todo)
    col3.metric("Em Progresso", progress_count)
    col4.metric("Concluído", done)

    st.subheader("Distribuição de tarefas")

    graf = pd.DataFrame({

        "Status":["A Fazer","Em Progresso","Concluído"],
        "Quantidade":[todo,progress_count,done]

    })

    st.bar_chart(graf.set_index("Status"))

    st.subheader("📌 Últimas tarefas")

    for t in st.session_state.tasks[-5:]:

        st.write(f"**{t['titulo']}** - {t['status']}")


# -----------------------
# NOVA TAREFA
# -----------------------

if menu == "Nova tarefa":

    st.title("➕ Criar tarefa")

    titulo = st.text_input("Título")
    descricao = st.text_area("Descrição")

    status = st.selectbox(
        "Status inicial",
        ["todo","progress","done"]
    )

    if st.button("Criar tarefa"):

        if titulo:

            st.session_state.tasks.append({

                "titulo":titulo,
                "descricao":descricao,
                "status":status

            })

            st.success("Tarefa criada!")

            st.rerun()

        else:

            st.warning("Digite um título")

    st.divider()

    if st.button("⚡ Gerar tarefas de exemplo"):

        exemplos = [

            {"titulo":"Criar API de usuários","descricao":"CRUD completo","status":"todo"},
            {"titulo":"Sistema de autenticação","descricao":"JWT login","status":"progress"},
            {"titulo":"Dashboard analytics","descricao":"Gráficos de dados","status":"todo"},
            {"titulo":"Deploy AWS","descricao":"Infraestrutura cloud","status":"done"}

        ]

        st.session_state.tasks.extend(exemplos)

        st.success("Tarefas de exemplo criadas!")

        st.rerun()


# -----------------------
# KANBAN
# -----------------------

if menu == "Kanban":

    st.title("🗂 Quadro Kanban")

    col1,col2,col3 = st.columns(3)

    todo_tasks = [t for t in st.session_state.tasks if t["status"]=="todo"]
    progress_tasks = [t for t in st.session_state.tasks if t["status"]=="progress"]
    done_tasks = [t for t in st.session_state.tasks if t["status"]=="done"]

    with col1:

        st.subheader("📌 A Fazer")

        for i,task in enumerate(todo_tasks):

            st.write(f"**{task['titulo']}**")
            st.write(task["descricao"])

            if st.button("➡ mover", key=f"todo{i}"):

                task["status"] = "progress"
                st.rerun()

            if st.button("🗑 excluir", key=f"deltodo{i}"):

                st.session_state.tasks.remove(task)
                st.rerun()

            st.divider()

    with col2:

        st.subheader("⚙ Em Progresso")

        for i,task in enumerate(progress_tasks):

            st.write(f"**{task['titulo']}**")
            st.write(task["descricao"])

            if st.button("➡ concluir", key=f"prog{i}"):

                task["status"] = "done"
                st.rerun()

            if st.button("🗑 excluir", key=f"delprog{i}"):

                st.session_state.tasks.remove(task)
                st.rerun()

            st.divider()

    with col3:

        st.subheader("✅ Concluído")

        for i,task in enumerate(done_tasks):

            st.write(f"**{task['titulo']}**")
            st.write(task["descricao"])

            if st.button("🗑 excluir", key=f"deldone{i}"):

                st.session_state.tasks.remove(task)
                st.rerun()

            st.divider()
