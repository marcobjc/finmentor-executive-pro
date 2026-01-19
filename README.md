# FinMentor: Executive Pro 📊

> **Seu CFO Virtual de Bolso** - Transforme desafios financeiros em Estratégias Estruturadas usando IA

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.31+-red.svg)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o--mini-green.svg)

## 🎯 Visão Geral

O **FinMentor: Executive Pro** é uma aplicação web que funciona como um **CFO Virtual**. O usuário envia um desafio financeiro (via texto ou áudio) e, opcionalmente, uma base Excel. O sistema processa usando IA (GPT-4o-mini), consulta dados de mercado em tempo real e retorna uma **Estratégia Estruturada** contendo:

- 🌳 **Árvore de Decisão Visual** (Graphviz)
- 📐 **Modelagem Matemática** (LaTeX)
- 📋 **Explicação Técnica Sênior**
- 🎬 **Sugestão de Vídeo do YouTube**
- 📥 **Template Excel para Download**

## ✨ Características

### Mobile-First Design
- Interface otimizada para dispositivos móveis
- Input de áudio separado do formulário para evitar bugs de teclado
- CSS customizado com fonte Quicksand
- Elementos do Streamlit ocultos para experiência limpa

### Inteligência Artificial
- **GPT-4o-mini** para economia de custos
- **Whisper** para transcrição de áudio
- **Chain of Thought Protocol** para raciocínio estruturado
- **RAG** com base de conhecimento local

### Dados em Tempo Real
- Dólar (USD/BRL) via Yahoo Finance
- IBOVESPA via Yahoo Finance
- SELIC via API do Banco Central
- IPCA via API do Banco Central

## 🚀 Instalação

### Pré-requisitos
- Python 3.9 ou superior
- Graphviz instalado no sistema

### Passo a Passo

1. **Clone ou baixe o projeto**
```bash
mkdir finmentor && cd finmentor
```

2. **Instale as dependências Python**
```bash
pip install -r requirements.txt
```

3. **Instale o Graphviz no sistema**
```bash
# Ubuntu/Debian
sudo apt-get install graphviz

# macOS
brew install graphviz

# Windows
choco install graphviz
```

4. **Configure a API Key da OpenAI**

Opção A - Variável de ambiente:
```bash
export OPENAI_API_KEY="sua-api-key-aqui"
```

Opção B - Arquivo secrets.toml:
```bash
mkdir -p .streamlit
echo 'OPENAI_API_KEY = "sua-api-key-aqui"' > .streamlit/secrets.toml
```

5. **Execute o aplicativo**
```bash
streamlit run app.py
```

6. **Acesse no navegador**
```
http://localhost:8501
```

## 📁 Estrutura do Projeto

```
finmentor/
├── app.py                  # Aplicativo principal (único arquivo)
├── requirements.txt        # Dependências Python
├── README.md              # Este arquivo
├── .streamlit/
│   └── secrets.toml       # API Keys (não commitar!)
└── materiais_publicos/    # Base de conhecimento RAG
    ├── glossario.txt
    ├── metodologias.pdf
    └── cases.docx
```

## 📚 Base de Conhecimento (RAG)

Crie uma pasta `materiais_publicos/` e adicione arquivos `.txt`, `.pdf` ou `.docx` com conteúdo relevante. O sistema automaticamente:

1. Lê todos os arquivos na inicialização
2. Extrai o texto
3. Injeta no contexto da IA

Exemplos de conteúdo útil:
- Glossário de termos financeiros
- Metodologias de valuation
- Cases de estudo
- Políticas internas da empresa

## 🎨 Personalização

### Cores e Temas
Edite as variáveis CSS no bloco `CUSTOM_CSS` do `app.py`:

```css
/* Gradiente principal */
background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);

/* Cor de destaque */
color: #4dabf7;
```

### Prompt da IA
Modifique o `SYSTEM_PROMPT` na classe `LLMClient` para ajustar:
- Áreas de conhecimento
- Frameworks preferidos
- Formato de resposta

## 🔧 Troubleshooting

### Erro: "Graphviz not found"
```bash
# Verifique se o Graphviz está instalado
dot -V

# Se não estiver, instale conforme seu OS (veja seção Instalação)
```

### Erro: "Invalid API Key"
- Verifique se a chave está correta
- Confirme que a variável de ambiente está definida
- Tente usar o arquivo `.streamlit/secrets.toml`

### Spinner infinito
- A API pode estar lenta - aguarde até 60s
- Verifique sua conexão com a internet
- Veja o console para mensagens de erro

### Áudio não transcreve
- Certifique-se que o áudio está em formato WAV
- Verifique se a API Key tem acesso ao Whisper
- Tente gravar um áudio mais curto

## 📱 Uso Mobile

Para melhor experiência mobile:

1. Acesse via navegador do celular
2. Adicione à tela inicial (PWA)
3. Use o input de áudio para perguntas longas
4. Gire para paisagem ao visualizar árvores de decisão

## 🔐 Segurança

- **NUNCA** commite sua API Key
- Use `.gitignore` para excluir `.streamlit/secrets.toml`
- Em produção, use variáveis de ambiente do servidor

## 📄 Licença

Este projeto é proprietário e desenvolvido exclusivamente para **Marco A. Duarte Jr.**

## 👨‍💻 Desenvolvedor

Desenvolvido seguindo o **Prompt Mestre de Engenharia de Software** com:
- Clean Code
- Interface minimalista
- Performance mobile-first
- Resiliência a falhas

---

**FinMentor: Executive Pro** - Democratizando conhecimento financeiro de alto nível 📊
