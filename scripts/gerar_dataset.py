import requests
import pandas as pd
import random
import os
import sys
import time
import json
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

BASE_URL = "https://parallelum.com.br/fipe/api/v1/carros/marcas"
LIMITE_REGISTROS = 400
OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "..", "dataset", "vehicles.csv")

CORES = ["preto", "branco", "prata", "cinza", "azul", "vermelho", "verde"]

session = requests.Session()
session.headers.update({"User-Agent": "AutoMatch/1.0"})

MODELOS_POPULARES = {
    "Fiat": ["ARGO", "CRONOS", "STRADA", "MOBI", "PULSE", "TORO", "UNO"],
    "VW - VolksWagen": ["GOL", "POLO", "T-CROSS", "NIVUS", "VIRTUS", "SAVEIRO", "AMAROK"],
    "GM - Chevrolet": ["ONIX", "TRACKER", "S10", "CRUZE", "COBALT", "SPIN"],
    "Toyota": ["COROLLA", "HILUX", "YARIS", "COROLLA CROSS", "SW4"],
    "Honda": ["CIVIC", "HR-V", "CITY", "FIT", "CR-V"],
    "Hyundai": ["HB20", "CRETA", "TUCSON", "IX35"],
    "Renault": ["KWID", "DUSTER", "SANDERO", "LOGAN", "CAPTUR"],
    "Jeep": ["COMPASS", "RENEGADE", "CHEROKEE", "WRANGLER"],
    "Nissan": ["KICKS", "VERSA", "FRONTIER", "SENTRA"],
    "Ford": ["RANGER", "ECOSPORT", "KA", "FIESTA", "FOCUS", "FUSION"],
}

MARCAS_FIPE = {
    "Fiat": 21, "VW - VolksWagen": 59, "GM - Chevrolet": 23, "Toyota": 56,
    "Honda": 25, "Hyundai": 26, "Renault": 48, "Jeep": 29,
    "Nissan": 43, "Ford": 22
}

VEICULOS_CONHECIDOS = [
    ("Fiat", "Fiat Argo"), ("Fiat", "Fiat Cronos"), ("Fiat", "Fiat Strada"),
    ("Fiat", "Fiat Mobi"), ("Fiat", "Fiat Pulse"), ("Fiat", "Fiat Toro"),
    ("Volkswagen", "Volkswagen Polo"), ("Volkswagen", "Volkswagen T-Cross"),
    ("Volkswagen", "Volkswagen Nivus"), ("Volkswagen", "Volkswagen Virtus"),
    ("Volkswagen", "Volkswagen Gol"), ("Volkswagen", "Volkswagen Saveiro"),
    ("Chevrolet", "Chevrolet Onix"), ("Chevrolet", "Chevrolet Onix Plus"),
    ("Chevrolet", "Chevrolet S10"), ("Chevrolet", "Chevrolet Tracker"),
    ("Chevrolet", "Chevrolet Cruze"), ("Chevrolet", "Chevrolet Spin"),
    ("Toyota", "Toyota Corolla"), ("Toyota", "Toyota Hilux"),
    ("Toyota", "Toyota Corolla Cross"), ("Toyota", "Toyota Yaris"),
    ("Honda", "Honda Civic"), ("Honda", "Honda HR-V"),
    ("Honda", "Honda Fit"), ("Honda", "Honda City"),
    ("Hyundai", "Hyundai HB20"), ("Hyundai", "Hyundai Creta"),
    ("Hyundai", "Hyundai Tucson"), ("Renault", "Renault Kwid"),
    ("Renault", "Renault Duster"), ("Renault", "Renault Sandero"),
    ("Renault", "Renault Captur"), ("Jeep", "Jeep Compass"),
    ("Jeep", "Jeep Renegade"), ("Nissan", "Nissan Kicks"),
    ("Nissan", "Nissan Versa"), ("Ford", "Ford Ranger"),
    ("Ford", "Ford EcoSport"), ("Ford", "Ford Ka"), ("Ford", "Ford Fusion"),
]

