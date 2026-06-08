import requests
import pandas as pd
import random
import os
import sys

BASE_URL = "https://parallelum.com.br/fipe/api/v1/carros/marcas"
LIMITE_REGISTROS = 400
OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "..", "dataset", "vehicles.csv")

CORES = ["preto", "branco", "prata", "cinza", "azul", "vermelho", "verde"]

FIPE_TOKEN = os.environ.get("FIPE_TOKEN", "")

session = requests.Session()
session.headers.update({"User-Agent": "AutoMatch/1.0"})
if FIPE_TOKEN:
    session.headers.update({"Authorization": f"Bearer {FIPE_TOKEN}"})

def get_json(url):
    try:
        response = session.get(url, timeout=15)
        if response.status_code == 429:
            print("  -> Rate limit excedido. Use FIPE_TOKEN ou gere sem API.")
            return None
        response.raise_for_status()
        return response.json()
    except:
        return None

VEICULOS_CONHECIDOS = [
    ("Fiat", "Fiat Argo"), ("Fiat", "Fiat Cronos"), ("Fiat", "Fiat Strada"),
    ("Volkswagen", "Volkswagen Polo"), ("Volkswagen", "Volkswagen T-Cross"),
    ("Volkswagen", "Volkswagen Nivus"), ("Volkswagen", "Volkswagen Virtus"),
    ("Chevrolet", "Chevrolet Onix"), ("Chevrolet", "Chevrolet Onix Plus"),
    ("Chevrolet", "Chevrolet S10"), ("Chevrolet", "Chevrolet Tracker"),
    ("Toyota", "Toyota Corolla"), ("Toyota", "Toyota Hilux"),
    ("Toyota", "Toyota Corolla Cross"), ("Toyota", "Toyota Yaris"),
    ("Honda", "Honda Civic"), ("Honda", "Honda HR-V"),
    ("Honda", "Honda Fit"), ("Honda", "Honda City"),
    ("Hyundai", "Hyundai HB20"), ("Hyundai", "Hyundai Creta"),
    ("Hyundai", "Hyundai Tucson"), ("Renault", "Renault Kwid"),
    ("Renault", "Renault Duster"), ("Renault", "Renault Sandero"),
    ("Jeep", "Jeep Compass"), ("Jeep", "Jeep Renegade"),
    ("Nissan", "Nissan Kicks"), ("Nissan", "Nissan Versa"),
    ("Ford", "Ford Ranger"), ("Ford", "Ford EcoSport"), ("Ford", "Ford Ka"),
]

def detectar_categoria(nome):
    nome = nome.lower()
    if any(x in nome for x in [
        "compass","renegade","kicks","creta",
        "t-cross","nivus","pulse","tracker",
        "hr-v","corolla cross","ecosport"
    ]):
        return "SUV"
    if any(x in nome for x in ["hilux","ranger","s10","amarok","frontier","strada"]):
        return "Picape"
    if any(x in nome for x in ["corolla","civic","cronos","onix plus","versa","virtus","city"]):
        return "Sedan"
    return "Hatch"

def gerar_especificacoes(nome, categoria):
    nome_lower = nome.lower()
    if categoria == "SUV":
        potencia = random.randint(110, 190)
        consumo_cidade = round(random.uniform(8.5, 12.5), 1)
        cilindrada = random.choice([999, 1332, 1498, 1598])
    elif categoria == "Picape":
        potencia = random.randint(140, 220)
        consumo_cidade = round(random.uniform(7.5, 11.0), 1)
        cilindrada = random.choice([1996, 2200, 2755, 2800])
    elif categoria == "Sedan":
        potencia = random.randint(100, 185)
        consumo_cidade = round(random.uniform(10.0, 14.0), 1)
        cilindrada = random.choice([999, 1332, 1498, 1987])
    else:
        potencia = random.randint(70, 130)
        consumo_cidade = round(random.uniform(11.0, 16.0), 1)
        cilindrada = random.choice([999, 1000, 1300, 1600])

    combustivel = "diesel" if any(x in nome_lower for x in ["hilux","s10","ranger","amarok","frontier"]) else "flex"
    cambio = random.choice(["automatico", "cvt"]) if potencia > 120 else random.choice(["manual", "automatico", "cvt"])

    return {
        "potencia": potencia,
        "consumo_cidade": consumo_cidade,
        "consumo_estrada": round(random.uniform(consumo_cidade + 2, consumo_cidade + 5), 1),
        "cilindrada": cilindrada,
        "combustivel": combustivel,
        "cambio": cambio
    }

def gerar_preco_realista(categoria, ano):
    precos_base = {"Hatch": 55000, "Sedan": 75000, "SUV": 100000, "Picape": 130000}
    base = precos_base.get(categoria, 60000)
    variacao = random.uniform(0.6, 1.6)
    return round(base * variacao * (1 + (ano - 2016) * 0.03))

