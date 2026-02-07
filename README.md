# 💼 AgentAI Biz — Sistema de Agentes Inteligentes para Negócios

**AgentAI Biz** é uma plataforma baseada em **Inteligência Artificial Multiagente (CrewAI)**, desenvolvida para **automatizar a criação de planos de negócio completos** — desde a análise de mercado até a geração automática de **pitch decks profissionais em PDF**.

<p align="center">
  <img src="Img/logoAI.png" alt="AgentAI Biz Logo" width="320"/>
</p>

---

## 🧭 Visão Geral

Empreender exige planejamento, análise de dados e uma comunicação eficaz com investidores.  
O **AgentAI Biz** utiliza múltiplos **agentes inteligentes** trabalhando em conjunto para gerar, de forma automática:

- 📊 **Análises de mercado**  
- 💰 **Projeções financeiras completas**  
- 💡 **Estratégias de marca e posicionamento**  
- 🧾 **Pitch decks prontos para apresentação**  

Tudo isso em **minutos**, com relatórios exportáveis em **Markdown e PDF**.

---

## 🤖 Estrutura Multiagente

O sistema é composto por quatro agentes principais, coordenados pelo framework **CrewAI**:

| Agente | Função |
|--------|--------|
| 🧠 **MarketAnalystAgent** | Analisa o mercado, identifica nichos e mapeia concorrentes. |
| 💹 **FinancialModelAgent** | Gera projeções financeiras automáticas e sustentáveis. |
| 🎯 **BrandStrategistAgent** | Define a proposta de valor e posicionamento da marca. |
| 🧾 **PitchDeckAgent** | Cria o resumo executivo e o pitch deck final em PDF. |

Esses agentes operam de forma **sequencial e colaborativa**, garantindo coerência entre todos os aspectos do negócio.

---

## 🚀 Funcionalidades Principais

✅ Login com autenticação e perfis de usuário (SQLite)  
✅ Formulário interativo para entrada de dados do negócio  
✅ Geração automática de relatórios `.md` e `.pdf`  
✅ Conversão Markdown → PDF com layout corporativo  
✅ Perfis de exemplo (E-commerce, SaaS, Startup IA, etc.)  
✅ Download individual ou em pacote `.zip`  
✅ Interface moderna com **Streamlit Option Menu**  
✅ Total integração com o framework **CrewAI**

---

## 🏗️ Arquitetura e Tecnologias

**Principais componentes do sistema:**

| Módulo | Descrição |
|--------|------------|
| `app_biz.py` | Interface principal e lógica de login/navegação |
| `biz_components.py` | Definições dos agentes de IA e suas funções |
| `biz_tasks.py` | Tarefas atribuídas a cada agente CrewAI |
| `biz_utils.py` | Utilitários de leitura, salvamento e conversão de arquivos |
| `style.css` | Personalização visual da aplicação |
| `biz_output/` | Diretório de saída dos relatórios gerados |

**Tecnologias utilizadas:**

- 🧠 [CrewAI](https://pypi.org/project/crewai/) — Coordenação de agentes inteligentes  
- 💾 SQLite — Banco de dados local de usuários  
- 🎨 Streamlit — Interface web interativa  
- 🧾 ReportLab + Markdown2 — Conversão e geração de PDFs  
- 🧩 Python 3.10+ — Base de execução  

---

📍 **Autor:** [Paulo Vinicius Meireles]  
🔗 Solução comercial disponível em: https://www.vimeup.com
