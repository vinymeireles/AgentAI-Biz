# app_biz.py
# ==========================================================
# 🧑‍💼 AgentAI Biz — Criador de Planos de Negócio
# ==========================================================
# login padrão: admin | senha: admin123
# ==========================================================

import streamlit as st
import sqlite3
import os, time
import hashlib
import binascii
import hmac
from datetime import datetime
from crewai import Crew, Process
from biz_components import BizAgents, BizTasks
from biz_utils import load_markdown, save_markdown, convert_md_to_pdf, file_exists
from biz_tools import safe_float
import shutil

from streamlit_option_menu import option_menu

# Importa renderizadores de página
from page.projeto import render_projeto
from page.sobre import render_sobre

# ==========================================================
# CONFIGURAÇÕES INICIAIS
# ==========================================================
DB_PATH = "users_biz.db"
OUTPUT_DIR = os.path.join(os.getcwd(), "biz_output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

st.set_page_config(page_title="AgentAI Biz", page_icon="💼", layout="wide")

# Style: CSS para esconder o menu hamburger (☰) e o footer
if os.path.exists('style.css'):
    with open('style.css') as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ==========================================================
# BANCO DE DADOS / LOGIN
# ==========================================================
def get_conn():
    return sqlite3.connect(DB_PATH, check_same_thread=False)

def init_db():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            salt TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'user',
            created_at TEXT NOT NULL
        )
    """)
    conn.commit()

    cur.execute("SELECT id FROM users WHERE username='admin'")
    if not cur.fetchone():
        pwd_hash, salt = hash_password('admin123')
        cur.execute(
            "INSERT INTO users (username, password_hash, salt, role, created_at) VALUES (?, ?, ?, ?, ?)",
            ('admin', pwd_hash, salt, 'admin', datetime.utcnow().isoformat())
        )
        conn.commit()
    conn.close()

def hash_password(password: str, salt: bytes = None):
    if salt is None:
        salt = os.urandom(16)
    dk = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 200000)
    return binascii.hexlify(dk).decode(), binascii.hexlify(salt).decode()

def verify_password(stored_hash_hex, stored_salt_hex, password_attempt):
    salt = binascii.unhexlify(stored_salt_hex)
    attempt_hash_hex, _ = hash_password(password_attempt, salt)
    return hmac.compare_digest(attempt_hash_hex, stored_hash_hex)

def authenticate_user(username, password):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT password_hash, salt, role FROM users WHERE username=?", (username,))
    row = cur.fetchone()
    conn.close()
    if not row:
        return False, "Usuário não encontrado", None
    stored_hash, stored_salt, role = row
    ok = verify_password(stored_hash, stored_salt, password)
    return (True, "Autenticado", role) if ok else (False, "Senha incorreta", None)

init_db()

# ==========================================================
# CONTROLE DE SESSÃO
# ==========================================================
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False
if 'login_flag' not in st.session_state:
    st.session_state['login_flag'] = False

# ==========================================================
# TELA DE LOGIN
# ==========================================================
if not st.session_state['authenticated']:
    st.title("🔐 Acesso - AgentAI Biz")

    with st.container(border=True):
        username = st.text_input("Usuário")
        password = st.text_input("Senha", type="password")
        submitted = st.button("Entrar")

        if submitted or st.session_state.get('login_flag', False):
            if not st.session_state.get('login_flag', False):
               with st.spinner("🔄 Verificando credenciais, aguarde..."): 
                    ok, msg, role = authenticate_user(username.strip(), password)
                    time.sleep(1.2)  # pequena pausa visual (~1 segundo)
                    if ok:
                        st.session_state['authenticated'] = True
                        st.session_state['username'] = username
                        st.session_state['role'] = role
                        st.session_state['login_flag'] = True
                        st.rerun()
                    else:
                        st.error(msg)
            else:
                st.session_state['login_flag'] = False

    st.stop()


# ==========================================================
# SIDEBAR E MENU
# ==========================================================
st.sidebar.image("Img/logoAI.png", width=160)
st.sidebar.markdown(f"👋 Olá, **{st.session_state.username}**!")
if st.sidebar.button("🚪 Sair"):
    for key in ["authenticated", "username", "role", "login_flag"]:
        st.session_state[key] = False if key == "authenticated" else ""
    st.rerun()

selected = option_menu(
    menu_title=None,
    options=["Aplicativo", "Projeto", "Sobre"],
    icons=["briefcase", "book", "info-circle"],
    orientation="horizontal",
    styles={
        "container": {"background-color": "#0b5cff", "border-radius": "8px"},
        "icon": {"color": "white", "font-size": "18px"},
        "nav-link": {"color": "white", "font-size": "15px", "padding": "8px 18px"},
        "nav-link-selected": {"background-color": "#053a9b", "font-weight": "bold", "color": "white"},
    },
)


# ==========================================================
# ROTEAMENTO SIMPLES
# ==========================================================
if selected == "Projeto":
    render_projeto()
    gerar = False
elif selected == "Sobre":
    render_sobre()
    gerar = False
else:
# ==========================================================
# APLICATIVO PRINCIPAL
# ==========================================================
    st.title("💼 AgentAI Biz — Criador de Planos de Negócio")
    st.markdown("Preencha as informações e gere seu **plano completo + pitch deck** automaticamente.")

    # ==========================================================
    # PERFIS RÁPIDOS
    # ==========================================================
    st.markdown("### 📂 Perfis Rápidos (exemplos)")
    perfis = {
        "Startup SaaS (B2B)": {
            "nome_empresa": "Acme SaaS",
            "segmento": "SaaS B2B",
            "publico_alvo": "PMEs de tecnologia",
            "modelo_receita": "Assinatura",
            "ticket_medio": "150.0",
            "custo_medio_mensal": "20000.0",
            "meta_12m": "Crescer 200% na receita."
        },
        "E-commerce Local": {
            "nome_empresa": "Loja Bairro",
            "segmento": "E-commerce",
            "publico_alvo": "Consumidores locais",
            "modelo_receita": "Venda direta",
            "ticket_medio": "45.0",
            "custo_medio_mensal": "8000.0",
            "meta_12m": "Atingir EBITDA positivo."
        },
        "Consultoria Financeira": {
            "nome_empresa": "FinPro Consultoria",
            "segmento": "Serviços financeiros",
            "publico_alvo": "Empresas médias e startups",
            "modelo_receita": "Assinatura mensal",
            "ticket_medio": "1200.0",
            "custo_medio_mensal": "15000.0",
            "meta_12m": "Expandir carteira de clientes em 50%."
        },
        "Agência de Marketing Digital": {
            "nome_empresa": "MktBoost",
            "segmento": "Marketing Digital",
            "publico_alvo": "E-commerces e influenciadores",
            "modelo_receita": "Prestação de serviços",
            "ticket_medio": "3500.0",
            "custo_medio_mensal": "25000.0",
            "meta_12m": "Aumentar taxa de retenção para 90%."
        },
        "Desenvolvedor de Aplicações IA e Agents AI": {
            "nome_empresa": "AgentAI Labs",
            "segmento": "Tecnologia / IA",
            "publico_alvo": "Empresas que buscam automação inteligente",
            "modelo_receita": "Licenciamento e consultoria",
            "ticket_medio": "5000.0",
            "custo_medio_mensal": "35000.0",
            "meta_12m": "Lançar 3 novos produtos baseados em agentes inteligentes."
        },
        "Restaurante Saudável": {
            "nome_empresa": "Vida Leve",
            "segmento": "Alimentação saudável",
            "publico_alvo": "Profissionais urbanos",
            "modelo_receita": "Venda direta e delivery",
            "ticket_medio": "60.0",
            "custo_medio_mensal": "18000.0",
            "meta_12m": "Abrir segunda unidade na cidade."
        }
}

    perfil_escolhido = st.selectbox("Selecione um perfil de negócio:", ["Nenhum"] + list(perfis.keys()))
    if perfil_escolhido != "Nenhum":
        perfil = perfis[perfil_escolhido]
        st.success(f"✅ Perfil '{perfil_escolhido}' carregado.")
        for k, v in perfil.items():
            st.session_state[k] = v
    else:
        for campo in ["nome_empresa", "segmento", "publico_alvo", "modelo_receita", "ticket_medio", "custo_medio_mensal", "meta_12m"]:
            st.session_state[campo] = st.session_state.get(campo, "")

    # ==========================================================
    # FORMULÁRIO PRINCIPAL
    # ==========================================================
    gerar = False
    limpar = False

    with st.form("form_biz"):
        st.subheader("📋 Dados do Negócio")

        nome_empresa = st.text_input("Nome da Empresa", value=st.session_state.get("nome_empresa", ""))
        segmento = st.text_input("Segmento / Nicho", value=st.session_state.get("segmento", ""))
        publico_alvo = st.text_area("Público-alvo", value=st.session_state.get("publico_alvo", ""))
        modelo_receita = st.selectbox("Modelo de Receita", ["Assinatura", "Venda direta", "Marketplace", "Freemium", "Outro"])
        ticket_medio = st.number_input("Ticket médio (R$)", value=safe_float(st.session_state.get("ticket_medio", 0.0)))
        custo_medio_mensal = st.number_input("Custo médio mensal (R$)", value=safe_float(st.session_state.get("custo_medio_mensal", 0.0)))
        meta_12m = st.text_input("Meta para 12 meses", value=st.session_state.get("meta_12m", ""))

        colA, colB = st.columns(2)
        with colA:
            gerar = st.form_submit_button("🚀 Gerar Plano")
        with colB:
            limpar = st.form_submit_button("🧹 Limpar")

    # ==========================================================
    # LIMPAR ARQUIVOS E CAMPOS
    # ==========================================================
    def clear_output_dir():
        for file in os.listdir(OUTPUT_DIR):
            path = os.path.join(OUTPUT_DIR, file)
            if os.path.isfile(path) and file.lower().endswith(('.md', '.pdf')):
                os.remove(path)

    if limpar:
        clear_output_dir()
        for k in ["nome_empresa","segmento","publico_alvo","modelo_receita","ticket_medio","custo_medio_mensal","meta_12m"]:
            st.session_state[k] = "" if isinstance(st.session_state.get(k,""), str) else 0.0
        st.success("🧼 Relatórios e formulário limpos.")
        st.rerun()

    # ==========================================================
    # EXECUÇÃO DOS AGENTES
    # ==========================================================
    expected_files = {
        "plano_negocios.md": "plano_negocios.pdf",
        "resumo_executivo.md": "resumo_executivo.pdf",
        "pitch_deck.md": "pitch_deck.pdf",
    }

    gerar = gerar if "gerar" in locals() else False

    if gerar:
        with st.spinner("🤖 Gerando plano de negócios..."):
            agents = BizAgents()
            tasks = BizTasks()

            market_agent = agents.market_agent()
            finance_agent = agents.finance_agent()
            brand_agent = agents.brand_agent()
            pitch_agent = agents.pitch_agent()

            profile_data = {
                "nome_empresa": nome_empresa,
                "segmento": segmento,
                "publico_alvo": publico_alvo,
                "modelo_receita": modelo_receita,
                "ticket_medio": ticket_medio,
                "custo_medio_mensal": custo_medio_mensal,
                "meta_12m": meta_12m
            }

            market_task = tasks.market_task(market_agent, profile_data)
            finance_task = tasks.finance_task([market_task], finance_agent, profile_data)
            brand_task = tasks.brand_task([finance_task], brand_agent, profile_data)
            pitch_task = tasks.pitch_task([brand_task], pitch_agent, profile_data)

            crew = Crew(
                agents=[market_agent, finance_agent, brand_agent, pitch_agent],
                tasks=[market_task, finance_task, brand_task, pitch_task],
                process=Process.sequential,
                full_output=True,
                verbose=True
            )

            try:
                crew.kickoff()
            except Exception as e:
                st.error(f"Erro ao executar agentes: {e}")

        for md_name, pdf_name in expected_files.items():
            md_path = os.path.join(OUTPUT_DIR, md_name)
            pdf_path = os.path.join(OUTPUT_DIR, pdf_name)
            if os.path.exists(md_path):
                convert_md_to_pdf(md_path, pdf_path)
        st.success("✅ Plano de Negócios e Pitch Deck gerados!")

        # mover MD gerados para OUTPUT_DIR
        moved_any = False
        for md_name, pdf_name in expected_files.items():
            src_cwd = os.path.join(os.getcwd(), md_name)
            dest_md = os.path.join(OUTPUT_DIR, md_name)
            if os.path.exists(src_cwd):
                try:
                    shutil.move(src_cwd, dest_md)
                    moved_any = True
                except Exception as e:
                    st.warning(f"Não foi possível mover {md_name} para {OUTPUT_DIR}: {e}")
            elif os.path.exists(dest_md):
                moved_any = True

        # converter MD -> PDF somente quando MD existir em OUTPUT_DIR
        for md_name, pdf_name in expected_files.items():
            md_path = os.path.join(OUTPUT_DIR, md_name)
            pdf_path = os.path.join(OUTPUT_DIR, pdf_name)
            if os.path.exists(md_path):
                ok = convert_md_to_pdf(md_path, pdf_path)
                if not ok:
                    st.warning(f"Falha ao converter {md_name} para PDF.")
            else:
                st.info(f"Atenção: {md_name} não foi gerado pelos agentes.")

        st.success("✅ Planos e relatórios processados (movidos/convertidos).")

# ==========================================================
# EXIBIÇÃO E DOWNLOADS
# ==========================================================
if selected == "Aplicativo":
    # Verifica se há relatórios gerados (MDs)
    if any(os.path.exists(os.path.join(OUTPUT_DIR, md)) for md in expected_files.keys()):
        tabs = st.tabs(["📝 Plano de Negócios", "📄 Resumo Executivo", "📊 Pitch Deck", "📥 Downloads"])

        # ==============================
        # 📝 Plano de Negócios
        # ==============================
        with tabs[0]:
            md_path = os.path.join(OUTPUT_DIR, "plano_negocios.md")
            content = load_markdown(md_path) 
            if content:
                st.markdown(content, unsafe_allow_html=True)
            else:
                st.info("Nenhum plano de negócios gerado ainda.")

        # ==============================
        # 📄 Resumo Executivo
        # ==============================
        with tabs[1]:
            md_path = os.path.join(OUTPUT_DIR, "resumo_executivo.md")
            content = load_markdown(md_path) 
            if content:
                st.markdown(content, unsafe_allow_html=True)
            else:
                st.info("Nenhum resumo executivo gerado ainda.")

        # ==============================
        # 📊 Pitch Deck
        # ==============================
        with tabs[2]:
            md_path = os.path.join(OUTPUT_DIR, "pitch_deck.md")
            content = load_markdown(md_path) 
            if content:
                st.markdown(content, unsafe_allow_html=True)
            else:
                st.info("Nenhum pitch deck gerado ainda.")

        # ==============================
        # 📥 Downloads
        # ==============================
        with tabs[3]:
            st.subheader("📥 Relatórios disponíveis para download")

            # Lista de arquivos PDF disponíveis
            pdfs = [f for f in os.listdir(OUTPUT_DIR) if f.lower().endswith(".pdf")]

            if pdfs:
                for file in pdfs:
                    path = os.path.join(OUTPUT_DIR, file)
                    if os.path.exists(path):
                        # Lê o PDF em memória
                        with open(path, "rb") as f:
                            pdf_bytes = f.read()

                        # Botão de download individual
                        st.download_button(
                            label=f"📄 Baixar {file}",
                            data=pdf_bytes,
                            file_name=file,
                            mime="application/pdf",
                            use_container_width=False
                        )
                    else:
                        st.warning(f"⚠️ Arquivo esperado não encontrado: {file}")
            else:
                st.info("Nenhum PDF disponível para download ainda.")

    else:
        st.info("Nenhum relatório disponível ainda. Gere planos usando o formulário acima.")


st.info("💼 Desenvolvido por Vinicius Meireles | AgentAI Biz 2025")
