# Know Your Fan — MVP com IA + eSports 🎮🤖

Este projeto é um protótipo funcional que coleta dados de fãs de eSports para entender melhor seus interesses, atividades e engajamento com organizações como a FURIA. A aplicação utiliza IA (OpenAI), redes sociais (Twitter) e Supabase como banco de dados em nuvem.

🔗 **App em produção**:  
👉 https://know-your-fan.streamlit.app/

---

## ✨ Funcionalidades

- 📋 Formulário para cadastro de dados pessoais e interesses
- 🪪 Upload e validação de documentos com OCR (Tesseract) + IA (OpenAI)
- 🐦 Integração com Twitter (via Tweepy) para leitura de engajamento com eSports
- 🌐 Validação de perfis em sites externos (Liquipedia, HLTV, etc) com IA
- 🗃️ Armazenamento persistente com Supabase (PostgreSQL em nuvem)

---

## 🚀 Como rodar localmente

### 1. Clone o repositório

```bash
git clone https://github.com/athena272/know-your-fan.git
cd know-your-fan
```
### 2. Crie e ative o ambiente virtual
```bash
python -m venv venv
# Ative no Windows:
venv\Scripts\activate
# Ou no Linux/macOS:
source venv/bin/activate
```
### 3. Instale as dependências
```bash
pip install -r requirements.txt
```
### 4. Configure as variáveis secretas
```bash
cp .streamlit/secrets.example.toml .streamlit/secrets.toml
```
### Estrutura do arquivo .streamlit/secrets.toml
```bash
OPENAI_API_KEY = "COLOQUE_SUA_CHAVE_AQUI"
TW_BEARER       = "COLOQUE_SEU_BEARER_TOKEN_AQUI"
SUPABASE_URL = "COLOQUE_SUA_CHAVE_AQUI"
SUPABASE_KEY = "COLOQUE_SUA_CHAVE_AQUI"
```
### 5. Rode o app
```bash
streamlit run app.py
```

## 🧠 Tecnologias utilizadas
| Tecnologia           | Finalidade                           |
| -------------------- | ------------------------------------ |
| Streamlit            | Interface web                        |
| OpenAI GPT           | Validação de documentos e perfis     |
| Tesseract OCR        | Extração de texto de documentos      |
| Tweepy (Twitter API) | Coleta de interações sociais         |
| Supabase             | Banco de dados em nuvem (PostgreSQL) |
| BeautifulSoup        | Extração de texto de páginas HTML    |

## 📁 Estrutura do Projeto
```
know-your-fan/
├── app.py                      # Código principal da aplicação
├── requirements.txt            # Lista de dependências
├── README.md                   # Este arquivo
├── .gitignore
├── LICENSE
├── .streamlit/
│   └── secrets.example.toml    # Exemplo de arquivo de configuração
└── .devcontainer/
    └── devcontainer.json       # (opcional) suporte para VS Code Containers
```

## ☁️ Deploy gratuito
Este projeto está hospedado gratuitamente com [Streamlit Community Cloud.](https://streamlit.io/cloud)

Para publicar o seu:
Faça push deste projeto para o GitHub:
- Acesse Streamlit Cloud
- Clique em “New app” e selecione seu repositório
- Vá em Settings > Secrets e adicione as chaves como no secrets.toml

## 👨‍💻 Autor
Desenvolvido por Guilherme como parte de um desafio técnico de integração de IA com coleta de dados no universo de eSports.

## 📌 Observações
- O Supabase requer que você crie previamente as tabelas user, docs, social e links no painel do banco.
- O service_role deve ser usado com cuidado e nunca exposto publicamente fora do servidor/secrets.toml.
