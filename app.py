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
    initial_sidebar_state="collapsed",
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
    
    /* Container principal */
    .main .block-container {
        padding-top: 1rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }
    
    /* Cards de vídeo - borda vermelha esquerda */
    .video-card {
        border-left: 4px solid #FF0000;
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        padding: 1rem 1.5rem;
        border-radius: 0 8px 8px 0;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
    }
    
    .video-card h4 {
        color: #FF4444;
        margin-bottom: 0.5rem;
        font-weight: 600;
    }
    
    .video-card a {
        color: #4dabf7 !important;
        text-decoration: none;
        font-weight: 500;
    }
    
    .video-card a:hover {
        text-decoration: underline;
    }
    
    /* Badges de foco - azul claro */
    .focus-badge {
        background: linear-gradient(135deg, #74b9ff, #0984e3);
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        display: inline-block;
        margin: 0.2rem;
        box-shadow: 0 2px 8px rgba(9, 132, 227, 0.4);
    }
    
    /* Blocos de código - escuro */
    .code-block {
        background: #1e1e1e;
        color: #d4d4d4;
        padding: 1rem;
        border-radius: 8px;
        font-family: 'Fira Code', 'Monaco', monospace !important;
        font-size: 0.85rem;
        overflow-x: auto;
        border: 1px solid #333;
    }
    
/* Card de estratégia */
  .strategy-card {
        background: linear-gradient(135deg, #1e2a3a 0%, #2d3748 100%);
        border: 1px solid #4a5568;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
        color: #f7fafc;
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
    
/* Seção de análise */
    .analysis-section {
        background: linear-gradient(135deg, #1e2a3a 0%, #2d3748 100%);
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
        border-left: 3px solid #667eea;
        color: #e2e8f0;
    }
    
    /* KPI badges */
    .kpi-badge {
        background: linear-gradient(135deg, #00b894, #00cec9);
        color: white;
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
        font-size: 1.4rem;
        font-weight: 700;
        color: #4dabf7;
    }
    
    .market-indicator .label {
        font-size: 0.8rem;
        color: #888;
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
    }
    
    /* Botões customizados */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
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
    
    /* Avatar sidebar */
    .sidebar-avatar {
        text-align: center;
        padding: 1rem;
        margin-bottom: 1rem;
    }
    
    .sidebar-avatar img {
        border-radius: 50%;
        border: 3px solid #667eea;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    
    /* Checklist items */
    .checklist-item {
        padding: 0.5rem 0;
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
    }
    
    .checklist-item:last-child {
        border-bottom: none;
    }
    
    /* Árvore de decisão nodes */
    .tree-node {
        background: linear-gradient(135deg, #2d3436 0%, #636e72 100%);
        border-radius: 8px;
        padding: 0.8rem;
        margin: 0.5rem 0;
        border-left: 3px solid #74b9ff;
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
            font-size: 1.1rem;
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
    
    /* Audio input styling */
    .stAudioInput {
        margin-bottom: 1rem;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 8px;
    }
    
    /* Spinner override */
    .stSpinner > div {
        border-color: #667eea transparent transparent transparent;
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
        'fase': 1,  # 1 = Input, 2 = Output
        'ctx': None,  # Contexto do usuário (texto + transcrição)
        'tree': None,  # Árvore de decisão gerada
        'market_data': None,  # Dados de mercado em tempo real
        'strategy_response': None,  # Resposta completa da IA
        'excel_data': None,  # Dados do Excel enviado
        'audio_transcription': '',  # Transcrição do áudio
        'kb_content': '',  # Conteúdo da base de conhecimento
        'processing': False,  # Flag de processamento
        'error_message': None  # Mensagem de erro
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
    @st.cache_data(ttl=300)  # Cache de 5 minutos
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
            # Dólar (USDBRL)
            ticker_usd = yf.Ticker('USDBRL=X')
            hist = ticker_usd.history(period='1d')
            if not hist.empty:
                data['dolar'] = round(hist['Close'].iloc[-1], 2)
        except Exception:
            data['dolar'] = 'N/D'
        
        try:
            # IBOVESPA
            ticker_ibov = yf.Ticker('^BVSP')
            hist = ticker_ibov.history(period='1d')
            if not hist.empty:
                data['ibov'] = f"{int(hist['Close'].iloc[-1]):,}".replace(',', '.')
        except Exception:
            data['ibov'] = 'N/D'
        
        try:
            # SELIC - API Banco Central
            url_selic = 'https://api.bcb.gov.br/dados/serie/bcdata.sgs.432/dados/ultimos/1?formato=json'
            response = requests.get(url_selic, timeout=5)
            if response.status_code == 200:
                selic_data = response.json()
                if selic_data:
                    data['selic'] = f"{float(selic_data[0]['valor']):.2f}%"
        except Exception:
            data['selic'] = 'N/D'
        
        try:
            # IPCA - API Banco Central
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
    @st.cache_data(ttl=3600)  # Cache de 1 hora
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
☑ Contexto do pedido foi completamente entendido?
☑ Dados de mercado foram incorporados (se relevantes)?
☑ Base de conhecimento foi consultada (se fornecida)?
☑ Árvore de decisão tem pelo menos 3 níveis de profundidade?
☑ Fórmulas matemáticas estão corretas?
☑ Recomendação é prática e acionável?

## FORMATO DE RESPOSTA

Retorne EXCLUSIVAMENTE um JSON válido (sem markdown, sem ```json) com esta estrutura:

{
    "titulo": "Título da Estratégia",
    "area_identificada": "Área principal identificada",
    "kpis_relevantes": ["KPI1", "KPI2", "KPI3"],
    "frameworks_utilizados": ["Framework1", "Framework2"],
    "analise_dos_dados": "Explicação detalhada do raciocínio Chain of Thought usado",
    "resumo": "Resumo executivo em 3-5 parágrafos com linguagem técnica sênior",
    "modelagem_matematica": "Fórmulas em LaTeX puro (sem delimitadores como $ ou \\[)",
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
- Escape aspas internas com \\"
- Use LaTeX puro sem delimitadores ($ ou \\[ ou \\])
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
        
        # Monta o prompt do usuário
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
            
            # Limpa possíveis artefatos de markdown
            content = re.sub(r'^```json\s*', '', content)
            content = re.sub(r'\s*```$', '', content)
            content = content.strip()
            
            # Parse do JSON
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
            # Cria arquivo temporário
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


class DecisionTreeRenderer:
    """Renderiza árvores de decisão usando Graphviz."""
    
    @staticmethod
    def render_tree(componentes: Dict) -> Optional[str]:
        """Gera árvore de decisão visual."""
        try:
            import graphviz
            
            dot = graphviz.Digraph(
                format='svg',
                graph_attr={
                    'bgcolor': 'transparent',
                    'fontname': 'Quicksand',
                    'rankdir': 'TB',
                    'splines': 'ortho',
                    'nodesep': '0.5',
                    'ranksep': '0.8'
                },
                node_attr={
                    'fontname': 'Quicksand',
                    'fontsize': '11',
                    'shape': 'box',
                    'style': 'rounded,filled',
                    'fillcolor': '#1a1a3e',
                    'fontcolor': 'white',
                    'color': '#667eea',
                    'penwidth': '2'
                },
                edge_attr={
                    'fontname': 'Quicksand',
                    'fontsize': '9',
                    'color': '#4dabf7',
                    'fontcolor': '#4dabf7',
                    'penwidth': '1.5'
                }
            )
            
            # Nó raiz
            root_label = componentes.get('pergunta_raiz', 'Decisão Principal')
            dot.node('root', root_label, fillcolor='#667eea', fontcolor='white')
            
            # Função recursiva para adicionar nós
            node_counter = [0]
            
            def add_children(parent_id: str, children: List[Dict], depth: int = 0):
                colors = ['#2d3436', '#0984e3', '#00b894', '#6c5ce7', '#e17055']
                
                for child in children:
                    node_counter[0] += 1
                    child_id = f"node_{node_counter[0]}"
                    
                    label = f"{child.get('condicao', '')}\n───\n{child.get('acao', '')}"
                    color = colors[depth % len(colors)]
                    
                    dot.node(child_id, label, fillcolor=color)
                    dot.edge(parent_id, child_id)
                    
                    if 'filhos' in child and child['filhos']:
                        add_children(child_id, child['filhos'], depth + 1)
            
            # Adiciona filhos do nó raiz
            if 'filhos' in componentes:
                add_children('root', componentes['filhos'])
            
            return dot.pipe(format='svg').decode('utf-8')
            
        except Exception as e:
            return None


class ExcelTemplateGenerator:
    """Gera templates Excel para download."""
    
    @staticmethod
    def generate_template(template_data: Dict) -> BytesIO:
        """Cria arquivo Excel a partir do template sugerido."""
        import pandas as pd
        
        output = BytesIO()
        
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            # Cria DataFrame com os dados
            colunas = template_data.get('colunas', ['Coluna1', 'Coluna2'])
            linhas = template_data.get('linhas_exemplo', [])
            
            if linhas:
                df = pd.DataFrame(linhas)
            else:
                df = pd.DataFrame(columns=colunas)
            
            df.to_excel(writer, sheet_name='Dados', index=False)
            
            # Formata a planilha
            workbook = writer.book
            worksheet = writer.sheets['Dados']
            
            # Formato do cabeçalho
            header_format = workbook.add_format({
                'bold': True,
                'bg_color': '#667eea',
                'font_color': 'white',
                'border': 1,
                'align': 'center',
                'valign': 'vcenter',
                'font_name': 'Arial'
            })
            
            # Aplica formato ao cabeçalho
            for col_num, value in enumerate(df.columns):
                worksheet.write(0, col_num, value, header_format)
                worksheet.set_column(col_num, col_num, 18)
            
            # Adiciona aba com fórmulas sugeridas
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
    
    # Remove delimitadores comuns
    text = re.sub(r'\\\[', '', text)
    text = re.sub(r'\\\]', '', text)
    text = re.sub(r'\\\(', '', text)
    text = re.sub(r'\\\)', '', text)
    text = re.sub(r'\$\$', '', text)
    text = re.sub(r'\$', '', text)
    
    return text.strip()


def render_checklist(items: List[str]):
    """Renderiza checklist de forma segura (sem list comprehension)."""
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
        <div style="
            background: linear-gradient(135deg, #2d2d2d 0%, #1a1a1a 100%);
            border-left: 4px solid #f6ad55;
            border-radius: 0 8px 8px 0;
            padding: 1rem 1.5rem;
            margin: 0.5rem 0;
        ">
            <p style="color: #f6ad55; font-weight: 600; margin-bottom: 0.5rem;">
                ⚠️ {risco_texto}
            </p>
            <p style="color: #e2e8f0; margin: 0;">
                <strong>Mitigação:</strong> {mitigacao_texto}
            </p>
        </div>
        """, unsafe_allow_html=True)


# ============================================================================
# INTERFACE PRINCIPAL
# ============================================================================

def render_sidebar():
    """Renderiza a barra lateral com avatar e links."""
    with st.sidebar:
        st.markdown("""
        <div class="sidebar-avatar">
            <img src="https://media.licdn.com/dms/image/v2/C4E03AQHzVxvVtUV_Nw/profile-displayphoto-shrink_200_200/profile-displayphoto-shrink_200_200/0/1647288847756?e=2147483647&v=beta&t=Qs5YK0JnNTYtVRLVQJ5NJQR-tNgLKqUX0XN-2tN8Qb4" width="120" alt="Marco A. Duarte Jr.">
            <h3 style="margin-top: 1rem; color: #4dabf7;">Marco A. Duarte Jr.</h3>
            <p style="color: #888; font-size: 0.9rem;">CFO Virtual User</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        st.markdown("""
        <a href="https://www.linkedin.com/in/marcoaureliodj/" target="_blank" style="
            display: flex;
            align-items: center;
            gap: 8px;
            padding: 0.8rem;
            background: linear-gradient(135deg, #0077b5, #005885);
            color: white;
            text-decoration: none;
            border-radius: 8px;
            font-weight: 600;
            transition: all 0.3s ease;
        ">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" viewBox="0 0 16 16">
                <path d="M0 1.146C0 .513.526 0 1.175 0h13.65C15.474 0 16 .513 16 1.146v13.708c0 .633-.526 1.146-1.175 1.146H1.175C.526 16 0 15.487 0 14.854V1.146zm4.943 12.248V6.169H2.542v7.225h2.401zm-1.2-8.212c.837 0 1.358-.554 1.358-1.248-.015-.709-.52-1.248-1.342-1.248-.822 0-1.359.54-1.359 1.248 0 .694.521 1.248 1.327 1.248h.016zm4.908 8.212V9.359c0-.216.016-.432.08-.586.173-.431.568-.878 1.232-.878.869 0 1.216.662 1.216 1.634v3.865h2.401V9.25c0-2.22-1.184-3.252-2.764-3.252-1.274 0-1.845.7-2.165 1.193v.025h-.016a5.54 5.54 0 0 1 .016-.025V6.169h-2.4c.03.678 0 7.225 0 7.225h2.4z"/>
            </svg>
            LinkedIn Profile
        </a>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        if st.session_state.market_data:
            st.markdown("### 📊 Mercado em Tempo Real")
            
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
        <p style="color: #888; font-size: 1.1rem; margin-top: 0.5rem;">
            Seu CFO Virtual de Bolso
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Verifica API Key
    api_key = os.getenv('OPENAI_API_KEY') or st.secrets.get('OPENAI_API_KEY', '')
    
    if not api_key:
        st.warning("⚠️ Configure a variável de ambiente `OPENAI_API_KEY` ou adicione em `.streamlit/secrets.toml`")
        api_key = st.text_input("Ou insira sua API Key:", type="password")
        
        if not api_key:
            st.stop()
    
    st.markdown("---")
    
    # ==========================================
    # ÁUDIO INPUT - FORA DO FORMULÁRIO (Mobile Fix)
    # ==========================================
    st.markdown("### 🎤 Entrada por Áudio (Opcional)")
    st.caption("Grave sua pergunta ou desafio financeiro")
    
    audio_value = st.audio_input("Grave seu áudio:", key="audio_recorder")
    
    if audio_value is not None:
        # Transcrição em tempo real
        with st.spinner("Transcrevendo áudio..."):
            audio_bytes = audio_value.read()
            transcription = LLMClient.transcribe_audio(audio_bytes, api_key)
            st.session_state.audio_transcription = transcription
            st.success(f"✅ Transcrição: {transcription[:100]}...")
    
    st.markdown("---")
    
    # ==========================================
    # FORMULÁRIO - Texto e Upload (Mobile Fix)
    # ==========================================
    st.markdown("### 📝 Descreva seu Desafio Financeiro")
    
    with st.form(key="challenge_form", clear_on_submit=False):
        # Campo de texto
        default_text = st.session_state.audio_transcription if st.session_state.audio_transcription else ""
        
        user_challenge = st.text_area(
            "Seu desafio ou pergunta:",
            value=default_text,
            height=150,
            placeholder="Ex: Preciso avaliar se devo investir R$ 500k em um novo projeto. O TIR esperado é 18% a.a. e o payback 3 anos. Vale a pena considerando a SELIC atual?",
            key="challenge_input"
        )
        
        # Upload de Excel
        st.markdown("---")
        st.markdown("### 📎 Base de Dados (Opcional)")
        
        uploaded_file = st.file_uploader(
            "Envie uma planilha Excel com seus dados:",
            type=['xlsx', 'xls', 'csv'],
            key="excel_upload"
        )
        
        # Persona
        st.markdown("---")
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
        
        # Botão de envio
        st.markdown("<br>", unsafe_allow_html=True)
        submitted = st.form_submit_button(
            "🚀 Gerar Estratégia",
            use_container_width=True
        )
        
        if submitted:
            if not user_challenge.strip():
                st.error("❌ Por favor, descreva seu desafio financeiro.")
            else:
                # Processa
                st.session_state.processing = True
                st.session_state.ctx = user_challenge
                
                # Carrega dados de mercado
                with st.spinner("📊 Buscando dados de mercado..."):
                    st.session_state.market_data = MarketDataFetcher.get_market_data()
                
                # Carrega base de conhecimento
                with st.spinner("📚 Carregando base de conhecimento..."):
                    st.session_state.kb_content = KnowledgeBaseLoader.load_knowledge_base()
                
                # Processa Excel se enviado
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
                
                # Gera estratégia
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
    
    st.markdown("---")
    
    # ==========================================
    # KPIs e Frameworks
    # ==========================================
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📈 KPIs Relevantes")
        kpis = response.get('kpis_relevantes', [])
        for kpi in kpis:
            st.markdown(f'<span class="kpi-badge">{kpi}</span>', unsafe_allow_html=True)
    
    with col2:
        st.markdown("### 📚 Frameworks Utilizados")
        frameworks = response.get('frameworks_utilizados', [])
        for fw in frameworks:
            st.markdown(f'<span class="focus-badge">{fw}</span>', unsafe_allow_html=True)
    
    st.markdown("---")
    
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
    
    st.markdown("---")
    
    # ==========================================
    # Árvore de Decisão
    # ==========================================
    st.markdown("### 🌳 Árvore de Decisão")
    
    componentes = response.get('componentes', {})
    if componentes:
        tree_svg = DecisionTreeRenderer.render_tree(componentes)
        
        if tree_svg:
            st.markdown(tree_svg, unsafe_allow_html=True)
        else:
            # Fallback: renderização textual
            st.markdown(f"""
            <div class="tree-node">
                <strong>❓ {componentes.get('pergunta_raiz', 'Decisão Principal')}</strong>
            </div>
            """, unsafe_allow_html=True)
            
            filhos = componentes.get('filhos', [])
            for filho in filhos:
                st.markdown(f"""
                <div class="tree-node" style="margin-left: 2rem;">
                    <strong>📍 {filho.get('condicao', '')}</strong><br>
                    ➡️ {filho.get('acao', '')}
                </div>
                """, unsafe_allow_html=True)
                
                sub_filhos = filho.get('filhos', [])
                for sub in sub_filhos:
                    st.markdown(f"""
                    <div class="tree-node" style="margin-left: 4rem;">
                        <strong>📌 {sub.get('condicao', '')}</strong><br>
                        ➡️ {sub.get('acao', '')}
                    </div>
                    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # ==========================================
    # Checklist de Implementação
    # ==========================================
    checklist = response.get('checklist_implementacao', [])
    if checklist:
        st.markdown("### ✅ Checklist de Implementação")
        render_checklist(checklist)
    
    # ==========================================
    # Riscos e Mitigações
    # ==========================================
    riscos = response.get('riscos_mitigacoes', [])
    if riscos:
        st.markdown("### ⚠️ Riscos e Mitigações")
        render_risks(riscos)
    
    st.markdown("---")
    
    # ==========================================
    # Vídeo Sugerido
    # ==========================================
    video = response.get('video_sugestao', {})
    if video and video.get('url'):
        st.markdown(f"""
        <div class="video-card">
            <h4>🎬 Vídeo Recomendado</h4>
            <p><strong>{video.get('titulo', 'Vídeo')}</strong></p>
            <p>{video.get('motivo', '')}</p>
            <a href="{video.get('url', '#')}" target="_blank">▶️ Assistir no YouTube</a>
        </div>
        """, unsafe_allow_html=True)
    
    # ==========================================
    # Download Excel Template
    # ==========================================
    template = response.get('template_sugerido', {})
    if template and template.get('colunas'):
        st.markdown("### 📥 Template Excel para Download")
        st.caption(f"**{template.get('nome', 'Template')}**")
        
        excel_file = ExcelTemplateGenerator.generate_template(template)
        
        st.download_button(
            label="⬇️ Baixar Template Excel",
            data=excel_file,
            file_name=f"FinMentor_{template.get('nome', 'Template').replace(' ', '_')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )


# ============================================================================
# EXECUÇÃO PRINCIPAL
# ============================================================================

def main():
    """Função principal do aplicativo."""
    # Renderiza sidebar
    render_sidebar()
    
    # Renderiza fase atual
    if st.session_state.fase == 1:
        render_phase_1()
    else:
        render_phase_2()


if __name__ == "__main__":
    main()
