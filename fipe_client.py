import requests
import time
import os
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# API v2 da FIPE Online (https://fipe.online) — requer token Bearer
# A URL fipe.parallelum.com.br/api/v2 é o endpoint oficial da FIPE Online
FIPE_API = "https://fipe.parallelum.com.br/api/v2/cars"
TOKEN = os.environ.get("FIPE_TOKEN") or "eyJhbGciOiJIUzI1NiJ9.eyJ1c2VySWQiOiJiOTAwZDRmYS03NGExLTRlYWItYjQ1ZS1mZGI2ZDFjODczODEiLCJlbWFpbCI6ImpvYW92aWN0b3JmZXJyYXowMUBnbWFpbC5jb20iLCJpYXQiOjE3ODEwMDEzMzh9.NStnk6188FRsH6nYRyqUgIzglJC54m6oS3g16v6B0lw"

MARCAS_FIPE = {
    "Fiat": 21, "VW - VolksWagen": 59, "GM - Chevrolet": 23, "Toyota": 56,
    "Honda": 25, "Hyundai": 26, "Renault": 48, "Jeep": 29,
    "Nissan": 43, "Ford": 22
}

COMBUSTIVEL_FIPE = {
    "flex": 1, "gasolina": 1, "diesel": 3, "eletrico": 4, "hibrido": 6
}

session = requests.Session()
session.headers.update({
    "User-Agent": "AutoMatch/1.0",
    "Authorization": f"Bearer {TOKEN}"
})

def get_marcas():
    r = session.get(f"{FIPE_API}/brands", timeout=10, verify=False)
    return r.json() if r.ok else []

def get_modelos(codigo_marca):
    r = session.get(f"{FIPE_API}/brands/{codigo_marca}/models", timeout=10, verify=False)
    return r.json() if r.ok else []

def get_anos(codigo_marca, codigo_modelo):
    r = session.get(f"{FIPE_API}/brands/{codigo_marca}/models/{codigo_modelo}/years", timeout=10, verify=False)
    return r.json() if r.ok else []

def get_preco(codigo_marca, codigo_modelo, codigo_ano):
    r = session.get(f"{FIPE_API}/brands/{codigo_marca}/models/{codigo_modelo}/years/{codigo_ano}", timeout=10, verify=False)
    if r.ok:
        data = r.json()
        preco_str = data.get("price", "0").replace("R$", "").replace(".", "").replace(",", ".").strip()
        return {
            "preco": preco_str,
            "fipe_codigo": data.get("codeFipe", ""),
            "mes_referencia": data.get("referenceMonth", ""),
            "combustivel": data.get("fuel", ""),
            "marca_fipe": data.get("brand", ""),
            "modelo_fipe": data.get("model", ""),
            "ano_modelo": data.get("modelYear", "")
        }
    return None

def buscar_modelo(nome_busca, modelos_lista):
    nome_busca = nome_busca.lower().replace("-", " ").replace("/", " ")
    palavras = nome_busca.split()
    melhor = None
    melhor_score = 0
    for m in modelos_lista:
        nome_modelo = m["name"].lower()
        score = sum(1 for p in palavras if p in nome_modelo)
        if score > melhor_score:
            melhor_score = score
            melhor = m
    return melhor

def atualizar_preco(veiculo):
    marca = veiculo["marca"]
    cod_marca = MARCAS_FIPE.get(marca)
    if not cod_marca:
        return None
    time.sleep(0.3)
    modelos = get_modelos(cod_marca)
    if not modelos:
        return None
    match = buscar_modelo(veiculo["nome"], modelos)
    if not match:
        return None
    anos = get_anos(cod_marca, match["code"])
    ano_veiculo = veiculo["ano"]
    combustivel = veiculo.get("tipo_combustivel", "flex")
    cod_comb = COMBUSTIVEL_FIPE.get(combustivel, 1)
    ano_alvo = f"{ano_veiculo}-{cod_comb}"
    for a in anos:
        if a["code"] == ano_alvo:
            return get_preco(cod_marca, match["code"], ano_alvo)
    if anos:
        ultimo = anos[-1]["code"]
        return get_preco(cod_marca, match["code"], ultimo)
    return None