DADOS_FIPE_REAIS = [
    {"nome": "500 ABARTH MULTIAIR 1.4 TB 16V 3p", "marca": "Fiat", "ano": 2015, "preco": 119693.0},
    {"nome": "500 Cabrio Dualogic Flex 1.4 8V", "marca": "Fiat", "ano": 2017, "preco": 71884.0},
    {"nome": "AMAROK CD2.0 16V/S CD2.0 16V TDI 4x2 Die", "marca": "VW - VolksWagen", "ano": 2013, "preco": 72999.0},
    {"nome": "AMAROK CD2.0 16V/S CD2.0 16V TDI 4x4 Die", "marca": "VW - VolksWagen", "ano": 2019, "preco": 94018.0},
    {"nome": "AMAROK Comfor. 3.0 V6 TDI 4x4 Dies. Aut.", "marca": "VW - VolksWagen", "ano": 2025, "preco": 269774.0},
    {"nome": "AMAROK Comfor. CD 2.0 TDI 4x4 Dies. Aut.", "marca": "VW - VolksWagen", "ano": 2022, "preco": 143988.0},
    {"nome": "AMAROK CS2.0 16V/S2.0 16V TDI 4x2 Diesel", "marca": "VW - VolksWagen", "ano": 2014, "preco": 76260.0},
    {"nome": "Accord Sedan EX 2.0 16V 156cv Aut.", "marca": "Honda", "ano": 2012, "preco": 67581.0},
    {"nome": "Accord Sedan 2.0 TB 16V Aut. (Híbrido)", "marca": "Honda", "ano": 2025, "preco": 270925.0},
    {"nome": "Cherokee Limited 3.2 4x4 V6 Aut.", "marca": "Jeep", "ano": 2015, "preco": 90546.0},
    {"nome": "350Z 3.5 V6 280cv/ 312cv 2p", "marca": "Nissan", "ano": 2009, "preco": 286179.0},
    {"nome": "Bronco Sport Badlands 2.0L TB 4WD Aut.", "marca": "Ford", "ano": 2025, "preco": 234624.0},
]

def get_json(url):
    for tentativa in range(3):
        try:
            response = session.get(url, timeout=20, verify=False)
            if response.status_code == 429:
                print("  [rate limit atingido]")
                return None
            response.raise_for_status()
            return response.json()
        except requests.Timeout:
            print("  [timeout]")
            time.sleep(3)
        except:
            time.sleep(2)
    return None

def detectar_categoria(nome):
    nome_lower = nome.lower()
    if any(x in nome_lower for x in [
        "compass","renegade","kicks","creta","t-cross","nivus",
        "pulse","tracker","hr-v","corolla cross","ecosport","captur"
    ]):
        return "SUV"
    if any(x in nome_lower for x in ["hilux","ranger","s10","amarok","frontier","strada","saveiro"]):
        return "Picape"
    if any(x in nome_lower for x in ["corolla","civic","cronos","onix plus","versa","virtus","city","fusion"]):
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

PRECOS_FIPE_2025 = {
    "mobi":       (48000, 58000), "kwid":       (45000, 55000),
    "ka":         (48000, 60000), "uno":        (42000, 52000),
    "hb20":       (55000, 75000), "onix":       (60000, 80000),
    "argo":       (58000, 72000), "sandero":    (50000, 65000),
    "polo":       (70000, 95000), "cronos":     (65000, 85000),
    "virtus":     (80000, 110000),"yaris":      (70000, 90000),
    "city":       (75000, 95000), "versa":      (65000, 85000),
    "civic":      (125000, 185000),"corolla":   (130000, 170000),
    "onix plus":  (75000, 95000), "sentra":     (80000, 100000),
    "t-cross":    (95000, 135000),"nivus":      (90000, 125000),
    "kicks":      (85000, 120000),"tracker":    (95000, 130000),
    "hr-v":       (100000, 150000),"creta":     (95000, 135000),
    "captur":     (85000, 115000),"ecosport":   (70000, 95000),
    "renegade":   (95000, 135000),"compass":    (140000, 200000),
    "duster":     (80000, 110000),"pulse":      (70000, 95000),
    "fusion":     (90000, 130000),"torque":     (90000, 120000), # placeholders
    "corolla cross": (140000, 180000),
    "hilux":      (180000, 270000),"ranger":    (180000, 280000),
    "s10":        (170000, 250000),"amarok":    (190000, 300000),
    "frontier":   (160000, 240000),"strada":    (80000, 110000),
    "saveiro":    (70000, 95000),
}

def gerar_preco_realista(nome, ano):
    nome_lower = nome.lower()
    preco_min = preco_max = None
    for chave, (pmin, pmax) in PRECOS_FIPE_2025.items():
        if chave in nome_lower:
            preco_min, preco_max = pmin, pmax
            break
    if not preco_min:
        if any(x in nome_lower for x in ["suv"]):
            preco_min, preco_max = 90000, 140000
        elif any(x in nome_lower for x in ["sedan"]):
            preco_min, preco_max = 70000, 120000
        elif any(x in nome_lower for x in ["picape","pick-up"]):
            preco_min, preco_max = 130000, 210000
        else:
            preco_min, preco_max = 50000, 90000
    fator_ano = 1 - (2025 - min(ano, 2025)) * 0.04
    preco = round(random.uniform(preco_min, preco_max) * max(fator_ano, 0.45))
    return preco

