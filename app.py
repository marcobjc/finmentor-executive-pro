"""
FinMentor: Executive Pro
========================
CFO Virtual - Consultor Financeiro de Bolso
Desenvolvido para: Marco A. Duarte Jr.
VERSÃO CORRIGIDA - JSON Parsing Robusto
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

# ✅ IMPORTS DE IA
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

# ✅ CSS ATUALIZADO (Expander sempre branco + Estilização Dark)
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

/* --- CORREÇÃO AGRESSIVA DO EXPANDER --- */
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
    """Cliente LLM com parsing JSON robusto"""
    
    # ✅ Modelo estável
    MODELO_ESCOLHIDO = "claude-sonnet-4-5-20250929"

    def __init__(self, api_key: str):
        self.api_key = api_key

    @staticmethod
    def _get_system_prompt(conhecimento: str) -> str:
        """System prompt otimizado para JSON válido"""
        # Limita conhecimento para evitar timeout
        kb_truncated = conhecimento[:50000] if conhecimento else ""
        
        return f"""Você é o FinMentor, um CFO Virtual especializado em finanças corporativas brasileiras.

TAREFA: Analisar o desafio financeiro e retornar uma estratégia estruturada.

REGRAS CRÍTICAS DE FORMATO:
1. Retorne APENAS JSON válido, sem markdown, sem ```json, sem texto antes ou depois
2. Todas as strings devem estar em uma única linha (sem quebras de linha dentro de strings)
3. Use aspas duplas para todas as strings
4. Não use caracteres de controle dentro das strings
5. Para fórmulas matemáticas, use texto simples como "VPL = soma(FC/(1+r)^t)" em vez de LaTeX

BASE DE CONHECIMENTO (resumida):
{kb_truncated[:20000]}

ESTRUTURA JSON OBRIGATÓRIA:
{{
  "titulo": "Título da estratégia (máx 60 caracteres)",
  "area_identificada": "Área financeira principal",
  "kpis_relevantes": ["KPI1", "KPI2", "KPI3"],
  "frameworks_utilizados": ["Framework1", "Framework2"],
  "analise_dos_dados": "Análise concisa em 2-3 parágrafos sem quebras de linha",
  "resumo": "Resumo executivo em 1 parágrafo",
  "modelagem_matematica": "VPL = soma dos fluxos descontados",
  "video_sugestao": {{
    "titulo": "Nome do vídeo sugerido",
    "termo_busca": "termo para buscar no youtube",
    "motivo": "Por que este conteúdo é relevante"
  }},
  "template_sugerido": {{
    "nome": "Nome do template Excel",
    "colunas": ["Coluna1", "Coluna2", "Coluna3", "Coluna4"],
    "linhas_exemplo": [
      {{"Coluna1": "Exemplo1", "Coluna2": "100", "Coluna3": "200", "Coluna4": "300"}}
    ],
    "formulas_sugeridas": ["=SOMA(B2:B10)", "=VPL(taxa;fluxos)"]
  }},
  "componentes": {{
    "pergunta_raiz": "Qual a decisão principal?",
    "filhos": [
      {{
        "condicao": "Se cenário A",
        "acao": "Recomendação para cenário A",
        "filhos": []
      }},
      {{
        "condicao": "Se cenário B", 
        "acao": "Recomendação para cenário B",
        "filhos": []
      }}
    ]
  }},
  "checklist_implementacao": [
    "Passo 1: Ação específica",
    "Passo 2: Ação específica",
    "Passo 3: Ação específica"
  ],
  "riscos_mitigacoes": [
    {{
      "risco": "Descrição do risco",
      "mitigacao": "Como mitigar"
    }}
  ]
}}

Retorne APENAS o JSON, começando com {{ e terminando com }}."""

    def _extract_json_from_response(self, text: str) -> Dict[str, Any]:
        """Extrai JSON de forma robusta, mesmo com texto extra"""
        
        # Remove blocos de código markdown
        text = re.sub(r'```json\s*', '', text)
        text = re.sub(r'```\s*', '', text)
        text = text.strip()
        
        # Tenta encontrar o JSON no texto
        # Procura pelo primeiro { e último }
        start_idx = text.find('{')
        end_idx = text.rfind('}')
        
        if start_idx == -1 or end_idx == -1 or end_idx <= start_idx:
            raise ValueError("Não foi possível encontrar JSON válido na resposta")
        
        json_str = text[start_idx:end_idx + 1]
        
        # Tenta parse direto
        try:
            return json.loads(json_str)
        except json.JSONDecodeError:
            pass
        
        # Tenta corrigir problemas comuns
        # Remove caracteres de controle exceto \n \r \t
        json_str = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f]', '', json_str)
        
        # Substitui quebras de linha dentro de strings por espaços
        # Isso é feito de forma mais cuidadosa
        in_string = False
        result = []
        i = 0
        while i < len(json_str):
            char = json_str[i]
            
            if char == '"' and (i == 0 or json_str[i-1] != '\\'):
                in_string = not in_string
                result.append(char)
            elif in_string and char in '\n\r':
                result.append(' ')
            else:
                result.append(char)
            i += 1
        
        json_str = ''.join(result)
        
        # Tenta parse novamente
        try:
            return json.loads(json_str)
        except json.JSONDecodeError as e:
            # Se ainda falhar, retorna erro estruturado
            raise ValueError(f"JSON inválido após correções: {str(e)}")

    def generate_strategy(self, contexto: str, persona: str, mercado: Dict[str, Any], kb: str) -> Dict[str, Any]:
        """Gera estratégia financeira com parsing robusto"""
        
        client = anthropic.Anthropic(api_key=self.api_key)
        system_prompt = self._get_system_prompt(kb)
        
        user_prompt = f"""DESAFIO DO USUÁRIO:
{contexto}

PERFIL: {persona}
DADOS DE MERCADO: Dólar R$ {mercado.get('dolar', 'N/D')}, IBOVESPA {mercado.get('ibov', 'N/D')} pontos, SELIC {mercado.get('selic', 'N/D')}, IPCA {mercado.get('ipca', 'N/D')}

Analise o desafio e retorne o JSON estruturado conforme especificado."""

        try:
            response = client.messages.create(
                model=self.MODELO_ESCOLHIDO,
                max_tokens=4096,  # Reduzido para evitar respostas muito longas
                temperature=0.3,  # Mais determinístico para JSON
                system=system_prompt,
                messages=[{"role": "user", "content": user_prompt}]
            )
            
            raw_content = response.content[0].text
            
            # Tenta extrair JSON
            try:
                result = self._extract_json_from_response(raw_content)
                
                # Validação básica dos campos obrigatórios
                required_fields = ['titulo', 'area_identificada', 'resumo']
                for field in required_fields:
                    if field not in result:
                        result[field] = "Não especificado"
                
                # Garante que listas existam
                if 'kpis_relevantes' not in result or not isinstance(result['kpis_relevantes'], list):
                    result['kpis_relevantes'] = ["VPL", "TIR", "Payback"]
                if 'frameworks_utilizados' not in result or not isinstance(result['frameworks_utilizados'], list):
                    result['frameworks_utilizados'] = ["Análise de Viabilidade"]
                if 'checklist_implementacao' not in result or not isinstance(result['checklist_implementacao'], list):
                    result['checklist_implementacao'] = ["Revisar análise", "Implementar recomendações"]
                if 'riscos_mitigacoes' not in result or not isinstance(result['riscos_mitigacoes'], list):
                    result['riscos_mitigacoes'] = []
                
                # Garante estrutura do vídeo
                if 'video_sugestao' not in result or not isinstance(result['video_sugestao'], dict):
                    result['video_sugestao'] = {
                        "titulo": "Análise Financeira",
                        "termo_busca": "análise financeira investimentos",
                        "motivo": "Aprofundar conhecimentos sobre o tema"
                    }
                
                # Garante estrutura do template
                if 'template_sugerido' not in result or not isinstance(result['template_sugerido'], dict):
                    result['template_sugerido'] = {
                        "nome": "Análise Financeira",
                        "colunas": ["Período", "Valor", "Acumulado"],
                        "linhas_exemplo": [{"Período": "Mês 1", "Valor": "1000", "Acumulado": "1000"}],
                        "formulas_sugeridas": ["=SOMA(B:B)"]
                    }
                elif 'colunas' not in result['template_sugerido'] or not result['template_sugerido']['colunas']:
                    result['template_sugerido']['colunas'] = ["Período", "Valor", "Acumulado"]
                
                # Garante estrutura dos componentes (árvore de decisão)
                if 'componentes' not in result or not isinstance(result['componentes'], dict):
                    result['componentes'] = {
                        "pergunta_raiz": "Qual a melhor decisão?",
                        "filhos": []
                    }
                
                return result
                
            except ValueError as e:
                # Retorna resposta de fallback com texto bruto
                return {
                    "titulo": "Análise Financeira",
                    "area_identificada": "Finanças Corporativas",
                    "kpis_relevantes": ["VPL", "TIR", "Payback"],
                    "frameworks_utilizados": ["Análise de Viabilidade"],
                    "analise_dos_dados": raw_content[:2000] if raw_content else "Análise não disponível",
                    "resumo": "A análise foi processada. Veja os detalhes acima.",
                    "modelagem_matematica": "",
                    "video_sugestao": {
                        "titulo": "Análise de Investimentos",
                        "termo_busca": "análise investimentos VPL TIR",
                        "motivo": "Aprofundar conhecimento em análise de viabilidade"
                    },
                    "template_sugerido": {
                        "nome": "Fluxo de Caixa",
                        "colunas": ["Período", "Entrada", "Saída", "Saldo"],
                        "linhas_exemplo": [{"Período": "Mês 1", "Entrada": "10000", "Saída": "5000", "Saldo": "5000"}],
                        "formulas_sugeridas": ["=B2-C2"]
                    },
                    "componentes": {
                        "pergunta_raiz": "O investimento é viável?",
                        "filhos": [
                            {"condicao": "VPL > 0", "acao": "Investimento recomendado", "filhos": []},
                            {"condicao": "VPL < 0", "acao": "Reavaliar premissas", "filhos": []}
                        ]
                    },
                    "checklist_implementacao": [
                        "Validar premissas do modelo",
                        "Calcular cenários alternativos",
                        "Apresentar para stakeholders"
                    ],
                    "riscos_mitigacoes": [
                        {"risco": "Variação cambial", "mitigacao": "Considerar hedge"},
                        {"risco": "Cenário macroeconômico", "mitigacao": "Análise de sensibilidade"}
                    ],
                    "parse_warning": str(e)
                }
                
        except anthropic.APIError as e:
            return {"error": True, "message": f"Erro na API Anthropic: {str(e)}"}
        except Exception as e:
            return {"error": True, "message": f"Erro inesperado: {str(e)}"}

    @staticmethod
    def transcribe_audio(audio_bytes: bytes, openai_api_key: str) -> str:
        if not openai_api_key: 
            return "[Erro: Chave OpenAI necessária para transcrição]"
        try:
            client = OpenAI(api_key=openai_api_key)
            audio_file = BytesIO(audio_bytes)
            audio_file.name = "audio.wav"
            return client.audio.transcriptions.create(
                model="whisper-1", 
                file=audio_file, 
                language="pt"
            ).text
        except Exception as e:
            return f"[Erro na transcrição: {str(e)}]"
            
    @staticmethod
    def chat_followup(user_message: str, chat_history: List[Dict], main_context: str, kb: str, api_key: str) -> str:
        client = anthropic.Anthropic(api_key=api_key)
        
        messages_payload = []
        for msg in chat_history[-10:]:
            if msg["role"] in ["user", "assistant"]:
                messages_payload.append({"role": msg["role"], "content": msg["content"]})
        messages_payload.append({"role": "user", "content": user_message})
        
        try:
            response = client.messages.create(
                model="claude-sonnet-4-5-20250929",
                max_tokens=1000,
                temperature=0.7,
                system=f"""Você é o FinMentor, um CFO Virtual. Responda de forma direta e profissional em português brasileiro.
                
Contexto da conversa anterior:
{main_context[:5000]}""",
                messages=messages_payload
            )
            return response.content[0].text.strip()
        except Exception as e:
            return f"❌ Erro ao processar: {str(e)}"


