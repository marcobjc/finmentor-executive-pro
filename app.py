"""
FinMentor: Executive Pro
========================
CFO Virtual - Consultor Financeiro de Bolso
Desenvolvido para: Marco A. Duarte Jr.

Um aplicativo mobile-first que transforma desafios financeiros
em Estratégias Estruturadas usando IA (GPT-4o-mini), dados de mercado
em tempo real e uma base de conhecimento proprietária (RAG).
"""

import streamlit as st
import warnings
import logging
import os
import json
import re
from datetime import datetime
from typing import Optional, Dict, Any, List
from io import BytesIO

# Silenciamento de warnings e logs
warnings.filterwarnings("ignore")
logging.getLogger("streamlit").setLevel(logging.ERROR)
logging.getLogger("urllib3").setLevel(logging.ERROR)
logging.getLogger("openai").setLevel(logging.ERROR)

# ============================================================================
# CONFIGURAÇÃO INICIAL
# ============================================================================

st.set_page_config(
    page_title="FinMentor: Executive Pro",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': None
    }
)

# ============================================================================
# DESIGN SYSTEM - CSS "Zero-Glitch"
# ============================================================================

CUSTOM_CSS = """
<style>
    /* Importar fonte Quicksand */
    @import url('https://fonts.googleapis.com/css2?family=Quicksand:wght@300;400;500;600;700&display=swap');
    
    /* Reset e fonte global */
    * {
        font-family: 'Quicksand', sans-serif !important;
    }
    
    /* Ocultar elementos do Streamlit */
    #MainMenu {visibility: hidden !important;}
    header {visibility: hidden !important;}
    footer {visibility: hidden !important;}
    .stDeployButton {display: none !important;}
    
    /* Fix crítico para ícones vazando (stIconMaterial) */
    .stIconMaterial {
        visibility: hidden !important;
        display: none !important;
    }
    
    [data-testid="stToolbar"] {
        display: none !important;
    }
    
    [data-testid="stDecoration"] {
        display: none !important;
    }
    
    /* Sidebar sempre visível no mobile */
    [data-testid="stSidebar"] {
        min-width: 280px !important;
        max-width: 320px !important;
    }
    
    @media (max-width: 768px) {
        [data-testid="stSidebar"] {
            min-width: 100% !important;
            max-width: 100% !important;
        }
        
        [data-testid="stSidebar"] > div {
            width: 100% !important;
        }
    }
    
    /* Container principal */
    .main .block-container {
        padding-top: 1rem;
        padding-bottom: 2rem;
        max-width: 1000px;
    }
    
    /* Avatar container */
    .avatar-container {
        text-align: center;
        padding: 1.5rem 1rem;
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        border-radius: 12px;
        margin-bottom: 1rem;
        border: 1px solid #333;
    }
    
    .avatar-image {
        width: 120px;
        height: 120px;
        border-radius: 50%;
        border: 4px solid #667eea;
        box-shadow: 0 4px 20px rgba(102, 126, 234, 0.5);
        margin-bottom: 1rem;
        object-fit: cover;
    }
    
    .avatar-name {
        color: #E2E8F0 !important;
        font-size: 1.2rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    
    .avatar-title {
        color: #A0AEC0 !important;
        font-size: 0.85rem;
        margin-bottom: 1rem;
    }
    
    .linkedin-btn {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        gap: 8px;
        padding: 0.6rem 1.2rem;
        background: linear-gradient(135deg, #0077b5, #005885);
        color: white !important;
        text-decoration: none !important;
        border-radius: 8px;
        font-weight: 600;
        font-size: 0.9rem;
        transition: all 0.3s ease;
        width: 100%;
        box-sizing: border-box;
    }
    
    .linkedin-btn:hover {
        background: linear-gradient(135deg, #005885, #004165);
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(0, 119, 181, 0.4);
    }
    
    /* Material download section */
    .material-section {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        border-radius: 12px;
        padding: 1rem;
        margin-top: 1rem;
        border: 1px solid #333;
    }
    
    .material-section h4 {
        color: #90CDF4 !important;
        font-size: 1rem;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 1px solid #333;
    }
    
    .material-item {
        display: flex;
        align-items: center;
        gap: 10px;
        padding: 0.7rem;
        background: rgba(255, 255, 255, 0.03);
        border-radius: 8px;
        margin-bottom: 0.5rem;
        transition: all 0.2s ease;
        text-decoration: none !important;
        color: #E2E8F0 !important;
    }
    
    .material-item:hover {
        background: rgba(255, 255, 255, 0.08);
        transform: translateX(5px);
    }
    
    .material-icon {
        font-size: 1.5rem;
    }
    
    .material-info {
        flex: 1;
    }
    
    .material-title {
        color: #E2E8F0 !important;
        font-weight: 600;
        font-size: 0.9rem;
        margin-bottom: 2px;
    }
    
    .material-type {
        color: #718096 !important;
        font-size: 0.75rem;
    }
    
    /* Cards de vídeo - CORRIGIDO */
    .video-card {
        border-left: 4px solid #FF4444;
        background: linear-gradient(135deg, #2d3748 0%, #1a202c 100%);
        padding: 1.2rem 1.5rem;
        border-radius: 0 12px 12px 0;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
    }
    
    .video-card h4 {
        color: #FC8181 !important;
        margin-bottom: 0.8rem;
        font-weight: 700;
        font-size: 1.2rem;
    }
    
    .video-card .video-title {
        color: #E2E8F0 !important;
        font-weight: 600;
        font-size: 1.1rem;
        margin-bottom: 0.5rem;
    }
    
    .video-card .video-desc {
        color: #A0AEC0 !important;
        font-size: 0.95rem;
        margin-bottom: 1rem;
        line-height: 1.5;
    }
    
    .video-card a {
        color: #63B3ED !important;
        text-decoration: none;
        font-weight: 600;
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 0.5rem 1rem;
        background: rgba(99, 179, 237, 0.15);
        border-radius: 6px;
        transition: all 0.3s ease;
    }
    
    .video-card a:hover {
        background: rgba(99, 179, 237, 0.25);
    }
    
    /* Badges de foco - azul claro */
    .focus-badge {
        background: linear-gradient(135deg, #74b9ff, #0984e3);
        color: white !important;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        display: inline-block;
        margin: 0.2rem;
        box-shadow: 0 2px 8px rgba(9, 132, 227, 0.4);
    }
    
    /* Card de estratégia - CORRIGIDO CONTRASTE */
    .strategy-card {
        background: linear-gradient(135deg, #2d3748 0%, #1a202c 100%);
        border: 1px solid #4a5568;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
        color: #E2E8F0 !important;
    }
    
    .strategy-card p, .strategy-card span, .strategy-card div {
        color: #E2E8F0 !important;
    }
    
    /* Header da estratégia */
    .strategy-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 1.8rem;
        font-weight: 700;
        margin-bottom: 1rem;
    }
    
    /* Seção de análise - CORRIGIDO CONTRASTE */
    .analysis-section {
        background: linear-gradient(135deg, #2d3748 0%, #1a202c 100%);
        border-radius: 8px;
        padding: 1.2rem;
        margin: 0.5rem 0;
        border-left: 3px solid #667eea;
        color: #E2E8F0 !important;
    }
    
    .analysis-section p, .analysis-section span, .analysis-section div {
        color: #E2E8F0 !important;
        line-height: 1.6;
    }
    
    /* KPI badges */
    .kpi-badge {
        background: linear-gradient(135deg, #00b894, #00cec9);
        color: white !important;
        padding: 0.4rem 1rem;
        border-radius: 6px;
        font-weight: 600;
        font-size: 0.9rem;
        display: inline-block;
        margin: 0.3rem;
    }
    
    /* Indicadores de mercado */
    .market-indicator {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 8px;
        padding: 0.8rem;
        text-align: center;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .market-indicator .value {
        font-size: 1.2rem;
        font-weight: 700;
        color: #4dabf7 !important;
    }
    
    .market-indicator .label {
        font-size: 0.75rem;
        color: #888 !important;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* LaTeX styling */
    .latex-block {
        background: #0d1117;
        padding: 1rem;
        border-radius: 8px;
        overflow-x: auto;
        margin: 1rem 0;
        border: 1px solid #30363d;
        color: #E2E8F0 !important;
    }
    
    /* Botões customizados */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white !important;
        border: none;
        border-radius: 8px;
        padding: 0.6rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
    }
    
    /* Checklist items - CORRIGIDO CONTRASTE */
    .checklist-item {
        padding: 0.8rem 1rem;
        background: linear-gradient(135deg, #2d3748 0%, #1a202c 100%);
        margin: 0.3rem 0;
        border-radius: 6px;
        color: #E2E8F0 !important;
        border-left: 3px solid #48BB78;
    }
    
    /* Árvore de decisão nodes - CORRIGIDO CONTRASTE */
    .tree-node {
        background: linear-gradient(135deg, #2d3748 0%, #3d4a5c 100%);
        border-radius: 8px;
        padding: 1rem 1.2rem;
        margin: 0.5rem 0;
        border-left: 4px solid #74b9ff;
        color: #E2E8F0 !important;
    }
    
    .tree-node strong {
        color: #90CDF4 !important;
    }
    
    .tree-node-root {
        background: linear-gradient(135deg, #553C9A 0%, #6B46C1 100%);
        border-radius: 8px;
        padding: 1rem 1.2rem;
        margin: 0.5rem 0;
        border-left: 4px solid #B794F4;
        color: #FFFFFF !important;
    }
    
    .tree-node-root strong {
        color: #FFFFFF !important;
    }
    
    /* Risco card */
    .risk-card {
        background: linear-gradient(135deg, #2d3748 0%, #1a202c 100%);
        border-left: 4px solid #F6AD55;
        border-radius: 0 8px 8px 0;
        padding: 1rem 1.5rem;
        margin: 0.5rem 0;
    }
    
    .risk-card .risk-title {
        color: #F6AD55 !important;
        font-weight: 600;
        margin-bottom: 0.5rem;
        font-size: 1rem;
    }
    
    .risk-card .risk-mitigation {
        color: #E2E8F0 !important;
        margin: 0;
        line-height: 1.5;
    }
    
    /* Download section */
    .download-section {
        background: linear-gradient(135deg, #1a365d 0%, #2a4365 100%);
        border: 1px solid #3182ce;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
    }
    
    .download-section h4 {
        color: #90CDF4 !important;
        margin-bottom: 0.5rem;
    }
    
    .download-section p {
        color: #A0AEC0 !important;
        margin-bottom: 1rem;
    }
    
    /* Quick actions section */
    .quick-actions {
        background: linear-gradient(135deg, #1a365d 0%, #234E6F 100%);
        border-radius: 12px;
        padding: 1.2rem;
        margin: 1rem 0;
        border: 1px solid #3182ce;
    }
    
    .quick-actions h4 {
        color: #90CDF4 !important;
        font-size: 1rem;
        margin-bottom: 1rem;
    }
    
    /* Mobile responsiveness */
    @media (max-width: 768px) {
        .main .block-container {
            padding: 0.5rem;
        }
        
        .strategy-header {
            font-size: 1.4rem;
        }
        
        .market-indicator .value {
            font-size: 1rem;
        }
        
        .avatar-image {
            width: 100px;
            height: 100px;
        }
    }
    
    /* Form styling fix for mobile */
    .stForm {
        background: transparent;
    }
    
    [data-testid="stForm"] {
        border: none !important;
        padding: 0 !important;
    }
    
    /* Expander styling - CORRIGIDO */
    .streamlit-expanderHeader {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 8px;
        color: #E2E8F0 !important;
    }
    
    /* Spinner override */
    .stSpinner > div {
        border-color: #667eea transparent transparent transparent;
    }
    
    /* Divider */
    .custom-divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, #4a5568, transparent);
        margin: 1.5rem 0;
    }
</style>
"""

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ============================================================================
# SESSION STATE - Inicialização Robusta
# ============================================================================

