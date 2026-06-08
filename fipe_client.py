import requests
import time

FIPE_API = "https://parallelum.com.br/fipe/api/v1/carros"
MARCAS_FIPE = {
    "Fiat": 21, "Volkswagen": 59, "Chevrolet": 23, "Toyota": 56,
    "Honda": 25, "Hyundai": 26, "Renault": 48, "Jeep": 29,
    "Nissan": 43, "BYD": 238, "BMW": 7, "Mercedes": 39,
    "Audi": 6, "Ford": 22, "Peugeot": 44, "Citroen": 13,
    "Citroën": 13, "GWM": 240, "Caoa Chery": 245, "Land Rover": 33,
    "Volvo": 58, "Porsche": 47, "Mitsubishi": 41, "Kia Motors": 31,
    "Peugeot": 44, "Ford": 22
}

COMBUSTIVEL_FIPE = {
    "flexivel": 5, "gasolina": 1, "diesel": 3, "eletrico": 4, "hibrido": 6
}

session = requests.Session()
session.headers.update({"User-Agent": "AutoMatch/1.0"})

def get_marcas():
    r = session.get(f"{FIPE_API}/marcas", timeout=10)
    return r.json() if r.ok else []

def get_modelos(codigo_marca):
    r = session.get(f"{FIPE_API}/marcas/{codigo_marca}/modelos", timeout=10)
    return r.json() if r.ok else {"modelos": [], "anos": []}

def get_anos(codigo_marca, codigo_modelo):
    r = session.get(f"{FIPE_API}/marcas/{codigo_marca}/modelos/{codigo_modelo}/anos", timeout=10)
    return r.json() if r.ok else []

def get_preco(codigo_marca, codigo_modelo, codigo_ano):
    r = session.get(f"{FIPE_API}/marcas/{codigo_marca}/modelos/{codigo_modelo}/anos/{codigo_ano}", timeout=10)
    if r.ok:
        data = r.json()
        return {
            "preco": data.get("Valor", "0").replace("R$ ", "").replace(".", "").replace(",", "."),
            "fipe_codigo": data.get("CodigoFipe", ""),
            "mes_referencia": data.get("MesReferencia", ""),
            "combustivel": data.get("Combustivel", ""),
            "marca_fipe": data.get("Marca", ""),
            "modelo_fipe": data.get("Modelo", "")
        }
    return None

def buscar_modelo(nome_busca, modelos_lista):
    nome_busca = nome_busca.lower().replace("-", " ").replace("/", " ")
    palavras = nome_busca.split()
    melhor = None
    melhor_score = 0
    for m in modelos_lista:
        nome_modelo = m["nome"].lower()
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
    data = get_modelos(cod_marca)
    modelos = data.get("modelos", [])
    if not modelos:
        return None
    match = buscar_modelo(veiculo["nome"], modelos)
    if not match:
        return None
    anos = get_anos(cod_marca, match["codigo"])
    ano_veiculo = veiculo["ano"]
    combustivel = veiculo.get("tipo_combustivel", "flexivel")
    cod_comb = COMBUSTIVEL_FIPE.get(combustivel, 5)
    ano_alvo = f"{ano_veiculo}-{cod_comb}"
    ano_zero = f"32000-{cod_comb}"
    for a in anos:
        if a["codigo"] == ano_alvo:
            return get_preco(cod_marca, match["codigo"], ano_alvo)
    if anos:
        ultimo = anos[-1]["codigo"]
        return get_preco(cod_marca, match["codigo"], ultimo)
    return None