class ExcelTemplateGenerator:
    @staticmethod
    def generate_template(template_data: Dict) -> BytesIO:
        import pandas as pd
        output = BytesIO()
        
        try:
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                colunas = template_data.get('colunas', ['Coluna1', 'Coluna2', 'Coluna3'])
                linhas = template_data.get('linhas_exemplo', [])
                
                # Cria DataFrame
                if linhas and isinstance(linhas, list):
                    # Normaliza as linhas para garantir que todas as colunas existam
                    normalized_rows = []
                    for row in linhas:
                        if isinstance(row, dict):
                            normalized_row = {col: row.get(col, '') for col in colunas}
                            normalized_rows.append(normalized_row)
                    df = pd.DataFrame(normalized_rows) if normalized_rows else pd.DataFrame(columns=colunas)
                else:
                    df = pd.DataFrame(columns=colunas)
                
                # Adiciona linhas vazias para o usuário preencher
                empty_rows = pd.DataFrame([{col: '' for col in colunas} for _ in range(10)])
                df = pd.concat([df, empty_rows], ignore_index=True)
                
                df.to_excel(writer, sheet_name='Dados', index=False)
                
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
                
                for col_num, value in enumerate(df.columns):
                    worksheet.write(0, col_num, value, header_format)
                    worksheet.set_column(col_num, col_num, 18)
                
                # Aba de fórmulas
                formulas = template_data.get('formulas_sugeridas', [])
                if formulas:
                    formula_sheet = workbook.add_worksheet('Fórmulas')
                    formula_sheet.write(0, 0, 'Fórmulas Sugeridas', header_format)
                    for i, formula in enumerate(formulas, start=1):
                        formula_sheet.write(i, 0, str(formula))
                    formula_sheet.set_column(0, 0, 50)
                    
        except Exception as e:
            # Se falhar, cria um Excel mínimo
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                pd.DataFrame({'Erro': [str(e)]}).to_excel(writer, index=False)
        
        output.seek(0)
        return output


