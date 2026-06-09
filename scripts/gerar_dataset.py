import requests
import pandas as pd
import random
import os
import sys
import time
import json
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

TOKEN = os.environ.get("FIPE_TOKEN") or "eyJhbGciOiJIUzI1NiJ9.eyJ1c2VySWQiOiJiOTAwZDRmYS03NGExLTRlYWItYjQ1ZS1mZGI2ZDFjODczODEiLCJlbWFpbCI6ImpvYW92aWN0b3JmZXJyYXowMUBnbWFpbC5jb20iLCJpYXQiOjE3ODEwMDEzMzh9.NStnk6188FRsH6nYRyqUgIzglJC54m6oS3g16v6B0lw"
BASE_URL = "https://fipe.parallelum.com.br/api/v2"
LIMITE_REGISTROS = 600
OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "..", "dataset", "vehicles.csv")

CORES = ["preto", "branco", "prata", "cinza", "azul", "vermelho", "verde"]

session = requests.Session()
session.headers.update({
    "User-Agent": "AutoMatch/1.0",
    "Authorization": f"Bearer {TOKEN}"
})

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
    "BYD": ["DOLPHIN", "SEAL", "YUAN", "SONG", "HAN", "KING"],
    "BMW": ["320I", "X1", "X3", "X5", "X6", "IX", "I4", "M3", "M4"],
    "Mercedes-Benz": ["C180", "C200", "GLA", "GLC", "GLE", "CLA", "A200"],
    "Audi": ["A3", "A4", "Q3", "Q5", "Q7", "E-TRON"],
    "Peugeot": ["208", "2008", "3008", "EXPERT", "PARTNER", "LANDTREK"],
    "Citroën": ["C3", "C4", "AIRCROSS", "JUMPER"],
    "GWM": ["HAVAL", "ORA", "POER"],
    "Caoa Chery": ["TIGGO", "ICAR", "QQ"],
    "Land Rover": ["EVOQUE", "VELAR", "SPORT", "DISCOVERY"],
    "Volvo": ["XC40", "XC60", "XC90", "S60", "S90", "V60"],
    "Porsche": ["CAYENNE", "MACAN", "PANAMERA", "911", "TAYCAN"],
    "Mitsubishi": ["OUTLANDER", "LANCER", "PAJERO", "ASX", "TR4"],
}

MARCAS_FIPE = {
    "Fiat": 21, "VW - VolksWagen": 59, "GM - Chevrolet": 23, "Toyota": 56,
    "Honda": 25, "Hyundai": 26, "Renault": 48, "Jeep": 29,
    "Nissan": 43, "Ford": 22,
    "BYD": 238, "BMW": 7, "Mercedes-Benz": 39,
    "Audi": 6, "Peugeot": 44, "Citroën": 13, "GWM": 240,
    "Caoa Chery": 245, "Land Rover": 33, "Volvo": 58,
    "Porsche": 47, "Mitsubishi": 41,
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
    ("BYD", "BYD Dolphin"), ("BYD", "BYD Seal"), ("BYD", "BYD Yuan Plus"),
    ("BMW", "BMW 320i"), ("BMW", "BMW X1"), ("BMW", "BMW X3"),
    ("Mercedes-Benz", "Mercedes-Benz C180"), ("Mercedes-Benz", "Mercedes-Benz GLA"),
    ("Audi", "Audi A3"), ("Audi", "Audi Q3"), ("Audi", "Audi Q5"),
    ("Peugeot", "Peugeot 208"), ("Peugeot", "Peugeot 2008"),
    ("Citroën", "Citroën C3"), ("Citroën", "Citroën Aircross"),
    ("GWM", "GWM Haval H6"), ("GWM", "GWM ORA 03"),
    ("Caoa Chery", "Caoa Chery Tiggo 5X"), ("Caoa Chery", "Caoa Chery Tiggo 7"),
    ("Land Rover", "Land Rover Discovery"), ("Land Rover", "Land Rover Evoque"),
    ("Volvo", "Volvo XC40"), ("Volvo", "Volvo XC60"),
    ("Porsche", "Porsche Cayenne"), ("Porsche", "Porsche Macan"),
    ("Mitsubishi", "Mitsubishi Outlander"), ("Mitsubishi", "Mitsubishi Lancer"),
]

req_count = 0

