# biz_components.py
# Agents and Tasks for AgentAI Biz (CrewAI)
from crewai import Agent, Task, LLM
from textwrap import dedent
import os

class BizAgents:
    def __init__(self):
        self.llm = LLM(model="gpt-4o-mini", api_key=os.getenv("OPENAI_API_KEY"))

    def market_agent(self):
        return Agent(
            role="MarketAnalystAgent",
            goal=dedent("""
                Pesquisar nicho, concorrência, tamanho de mercado e diferenciais competitivos.
                Produzir análise de mercado e mapa de concorrentes.
            """),
            backstory=dedent("""
                Sou um analista de mercado experiente que sintetiza dados e gera insights acionáveis.
            """),
            llm=self.llm,
            verbose=True,
            max_iter=6,
            allow_delegation=False
        )

    def finance_agent(self):
        return Agent(
            role="FinancialModelAgent",
            goal=dedent("""
                Gerar projeções financeiras simples (receita, custos, margem) e estimativas para 12 meses.
            """),
            backstory=dedent("""
                Sou um analista financeiro que cria modelos práticos para negócios em estágio inicial.
            """),
            llm=self.llm,
            verbose=True,
            max_iter=8,
            allow_delegation=False
        )

    def brand_agent(self):
        return Agent(
            role="BrandStrategistAgent",
            goal=dedent("""
                Definir proposta de valor, positioning, público-alvo e principais mensagens de comunicação.
            """),
            backstory=dedent("""
                Sou um estrategista de marca que transforma insights de mercado em posicionamento e tom de voz.
            """),
            llm=self.llm,
            verbose=True,
            max_iter=6,
            allow_delegation=False
        )

    def pitch_agent(self):
        return Agent(
            role="PitchDeckAgent",
            goal=dedent("""
                Compilar um resumo executivo e criar estrutura de pitch deck (slides em texto) pronto para exportar em PDF.
            """),
            backstory=dedent("""
                Sou um consultor de startups que cria pitch decks claros, concisos e persuasivos.
            """),
            llm=self.llm,
            verbose=True,
            max_iter=6,
            allow_delegation=False
        )


class BizTasks:
    def market_task(self, agent, profile_data):
        return Task(
            description=dedent(f"""
                Analisar mercado e concorrência para:
                {profile_data}
            """),
            expected_output=dedent("""
                Relatório de análise de mercado em markdown:
                - Sumário do mercado
                - Principais concorrentes
                - Tendências e oportunidades
            """),
            agent=agent,
            output_file="plano_negocios.md"
        )

    def finance_task(self, context, agent, profile_data):
        return Task(
            description=dedent(f"""
                Gerar projeções financeiras simples com base nos dados:
                {profile_data}
            """),
            expected_output=dedent("""
                Seção de projeção financeira em markdown:
                - Receita estimada (12 meses)
                - Custos estimados e margem
                - Ponto de equilíbrio (breakeven) aproximado
            """),
            context=context,
            agent=agent,
            output_file="resumo_executivo.md"
        )

    def brand_task(self, context, agent, profile_data):
        return Task(
            description=dedent(f"""
                Criar proposta de valor e estratégia de marca para:
                {profile_data}
            """),
            expected_output=dedent("""
                Seção de brand e positioning em markdown:
                - Proposta de valor
                - Público-alvo detalhado
                - Principais mensagens
            """),
            context=context,
            agent=agent,
            output_file="plano_negocios.md"  # pode acrescentar ao plano
        )

    def pitch_task(self, context, agent, profile_data):
        return Task(
            description=dedent(f"""
                Criar um pitch deck textual (slides) a partir do planejamento e projeções.
            """),
            expected_output=dedent("""
                Pitch deck em markdown com seções:
                - Capa
                - Problema
                - Solução
                - Modelo de negócio
                - Projeções
                - Time
                - Call to Action
            """),
            context=context,
            agent=agent,
            output_file="pitch_deck.md"
        )