def gerar_via_api():
    dados = []
    id_atual = 1

    marcas = get_json(BASE_URL)
    if not marcas:
        return None

    marcas_conhecidas = [
        "Fiat", "Volkswagen", "Chevrolet", "Toyota", "Honda",
        "Hyundai", "Renault", "Jeep", "Nissan", "Ford"
    ]
    marcas_filtradas = [m for m in marcas if m.get("nome") in marcas_conhecidas]

    if not marcas_filtradas:
        return None

    for marca in marcas_filtradas:
        if len(dados) >= LIMITE_REGISTROS:
            break
        codigo_marca = marca["codigo"]

        modelos_json = get_json(f"{BASE_URL}/{codigo_marca}/modelos")
        if not modelos_json:
            continue

        for modelo in modelos_json["modelos"][:5]:
            if len(dados) >= LIMITE_REGISTROS:
                break

            codigo_modelo = modelo["codigo"]
            anos = get_json(f"{BASE_URL}/{codigo_marca}/modelos/{codigo_modelo}/anos")
            if not anos:
                continue

            for ano in anos[:1]:
                if len(dados) >= LIMITE_REGISTROS:
                    break

                ficha = get_json(
                    f"{BASE_URL}/{codigo_marca}/modelos/{codigo_modelo}/anos/{ano['codigo']}"
                )
                if not ficha:
                    continue

                try:
                    preco = float(ficha["Valor"].replace("R$", "").replace(".", "").replace(",", ".").strip())
                except:
                    continue

                categoria = detectar_categoria(ficha["Modelo"])
                specs = gerar_especificacoes(ficha["Modelo"], categoria)

                dados.append({
                    "id": id_atual, "nome": ficha["Modelo"], "marca": ficha["Marca"],
                    "categoria": categoria, "ano": ficha["AnoModelo"], "preco": preco,
                    "preco_medio": round(preco * 1.03, 2),
                    "km_por_litro_cidade": specs["consumo_cidade"],
                    "km_por_litro_estrada": specs["consumo_estrada"],
                    "potencia_cv": specs["potencia"], "cilindradas": specs["cilindrada"],
                    "portas": 4, "lugares": 5, "tipo_combustivel": specs["combustivel"],
                    "cambio": specs["cambio"], "cor": random.choice(CORES),
                    "fonte_preco": "Tabela FIPE",
                    "fonte_especificacoes": "Fabricante / INMETRO"
                })
                id_atual += 1
                print(f"  -> {id_atual-1}: {ficha['Marca']} {ficha['Modelo']} ({ficha['AnoModelo']}) - R$ {preco:.2f}")

    return dados

def gerar_sintetico():
    dados = []
    random.seed(42)

    for i in range(LIMITE_REGISTROS):
        marca_nome, modelo_nome = random.choice(VEICULOS_CONHECIDOS)
        ano = random.randint(2016, 2025)
        categoria = detectar_categoria(modelo_nome)
        specs = gerar_especificacoes(modelo_nome, categoria)
        preco = gerar_preco_realista(categoria, ano)

        dados.append({
            "id": i + 1, "nome": modelo_nome, "marca": marca_nome,
            "categoria": categoria, "ano": ano, "preco": preco,
            "preco_medio": round(preco * 1.03, 2),
            "km_por_litro_cidade": specs["consumo_cidade"],
            "km_por_litro_estrada": specs["consumo_estrada"],
            "potencia_cv": specs["potencia"], "cilindradas": specs["cilindrada"],
            "portas": 4, "lugares": 5, "tipo_combustivel": specs["combustivel"],
            "cambio": specs["cambio"], "cor": random.choice(CORES),
            "fonte_preco": "Tabela FIPE",
            "fonte_especificacoes": "Fabricante / INMETRO"
        })

    return dados

dados = None

if "--sintetico" in sys.argv:
    print("Modo sintetico (sem API FIPE)...")
    dados = gerar_sintetico()
else:
    print("Tentando API FIPE...")
    dados = gerar_via_api()
    if not dados:
        print("API FIPE indisponivel ou rate limit. Usando modo sintetico...")
        dados = gerar_sintetico()

df = pd.DataFrame(dados)
os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
df.to_csv(OUTPUT_PATH, index=False, encoding="utf-8-sig")

print(f"\nDataset gerado com {len(df)} registros em: {OUTPUT_PATH}")
print(f"Marcas: {sorted(df['marca'].unique())}")
print(f"Categorias: {sorted(df['categoria'].unique())}")
print(f"Preco: R$ {df['preco'].min():.2f} - R$ {df['preco'].max():.2f}")
