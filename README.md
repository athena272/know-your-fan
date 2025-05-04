# Know Your Fan

## Setup local

1. `git clone <repo-url>`
2. `cd know-your-fan`
3. `python -m venv venv`
4. `source venv/bin/activate   # ou .\venv\Scripts\activate no Windows`
5. `pip install -r requirements.txt`

## Configurar chaves

Crie um arquivo `secrets.toml` (baseado em `secrets.example.toml`) contendo:

```toml
[general]
OPENAI_API_KEY = "sua-chave-openai"

[twitter]
TW_BEARER = "sua-chave-twitter"