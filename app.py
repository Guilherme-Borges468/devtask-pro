import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="DevTask Pro",
    page_icon="🚀",
    layout="wide"
)

# -------------------------
# ESTILO
# -------------------------

st.markdown("""
<style>

.block-container{
padding-top: 2rem;
}

.login-box{
max-width:400px;
margin:auto;
padding:40px;
border-radius:10px;
background-color:#1e1e1e;
box-shadow:0 0 20px rgba(0,0,0,0.3);
}

</style>
""", unsafe_allow_html=True)

# -------------------------
# LOGIN
# -------------------------

def login():

    st.markdown("<div class='login-box'>", unsafe_allow_html=True)

    st.title("🚀 DevTask Pro")
    st.write("Gerenciador de tarefas para desenvolvedores")

    user = st.text_input("Usuário")
    password = st.text_input("Senha", type="password")

    if st.button("Entrar", use_container_width=True):

        if user == "admin" and password == "123":

            st.session_state["logado"] = True
            st.rerun()

        else:

            st.error("Credenciais inválidas")

    st.markdown("</div>", unsafe_allow_html=True)


if "logado" not in st.session_state:
    st.session_state["logado"] = False

if not st.session_state["logado"]:
    login()
    st.stop()

# -------------------------
# BANCO FAKE
# -------------------------

if "tasks" not in st.session_state:

    st.session_state.tasks = [

        {"titulo":"Criar sistema de login","descricao":"Implementar autenticação","done":True},

        {"titulo":"Criar dashboard","descricao":"Adicionar métricas e gráficos","done":True},

        {"titulo":"Criar API","descricao":"Integração com backend","done":False},

        {"titulo":"Sistema de notificações","descricao":"Alertar usuários","done":False},

        {"titulo":"Melhorar UI","descricao":"Aplicar design moderno","done":False},

    ]

# -------------------------
# SIDEBAR
# -------------------------

st.sidebar.title("🚀 DevTask Pro")

menu = st.sidebar.radio(
    "Menu",
    ["Dashboard","Nova tarefa","Tarefas"]
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
    done = sum(t["done"] for t in st.session_state.tasks)

    col1,col2,col3 = st.columns(3)

    col1.metric("Total tarefas", total)
    col2.metric("Concluídas", done)
    col3.metric("Pendentes", total-done)

    if total > 0:

        progresso = done/total
        st.progress(progresso)

    df = pd.DataFrame({
        "Status":["Concluídas","Pendentes"],
        "Quantidade":[done,total-done]
    })

    st.subheader("Distribuição de tarefas")

    st.bar_chart(df.set_index("Status"))

# -------------------------
# NOVA TAREFA
# -------------------------

if menu == "Nova tarefa":

    st.title("➕ Criar nova tarefa")

    titulo = st.text_input("Título")
    descricao = st.text_area("Descrição")

    if st.button("Salvar"):

        if titulo:

            st.session_state.tasks.append({

                "titulo":titulo,
                "descricao":descricao,
                "done":False

            })

            st.success("Tarefa criada!")

            st.rerun()

# -------------------------
# LISTA
# -------------------------

if menu == "Tarefas":

    st.title("📋 Lista de tarefas")

    for i,task in enumerate(st.session_state.tasks):

        col1,col2,col3 = st.columns([4,1,1])

        with col1:

            if task["done"]:
                st.write(f"✅ **{task['titulo']}**")
            else:
                st.write(f"⬜ **{task['titulo']}**")

            st.write(task["descricao"])

        with col2:

            if not task["done"]:

                if st.button("Concluir", key=f"done{i}"):

                    st.session_state.tasks[i]["done"] = True
                    st.rerun()

        with col3:

            if st.button("Excluir", key=f"del{i}"):

                st.session_state.tasks.pop(i)
                st.rerun()