def get_json(url):
    global req_count
    for tentativa in range(3):
        try:
            response = session.get(url, timeout=20, verify=False)
            req_count += 1
            if response.status_code == 429:
                print("  [rate limit atingido]")
                return None
            if response.status_code == 402:
                print("  [payment required]")
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
        "pulse","tracker","hr-v","corolla cross","ecosport","captur",
        "haval","tiggo","evoque","velar","xc40","xc60","xc90",
        "outlander","pajero","asx","tr4","glc","gle","gla","glb",
        "q3","q5","q7","x1","x3","x5","x6","cayenne","macan",
        "dolphin","yuan","song","t-cross","2008","3008","aircross",
        "landtrek","discovery","ix", "etron", "q8",
    ]):
        return "SUV"
    if any(x in nome_lower for x in [
        "hilux","ranger","s10","amarok","frontier","strada","saveiro",
        "poer",
    ]):
        return "Picape"
    if any(x in nome_lower for x in [
        "corolla","civic","cronos","onix plus","versa","virtus","city","fusion",
        "a3","a4","a5","a6","s60","s90","320i","c180","c200","a200",
        "s60","s90","panamera","911","taycan","seal","han","king",
        "lancer",
    ]):
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
    "fusion":     (90000, 130000),
    "corolla cross": (140000, 180000),
    "hilux":      (180000, 270000),"ranger":    (180000, 280000),
    "s10":        (170000, 250000),"amarok":    (190000, 300000),
    "frontier":   (160000, 240000),"strada":    (80000, 110000),
    "saveiro":    (70000, 95000),
    "dolphin":    (115000, 150000),"seal":      (180000, 230000),
    "yuan":       (140000, 180000),"song":      (120000, 160000),
    "han":        (220000, 270000),"king":      (170000, 210000),
    "320i":       (180000, 240000),"x1":        (220000, 290000),
    "x3":         (280000, 350000),"x5":        (380000, 500000),
    "x6":         (420000, 550000),"ix":        (350000, 450000),
    "i4":         (300000, 400000),"m3":        (400000, 500000),
    "c180":       (120000, 160000),"c200":      (150000, 200000),
    "gla":        (180000, 240000),"glc":        (240000, 320000),
    "gle":        (350000, 480000),"cla":        (160000, 220000),
    "a200":       (130000, 170000),"a3":        (130000, 170000),
    "a4":         (170000, 230000),"q3":        (170000, 230000),
    "q5":         (260000, 350000),"q7":        (380000, 500000),
    "etron":      (350000, 450000),
    "208":        (60000, 80000), "2008":       (85000, 115000),
    "3008":       (130000, 170000),"partner":   (70000, 95000),
    "c3":         (50000, 70000), "aircross":   (70000, 95000),
    "jumper":     (160000, 220000),
    "haval":      (140000, 190000),"ora":       (120000, 150000),
    "tiggo":      (80000, 130000),"icar":       (90000, 120000),
    "evoque":     (220000, 300000),"velar":     (320000, 420000),
    "discovery":  (350000, 500000),"sport":     (280000, 380000),
    "xc40":       (200000, 270000),"xc60":      (270000, 360000),
    "xc90":       (380000, 500000),"s60":       (200000, 270000),
    "s90":        (300000, 400000),"v60":       (230000, 300000),
    "cayenne":    (450000, 650000),"macan":     (350000, 480000),
    "panamera":   (500000, 700000),"911":       (650000, 900000),
    "taycan":     (500000, 700000),
    "outlander":  (110000, 160000),"lancer":    (70000, 100000),
    "pajero":     (180000, 280000),"asx":       (80000, 110000),
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

def parse_preco(price_str):
    try:
        return float(price_str.replace("R$", "").replace(".", "").replace(",", ".").strip())
    except:
        return None

def gerar_via_api():
    global req_count
    dados = []
    id_atual = 1
    MAX_POR_MARCA = max(30, LIMITE_REGISTROS // len(MARCAS_FIPE))

    marcas_ordem = list(MARCAS_FIPE.items())
    random.shuffle(marcas_ordem)

    for nome_marca, codigo_marca in marcas_ordem:
        if len(dados) >= LIMITE_REGISTROS:
            break
        cont_marca = 0

        modelos_json = get_json(f"{BASE_URL}/cars/brands/{codigo_marca}/models")
        if not modelos_json:
            continue

        modelos_pop = MODELOS_POPULARES.get(nome_marca, [])
        modelos_filtrados = [
            m for m in modelos_json
            if any(p.lower() in m["name"].lower() for p in modelos_pop)
        ]
        if not modelos_filtrados:
            modelos_filtrados = modelos_json[:30]

        random.shuffle(modelos_filtrados)

        for modelo in modelos_filtrados:
            if len(dados) >= LIMITE_REGISTROS or cont_marca >= MAX_POR_MARCA:
                break

            anos = get_json(f"{BASE_URL}/cars/brands/{codigo_marca}/models/{modelo['code']}/years")
            if not anos:
                continue

            anos = anos[-4:]

            for ano in anos:
                if len(dados) >= LIMITE_REGISTROS or cont_marca >= MAX_POR_MARCA:
                    break

                ficha = get_json(f"{BASE_URL}/cars/brands/{codigo_marca}/models/{modelo['code']}/years/{ano['code']}")
                if not ficha:
                    continue

                preco = parse_preco(ficha.get("price", ""))
                if not preco or preco < 15000:
                    continue

                categoria = detectar_categoria(ficha["model"])
                specs = gerar_especificacoes(ficha["model"], categoria)
                dados.append(montar_registro(id_atual, ficha["model"], ficha["brand"],
                    categoria, ficha["modelYear"], preco, specs, "Tabela FIPE"))
                id_atual += 1
                cont_marca += 1
                print(f"  FIPE #{id_atual-1:3d}: R$ {preco:>9.2f} | {nome_marca:16s} {ficha['model']:45s} ({ficha['modelYear']})")

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
    print("Buscando precos reais na API FIPE v2...")
    api_data, id_counter = gerar_via_api()
    if api_data:
        dados_finais.extend(api_data)
        print(f"\nObtidos {len(api_data)} precos reais da FIPE API ({req_count} requisicoes)")

    if len(dados_finais) < LIMITE_REGISTROS:
        restante = LIMITE_REGISTROS - len(dados_finais)
        print(f"Complementando com {restante} registros sinteticos...")
        dados_finais.extend(gerar_sintetico(restante, id_counter))

df = pd.DataFrame(dados_finais)
os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
df.to_csv(OUTPUT_PATH, index=False, encoding="utf-8-sig")

api_count = len(api_data) if 'api_data' in dir() and api_data else 0
print(f"\nDataset gerado com {len(df)} registros em: {OUTPUT_PATH}")
print(f"Marcas: {sorted(df['marca'].unique())}")
print(f"Categorias: {sorted(df['categoria'].unique())}")
print(f"Preco: R$ {df['preco'].min():.2f} - R$ {df['preco'].max():.2f}")
print(f"FIPE real: {api_count} registros, {req_count} requisicoes")