def init_session_state():
    """Garante persistência de variáveis entre reruns."""
    defaults = {
        'fase': 1,
        'ctx': None,
        'tree': None,
        'market_data': None,
        'strategy_response': None,
        'excel_data': None,
        'audio_transcription': '',
        'kb_content': '',
        'processing': False,
        'error_message': None
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

init_session_state()

# ============================================================================
# CLASSES E FUNÇÕES AUXILIARES
# ============================================================================

class MarketDataFetcher:
    """Busca dados de mercado em tempo real."""
    
    @staticmethod
    @st.cache_data(ttl=300)
    def get_market_data() -> Dict[str, Any]:
        """Retorna cotações e taxas atualizadas."""
        import yfinance as yf
        import requests
        
        data = {
            'dolar': None,
            'ibov': None,
            'selic': None,
            'ipca': None,
            'timestamp': datetime.now().strftime('%d/%m/%Y %H:%M')
        }
        
        try:
            ticker_usd = yf.Ticker('USDBRL=X')
            hist = ticker_usd.history(period='1d')
            if not hist.empty:
                data['dolar'] = round(hist['Close'].iloc[-1], 2)
        except Exception:
            data['dolar'] = 'N/D'
        
        try:
            ticker_ibov = yf.Ticker('^BVSP')
            hist = ticker_ibov.history(period='1d')
            if not hist.empty:
                data['ibov'] = f"{int(hist['Close'].iloc[-1]):,}".replace(',', '.')
        except Exception:
            data['ibov'] = 'N/D'
        
        try:
            url_selic = 'https://api.bcb.gov.br/dados/serie/bcdata.sgs.432/dados/ultimos/1?formato=json'
            response = requests.get(url_selic, timeout=5)
            if response.status_code == 200:
                selic_data = response.json()
                if selic_data:
                    data['selic'] = f"{float(selic_data[0]['valor']):.2f}%"
        except Exception:
            data['selic'] = 'N/D'
        
        try:
            url_ipca = 'https://api.bcb.gov.br/dados/serie/bcdata.sgs.433/dados/ultimos/1?formato=json'
            response = requests.get(url_ipca, timeout=5)
            if response.status_code == 200:
                ipca_data = response.json()
                if ipca_data:
                    data['ipca'] = f"{float(ipca_data[0]['valor']):.2f}%"
        except Exception:
            data['ipca'] = 'N/D'
        
        return data


class KnowledgeBaseLoader:
    """Carrega base de conhecimento RAG de arquivos locais."""
    
    @staticmethod
    @st.cache_data(ttl=3600)
    def load_knowledge_base(folder: str = "materiais_publicos") -> str:
        """Lê arquivos txt, pdf e docx da pasta especificada."""
        content_parts = []
        
        if not os.path.exists(folder):
            return ""
        
        for filename in os.listdir(folder):
            filepath = os.path.join(folder, filename)
            
            try:
                if filename.endswith('.txt'):
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content_parts.append(f"[{filename}]\n{f.read()}\n")
                
                elif filename.endswith('.pdf'):
                    try:
                        from pypdf import PdfReader
                        reader = PdfReader(filepath)
                        text = "\n".join([page.extract_text() or "" for page in reader.pages])
                        content_parts.append(f"[{filename}]\n{text}\n")
                    except ImportError:
                        pass
                
                elif filename.endswith('.docx'):
                    try:
                        from docx import Document
                        doc = Document(filepath)
                        text = "\n".join([para.text for para in doc.paragraphs])
                        content_parts.append(f"[{filename}]\n{text}\n")
                    except ImportError:
                        pass
                        
            except Exception:
                continue
        
        return "\n---\n".join(content_parts)


class LLMClient:
    """Motor de Inteligência com Chain of Thought Protocol."""
    
    SYSTEM_PROMPT = """Você é o FinMentor, um CFO Virtual de alto nível especializado em finanças corporativas e pessoais.
    
## PROTOCOLO DE CADEIA DE RACIOCÍNIO (Chain of Thought)

Antes de responder, OBRIGATORIAMENTE siga este protocolo mental:

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
- Contexto do pedido foi completamente entendido?
- Dados de mercado foram incorporados (se relevantes)?
- Base de conhecimento foi consultada (se fornecida)?
- Árvore de decisão tem pelo menos 3 níveis de profundidade?
- Fórmulas matemáticas estão corretas?
- Recomendação é prática e acionável?

## FORMATO DE RESPOSTA

Retorne EXCLUSIVAMENTE um JSON válido (sem markdown, sem ```json) com esta estrutura:

{
    "titulo": "Título da Estratégia",
    "area_identificada": "Área principal identificada",
    "kpis_relevantes": ["KPI1", "KPI2", "KPI3"],
    "frameworks_utilizados": ["Framework1", "Framework2"],
    "analise_dos_dados": "Explicação detalhada do raciocínio Chain of Thought usado",
    "resumo": "Resumo executivo em 3-5 parágrafos com linguagem técnica sênior",
    "modelagem_matematica": "Fórmulas em LaTeX puro (sem delimitadores como $ ou backslash[)",
    "video_sugestao": {
        "titulo": "Título do vídeo sugerido",
        "url": "https://youtube.com/watch?v=...",
        "motivo": "Por que este vídeo é relevante"
    },
    "template_sugerido": {
        "nome": "Nome do template Excel",
        "colunas": ["Coluna1", "Coluna2", "Coluna3"],
        "linhas_exemplo": [
            {"Coluna1": "Valor1", "Coluna2": "Valor2", "Coluna3": "Valor3"}
        ],
        "formulas_sugeridas": ["=FORMULA1", "=FORMULA2"]
    },
    "componentes": {
        "pergunta_raiz": "Pergunta principal da árvore",
        "filhos": [
            {
                "condicao": "Se condição X",
                "acao": "Então faça Y",
                "filhos": [
                    {
                        "condicao": "Sub-condição",
                        "acao": "Sub-ação"
                    }
                ]
            }
        ]
    },
    "checklist_implementacao": [
        "Passo 1: Descrição",
        "Passo 2: Descrição",
        "Passo 3: Descrição"
    ],
    "riscos_mitigacoes": [
        {"risco": "Descrição do risco", "mitigacao": "Como mitigar"}
    ]
}

IMPORTANTE:
- Retorne APENAS o JSON, sem texto adicional
- Não use ```json ou qualquer formatação markdown
- Escape aspas internas corretamente
- Use LaTeX puro sem delimitadores
"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        
    def generate_strategy(
        self, 
        contexto: str, 
        persona: str,
        mercado: Dict[str, Any],
        kb: str
    ) -> Dict[str, Any]:
        """Gera estratégia estruturada usando GPT-4o-mini."""
        from openai import OpenAI
        
        client = OpenAI(api_key=self.api_key)
        
        user_prompt = f"""## CONTEXTO DO USUÁRIO
{contexto}

## PERFIL DO SOLICITANTE
{persona}

## DADOS DE MERCADO EM TEMPO REAL
- Dólar (USD/BRL): R$ {mercado.get('dolar', 'N/D')}
- IBOVESPA: {mercado.get('ibov', 'N/D')} pontos
- Taxa SELIC: {mercado.get('selic', 'N/D')}
- IPCA: {mercado.get('ipca', 'N/D')}
- Atualizado em: {mercado.get('timestamp', 'N/D')}

## BASE DE CONHECIMENTO DISPONÍVEL
{kb[:4000] if kb else 'Nenhuma base de conhecimento carregada.'}

---
Analise o contexto acima e gere uma Estratégia Estruturada seguindo o protocolo Chain of Thought.
Retorne APENAS o JSON, sem formatação markdown."""

        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": self.SYSTEM_PROMPT},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7,
                max_tokens=4000
            )
            
            content = response.choices[0].message.content.strip()
            
            content = re.sub(r'^```json\s*', '', content)
            content = re.sub(r'\s*```$', '', content)
            content = content.strip()
            
            result = json.loads(content)
            return result
            
        except json.JSONDecodeError as e:
            return {
                "error": True,
                "message": f"Erro ao processar resposta da IA: {str(e)}",
                "raw_content": content[:500] if 'content' in locals() else "N/D"
            }
        except Exception as e:
            return {
                "error": True,
                "message": f"Erro na API: {str(e)}"
            }
    
    @staticmethod
    def transcribe_audio(audio_bytes: bytes, api_key: str) -> str:
        """Transcreve áudio usando Whisper."""
        from openai import OpenAI
        
        client = OpenAI(api_key=api_key)
        
        try:
            audio_file = BytesIO(audio_bytes)
            audio_file.name = "audio.wav"
            
            response = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                language="pt"
            )
            
            return response.text
            
        except Exception as e:
            return f"[Erro na transcrição: {str(e)}]"


class ExcelTemplateGenerator:
    """Gera templates Excel para download."""
    
    @staticmethod
    def generate_template(template_data: Dict) -> BytesIO:
        """Cria arquivo Excel a partir do template sugerido."""
        import pandas as pd
        
        output = BytesIO()
        
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            colunas = template_data.get('colunas', ['Coluna1', 'Coluna2'])
            linhas = template_data.get('linhas_exemplo', [])
            
            if linhas:
                df = pd.DataFrame(linhas)
            else:
                df = pd.DataFrame(columns=colunas)
            
            df.to_excel(writer, sheet_name='Dados', index=False)
            
            workbook = writer.book
            worksheet = writer.sheets['Dados']
            
            header_format = workbook.add_format({
                'bold': True,
                'bg_color': '#667eea',
                'font_color': 'white',
                'border': 1,
                'align': 'center',
                'valign': 'vcenter',
                'font_name': 'Arial'
            })
            
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
    """Remove delimitadores de LaTeX para exibição limpa."""
    if not text:
        return ""
    
    text = re.sub(r'\\\[', '', text)
    text = re.sub(r'\\\]', '', text)
    text = re.sub(r'\\\(', '', text)
    text = re.sub(r'\\\)', '', text)
    text = re.sub(r'\$\$', '', text)
    text = re.sub(r'\$', '', text)
    
    return text.strip()


def get_file_icon(filename: str) -> str:
    """Retorna emoji baseado na extensão do arquivo."""
    ext = filename.lower().split('.')[-1] if '.' in filename else ''
    icons = {
        'pdf': '📕',
        'doc': '📘',
        'docx': '📘',
        'xls': '📗',
        'xlsx': '📗',
        'ppt': '📙',
        'pptx': '📙',
        'txt': '📄',
        'csv': '📊'
    }
    return icons.get(ext, '📎')


def get_file_type(filename: str) -> str:
    """Retorna tipo legível do arquivo."""
    ext = filename.lower().split('.')[-1] if '.' in filename else ''
    types = {
        'pdf': 'Documento PDF',
        'doc': 'Word Document',
        'docx': 'Word Document',
        'xls': 'Excel Spreadsheet',
        'xlsx': 'Excel Spreadsheet',
        'ppt': 'PowerPoint',
        'pptx': 'PowerPoint',
        'txt': 'Texto',
        'csv': 'CSV Data'
    }
    return types.get(ext, 'Arquivo')


def render_checklist(items: List[str]):
    """Renderiza checklist de forma segura."""
    for item in items:
        st.markdown(f"""
        <div class="checklist-item">
            ✅ {item}
        </div>
        """, unsafe_allow_html=True)


def render_risks(risks: List[Dict]):
    """Renderiza riscos e mitigações de forma segura."""
    for risk in risks:
        risco_texto = risk.get('risco', 'Risco')
        mitigacao_texto = risk.get('mitigacao', 'N/D')
        st.markdown(f"""
        <div class="risk-card">
            <p class="risk-title">⚠️ {risco_texto}</p>
            <p class="risk-mitigation"><strong>Mitigação:</strong> {mitigacao_texto}</p>
        </div>
        """, unsafe_allow_html=True)


def render_tree_node(node: Dict, level: int = 0):
    """Renderiza nó da árvore de decisão de forma segura."""
    indent = level * 2
    margin_left = f"{indent}rem"
    
    condicao = node.get('condicao', '')
    acao = node.get('acao', '')
    
    if level == 0:
        css_class = "tree-node-root"
        icon = "❓"
    else:
        css_class = "tree-node"
        icon = "📍" if level == 1 else "📌"
    
    st.markdown(f"""
    <div class="{css_class}" style="margin-left: {margin_left};">
        <strong>{icon} {condicao}</strong><br>
        ➡️ {acao}
    </div>
    """, unsafe_allow_html=True)
    
    filhos = node.get('filhos', [])
    for filho in filhos:
        render_tree_node(filho, level + 1)


# ============================================================================
# SIDEBAR - Perfil e Materiais
# ============================================================================

def render_sidebar():
    """Renderiza a barra lateral com avatar, LinkedIn e materiais."""
    with st.sidebar:
        # Avatar e Perfil
        st.markdown("""
        <div class="avatar-container">
            <img src="https://media.licdn.com/dms/image/v2/C4E03AQHzVxvVtUV_Nw/profile-displayphoto-shrink_200_200/profile-displayphoto-shrink_200_200/0/1647288847756?e=2147483647&v=beta&t=Qs5YK0JnNTYtVRLVQJ5NJQR-tNgLKqUX0XN-2tN8Qb4" 
                 class="avatar-image" 
                 alt="Marco A. Duarte Jr."
                 onerror="this.src='https://ui-avatars.com/api/?name=Marco+Duarte&background=667eea&color=fff&size=200'">
            <p class="avatar-name">Marco A. Duarte Jr.</p>
            <p class="avatar-title">CFO Virtual Creator</p>
            <a href="https://www.linkedin.com/in/marcoaureliodj/" target="_blank" class="linkedin-btn">
                <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" fill="currentColor" viewBox="0 0 16 16">
                    <path d="M0 1.146C0 .513.526 0 1.175 0h13.65C15.474 0 16 .513 16 1.146v13.708c0 .633-.526 1.146-1.175 1.146H1.175C.526 16 0 15.487 0 14.854V1.146zm4.943 12.248V6.169H2.542v7.225h2.401zm-1.2-8.212c.837 0 1.358-.554 1.358-1.248-.015-.709-.52-1.248-1.342-1.248-.822 0-1.359.54-1.359 1.248 0 .694.521 1.248 1.327 1.248h.016zm4.908 8.212V9.359c0-.216.016-.432.08-.586.173-.431.568-.878 1.232-.878.869 0 1.216.662 1.216 1.634v3.865h2.401V9.25c0-2.22-1.184-3.252-2.764-3.252-1.274 0-1.845.7-2.165 1.193v.025h-.016a5.54 5.54 0 0 1 .016-.025V6.169h-2.4c.03.678 0 7.225 0 7.225h2.4z"/>
                </svg>
                Conectar no LinkedIn
            </a>
        </div>
        """, unsafe_allow_html=True)
        
        # Dados de Mercado
        st.markdown("### 📊 Mercado em Tempo Real")
        
        if st.session_state.market_data is None:
            with st.spinner("Carregando..."):
                st.session_state.market_data = MarketDataFetcher.get_market_data()
        
        market = st.session_state.market_data
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""
            <div class="market-indicator">
                <div class="label">Dólar</div>
                <div class="value">R$ {market.get('dolar', 'N/D')}</div>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div class="market-indicator">
                <div class="label">SELIC</div>
                <div class="value">{market.get('selic', 'N/D')}</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        col3, col4 = st.columns(2)
        with col3:
            st.markdown(f"""
            <div class="market-indicator">
                <div class="label">IBOV</div>
                <div class="value">{market.get('ibov', 'N/D')}</div>
            </div>
            """, unsafe_allow_html=True)
        with col4:
            st.markdown(f"""
            <div class="market-indicator">
                <div class="label">IPCA</div>
                <div class="value">{market.get('ipca', 'N/D')}</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.caption(f"Atualizado: {market.get('timestamp', 'N/D')}")
        
        st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
        
        # Materiais para Download
        st.markdown("""
        <div class="material-section">
            <h4>📚 Materiais de Apoio</h4>
        </div>
        """, unsafe_allow_html=True)
        
        # Lista materiais da pasta 'materiais_download'
        materials_folder = "materiais_download"
        
        if os.path.exists(materials_folder):
            files = os.listdir(materials_folder)
            files = [f for f in files if not f.startswith('.')]
            
            if files:
                for filename in sorted(files):
                    filepath = os.path.join(materials_folder, filename)
                    icon = get_file_icon(filename)
                    file_type = get_file_type(filename)
                    display_name = filename.rsplit('.', 1)[0].replace('_', ' ').replace('-', ' ').title()
                    
                    try:
                        with open(filepath, 'rb') as f:
                            file_bytes = f.read()
                        
                        st.download_button(
                            label=f"{icon} {display_name}",
                            data=file_bytes,
                            file_name=filename,
                            mime="application/octet-stream",
                            key=f"download_{filename}",
                            use_container_width=True
                        )
                    except Exception:
                        st.markdown(f"""
                        <div class="material-item">
                            <span class="material-icon">{icon}</span>
                            <div class="material-info">
                                <p class="material-title">{display_name}</p>
                                <p class="material-type">{file_type}</p>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
            else:
                st.caption("Nenhum material disponível ainda.")
        else:
            st.caption("📁 Pasta de materiais não encontrada.")
            st.caption("Crie a pasta 'materiais_download' e adicione seus arquivos.")


# ============================================================================
# INTERFACE PRINCIPAL
# ============================================================================

def render_phase_1():
    """Renderiza a fase de input (tela inicial)."""
    st.markdown("""
    <div style="text-align: center; padding: 2rem 0;">
        <h1 style="
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            font-size: 2.5rem;
            font-weight: 700;
        ">📊 FinMentor: Executive Pro</h1>
        <p style="color: #A0AEC0; font-size: 1.1rem; margin-top: 0.5rem;">
            Seu CFO Virtual de Bolso
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    api_key = os.getenv('OPENAI_API_KEY') or st.secrets.get('OPENAI_API_KEY', '')
    
    if not api_key:
        st.warning("⚠️ Configure a variável de ambiente `OPENAI_API_KEY` ou adicione em `.streamlit/secrets.toml`")
        api_key = st.text_input("Ou insira sua API Key:", type="password")
        
        if not api_key:
            st.stop()
    
    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
    
    # Áudio Input - FORA do formulário
    st.markdown("### 🎤 Entrada por Áudio (Opcional)")
    st.caption("Grave sua pergunta ou desafio financeiro")
    
    audio_value = st.audio_input("Grave seu áudio:", key="audio_recorder")
    
    if audio_value is not None:
        with st.spinner("Transcrevendo áudio..."):
            audio_bytes = audio_value.read()
            transcription = LLMClient.transcribe_audio(audio_bytes, api_key)
            st.session_state.audio_transcription = transcription
            st.success(f"✅ Transcrição: {transcription[:100]}...")
    
    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
    
    # Formulário
    st.markdown("### 📝 Descreva seu Desafio Financeiro")
    
    with st.form(key="challenge_form", clear_on_submit=False):
        default_text = st.session_state.audio_transcription if st.session_state.audio_transcription else ""
        
        user_challenge = st.text_area(
            "Seu desafio ou pergunta:",
            value=default_text,
            height=150,
            placeholder="Ex: Preciso avaliar se devo investir R$ 500k em um novo projeto. O TIR esperado é 18% a.a. e o payback 3 anos. Vale a pena considerando a SELIC atual?",
            key="challenge_input"
        )
        
        st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
        st.markdown("### 📎 Base de Dados (Opcional)")
        
        uploaded_file = st.file_uploader(
            "Envie uma planilha Excel com seus dados:",
            type=['xlsx', 'xls', 'csv'],
            key="excel_upload"
        )
        
        st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
        st.markdown("### 👤 Seu Perfil")
        
        persona_options = [
            "Diretor Financeiro (CFO)",
            "Controller",
            "Gerente de Tesouraria",
            "Analista de FP&A",
            "Investidor Individual",
            "Empreendedor",
            "Estudante de Finanças"
        ]
        
        selected_persona = st.selectbox(
            "Selecione seu perfil:",
            options=persona_options,
            index=0,
            key="persona_select"
        )
        
        st.markdown("<br>", unsafe_allow_html=True)
        submitted = st.form_submit_button(
            "🚀 Gerar Estratégia",
            use_container_width=True
        )
        
        if submitted:
            if not user_challenge.strip():
                st.error("❌ Por favor, descreva seu desafio financeiro.")
            else:
                st.session_state.processing = True
                st.session_state.ctx = user_challenge
                
                with st.spinner("📊 Buscando dados de mercado..."):
                    st.session_state.market_data = MarketDataFetcher.get_market_data()
                
                with st.spinner("📚 Carregando base de conhecimento..."):
                    st.session_state.kb_content = KnowledgeBaseLoader.load_knowledge_base()
                
                if uploaded_file is not None:
                    try:
                        import pandas as pd
                        
                        if uploaded_file.name.endswith('.csv'):
                            df = pd.read_csv(uploaded_file)
                        else:
                            df = pd.read_excel(uploaded_file)
                        
                        st.session_state.excel_data = df.to_string()
                        st.session_state.ctx += f"\n\n## DADOS DO EXCEL ENVIADO:\n{df.to_string()}"
                        
                    except Exception as e:
                        st.warning(f"⚠️ Não foi possível ler o arquivo: {str(e)}")
                
                with st.spinner("🧠 Gerando estratégia com IA..."):
                    try:
                        llm_client = LLMClient(api_key)
                        
                        response = llm_client.generate_strategy(
                            contexto=st.session_state.ctx,
                            persona=selected_persona,
                            mercado=st.session_state.market_data,
                            kb=st.session_state.kb_content
                        )
                        
                        if response.get('error'):
                            st.error(f"❌ {response.get('message', 'Erro desconhecido')}")
                            if 'raw_content' in response:
                                with st.expander("Debug: Resposta bruta"):
                                    st.code(response['raw_content'])
                        else:
                            st.session_state.strategy_response = response
                            st.session_state.fase = 2
                            st.rerun()
                            
                    except Exception as e:
                        st.error(f"❌ Erro ao processar: {str(e)}")
                
                st.session_state.processing = False


def render_phase_2():
    """Renderiza a fase de output (estratégia gerada)."""
    response = st.session_state.strategy_response
    
    if not response:
        st.session_state.fase = 1
        st.rerun()
        return
    
    # Header
    st.markdown(f"""
    <div style="text-align: center; padding: 1rem 0;">
        <span class="focus-badge">{response.get('area_identificada', 'Finanças')}</span>
    </div>
    <h1 class="strategy-header">{response.get('titulo', 'Estratégia Financeira')}</h1>
    """, unsafe_allow_html=True)
    
    # Botão voltar
    if st.button("⬅️ Nova Consulta", key="back_btn"):
        st.session_state.fase = 1
        st.session_state.strategy_response = None
        st.session_state.audio_transcription = ''
        st.rerun()
    
    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
    
    # ==========================================
    # VÍDEO E DOWNLOAD - ANTES DA ANÁLISE
    # ==========================================
    col_video, col_excel = st.columns(2)
    
    # Vídeo Sugerido
    with col_video:
        video = response.get('video_sugestao', {})
        if video and video.get('url'):
            st.markdown(f"""
            <div class="video-card">
                <h4>🎬 Vídeo Recomendado</h4>
                <p class="video-title">{video.get('titulo', 'Vídeo')}</p>
                <p class="video-desc">{video.get('motivo', '')}</p>
                <a href="{video.get('url', '#')}" target="_blank">▶️ Assistir no YouTube</a>
            </div>
            """, unsafe_allow_html=True)
    
    # Download Excel Template
    with col_excel:
        template = response.get('template_sugerido', {})
        if template and template.get('colunas'):
            st.markdown(f"""
            <div class="download-section">
                <h4>📥 Template Excel</h4>
                <p>{template.get('nome', 'Template para análise')}</p>
            </div>
            """, unsafe_allow_html=True)
            
            excel_file = ExcelTemplateGenerator.generate_template(template)
            
            st.download_button(
                label="⬇️ Baixar Template Excel",
                data=excel_file,
                file_name=f"FinMentor_{template.get('nome', 'Template').replace(' ', '_')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )
    
    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
    
    # ==========================================
    # KPIs e Frameworks
    # ==========================================
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📈 KPIs Relevantes")
        kpis = response.get('kpis_relevantes', [])
        kpi_html = ""
        for kpi in kpis:
            kpi_html += f'<span class="kpi-badge">{kpi}</span>'
        st.markdown(kpi_html, unsafe_allow_html=True)
    
    with col2:
        st.markdown("### 📚 Frameworks Utilizados")
        frameworks = response.get('frameworks_utilizados', [])
        fw_html = ""
        for fw in frameworks:
            fw_html += f'<span class="focus-badge">{fw}</span>'
        st.markdown(fw_html, unsafe_allow_html=True)
    
    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
    
    # ==========================================
    # Análise (Chain of Thought)
    # ==========================================
    st.markdown("### 🧠 Análise Chain of Thought")
    st.markdown(f"""
    <div class="analysis-section">
        {response.get('analise_dos_dados', 'Análise não disponível.')}
    </div>
    """, unsafe_allow_html=True)
    
    # ==========================================
    # Resumo Executivo
    # ==========================================
    st.markdown("### 📋 Resumo Executivo")
    st.markdown(f"""
    <div class="strategy-card">
        {response.get('resumo', 'Resumo não disponível.')}
    </div>
    """, unsafe_allow_html=True)
    
    # ==========================================
    # Modelagem Matemática (LaTeX)
    # ==========================================
    math_content = response.get('modelagem_matematica', '')
    if math_content:
        st.markdown("### 📐 Modelagem Matemática")
        
        clean_math = clean_latex(math_content)
        
        try:
            st.latex(clean_math)
        except Exception:
            st.markdown(f"""
            <div class="latex-block">
                {clean_math}
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
    
    # ==========================================
    # Árvore de Decisão - CORRIGIDA
    # ==========================================
    st.markdown("### 🌳 Árvore de Decisão")
    
    componentes = response.get('componentes', {})
    if componentes:
        # Nó raiz
        pergunta_raiz = componentes.get('pergunta_raiz', 'Decisão Principal')
        st.markdown(f"""
        <div class="tree-node-root">
            <strong>❓ {pergunta_raiz}</strong>
        </div>
        """, unsafe_allow_html=True)
        
        # Filhos
        filhos = componentes.get('filhos', [])
        for filho in filhos:
            render_tree_node(filho, level=1)
    
    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
    
    # ==========================================
    # Checklist de Implementação
    # ==========================================
    checklist = response.get('checklist_implementacao', [])
    if checklist:
        st.markdown("### ✅ Checklist de Implementação")
        render_checklist(checklist)
    
    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
    
    # ==========================================
    # Riscos e Mitigações
    # ==========================================
    riscos = response.get('riscos_mitigacoes', [])
    if riscos:
        st.markdown("### ⚠️ Riscos e Mitigações")
        render_risks(riscos)


# ============================================================================
# EXECUÇÃO PRINCIPAL
# ============================================================================

def main():
    """Função principal do aplicativo."""
    render_sidebar()
    
    if st.session_state.fase == 1:
        render_phase_1()
    else:
        render_phase_2()


if __name__ == "__main__":
    main()