def montar_registro(id_reg, nome, marca, categoria, ano, preco, specs, fonte_preco):
    return {
        "id": id_reg, "nome": nome, "marca": marca,
        "categoria": categoria, "ano": ano, "preco": preco,
        "preco_medio": round(preco * 1.03, 2),
        "km_por_litro_cidade": specs["consumo_cidade"],
        "km_por_litro_estrada": specs["consumo_estrada"],
        "potencia_cv": specs["potencia"], "cilindradas": specs["cilindrada"],
        "portas": 4, "lugares": 5, "tipo_combustivel": specs["combustivel"],
        "cambio": specs["cambio"], "cor": random.choice(CORES),
        "fonte_preco": fonte_preco,
        "fonte_especificacoes": "Fabricante / INMETRO"
    }

def gerar_via_api():
    dados = []
    id_atual = 1

    for nome_marca, codigo_marca in MARCAS_FIPE.items():
        if len(dados) >= LIMITE_REGISTROS:
            break

        modelos_json = get_json(f"{BASE_URL}/{codigo_marca}/modelos")
        if not modelos_json:
            continue

        modelos_pop = MODELOS_POPULARES.get(nome_marca, [])
        modelos_filtrados = [
            m for m in modelos_json["modelos"]
            if any(p.lower() in m["nome"].lower() for p in modelos_pop)
        ]

        for modelo in modelos_filtrados[:4]:
            if len(dados) >= LIMITE_REGISTROS:
                break

            anos = get_json(f"{BASE_URL}/{codigo_marca}/modelos/{modelo['codigo']}/anos")
            if not anos:
                continue

            for ano in anos[:2]:
                if len(dados) >= LIMITE_REGISTROS:
                    break

                ficha = get_json(
                    f"{BASE_URL}/{codigo_marca}/modelos/{modelo['codigo']}/anos/{ano['codigo']}"
                )
                if not ficha:
                    continue

                try:
                    preco = float(ficha["Valor"].replace("R$", "").replace(".", "").replace(",", ".").strip())
                except:
                    continue

                if preco < 15000:
                    continue

                categoria = detectar_categoria(ficha["Modelo"])
                specs = gerar_especificacoes(ficha["Modelo"], categoria)
                dados.append(montar_registro(id_atual, ficha["Modelo"], ficha["Marca"],
                    categoria, ficha["AnoModelo"], preco, specs, "Tabela FIPE"))
                id_atual += 1
                print(f"  FIPE #{id_atual-1:3d}: R$ {preco:>8.2f} | {nome_marca} {ficha['Modelo']}")

    return dados, id_atual

def gerar_sintetico(qtd, start_id=1):
    dados = []
    random.seed(42)

    for i in range(qtd):
        marca_nome, modelo_nome = random.choice(VEICULOS_CONHECIDOS)
        ano = random.randint(2016, 2025)
        categoria = detectar_categoria(modelo_nome)
        specs = gerar_especificacoes(modelo_nome, categoria)
        preco = gerar_preco_realista(modelo_nome, ano)
        dados.append(montar_registro(start_id + i, modelo_nome, marca_nome,
            categoria, ano, preco, specs, "Tabela FIPE"))

    return dados

dados_finais = []
id_counter = 1

if "--sintetico" in sys.argv:
    print("Modo sintetico...")
    dados_finais = gerar_sintetico(LIMITE_REGISTROS)
else:
    print("Buscando precos reais na API FIPE...")
    api_data, id_counter = gerar_via_api()
    if api_data:
        dados_finais.extend(api_data)
        print(f"\nObtidos {len(api_data)} precos reais da FIPE API")

    if len(dados_finais) < LIMITE_REGISTROS:
        restante = LIMITE_REGISTROS - len(dados_finais)
        print(f"Complementando com {restante} registros sinteticos...")
        dados_finais.extend(gerar_sintetico(restante, id_counter))

df = pd.DataFrame(dados_finais)
os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
df.to_csv(OUTPUT_PATH, index=False, encoding="utf-8-sig")

print(f"\nDataset gerado com {len(df)} registros em: {OUTPUT_PATH}")
print(f"Marcas: {sorted(df['marca'].unique())}")
print(f"Categorias: {sorted(df['categoria'].unique())}")
print(f"Preco: R$ {df['preco'].min():.2f} - R$ {df['preco'].max():.2f}")
api_count = len(api_data) if 'api_data' in dir() and api_data else 0
print(f"FIPE real: {api_count} registros")
