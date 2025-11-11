# biz_utils.py
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, ListFlowable, ListItem, Image
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from datetime import datetime
import os
import re


# ==========================================================
# 📥 Função: Ler arquivo Markdown
# ==========================================================
def load_markdown(file_path):
    """Lê o conteúdo de um arquivo Markdown (.md)."""
    try:
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()
        else:
            print(f"[ERRO] Arquivo não encontrado: {file_path}")
            return ""
    except Exception as e:
        print(f"[ERRO] Falha ao ler o arquivo {file_path}: {e}")
        return ""


# ==========================================================
# 💾 Função: Salvar texto em Markdown
# ==========================================================
def save_markdown(file_path, content):
    """Salva texto no formato Markdown (.md)."""
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"[OK] Markdown salvo em: {file_path}")
        return True
    except Exception as e:
        print(f"[ERRO] Falha ao salvar o arquivo {file_path}: {e}")
        return False


# ==========================================================
# 📄 Função: Converter Markdown para PDF (formatação completa)
# ==========================================================
def convert_md_to_pdf(md_path, pdf_path):
    """
    Converte Markdown (.md) para PDF com layout hierárquico e visual aprimorado.
    Suporta:
    - Cabeçalho e rodapé com logo
    - Títulos coloridos (#, ##, ###)
    - Listas e sublistas aninhadas
    - Texto em negrito e itálico
    """
    try:
        if not os.path.exists(md_path):
            print(f"[ERRO] Arquivo não encontrado: {md_path}")
            return False

        with open(md_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        pdfmetrics.registerFont(UnicodeCIDFont('HeiseiMin-W3'))

        doc = SimpleDocTemplate(
            pdf_path,
            pagesize=A4,
            rightMargin=50,
            leftMargin=50,
            topMargin=80,
            bottomMargin=60
        )

        styles = getSampleStyleSheet()
        normal = ParagraphStyle('Normal', parent=styles['Normal'], fontName='HeiseiMin-W3', fontSize=11, leading=16)
        h1 = ParagraphStyle('Heading1', fontName='HeiseiMin-W3', textColor=colors.HexColor("#004085"), fontSize=18, spaceAfter=12)
        h2 = ParagraphStyle('Heading2', fontName='HeiseiMin-W3', textColor=colors.HexColor("#007bff"), fontSize=14, spaceAfter=8)
        h3 = ParagraphStyle('Heading3', fontName='HeiseiMin-W3', textColor=colors.HexColor("#0d6efd"), fontSize=12, spaceAfter=6)
        bullet = ParagraphStyle('Bullet', parent=styles['Normal'], fontName='HeiseiMin-W3', fontSize=11, leftIndent=20, leading=14)
        subbullet = ParagraphStyle('SubBullet', parent=styles['Normal'], fontName='HeiseiMin-W3', fontSize=10, leftIndent=40, leading=13)
        gray = ParagraphStyle('GrayText', fontName='HeiseiMin-W3', textColor=colors.gray, fontSize=9, alignment=TA_CENTER)

        story = []

        # Cabeçalho e Rodapé
        def header_footer(canvas, doc):
            canvas.saveState()
            width, height = A4

            logo_path = os.path.join("Img", "logoAI.png")
            if os.path.exists(logo_path):
                canvas.drawImage(logo_path, 40, height - 70, width=60, height=60, mask='auto')

            canvas.setFont("Helvetica-Bold", 12)
            canvas.setFillColor(colors.HexColor("#004085"))
            canvas.drawString(120, height - 40, "AgentAI Biz - Plano de Negócio")

            canvas.setFont("Helvetica", 9)
            canvas.setFillColor(colors.black)
            data_str = datetime.now().strftime("%d/%m/%Y - %H:%M")
            canvas.drawRightString(width - 50, height - 40, f"Gerado em: {data_str}")

            canvas.setFont("Helvetica-Oblique", 8)
            canvas.setFillColor(colors.gray)
            canvas.drawCentredString(width / 2, 30, f"Página {doc.page} • AgentAI Biz © 2025")
            canvas.restoreState()

        # Conversão de Markdown para elementos PDF
        list_stack = []  # controla subníveis
        for raw_line in lines:
            line = raw_line.rstrip()

            # Remove e converte negrito e itálico
            line = re.sub(r"\*\*(.*?)\*\*", r"<b>\1</b>", line)
            line = re.sub(r"_(.*?)_", r"<i>\1</i>", line)

            if not line:
                story.append(Spacer(1, 8))
                continue

            # Títulos hierárquicos
            if line.startswith("# "):
                story.append(Paragraph(line[2:], h1))
            elif line.startswith("## "):
                story.append(Paragraph(line[3:], h2))
            elif line.startswith("### "):
                story.append(Paragraph(line[4:], h3))
            elif re.match(r"^\s*-\s+", line) or re.match(r"^\s*\*\s+", line):
                # Calcula nível de recuo
                indent_level = len(line) - len(line.lstrip())
                content = line.strip("-* ").strip()

                # Determina estilo com base no recuo
                style = bullet if indent_level < 4 else subbullet
                story.append(Paragraph(f"• {content}", style))
            else:
                # Limpeza de expressões LaTeX (\[ ... \], \( ... \), \text{})
                line = re.sub(r"\\\\\[|\\\\\]", "", line)  # remove \[ e \]
                line = re.sub(r"\\\\\(|\\\\\)", "", line)  # remove \( e \)
                line = re.sub(r"\\\\text\{(.*?)\}", r"\1", line)  # mantém apenas o texto dentro de \text{}
                line = re.sub(r"\\times", "×", line)  # substitui \times pelo símbolo multiplicar
                line = re.sub(r"\\frac\{(.*?)\}\{(.*?)\}", r"(\1 / \2)", line)  # converte frações básicas
                line = re.sub(r"\\", "", line)  # remove barras invertidas restantes

                story.append(Paragraph(line, normal))

        story.append(Spacer(1, 20))
        story.append(Paragraph("🧠 Relatório gerado automaticamente pelo AgentAI Biz", gray))

        doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)
        print(f"[OK] PDF gerado com sucesso: {pdf_path}")
        return True

    except Exception as e:
        print(f"[ERRO] Falha ao converter {md_path} para PDF: {e}")
        return False


# ==========================================================
# 🧾 Função auxiliar: verificar se arquivo existe
# ==========================================================
def file_exists(path):
    """Verifica se um arquivo existe e não está vazio."""
    return os.path.exists(path) and os.path.getsize(path) > 0