def render_checklist(items: List[str]):
    for item in items:
        st.markdown(f'<div class="checklist-item">✅ {item}</div>', unsafe_allow_html=True)

def render_risks(risks: List[Dict]):
    for risk in risks:
        if isinstance(risk, dict):
            st.markdown(f'''<div class="risk-card">
                <p class="risk-title">⚠️ {risk.get('risco', 'Risco não especificado')}</p>
                <p class="risk-mitigation"><strong>Mitigação:</strong> {risk.get('mitigacao', 'Não especificada')}</p>
            </div>''', unsafe_allow_html=True)

def render_tree_node(node: Dict, level: int = 0):
    if not isinstance(node, dict):
        return
        
    margin_left = f"{level * 2}rem"
    css_class = "tree-node-root" if level == 0 else "tree-node"
    icon = "❓" if level == 0 else ("📍" if level == 1 else "📌")
    
    condicao = node.get('condicao', node.get('pergunta_raiz', ''))
    acao = node.get('acao', '')
    
    if condicao:
        st.markdown(f'''<div class="{css_class}" style="margin-left: {margin_left};">
            <strong>{icon} {condicao}</strong>
            {f'<br><span>➡️ {acao}</span>' if acao else ''}
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
        st.info("ℹ️ Chave OPENAI necessária apenas para áudio (opcional)")
        oai_key = st.text_input("OpenAI Key (sk-...):", type="password", key="input_oai_key")

    if not ant_key:
        st.stop()
        
    st.session_state.anthropic_key = ant_key
    st.session_state.openai_key = oai_key
    
    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
    st.markdown("### 🎤 Entrada por Áudio (Opcional)")
    
    if not st.session_state.openai_key:
        st.caption("Insira a chave OpenAI para habilitar transcrição de áudio.")
        audio_value = None
    else:
        audio_value = st.audio_input("Grave seu áudio:", key="audio_recorder")
        
    if audio_value is not None and st.session_state.openai_key:
        with st.spinner("Transcrevendo com Whisper (OpenAI)..."):
            st.session_state.audio_transcription = LLMClient.transcribe_audio(
                audio_value.read(), 
                st.session_state.openai_key
            )
            if not st.session_state.audio_transcription.startswith("[Erro"):
                st.success(f"✅ Transcrição: {st.session_state.audio_transcription[:100]}...")
    
    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
    st.markdown("### 📝 Descreva seu Desafio Financeiro")
    
    with st.form(key="challenge_form", clear_on_submit=False):
        user_challenge = st.text_area(
            "Seu desafio:", 
            value=st.session_state.audio_transcription or "", 
            height=150, 
            placeholder="Ex: Preciso avaliar se devo investir R$ 500k em um novo projeto..."
        )
        
        st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
        st.markdown("### 📎 Base de Dados (Opcional)")
        uploaded_file = st.file_uploader("Envie uma planilha:", type=['xlsx', 'xls', 'csv'])
        
        st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
        st.markdown("### 👤 Seu Perfil")
        selected_persona = st.selectbox("Selecione:", [
            "Diretor Financeiro (CFO)", 
            "Controller", 
            "Gerente de Tesouraria", 
            "Analista de FP&A", 
            "Investidor Individual", 
            "Empreendedor", 
            "Estudante de Finanças"
        ])
        
        submitted = st.form_submit_button("🚀 Gerar Estratégia", use_container_width=True)
        
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
                        if uploaded_file.name.endswith('.csv'):
                            df = pd.read_csv(uploaded_file)
                        else:
                            df = pd.read_excel(uploaded_file)
                        # Limita o tamanho dos dados
                        df_summary = df.head(50).to_string()
                        st.session_state.ctx += f"\n\n## DADOS DO ARQUIVO ({uploaded_file.name}):\n{df_summary[:5000]}"
                    except Exception as e:
                        st.warning(f"⚠️ Erro ao ler arquivo: {e}")
                
                with st.spinner("🧠 Analisando seu desafio... (pode levar 15-30 segundos)"):
                    try:
                        client = LLMClient(st.session_state.anthropic_key)
                        response = client.generate_strategy(
                            st.session_state.ctx, 
                            selected_persona, 
                            st.session_state.market_data, 
                            st.session_state.kb_content
                        )
                        
                        if response.get('error'):
                            st.error(f"❌ {response.get('message')}")
                        else:
                            if response.get('parse_warning'):
                                st.warning(f"⚠️ Aviso de parsing: {response.get('parse_warning')}")
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
    
    st.markdown(f'''<div style="text-align: center; padding: 1rem 0;">
        <span class="focus-badge">{response.get('area_identificada', 'Finanças')}</span>
    </div>
    <h1 class="strategy-header">{response.get('titulo', 'Estratégia Financeira')}</h1>''', unsafe_allow_html=True)
    
    if st.button("⬅️ Nova Consulta"):
        st.session_state.fase = 1
        st.session_state.strategy_response = None
        st.session_state.audio_transcription = ''
        st.session_state.chat_messages = []
        st.session_state.chat_context = ''
        st.rerun()
    
    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
    
    # Vídeo e Excel lado a lado
    col_video, col_excel = st.columns(2)
    
    with col_video:
        video = response.get('video_sugestao', {})
        if isinstance(video, dict):
            termo = video.get('termo_busca', 'análise financeira')
            titulo = video.get('titulo', 'Vídeo Recomendado')
            motivo = video.get('motivo', 'Aprofunde-se neste tema')
            
            encoded_term = urllib.parse.quote(termo)
            video_url = f"https://www.youtube.com/results?search_query={encoded_term}"
            
            st.markdown(f'''<div class="video-card">
                <h4>🎬 Vídeo Recomendado</h4>
                <p class="video-title">{titulo}</p>
                <p class="video-desc">{motivo}</p>
                <a href="{video_url}" target="_blank">
                    🔍 Pesquisar "{termo}" no YouTube
                </a>
            </div>''', unsafe_allow_html=True)

    with col_excel:
        template = response.get('template_sugerido', {})
        if isinstance(template, dict) and template.get('colunas'):
            nome_template = template.get('nome', 'Template Financeiro')
            st.markdown(f'''<div class="download-section">
                <h4>📥 Template Excel</h4>
                <p>{nome_template}</p>
            </div>''', unsafe_allow_html=True)
            
            try:
                excel_data = ExcelTemplateGenerator.generate_template(template)
                st.download_button(
                    "⬇️ Baixar Template", 
                    excel_data, 
                    f"FinMentor_{nome_template.replace(' ', '_')}.xlsx", 
                    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", 
                    use_container_width=True
                )
            except Exception as e:
                st.warning(f"Erro ao gerar Excel: {e}")
    
    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
    
    # KPIs e Frameworks
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 📈 KPIs Relevantes")
        kpis = response.get('kpis_relevantes', [])
        if kpis:
            st.markdown("".join([f'<span class="kpi-badge">{k}</span>' for k in kpis]), unsafe_allow_html=True)
    
    with col2:
        st.markdown("### 📚 Frameworks")
        frameworks = response.get('frameworks_utilizados', [])
        if frameworks:
            st.markdown("".join([f'<span class="focus-badge">{f}</span>' for f in frameworks]), unsafe_allow_html=True)
    
    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
    
    # Análise
    st.markdown("### 🧠 Análise Chain of Thought")
    analise = response.get('analise_dos_dados', 'Análise não disponível')
    st.markdown(f'<div class="analysis-section">{analise}</div>', unsafe_allow_html=True)
    
    # Resumo
    st.markdown("### 📋 Resumo Executivo")
    resumo = response.get('resumo', 'Resumo não disponível')
    st.markdown(f'<div class="strategy-card">{resumo}</div>', unsafe_allow_html=True)
    
    # Modelagem (se existir)
    if response.get('modelagem_matematica'):
        st.markdown("### 📐 Modelagem Matemática")
        st.code(response['modelagem_matematica'], language='text')
    
    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
    
    # Árvore de Decisão
    st.markdown("### 🌳 Árvore de Decisão")
    componentes = response.get('componentes', {})
    if isinstance(componentes, dict) and componentes:
        pergunta_raiz = componentes.get('pergunta_raiz', 'Qual a decisão?')
        st.markdown(f'<div class="tree-node-root"><strong>❓ {pergunta_raiz}</strong></div>', unsafe_allow_html=True)
        
        for filho in componentes.get('filhos', []):
            render_tree_node(filho, level=1)
    
    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
    
    # Checklist
    checklist = response.get('checklist_implementacao', [])
    if checklist:
        st.markdown("### ✅ Checklist de Implementação")
        render_checklist(checklist)
    
    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
    
    # Riscos
    riscos = response.get('riscos_mitigacoes', [])
    if riscos:
        st.markdown("### ⚠️ Riscos e Mitigações")
        render_risks(riscos)

    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
    
    # Chat de Follow-up
    st.markdown("### 💬 Tire suas Dúvidas")
    st.caption("Pergunte mais sobre este tema.")
    
    if not st.session_state.chat_context:
        st.session_state.chat_context = f"""
Tema: {response.get('titulo', 'Estratégia Financeira')}
Área: {response.get('area_identificada', 'Finanças')}
Contexto original: {st.session_state.ctx[:2000] if st.session_state.ctx else ''}
KPIs relevantes: {', '.join(response.get('kpis_relevantes', []))}
Resumo: {response.get('resumo', '')}
"""
    
    for msg in st.session_state.chat_messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
    
    if user_input := st.chat_input("Digite sua pergunta..."):
        st.session_state.chat_messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)
        
        with st.chat_message("assistant"):
            with st.spinner("Processando..."):
                response_text = LLMClient.chat_followup(
                    user_message=user_input,
                    chat_history=st.session_state.chat_messages,
                    main_context=st.session_state.chat_context,
                    kb=st.session_state.kb_content,
                    api_key=st.session_state.anthropic_key
                )
                st.markdown(response_text)
                st.session_state.chat_messages.append({"role": "assistant", "content": response_text})
        st.rerun()


def get_file_icon(filename: str) -> str:
    ext = filename.lower().split('.')[-1] if '.' in filename else ''
    icons = {
        'pdf': '📕', 'doc': '📘', 'docx': '📘', 
        'xls': '📗', 'xlsx': '📗', 
        'ppt': '📙', 'pptx': '📙', 
        'txt': '📄', 'csv': '📊'
    }
    return icons.get(ext, '📎')


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
