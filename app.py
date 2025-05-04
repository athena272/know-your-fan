import streamlit as st
import sqlite3
import pytesseract
from PIL import Image
import openai
import requests
from bs4 import BeautifulSoup
# import tweepy  # se usar

# --- CONFIGURAÇÕES INICIAIS ---
openai.api_key = st.secrets["OPENAI_API_KEY"]
conn = sqlite3.connect("fan_profile.db", check_same_thread=False)
c = conn.cursor()
c.execute("""
CREATE TABLE IF NOT EXISTS user (
    id INTEGER PRIMARY KEY,
    nome TEXT,
    cpf TEXT,
    endereco TEXT,
    interesses TEXT,
    compras_eventos TEXT
)""")
c.execute("""
CREATE TABLE IF NOT EXISTS docs (
    user_id INTEGER, tipo TEXT, resultado TEXT
)""")
c.execute("""
CREATE TABLE IF NOT EXISTS social (
    user_id INTEGER, plataforma TEXT, dados TEXT
)""")
c.execute("""
CREATE TABLE IF NOT EXISTS links (
    user_id INTEGER, url TEXT, relevancia TEXT
)""")
conn.commit()

st.title("Know Your Fan — Protótipo Mínimo Viável")

# --- 1. COLETA DE DADOS BÁSICOS ---
with st.form("dados_basicos"):
    nome = st.text_input("Nome completo")
    cpf  = st.text_input("CPF")
    endereco = st.text_area("Endereço")
    interesses = st.text_area("Seus interesses em e-sports (último ano)")
    compras_eventos = st.text_area("Compras e eventos que participou (último ano)")
    ok = st.form_submit_button("Salvar dados")
    if ok:
        c.execute("INSERT INTO user (nome,cpf,endereco,interesses,compras_eventos) VALUES (?,?,?,?,?)",
                  (nome,cpf,endereco,interesses,compras_eventos))
        conn.commit()
        st.success("Dados salvos!")

# --- 2. UPLOAD E VALIDAÇÃO de documento ---
st.header("Validação de Identidade")
doc = st.file_uploader("Envie foto do RG/CNH", type=["png","jpg","jpeg"])
if doc:
    img = Image.open(doc)
    text = pytesseract.image_to_string(img, lang="por")
    # Chama GPT para validar
    prompt = (
        f"Extraí este texto de um documento de identidade:\n\n"
        f"{text}\n\n"
        f"Compare com nome={nome!r} e cpf={cpf!r}. "
        "Responda sucintamente se os dados batem e, se não, quais divergências."
    )
    resp = openai.ChatCompletion.create(
        model="gpt-4o-mini", messages=[{"role":"user","content":prompt}]
    )
    resultado = resp.choices[0].message.content
    c.execute("INSERT INTO docs VALUES (?,?,?)", (1, "rg", resultado))
    conn.commit()
    st.write("**Resultado da validação:**", resultado)

# --- 3. INTEGRAÇÃO COM TWITTER (exemplo) ---
st.header("Redes Sociais")
twitter = st.text_input("Digite seu @ do Twitter (sem @)")
if st.button("Buscar tweets"):
    # autenticação simples (exigir chaves no secrets.toml)
    client = tweepy.Client(bearer_token=st.secrets["TW_BEARER"])
    tweets = client.get_users_tweets(id=client.get_user(username=twitter).data.id, max_results=50)
    relevantes = [t.text for t in tweets.data if "FURIA" in t.text.upper()]
    c.execute("INSERT INTO social VALUES (?,?,?)", (1, "twitter", "\n".join(relevantes)))
    conn.commit()
    st.write("Tweets citando FURIA:", relevantes)

# --- 4. VALIDAÇÃO DE LINKS de sites de e-sports ---
st.header("Perfis em Sites de e-sports")
url = st.text_input("Cole aqui o link do seu perfil (ex: liquipedia.net/…)")
if st.button("Validar link"):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    texto = soup.get_text(separator="\n")[:2000]
    prompt = (
        "Esse texto extraído do perfil pertence a um fã de esports "
        f"e corresponde a {nome!r}? Responda sim/não e explique brevemente."
        f"\n\n---\n{texto}"
    )
    resp2 = openai.ChatCompletion.create(
        model="gpt-4o-mini", messages=[{"role":"user","content":prompt}]
    )
    val = resp2.choices[0].message.content
    c.execute("INSERT INTO links VALUES (?,?,?)", (1, url, val))
    conn.commit()
    st.write("**Resultado de relevância:**", val)