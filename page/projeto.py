import streamlit as st
import os

# ======================================
# 🔧 Configurações iniciais
# ======================================
st.set_page_config(page_title="AgentAI Biz - Sistema de IA para Negócios", page_icon="💼", layout="wide")

if os.path.exists("style.css"):
    with open("style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


# ======================================
# 🎯 Cabeçalho do Projeto
# ======================================
def render_projeto():

    st.title("💼 Projeto: AgentAI Biz — Sistema de Agentes Inteligentes para Negócios")
    st.markdown("---")

    st.info("""
    O **AgentAI Biz** é um sistema baseado em **IA Multiagente** desenvolvido para automatizar a criação de 
    **planos de negócio completos**, combinando análise de mercado, modelagem financeira, branding estratégico 
    e geração automática de **pitch decks profissionais em PDF**.
    """)

    # ======================================
    # 🧭 Cenário Atual
    # ======================================
    st.header("🧭 Cenário Atual dos Negócios")
    st.markdown("""
    Empreender no século XXI exige **tomadas de decisão rápidas, dados precisos e estratégias bem estruturadas**.  
    No entanto, muitos empreendedores enfrentam obstáculos significativos:

    - Dificuldade em **analisar mercados** de forma aprofundada e competitiva.  
    - Falta de **planejamento financeiro consistente** e sustentável.  
    - Pouco conhecimento sobre **posicionamento de marca** e proposta de valor.  
    - Dificuldade em **apresentar ideias de forma profissional** para investidores.

    O **AgentAI Biz** surge como uma resposta tecnológica para acelerar e automatizar esses processos,
    tornando o planejamento de negócios **mais acessível, inteligente e estratégico**.
    """)

    st.markdown("---")

    # ======================================
    # ⚙️ Desafios Identificados
    # ======================================
    st.header("⚙️ Desafios Identificados")
    st.markdown("""
    A criação de um plano de negócios tradicional pode levar **semanas ou meses** e exige conhecimento multidisciplinar.

    Os principais desafios são:
    - 📊 Falta de dados de mercado estruturados e atualizados.  
    - 🧾 Planejamentos financeiros inconsistentes ou incompletos.  
    - 💡 Ausência de uma identidade de marca clara.  
    - 🎯 Dificuldade em sintetizar o plano em **apresentações (pitch decks)** atrativas e persuasivas.

    A proposta é **utilizar agentes de IA colaborativos** que trabalhem em conjunto para entregar um plano profissional 
    completo — desde a concepção da ideia até o material final de apresentação.
    """)

    st.markdown("---")

    # ======================================
    # 🤖 Solução Multiagente
    # ======================================
    st.header("🤖 Solução Multiagente — O Cérebro do Negócio Inteligente")
    st.markdown("""
    O **AgentAI Biz** adota uma arquitetura **multiagente**, onde cada agente é responsável por um 
    aspecto fundamental da construção de um negócio.

    Essa estrutura permite que as decisões e análises sejam **interdependentes**, garantindo coerência
    entre mercado, finanças, marca e apresentação.
    """)

    st.markdown("""
    #### 👥 Agentes de IA e suas Funções

    1. **MarketAnalystAgent**  
       Analisa o setor, identifica concorrentes e oportunidades de mercado, e define o posicionamento estratégico.

    2. **FinancialModelAgent**  
       Cria projeções financeiras automáticas, estimando custos, receitas, fluxo de caixa e lucratividade.

    3. **BrandStrategistAgent**  
       Define o propósito, valores, diferenciais competitivos e proposta de valor da marca.

    4. **PitchDeckAgent**  
       Sintetiza as informações geradas pelos outros agentes em um **pitch deck visual e objetivo**, pronto para investidores.
    """)

    st.markdown("---")

    # ======================================
    # 🎯 Objetivos
    # ======================================
    st.header("🎯 Objetivos do Projeto")
    st.markdown("""
    O **AgentAI Biz** busca democratizar o acesso a ferramentas de planejamento estratégico,
    permitindo que **empreendedores e startups** criem planos de negócio sólidos de forma autônoma e rápida.

    **Principais objetivos:**
    - 🤖 Automatizar a geração de **planos de negócio profissionais**.  
    - 📈 Aumentar a **precisão e consistência** das projeções financeiras.  
    - 💬 Fornecer **análises de mercado atualizadas** e contextualizadas.  
    - 💡 Criar uma **identidade de marca única** com base nos dados e perfil da empresa.  
    - 📊 Gerar automaticamente **relatórios em Markdown e PDFs empresariais**.  
    - 🚀 Facilitar a **apresentação a investidores** com um pitch deck pronto e visual.

    O sistema reduz drasticamente o tempo e custo de elaboração de um plano de negócios,
    sem comprometer a profundidade ou qualidade analítica.
    """)

    st.markdown("---")

    # ======================================
    # 💡 Tecnologia e Metodologia
    # ======================================
    st.header("💡 Tecnologia e Metodologia")
    st.markdown("""
    O projeto foi desenvolvido com base no framework **CrewAI**, responsável por orquestrar 
    múltiplos agentes especializados em **análise, geração de conteúdo e raciocínio autônomo**.

    **Principais tecnologias e conceitos aplicados:**
    - 🧠 **CrewAI Framework** — coordena as tarefas e fluxos entre os agentes.  
    - 🔄 **Arquitetura Multiagente** — colaboração entre agentes para decisões interligadas.  
    - 💾 **SQLite + Streamlit** — gerenciamento de usuários, login e interface interativa.  
    - 🧾 **ReportLab + Markdown2** — geração de relatórios e PDFs com design corporativo.  
    - 📂 **Modularidade** — fácil expansão para novos agentes (ex: Legal, Marketing, Tech).

    #### 🧩 Fluxo ReAct (Reasoning + Action)
    1. **Thought (Análise):** o agente compreende o contexto do negócio.  
    2. **Action (Ação):** gera análises, modelos e textos.  
    3. **Observation (Avaliação):** ajusta a resposta com base no resultado.  
    4. 🔁 **Loop contínuo** até chegar à solução ideal.
    """)

    st.markdown("---")

    # ======================================
    # 🚀 Resultados Esperados
    # ======================================
    st.header("🚀 Resultados Esperados")
    st.markdown("""
    Com o **AgentAI Biz**, espera-se que empreendedores e equipes possam criar planos de negócio
    **completos, coerentes e visualmente atraentes** em minutos.

    - ⚡ **Geração instantânea** de planos e apresentações.  
    - 📈 **Projeções financeiras confiáveis e dinâmicas**.  
    - 💬 **Análises de mercado e branding integradas**.  
    - 💻 **PDFs profissionais e prontos para envio**.  
    - 🔁 **Aprimoramento contínuo** com base no feedback do usuário.

    Essa solução eleva o padrão de planejamento empresarial, unindo **estratégia, automação e inteligência artificial**.
    """)

    st.markdown("---")

    # ======================================
    # 🗂️ Conclusão
    # ======================================
    st.header("🗂️ Conclusão")
    st.success("""
    O **AgentAI Biz** representa um novo paradigma na forma de **planejar, estruturar e apresentar negócios**.

    Ao unir agentes inteligentes especializados em **mercado, finanças, marca e estratégia**, 
    a plataforma transforma o processo tradicional em uma experiência **rápida, interativa e profissional**.

    Essa fusão entre **automação inteligente e planejamento estratégico** inaugura a era do 
    **Business Plan Assistido por IA**, tornando o empreendedorismo mais **eficiente, inclusivo e competitivo**.
    """)

