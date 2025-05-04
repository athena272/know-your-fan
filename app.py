import streamlit as st
from supabase import create_client
import pytesseract
from PIL import Image
import openai
import requests
from bs4 import BeautifulSoup
import tweepy

# --- CONFIGURAÇÕES INICIAIS ---
openai.api_key = st.secrets["OPENAI_API_KEY"]

SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]  # use aqui a service_role key
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

st.title("Know Your Fan")

# --- 1. COLETA DE DADOS BÁSICOS ---
with st.form("dados_basicos"):
    nome = st.text_input("Nome completo")
    cpf  = st.text_input("CPF")
    endereco = st.text_area("Endereço")
    interesses = st.text_area("Seus interesses em e-sports (último ano)")
    compras_eventos = st.text_area("Compras e eventos que participou (último ano)")
    ok = st.form_submit_button("Salvar dados")
    if ok:
        res = supabase.table("user").insert({
            "nome": nome,
            "cpf": cpf,
            "endereco": endereco,
            "interesses": interesses,
            "compras_eventos": compras_eventos
        }).execute()
        if res.error:
            st.error("Erro ao salvar dados: " + res.error.message)
        else:
            st.success("Dados salvos no Supabase!")

# --- 2. UPLOAD E VALIDAÇÃO DE DOCUMENTO ---
st.header("Validação de Identidade")
doc = st.file_uploader("Envie foto do RG/CNH", type=["png","jpg","jpeg"])
if doc:
    img = Image.open(doc)
    text = pytesseract.image_to_string(img, lang="por")
    prompt = (
        f"Extraí este texto de um documento de identidade:\n\n"
        f"{text}\n\n"
        f"Compare com nome={nome!r} e cpf={cpf!r}. "
        "Responda sucintamente se os dados batem e, se não, quais divergências."
    )
    resp = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role":"user","content":prompt}]
    )
    resultado = resp.choices[0].message.content
    supabase.table("docs").insert({
        "user_id": 1,
        "tipo": "rg",
        "resultado": resultado
    }).execute()
    st.write("**Resultado da validação:**", resultado)

# --- 3. INTEGRAÇÃO COM TWITTER ---
st.header("Redes Sociais")
twitter = st.text_input("Digite seu @ do Twitter (sem @)")
if st.button("Buscar tweets"):
    client = tweepy.Client(bearer_token=st.secrets["TW_BEARER"])
    user = client.get_user(username=twitter)
    if user.data:
        tweets = client.get_users_tweets(id=user.data.id, max_results=50)
        relevantes = [t.text for t in tweets.data if "FURIA" in t.text.upper()]
        supabase.table("social").insert({
            "user_id": 1,
            "plataforma": "twitter",
            "dados": "\n".join(relevantes)
        }).execute()
        st.write("Tweets citando FURIA:", relevantes)
    else:
        st.error("Usuário não encontrado.")

# --- 4. VALIDAÇÃO DE LINKS DE SITES DE E-SPORTS ---
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
        model="gpt-4o-mini",
        messages=[{"role":"user","content":prompt}]
    )
    val = resp2.choices[0].message.content
    supabase.table("links").insert({
        "user_id": 1,
        "url": url,
        "relevancia": val
    }).execute()
    st.write("**Resultado de relevância:**", val)
