"""
FinMentor: Executive Pro
========================
CFO Virtual - Consultor Financeiro de Bolso
Desenvolvido para: Marco A. Duarte Jr.
"""

import streamlit as st
import warnings
import logging
import os
import json
import re
import urllib.parse
from datetime import datetime
from typing import Optional, Dict, Any, List
from io import BytesIO
import base64
from pathlib import Path

# ✅ NOVOS IMPORTS
import anthropic
from openai import OpenAI

warnings.filterwarnings("ignore")
logging.getLogger("streamlit").setLevel(logging.ERROR)
logging.getLogger("urllib3").setLevel(logging.ERROR)
logging.getLogger("openai").setLevel(logging.ERROR)
logging.getLogger("anthropic").setLevel(logging.ERROR)

st.set_page_config(
    page_title="FinMentor: Executive Pro",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={'Get Help': None, 'Report a bug': None, 'About': None}
)

def get_image_base64(image_path: str) -> str:
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except Exception:
        return ""

AVATAR_PATH = "assets/avatar.jpg"

# ✅ CSS ATUALIZADO (Expander sempre branco)
CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Quicksand:wght@300;400;500;600;700&display=swap');
* { font-family: 'Quicksand', sans-serif !important; }
footer, .stDeployButton { visibility: hidden !important; display: none !important; }
span[data-testid="stIconMaterial"] { display: none !important; }

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f1419 0%, #1a1f2e 50%, #0f1419 100%) !important;
    border-right: 1px solid #2d3748;
}
[data-testid="stSidebar"] > div:first-child { background: transparent !important; padding-top: 1rem; }
[data-testid="collapsedControl"] { display: flex !important; visibility: visible !important; color: #E2E8F0 !important; }
[data-testid="stSidebar"][aria-expanded="true"] { min-width: 300px !important; max-width: 300px !important; }

.avatar-container {
    text-align: center; padding: 1.5rem 1rem;
    background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
    border-radius: 16px; margin: 0.5rem; border: 1px solid #334155;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
}
.avatar-image {
    width: 130px; height: 130px; border-radius: 50%;
    border: 4px solid #667eea; box-shadow: 0 4px 25px rgba(102, 126, 234, 0.5);
    margin-bottom: 1rem; object-fit: cover;
}
.avatar-name { color: #F1F5F9 !important; font-size: 1.3rem; font-weight: 700; margin-bottom: 0.3rem; }
.avatar-title { color: #94A3B8 !important; font-size: 0.9rem; margin-bottom: 1.2rem; font-weight: 500; }
.linkedin-btn {
    display: inline-flex; align-items: center; justify-content: center; gap: 10px;
    padding: 0.7rem 1.5rem; background: linear-gradient(135deg, #0077b5 0%, #0a66c2 100%);
    color: #FFFFFF !important; text-decoration: none !important; border-radius: 10px;
    font-weight: 600; font-size: 0.95rem; transition: all 0.3s ease;
    box-shadow: 0 4px 15px rgba(0, 119, 181, 0.3);
}
.linkedin-btn:hover {
    background: linear-gradient(135deg, #005885 0%, #004d77 100%);
    transform: translateY(-2px); box-shadow: 0 6px 20px rgba(0, 119, 181, 0.5);
}

.market-section {
    background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
    border-radius: 12px; padding: 1rem; margin: 0.5rem; border: 1px solid #334155;
}
.market-section-title {
    color: #F1F5F9 !important; font-size: 1rem; font-weight: 700;
    margin-bottom: 1rem; padding-bottom: 0.5rem; border-bottom: 1px solid #334155;
}
.market-indicator {
    background: linear-gradient(135deg, #1e3a5f 0%, #0f2744 100%);
    border-radius: 10px; padding: 0.8rem; text-align: center;
    border: 1px solid #2563eb33; margin-bottom: 0.5rem;
}
.market-indicator .value { font-size: 1.2rem; font-weight: 700; color: #60A5FA !important; }
.market-indicator .label { font-size: 0.75rem; color: #94A3B8 !important; text-transform: uppercase; letter-spacing: 1px; margin-top: 0.2rem; }
.market-timestamp { color: #64748B !important; font-size: 0.75rem; text-align: center; margin-top: 0.5rem; }

.material-section {
    background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
    border-radius: 12px; padding: 1rem; margin: 0.5rem; margin-top: 1rem; border: 1px solid #334155;
}
.material-section-title {
    color: #F1F5F9 !important; font-size: 1rem; font-weight: 700;
    margin-bottom: 1rem; padding-bottom: 0.5rem; border-bottom: 1px solid #334155;
}
.no-materials { color: #64748B !important; font-size: 0.85rem; text-align: center; padding: 1rem; font-style: italic; }

.video-card {
    border-left: 4px solid #EF4444;
    background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
    padding: 1.2rem 1.5rem; border-radius: 0 12px 12px 0; margin: 1rem 0;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3); border: 1px solid #334155;
}
.video-card h4 { color: #F87171 !important; margin-bottom: 0.8rem; font-weight: 700; font-size: 1.1rem; }
.video-card .video-title { color: #F1F5F9 !important; font-weight: 600; font-size: 1rem; margin-bottom: 0.5rem; }
.video-card .video-desc { color: #CBD5E1 !important; font-size: 0.9rem; margin-bottom: 1rem; line-height: 1.5; }
.video-card a {
    color: #60A5FA !important; text-decoration: none; font-weight: 600;
    display: inline-flex; align-items: center; gap: 8px; padding: 0.6rem 1.2rem;
    background: linear-gradient(135deg, #1e40af 0%, #1e3a8a 100%); border-radius: 8px; transition: all 0.3s ease;
}
.video-card a:hover { background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%); transform: translateY(-2px); }

.focus-badge {
    background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
    color: #FFFFFF !important; padding: 0.4rem 1rem; border-radius: 20px;
    font-size: 0.85rem; font-weight: 600; display: inline-block; margin: 0.2rem;
    box-shadow: 0 2px 10px rgba(59, 130, 246, 0.4);
}
.kpi-badge {
    background: linear-gradient(135deg, #10b981 0%, #059669 100%);
    color: #FFFFFF !important; padding: 0.4rem 1rem; border-radius: 8px;
    font-weight: 600; font-size: 0.9rem; display: inline-block; margin: 0.3rem;
    box-shadow: 0 2px 10px rgba(16, 185, 129, 0.3);
}

.strategy-card {
    background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
    border: 1px solid #334155; border-radius: 12px; padding: 1.5rem; margin: 1rem 0;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
}
.strategy-card, .strategy-card p, .strategy-card span, .strategy-card div { color: #E2E8F0 !important; line-height: 1.7; }
.strategy-header {
    background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text; font-size: 1.8rem; font-weight: 700; margin-bottom: 1rem;
}

.analysis-section {
    background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
    border-radius: 12px; padding: 1.2rem; margin: 0.5rem 0;
    border: 1px solid #334155; border-left: 4px solid #667eea;
}
.analysis-section, .analysis-section p, .analysis-section span, .analysis-section div { color: #E2E8F0 !important; line-height: 1.7; }

.tree-node-root {
    background: linear-gradient(135deg, #7c3aed 0%, #5b21b6 100%);
    border-radius: 12px; padding: 1.2rem 1.5rem; margin: 0.5rem 0;
    border-left: 4px solid #a78bfa; box-shadow: 0 4px 15px rgba(124, 58, 237, 0.3);
}
.tree-node-root, .tree-node-root strong, .tree-node-root span { color: #FFFFFF !important; }

.tree-node {
    background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
    border-radius: 10px; padding: 1rem 1.2rem; margin: 0.5rem 0;
    border: 1px solid #334155; border-left: 4px solid #3b82f6;
}
.tree-node, .tree-node span { color: #E2E8F0 !important; }
.tree-node strong { color: #93C5FD !important; }

.checklist-item {
    padding: 0.9rem 1.2rem; background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
    margin: 0.4rem 0; border-radius: 8px;
    border: 1px solid #334155; border-left: 4px solid #10b981;
}
.checklist-item, .checklist-item span { color: #E2E8F0 !important; }

.risk-card {
    background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
    border-radius: 0 10px 10px 0; padding: 1.2rem 1.5rem; margin: 0.5rem 0;
    border: 1px solid #334155; border-left: 4px solid #f59e0b;
}
.risk-card .risk-title { color: #FBBF24 !important; font-weight: 700; margin-bottom: 0.5rem; font-size: 1rem; }
.risk-card .risk-mitigation { color: #E2E8F0 !important; margin: 0; line-height: 1.6; }
.risk-card .risk-mitigation strong { color: #CBD5E1 !important; }

.download-section {
    background: linear-gradient(135deg, #1e3a5f 0%, #0f2744 100%);
    border: 1px solid #2563eb55; border-radius: 12px; padding: 1.5rem; margin: 1rem 0;
}
.download-section h4 { color: #93C5FD !important; margin-bottom: 0.5rem; font-weight: 700; }
.download-section p { color: #CBD5E1 !important; margin-bottom: 1rem; }

.stButton > button {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: #FFFFFF !important; border: none; border-radius: 10px;
    padding: 0.7rem 1.5rem; font-weight: 600; transition: all 0.3s ease;
    box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
}
.stButton > button:hover { transform: translateY(-2px); box-shadow: 0 6px 25px rgba(102, 126, 234, 0.6); }

.latex-block {
    background: #0f172a; padding: 1.2rem; border-radius: 10px;
    overflow-x: auto; margin: 1rem 0; border: 1px solid #334155; color: #E2E8F0 !important;
}
.custom-divider { height: 1px; background: linear-gradient(90deg, transparent, #475569, transparent); margin: 1.5rem 0; }

@media (max-width: 768px) {
    .main .block-container { padding: 0.5rem; }
    .strategy-header { font-size: 1.4rem; }
    .avatar-image { width: 100px; height: 100px; }
    [data-testid="stSidebar"][aria-expanded="true"] { min-width: 280px !important; max-width: 280px !important; }
}
.stForm { background: transparent; }
[data-testid="stForm"] { border: none !important; padding: 0 !important; }
.stSpinner > div { border-color: #667eea transparent transparent transparent; }

/* --- CORREÇÃO DO EXPANDER --- */
.streamlit-expanderHeader {
    background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%) !important;
    border: 1px solid #334155 !important;
    border-radius: 8px !important;
    color: #FFFFFF !important;
}
.streamlit-expanderHeader p, 
.streamlit-expanderHeader span, 
.streamlit-expanderHeader div {
    color: #FFFFFF !important;
    font-weight: 600 !important;
}
.streamlit-expanderHeader svg {
    fill: #FFFFFF !important;
    color: #FFFFFF !important;
}
.streamlit-expanderHeader:hover {
    border-color: #667eea !important;
}
</style>
"""

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

def init_session_state():
    defaults = {
        'fase': 1, 'ctx': None, 'tree': None, 'market_data': None,
        'strategy_response': None, 'excel_data': None, 'audio_transcription': '',
        'kb_content': '', 'processing': False, 'error_message': None,
        'chat_messages': [],
        'chat_context': '',
        # Chaves de API na sessão para persistência durante uso
        'anthropic_key': '',
        'openai_key': ''
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

init_session_state()

class MarketDataFetcher:
    @staticmethod
    @st.cache_data(ttl=300)
    def get_market_data() -> Dict[str, Any]:
        import yfinance as yf
        import requests
        data = {'dolar': None, 'ibov': None, 'selic': None, 'ipca': None, 'timestamp': datetime.now().strftime('%d/%m/%Y %H:%M')}
        try:
            ticker_usd = yf.Ticker('USDBRL=X')
            hist = ticker_usd.history(period='1d')
            if not hist.empty: data['dolar'] = round(hist['Close'].iloc[-1], 2)
        except: data['dolar'] = 'N/D'
        try:
            ticker_ibov = yf.Ticker('^BVSP')
            hist = ticker_ibov.history(period='1d')
            if not hist.empty: data['ibov'] = f"{int(hist['Close'].iloc[-1]):,}".replace(',', '.')
        except: data['ibov'] = 'N/D'
        try:
            response = requests.get('https://api.bcb.gov.br/dados/serie/bcdata.sgs.432/dados/ultimos/1?formato=json', timeout=5)
            if response.status_code == 200:
                selic_data = response.json()
                if selic_data: data['selic'] = f"{float(selic_data[0]['valor']):.2f}%"
        except: data['selic'] = 'N/D'
        try:
            response = requests.get('https://api.bcb.gov.br/dados/serie/bcdata.sgs.433/dados/ultimos/1?formato=json', timeout=5)
            if response.status_code == 200:
                ipca_data = response.json()
                if ipca_data: data['ipca'] = f"{float(ipca_data[0]['valor']):.2f}%"
        except: data['ipca'] = 'N/D'
        return data

class KnowledgeBaseLoader:
    @staticmethod
    @st.cache_data(ttl=3600)
    def load_knowledge_base(folder: str = "materiais_publicos") -> str:
        content_parts = []
        if not os.path.exists(folder):
            return ""
        for filename in sorted(os.listdir(folder)):
            if not filename.endswith('.txt'):
                continue
            filepath = os.path.join(folder, filename)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                    content_parts.append(f"\n\n{'='*80}\n")
                    content_parts.append(f"MÓDULO: {filename}\n")
                    content_parts.append(f"{'='*80}\n\n")
                    content_parts.append(content)
            except Exception as e:
                print(f"Erro ao ler {filename}: {e}")
                continue
        return "".join(content_parts)

class LLMClient:
    # ✅ CLAUDE 3.5 SONNET IMPLEMENTADO
    @staticmethod
    def _get_system_prompt(conhecimento: str) -> str:
        return f"""Você é o FinMentor, um CFO Virtual de alto nível especializado em finanças corporativas e pessoais.

## PROTOCOLO DE CADEIA DE RACIOCÍNIO (Chain of Thought)

### ETAPA 1 - IDENTIFICAÇÃO
- Qual é a área principal? (Tesouraria, Controladoria, FP&A, Contabilidade, Investimentos, Gestão de Caixa, M&A, Valuation)
- É uma questão operacional, tática ou estratégica?
- Qual o horizonte temporal (curto/médio/longo prazo)?

### ETAPA 2 - SELEÇÃO
- Quais KPIs são relevantes? (ROI, ROE, ROIC, EVA, EBITDA, Margem, Liquidez, Alavancagem)
- Quais autores/frameworks se aplicam? (Damodaran, Ross, IFRS, CPC, Assaf Neto, Gitman)
- Quais ferramentas de análise usar? (DuPont, WACC, DCF, Monte Carlo, Payback)

### ETAPA 3 - ESTRUTURA
- Monte a árvore de decisão com nós claros
- Defina critérios de escolha para cada bifurcação
- Inclua métricas e thresholds quando possível

### ETAPA 4 - CHECKLIST FINAL
Antes de enviar, confirme:
☑ Contexto do pedido foi completamente entendido?
☑ Dados de mercado foram incorporados (se relevantes)?
☑ Base de conhecimento foi consultada (se fornecida)?
☑ Árvore de decisão tem pelo menos 3 níveis de profundidade?
☑ Fórmulas matemáticas estão corretas?
☑ Recomendação é prática e acionável?

## BASE DE CONHECIMENTO PREMIUM

{conhecimento}

IMPORTANTE: Use este conhecimento técnico para fundamentar suas respostas.
⚠️ REGRA DE OURO PARA LATEX: Você DEVE usar barra invertida DUPLA para fórmulas LaTeX dentro do JSON.
- ERRADO: "\\frac{{A}}{{B}}"
- CORRETO: "\\\\frac{{A}}{{B}}"

## FORMATO DE RESPOSTA
Retorne EXCLUSIVAMENTE um JSON válido com esta estrutura:
{{
    "titulo": "Título da Estratégia",
    "area_identificada": "Área principal identificada",
    "kpis_relevantes": ["KPI1", "KPI2", "KPI3"],
    "frameworks_utilizados": ["Framework1", "Framework2"],
    "analise_dos_dados": "Explicação detalhada do raciocínio Chain of Thought usado",
    "resumo": "Resumo executivo em 3-5 parágrafos com linguagem técnica sênior",
    "modelagem_matematica": "Fórmulas em LaTeX puro (use double backslash)",
    "video_sugestao": {{
        "titulo": "Título chamativo para o vídeo", 
        "termo_busca": "Termo exato para pesquisar no YouTube (ex: Valuation Damodaran Prática)", 
        "motivo": "Por que é relevante"
    }},
    "template_sugerido": {{"nome": "Nome do template Excel", "colunas": ["Col1", "Col2"], "linhas_exemplo": [{{"Col1": "Val1", "Col2": "Val2"}}], "formulas_sugeridas": ["=FORMULA1"]}},
    "componentes": {{"pergunta_raiz": "Pergunta principal", "filhos": [{{"condicao": "Se X", "acao": "Faça Y", "filhos": []}}]}},
    "checklist_implementacao": ["Passo 1", "Passo 2"],
    "riscos_mitigacoes": [{{"risco": "Descrição", "mitigacao": "Como mitigar"}}]
}}
IMPORTANTE: Retorne APENAS o JSON, sem texto adicional ou formatação markdown."""

    def __init__(self, api_key: str):
        self.api_key = api_key # Chave Anthropic

    def generate_strategy(self, contexto: str, persona: str, mercado: Dict[str, Any], kb: str) -> Dict[str, Any]:
        # ✅ CLIENTE ANTHROPIC (CLAUDE)
        client = anthropic.Anthropic(api_key=self.api_key)
        
        system_prompt = self._get_system_prompt(kb[:180000] if kb else "Nenhuma base carregada.")
        
        user_prompt = f"""## CONTEXTO DO USUÁRIO
{contexto}

## PERFIL DO SOLICITANTE
{persona}

## DADOS DE MERCADO EM TEMPO REAL
- Dólar: R$ {mercado.get('dolar', 'N/D')}
- IBOVESPA: {mercado.get('ibov', 'N/D')} pontos
- SELIC: {mercado.get('selic', 'N/D')}
- IPCA: {mercado.get('ipca', 'N/D')}
- Atualizado: {mercado.get('timestamp', 'N/D')}

Gere uma Estratégia Estruturada. Retorne APENAS o JSON."""

        try:
            # Chamada da API Anthropic
            response = client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=4096,
                temperature=0.7,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": user_prompt}
                ]
            )
            
            content = response.content[0].text.strip()
            content = re.sub(r'^```json\s*', '', content)
            content = re.sub(r'\s*```$', '', content)
            
            # Tenta parsing direto, se falhar aplica correção de LaTeX
            try:
                return json.loads(content)
            except json.JSONDecodeError:
                fixed_content = re.sub(r'(?<!\\)\\(?!["\\/bfnrtu])', r'\\\\', content)
                return json.loads(fixed_content)

        except json.JSONDecodeError as e:
            return {"error": True, "message": f"Erro ao processar JSON: {str(e)}", "raw_content": content[:500] if 'content' in locals() else "N/D"}
        except Exception as e:
            return {"error": True, "message": f"Erro na API Anthropic: {str(e)}"}

    @staticmethod
    def transcribe_audio(audio_bytes: bytes, openai_api_key: str) -> str:
        # ✅ WHISPER VIA OPENAI
        if not openai_api_key:
            return "[Erro: Chave OpenAI necessária para áudio]"
        
        client = OpenAI(api_key=openai_api_key)
        try:
            audio_file = BytesIO(audio_bytes)
            audio_file.name = "audio.wav"
            response = client.audio.transcriptions.create(model="whisper-1", file=audio_file, language="pt")
            return response.text
        except Exception as e:
            return f"[Erro na transcrição: {str(e)}]"
            
    @staticmethod
    def chat_followup(user_message: str, chat_history: List[Dict], main_context: str, kb: str, api_key: str) -> str:
        # ✅ CLIENTE ANTHROPIC PARA CHAT
        client = anthropic.Anthropic(api_key=api_key)
        
        system_prompt = f"""Você é o FinMentor continuando uma consultoria financeira.

## CONTEXTO PRINCIPAL DA CONSULTA
{main_context}

## BASE DE CONHECIMENTO
{kb[:180000] if kb else "Nenhuma base disponível."}

## INSTRUÇÕES
- Você está em uma conversa contínua sobre o tema acima
- Responda dúvidas de forma técnica mas acessível
- Use o conhecimento da base para fundamentar respostas
- Seja conciso (2-4 parágrafos)
- Se a pergunta fugir muito do tema, gentilmente redirecione
- Use fórmulas e exemplos quando apropriado"""

        # Prepara histórico no formato Anthropic (System separado)
        messages_payload = []
        for msg in chat_history[-10:]:
            if msg["role"] in ["user", "assistant"]:
                messages_payload.append({"role": msg["role"], "content": msg["content"]})
        
        messages_payload.append({"role": "user", "content": user_message})
        
        try:
            response = client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=1000,
                temperature=0.7,
                system=system_prompt,
                messages=messages_payload
            )
            return response.content[0].text.strip()
        except Exception as e:
            return f"❌ Erro: {str(e)}"

class ExcelTemplateGenerator:
    @staticmethod
    def generate_template(template_data: Dict) -> BytesIO:
        import pandas as pd
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            colunas = template_data.get('colunas', ['Coluna1', 'Coluna2'])
            linhas = template_data.get('linhas_exemplo', [])
            df = pd.DataFrame(linhas) if linhas else pd.DataFrame(columns=colunas)
            df.to_excel(writer, sheet_name='Dados', index=False)
            workbook = writer.book
            worksheet = writer.sheets['Dados']
            header_format = workbook.add_format({'bold': True, 'bg_color': '#667eea', 'font_color': 'white', 'border': 1, 'align': 'center', 'valign': 'vcenter', 'font_name': 'Arial'})
            for col_num, value in enumerate(df.columns):
                worksheet.write(0, col_num, value, header_format)
                worksheet.set_column(col_num, col_num, 18)
            formulas = template_data.get('formulas_sugeridas', [])
            if formulas:
                formula_sheet = workbook.add_worksheet('Fórmulas')
                formula_sheet.write(0, 0, 'Fórmulas Sugeridas', header_format)
                for i, formula in enumerate(formulas, start=1):
                    formula_sheet.write(i, 0, formula)
                formula_sheet.set_column(0, 0, 50)
        output.seek(0)
        return output

def clean_latex(text: str) -> str:
    if not text: return ""
    text = re.sub(r'\\\[|\\\]|\\\(|\\\)|\$\$|\$', '', text)
    text = re.sub(r'\\text\{([^}]+)\}', r'\1', text)
    text = text.strip()
    return text

def get_file_icon(filename: str) -> str:
    ext = filename.lower().split('.')[-1] if '.' in filename else ''
    return {'pdf': '📕', 'doc': '📘', 'docx': '📘', 'xls': '📗', 'xlsx': '📗', 'ppt': '📙', 'pptx': '📙', 'txt': '📄', 'csv': '📊'}.get(ext, '📎')

def get_file_type(filename: str) -> str:
    ext = filename.lower().split('.')[-1] if '.' in filename else ''
    return {'pdf': 'PDF', 'doc': 'Word', 'docx': 'Word', 'xls': 'Excel', 'xlsx': 'Excel', 'ppt': 'PowerPoint', 'pptx': 'PowerPoint', 'txt': 'Texto', 'csv': 'CSV'}.get(ext, 'Arquivo')

def render_checklist(items: List[str]):
    for item in items:
        st.markdown(f'<div class="checklist-item">✅ {item}</div>', unsafe_allow_html=True)

def render_risks(risks: List[Dict]):
    for risk in risks:
        st.markdown(f'''<div class="risk-card">
            <p class="risk-title">⚠️ {risk.get('risco', 'Risco')}</p>
            <p class="risk-mitigation"><strong>Mitigação:</strong> {risk.get('mitigacao', 'N/D')}</p>
        </div>''', unsafe_allow_html=True)

def render_tree_node(node: Dict, level: int = 0):
    margin_left = f"{level * 2}rem"
    css_class = "tree-node-root" if level == 0 else "tree-node"
    icon = "❓" if level == 0 else ("📍" if level == 1 else "📌")
    st.markdown(f'''<div class="{css_class}" style="margin-left: {margin_left};">
        <strong>{icon} {node.get('condicao', '')}</strong><br>
        <span>➡️ {node.get('acao', '')}</span>
    </div>''', unsafe_allow_html=True)
    for filho in node.get('filhos', []):
        render_tree_node(filho, level + 1)

def render_phase_1():
    st.markdown('''<div style="text-align: center; padding: 2rem 0;">
        <h1 style="background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 2.5rem; font-weight: 700;">📊 FinMentor: Executive Pro</h1>
        <p style="color: #94A3B8; font-size: 1.1rem; margin-top: 0.5rem;">Seu CFO Virtual de Bolso</p>
    </div>''', unsafe_allow_html=True)
    
    # ✅ GERENCIAMENTO DE CHAVES (CLAUDE + OPENAI)
    ant_key = os.getenv('ANTHROPIC_API_KEY') or st.secrets.get('ANTHROPIC_API_KEY', '')
    oai_key = os.getenv('OPENAI_API_KEY') or st.secrets.get('OPENAI_API_KEY', '')
    
    if not ant_key:
        st.warning("⚠️ Chave ANTHROPIC necessária para o cérebro do FinMentor")
        ant_key = st.text_input("Anthropic Key (sk-ant...):", type="password", key="input_ant_key")
    
    if not oai_key:
        st.info("ℹ️ Chave OPENAI necessária apenas para áudio")
        oai_key = st.text_input("OpenAI Key (sk-...):", type="password", key="input_oai_key")

    if not ant_key:
        st.stop()
        
    st.session_state.anthropic_key = ant_key
    st.session_state.openai_key = oai_key
    
    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
    st.markdown("### 🎤 Entrada por Áudio (Opcional)")
    
    # Só habilita áudio se tiver chave OpenAI
    if not st.session_state.openai_key:
        st.caption("Insira a chave OpenAI para habilitar transcrição de áudio.")
        audio_value = None
    else:
        audio_value = st.audio_input("Grave seu áudio:", key="audio_recorder")
        
    if audio_value is not None and st.session_state.openai_key:
        with st.spinner("Transcrevendo com Whisper (OpenAI)..."):
            st.session_state.audio_transcription = LLMClient.transcribe_audio(audio_value.read(), st.session_state.openai_key)
            st.success(f"✅ Transcrição: {st.session_state.audio_transcription[:100]}...")
    
    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
    st.markdown("### 📝 Descreva seu Desafio Financeiro")
    
    with st.form(key="challenge_form", clear_on_submit=False):
        user_challenge = st.text_area("Seu desafio:", value=st.session_state.audio_transcription or "", height=150, placeholder="Ex: Preciso avaliar se devo investir R$ 500k em um novo projeto...")
        st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
        st.markdown("### 📎 Base de Dados (Opcional)")
        uploaded_file = st.file_uploader("Envie uma planilha:", type=['xlsx', 'xls', 'csv'])
        st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
        st.markdown("### 👤 Seu Perfil")
        selected_persona = st.selectbox("Selecione:", ["Diretor Financeiro (CFO)", "Controller", "Gerente de Tesouraria", "Analista de FP&A", "Investidor Individual", "Empreendedor", "Estudante de Finanças"])
        submitted = st.form_submit_button("🚀 Gerar Estratégia (com Claude)", use_container_width=True)
        
        if submitted:
            if not user_challenge.strip():
                st.error("❌ Descreva seu desafio financeiro.")
            else:
                st.session_state.ctx = user_challenge
                with st.spinner("📊 Buscando dados de mercado..."):
                    st.session_state.market_data = MarketDataFetcher.get_market_data()
                with st.spinner("📚 Carregando base de conhecimento..."):
                    st.session_state.kb_content = KnowledgeBaseLoader.load_knowledge_base()
                if uploaded_file:
                    try:
                        import pandas as pd
                        df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
                        st.session_state.ctx += f"\n\n## DADOS DO EXCEL:\n{df.to_string()}"
                    except Exception as e:
                        st.warning(f"⚠️ Erro ao ler arquivo: {e}")
                with st.spinner("🧠 Claude 3.5 Sonnet pensando..."):
                    try:
                        # Usa a chave Anthropic salva na sessão
                        client = LLMClient(st.session_state.anthropic_key)
                        response = client.generate_strategy(st.session_state.ctx, selected_persona, st.session_state.market_data, st.session_state.kb_content)
                        if response.get('error'):
                            st.error(f"❌ {response.get('message')}")
                        else:
                            st.session_state.strategy_response = response
                            st.session_state.fase = 2
                            st.rerun()
                    except Exception as e:
                        st.error(f"❌ Erro: {e}")

def render_phase_2():
    response = st.session_state.strategy_response
    if not response:
        st.session_state.fase = 1
        st.rerun()
        return
    
    st.markdown(f'''<div style="text-align: center; padding: 1rem 0;"><span class="focus-badge">{response.get('area_identificada', 'Finanças')}</span></div>
    <h1 class="strategy-header">{response.get('titulo', 'Estratégia Financeira')}</h1>''', unsafe_allow_html=True)
    
    if st.button("⬅️ Nova Consulta"):
        st.session_state.fase = 1
        st.session_state.strategy_response = None
        st.session_state.audio_transcription = ''
        st.session_state.chat_messages = []
        st.session_state.chat_context = ''
        st.rerun()
    
    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
    
    col_video, col_excel = st.columns(2)
    with col_video:
        video = response.get('video_sugestao', {})
        termo = video.get('termo_busca')
        
        if termo or video.get('url'):
            if termo:
                encoded_term = urllib.parse.quote(termo)
                video_url = f"https://www.youtube.com/results?search_query={encoded_term}"
            else:
                video_url = video.get('url', '#')

            st.markdown(f'''<div class="video-card">
                <h4>🎬 Vídeo Recomendado</h4>
                <p class="video-title">{video.get('titulo', 'Sugestão de Estudo')}</p>
                <p class="video-desc">{video.get('motivo', 'Aprofunde-se neste tópico.')}</p>
                <a href="{video_url}" target="_blank">
                    🔍 Pesquisar "{termo if termo else 'Vídeo'}" no YouTube
                </a>
            </div>''', unsafe_allow_html=True)

    with col_excel:
        template = response.get('template_sugerido', {})
        if template and template.get('colunas'):
            st.markdown(f'<div class="download-section"><h4>📥 Template Excel</h4><p>{template.get("nome", "Template")}</p></div>', unsafe_allow_html=True)
            st.download_button("⬇️ Baixar Template", ExcelTemplateGenerator.generate_template(template), f"FinMentor_{template.get('nome', 'Template').replace(' ', '_')}.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", use_container_width=True)
    
    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 📈 KPIs Relevantes")
        st.markdown("".join([f'<span class="kpi-badge">{k}</span>' for k in response.get('kpis_relevantes', [])]), unsafe_allow_html=True)
    with col2:
        st.markdown("### 📚 Frameworks")
        st.markdown("".join([f'<span class="focus-badge">{f}</span>' for f in response.get('frameworks_utilizados', [])]), unsafe_allow_html=True)
    
    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
    st.markdown("### 🧠 Análise Chain of Thought (Claude)")
    st.markdown(f'<div class="analysis-section">{response.get("analise_dos_dados", "N/D")}</div>', unsafe_allow_html=True)
    
    st.markdown("### 📋 Resumo Executivo")
    st.markdown(f'<div class="strategy-card">{response.get("resumo", "N/D")}</div>', unsafe_allow_html=True)
    
    if response.get('modelagem_matematica'):
        st.markdown("### 📐 Modelagem Matemática")
        try:
            formula = response['modelagem_matematica']
            formula = formula.strip()
            formula = re.sub(r'^\\\[|\\\]$|^\$\$|\$\$$|^\$|\$$', '', formula).strip()
            st.latex(formula)
        except Exception as e:
            st.code(response['modelagem_matematica'], language='latex')
    
    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
    st.markdown("### 🌳 Árvore de Decisão")
    componentes = response.get('componentes', {})
    if componentes:
        st.markdown(f'<div class="tree-node-root"><strong>❓ {componentes.get("pergunta_raiz", "Decisão")}</strong></div>', unsafe_allow_html=True)
        for filho in componentes.get('filhos', []):
            render_tree_node(filho, level=1)
    
    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
    if response.get('checklist_implementacao'):
        st.markdown("### ✅ Checklist")
        render_checklist(response['checklist_implementacao'])
    
    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
    if response.get('riscos_mitigacoes'):
        st.markdown("### ⚠️ Riscos e Mitigações")
        render_risks(response['riscos_mitigacoes'])

    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
    st.markdown("### 💬 Tire suas Dúvidas")
    st.caption("Pergunte mais sobre este tema. Claude 3.5 Sonnet já conhece o contexto.")
    
    if not st.session_state.chat_context:
        st.session_state.chat_context = f"""
Tema: {response.get('titulo', 'Estratégia Financeira')}
Área: {response.get('area_identificada', 'Finanças')}
Contexto original: {st.session_state.ctx}
KPIs relevantes: {', '.join(response.get('kpis_relevantes', []))}
"""
    
    for msg in st.session_state.chat_messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
    
    if user_input := st.chat_input("Digite sua pergunta..."):
        st.session_state.chat_messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)
        
        with st.chat_message("assistant"):
            with st.spinner("Claude pensando..."):
                response_text = LLMClient.chat_followup(
                    user_message=user_input,
                    chat_history=st.session_state.chat_messages,
                    main_context=st.session_state.chat_context,
                    kb=st.session_state.kb_content,
                    api_key=st.session_state.anthropic_key # Usa chave salva
                )
                st.markdown(response_text)
                st.session_state.chat_messages.append({"role": "assistant", "content": response_text})
        st.rerun()

def main():
    with st.sidebar:
        avatar_base64 = get_image_base64(AVATAR_PATH) if os.path.exists(AVATAR_PATH) else ""
        avatar_src = f"data:image/jpeg;base64,{avatar_base64}" if avatar_base64 else "https://ui-avatars.com/api/?name=Marco+Duarte&background=667eea&color=fff&size=200&font-size=0.35"
        
        st.markdown(f'''<div class="avatar-container">
            <img src="{avatar_src}" class="avatar-image" alt="Marco A. Duarte Jr.">
            <p class="avatar-name">Marco A. Duarte Jr.</p>
            <p class="avatar-title">Finance Professional | CFO Virtual Creator</p>
            <p style="color: #94A3B8; font-size: 0.85rem; margin-bottom: 1rem;">
                📧 marcobjc@gmail.com
            </p>
            <a href="https://www.linkedin.com/in/mduarte89/" target="_blank" class="linkedin-btn">
                <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" fill="currentColor" viewBox="0 0 16 16">
                    <path d="M0 1.146C0 .513.526 0 1.175 0h13.65C15.474 0 16 .513 16 1.146v13.708c0 .633-.526 1.146-1.175 1.146H1.175C.526 16 0 15.487 0 14.854V1.146zm4.943 12.248V6.169H2.542v7.225h2.401zm-1.2-8.212c.837 0 1.358-.554 1.358-1.248-.015-.709-.52-1.248-1.342-1.248-.822 0-1.359.54-1.359 1.248 0 .694.521 1.248 1.327 1.248h.016zm4.908 8.212V9.359c0-.216.016-.432.08-.586.173-.431.568-.878 1.232-.878.869 0 1.216.662 1.216 1.634v3.865h2.401V9.25c0-2.22-1.184-3.252-2.764-3.252-1.274 0-1.845.7-2.165 1.193v.025h-.016a5.54 5.54 0 0 1 .016-.025V6.169h-2.4c.03.678 0 7.225 0 7.225h2.4z"/>
                </svg>
                Conectar no LinkedIn
            </a>
        </div>''', unsafe_allow_html=True)
        
        st.markdown("---")
        
        if st.session_state.market_data is None:
            st.session_state.market_data = MarketDataFetcher.get_market_data()
        
        with st.expander("📚 Materiais de Apoio", expanded=False):
            materials_folder = "materiais_download"
            if os.path.exists(materials_folder):
                files = [f for f in os.listdir(materials_folder) if not f.startswith('.')]
                if files:
                    for filename in sorted(files):
                        filepath = os.path.join(materials_folder, filename)
                        icon = get_file_icon(filename)
                        display_name = filename.rsplit('.', 1)[0].replace('_', ' ').replace('-', ' ')
                        if len(display_name) > 25:
                            display_name = display_name[:22] + "..."
                        try:
                            with open(filepath, 'rb') as f:
                                st.download_button(
                                    label=f"{icon} {display_name}",
                                    data=f.read(),
                                    file_name=filename,
                                    mime="application/octet-stream",
                                    key=f"sidebar_dl_{filename}",
                                    use_container_width=True
                                )
                        except:
                            pass
                else:
                    st.caption("Nenhum material disponível.")
            else:
                st.caption("📁 Adicione arquivos na pasta `materiais_download`")
    
    if st.session_state.fase == 1:
        render_phase_1()
    else:
        render_phase_2()


if __name__ == "__main__":
    main()
