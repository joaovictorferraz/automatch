import csv
import random

random.seed(42)

veiculos = [
    # (nome_base, marca, categoria, ano_min, ano_max, preco_min, preco_max, consumo_cidade_min, consumo_cidade_max, potencia_min, potencia_max, cilindradas, portas, lugares, combustivel, cambio)
    # Economico - Flex
    ("Fiat Uno {}","Fiat","Economico",2010,2024,15000,50000,12,14,65,78,999,4,5,"flexivel","manual"),
    ("Fiat Mobi {}","Fiat","Economico",2016,2024,35000,45000,12.5,14.5,66,74,999,4,5,"flexivel","manual"),
    ("Fiat Argo {}","Fiat","Economico",2017,2024,55000,70000,11.5,13.5,72,110,999,4,5,"flexivel","manual"),
    ("Fiat Cronos {}","Fiat","Sedan",2018,2024,65000,85000,10.5,12.5,98,110,1332,4,5,"flexivel","manual"),
    ("Fiat Pulse {}","Fiat","SUV",2021,2024,75000,95000,9.5,11.5,85,130,999,4,5,"flexivel","automatico"),
    ("Fiat Fastback {}","Fiat","SUV",2022,2024,95000,120000,9.0,11.0,130,175,1332,4,5,"flexivel","automatico"),
    ("Fiat Strada {}","Fiat","Picape",2011,2024,55000,85000,9.5,11.5,85,110,1332,2,5,"flexivel","manual"),
    ("Fiat Toro {}","Fiat","SUV",2016,2024,75000,130000,8.0,10.5,139,175,1332,4,5,"flexivel","automatico"),
    ("Fiat Ducato {}","Fiat","Comercial",2015,2024,120000,180000,6.0,8.0,120,140,2287,2,3,"diesel","manual"),
    ("Fiat Fiorino {}","Fiat","Comercial",2010,2024,50000,80000,8.5,10.5,70,85,1242,2,2,"flexivel","manual"),
    # Volkswagen
    ("Volkswagen Gol {}","Volkswagen","Economico",2010,2024,15000,55000,11.5,14.0,68,85,999,4,5,"flexivel","manual"),
    ("Volkswagen Polo {}","Volkswagen","Economico",2017,2024,60000,85000,11.0,13.5,84,130,999,4,5,"flexivel","manual"),
    ("Volkswagen Virtus {}","Volkswagen","Sedan",2018,2024,75000,95000,11.0,13.5,116,150,999,4,5,"flexivel","automatico"),
    ("Volkswagen T-Cross {}","Volkswagen","SUV",2019,2024,85000,115000,9.5,12.0,116,150,999,4,5,"flexivel","automatico"),
    ("Volkswagen Nivus {}","Volkswagen","SUV",2020,2024,85000,110000,9.5,12.0,116,128,999,4,5,"flexivel","automatico"),
    ("Volkswagen Taos {}","Volkswagen","SUV",2021,2024,120000,160000,8.5,11.0,150,190,1395,4,5,"flexivel","automatico"),
    ("Volkswagen Saveiro {}","Volkswagen","Picape",2010,2024,50000,85000,9.0,11.5,90,110,1598,2,5,"flexivel","manual"),
    ("Volkswagen Amarok {}","Volkswagen","Picape",2012,2024,120000,220000,6.5,9.0,140,200,1968,4,5,"diesel","automatica"),
    ("Volkswagen Fox {}","Volkswagen","Economico",2010,2020,15000,40000,11.5,14.0,68,78,999,4,5,"flexivel","manual"),
    ("Volkswagen up! {}","Volkswagen","Economico",2014,2023,25000,55000,12.0,14.5,75,82,999,4,5,"flexivel","manual"),
    # Chevrolet
    ("Chevrolet Onix {}","Chevrolet","Economico",2012,2024,25000,60000,11.5,14.0,78,85,999,4,5,"flexivel","manual"),
    ("Chevrolet Onix Plus {}","Chevrolet","Sedan",2019,2024,60000,80000,11.0,13.5,82,116,999,4,5,"flexivel","automatico"),
    ("Chevrolet Cruze {}","Chevrolet","Sedan",2016,2024,65000,110000,10.0,13.0,144,163,1399,4,5,"flexivel","automatico"),
    ("Chevrolet Tracker {}","Chevrolet","SUV",2019,2024,80000,110000,9.5,12.0,116,177,999,4,5,"flexivel","automatico"),
    ("Chevrolet S10 {}","Chevrolet","Picape",2012,2024,120000,220000,6.5,9.0,147,200,2776,4,5,"diesel","automatica"),
    ("Chevrolet Montana {}","Chevrolet","Picape",2010,2024,55000,95000,9.5,11.5,101,120,1221,4,5,"flexivel","manual"),
    ("Chevrolet Spin {}","Chevrolet","SUV",2012,2024,55000,85000,8.0,10.5,106,120,1796,4,7,"flexivel","automatico"),
    ("Chevrolet Bolt EUV {}","Chevrolet","Eletrico",2022,2024,150000,180000,50,55,200,210,0,4,5,"eletrico","automatico"),
    ("Chevrolet Celta {}","Chevrolet","Economico",2010,2016,10000,25000,12.0,14.5,60,70,999,4,5,"flexivel","manual"),
    ("Chevrolet Prisma {}","Chevrolet","Sedan",2010,2020,15000,45000,10.5,13.0,98,108,1389,4,5,"flexivel","manual"),
    # Toyota
    ("Toyota Corolla {}","Toyota","Sedan",2010,2024,45000,130000,9.5,12.5,140,177,1987,4,5,"flexivel","cvt"),
    ("Toyota Yaris {}","Toyota","Economico",2018,2024,65000,85000,11.0,13.5,101,110,1496,4,5,"flexivel","cvt"),
    ("Toyota Corolla Cross {}","Toyota","SUV",2021,2024,120000,160000,9.5,12.5,101,177,1798,4,5,"flexivel","cvt"),
    ("Toyota Hilux {}","Toyota","Picape",2010,2024,120000,250000,6.5,9.0,147,205,2755,4,5,"diesel","automatica"),
    ("Toyota SW4 {}","Toyota","SUV",2015,2024,180000,300000,6.0,8.5,164,204,2694,4,7,"flexivel","automatica"),
    ("Toyota Etios {}","Toyota","Economico",2012,2024,30000,55000,11.5,14.0,88,96,1496,4,5,"flexivel","manual"),
    # Honda
    ("Honda Civic {}","Honda","Sedan",2010,2024,45000,130000,9.5,12.5,140,177,1996,4,5,"flexivel","cvt"),
    ("Honda HR-V {}","Honda","SUV",2015,2024,70000,130000,9.0,12.0,116,177,1496,4,5,"flexivel","cvt"),
    ("Honda Fit {}","Honda","Economico",2010,2024,25000,85000,10.5,13.5,115,130,1496,4,5,"flexivel","cvt"),
    ("Honda City {}","Honda","Sedan",2019,2024,75000,100000,10.5,13.5,126,130,1496,4,5,"flexivel","cvt"),
    ("Honda CR-V {}","Honda","SUV",2010,2024,60000,180000,7.5,10.5,150,190,1996,4,5,"flexivel","cvt"),
    # Hyundai
    ("Hyundai HB20 {}","Hyundai","Economico",2012,2024,25000,60000,11.5,14.0,80,96,999,4,5,"flexivel","manual"),
    ("Hyundai HB20S {}","Hyundai","Sedan",2013,2024,35000,70000,11.0,13.5,80,96,999,4,5,"flexivel","manual"),
    ("Hyundai Creta {}","Hyundai","SUV",2017,2024,80000,120000,9.5,12.0,120,177,998,4,5,"flexivel","automatico"),
    ("Hyundai Tucson {}","Hyundai","SUV",2015,2024,70000,140000,8.0,11.0,150,177,1999,4,5,"flexivel","automatico"),
    ("Hyundai Santa Fe {}","Hyundai","SUV",2010,2024,60000,180000,7.0,10.0,170,235,2359,4,7,"flexivel","automatica"),
    # Renault
    ("Renault Kwid {}","Renault","Economico",2017,2024,35000,50000,13.0,15.0,66,70,999,4,5,"flexivel","manual"),
    ("Renault Sandero {}","Renault","Economico",2010,2024,15000,50000,11.5,14.0,66,90,999,4,5,"flexivel","manual"),
    ("Renault Duster {}","Renault","SUV",2012,2024,50000,95000,8.0,11.0,100,145,1598,4,5,"flexivel","manual"),
    ("Renault Captur {}","Renault","SUV",2017,2024,65000,95000,9.0,11.5,100,120,1199,4,5,"flexivel","cvt"),
    ("Renault Zoe {}","Renault","Eletrico",2021,2024,120000,150000,50,58,100,110,0,4,5,"eletrico","automatico"),
    ("Renault Master {}","Renault","Comercial",2015,2024,110000,170000,6.0,8.0,120,130,2299,2,3,"diesel","manual"),
    ("Renault Oroch {}","Renault","Picape",2015,2024,60000,95000,9.0,11.0,100,120,1598,4,5,"flexivel","manual"),
    # Jeep
    ("Jeep Renegade {}","Jeep","SUV",2015,2024,55000,110000,8.0,10.5,120,175,1796,4,5,"flexivel","automatico"),
    ("Jeep Compass {}","Jeep","SUV",2016,2024,80000,160000,8.5,11.0,130,175,1332,4,5,"flexivel","automatico"),
    ("Jeep Commander {}","Jeep","SUV",2021,2024,140000,190000,8.0,10.5,130,200,1995,4,7,"flexivel","automatico"),
    ("Jeep Wrangler {}","Jeep","SUV",2015,2024,180000,350000,5.5,8.0,200,285,1996,4,5,"diesel","automatica"),
    # Nissan
    ("Nissan Versa {}","Nissan","Sedan",2010,2024,25000,70000,10.5,13.5,111,130,1598,4,5,"flexivel","cvt"),
    ("Nissan Kicks {}","Nissan","SUV",2016,2024,65000,110000,9.5,12.0,113,130,1598,4,5,"flexivel","cvt"),
    ("Nissan Sentra {}","Nissan","Sedan",2010,2024,45000,110000,9.5,12.5,130,150,1998,4,5,"flexivel","cvt"),
    ("Nissan Leaf {}","Nissan","Eletrico",2020,2024,130000,160000,50,56,145,150,0,4,5,"eletrico","automatico"),
    ("Nissan Frontier {}","Nissan","Picape",2010,2024,100000,210000,6.5,9.0,130,190,2488,4,5,"diesel","automatica"),
    # BYD
    ("BYD Dolphin Mini {}","BYD","Eletrico",2023,2024,65000,75000,55,62,70,80,0,4,5,"eletrico","automatico"),
    ("BYD Dolphin {}","BYD","Eletrico",2023,2024,90000,110000,50,58,90,100,0,4,5,"eletrico","automatico"),
    ("BYD Yuan Pro {}","BYD","Eletrico",2023,2024,120000,140000,48,55,140,160,0,4,5,"eletrico","automatico"),
    ("BYD Song Plus {}","BYD","Eletrico",2023,2024,160000,185000,45,52,210,230,0,4,5,"eletrico","automatico"),
    ("BYD Seal {}","BYD","Eletrico",2023,2024,200000,230000,40,48,310,330,0,4,5,"eletrico","automatico"),
    # GWM
    ("GWM Haval H6 {}","GWM","Eletrico",2023,2024,180000,210000,42,50,380,400,0,4,5,"eletrico","automatico"),
    ("GWM Ora 03 {}","GWM","Eletrico",2023,2024,120000,150000,48,55,170,185,0,4,5,"eletrico","automatico"),
    # Caoa Chery
    ("Caoa Chery Tiggo 5X {}","Caoa Chery","SUV",2020,2024,75000,100000,9.0,11.5,113,150,1498,4,5,"flexivel","cvt"),
    ("Caoa Chery Tiggo 7 {}","Caoa Chery","SUV",2021,2024,100000,135000,8.5,11.0,150,180,1498,4,5,"flexivel","cvt"),
    ("Caoa Chery Tiggo 8 {}","Caoa Chery","SUV",2021,2024,140000,180000,8.0,10.5,180,220,1998,4,7,"flexivel","automatico"),
    # Peugeot
    ("Peugeot 208 {}","Peugeot","Economico",2016,2024,50000,75000,11.5,14.0,75,90,1199,4,5,"flexivel","manual"),
    ("Peugeot 2008 {}","Peugeot","SUV",2015,2024,55000,90000,9.0,11.5,75,130,1199,4,5,"flexivel","automatico"),
    ("Peugeot e-208 {}","Peugeot","Eletrico",2022,2024,130000,160000,48,54,130,140,0,4,5,"eletrico","automatico"),
    ("Peugeot Partner {}","Peugeot","Comercial",2015,2024,55000,85000,8.0,10.0,75,95,1199,2,2,"flexivel","manual"),
    # Citroen
    ("Citroën C3 {}","Citroën","Economico",2012,2024,35000,60000,12.0,14.5,65,85,999,4,5,"flexivel","manual"),
    ("Citroën C4 Cactus {}","Citroën","SUV",2018,2024,65000,95000,9.5,12.0,115,150,1199,4,5,"flexivel","automatico"),
    # BMW
    ("BMW 320i {}","BMW","Sedan",2015,2024,120000,220000,8.5,11.5,184,245,1998,4,5,"flexivel","automatica"),
    ("BMW X1 {}","BMW","SUV",2015,2024,130000,240000,8.0,11.0,150,200,1998,4,5,"flexivel","automatica"),
    ("BMW X3 {}","BMW","SUV",2015,2024,180000,320000,7.5,10.5,184,260,1998,4,5,"flexivel","automatica"),
    ("BMW i4 {}","BMW","Eletrico",2022,2024,280000,350000,42,50,330,350,0,4,5,"eletrico","automatico"),
    # Mercedes
    ("Mercedes-Benz C200 {}","Mercedes","Sedan",2015,2024,140000,240000,8.5,11.5,184,204,1991,4,5,"flexivel","automatica"),
    ("Mercedes-Benz GLA {}","Mercedes","SUV",2015,2024,150000,270000,8.0,11.0,150,220,1991,4,5,"flexivel","automatica"),
    ("Mercedes-Benz GLB {}","Mercedes","SUV",2020,2024,220000,320000,8.0,10.5,163,224,1991,4,7,"flexivel","automatica"),
    ("Mercedes-Benz EQA {}","Mercedes","Eletrico",2022,2024,280000,350000,42,50,190,210,0,4,5,"eletrico","automatico"),
    # Audi
    ("Audi A3 {}","Audi","Sedan",2015,2024,120000,200000,9.5,12.5,150,190,1984,4,5,"flexivel","automatico"),
    ("Audi Q3 {}","Audi","SUV",2015,2024,140000,240000,8.5,11.5,150,220,1984,4,5,"flexivel","automatico"),
    ("Audi Q5 {}","Audi","SUV",2015,2024,200000,350000,7.5,10.5,190,265,1984,4,5,"flexivel","automatica"),
    ("Audi e-tron {}","Audi","Eletrico",2022,2024,350000,450000,38,45,300,360,0,4,5,"eletrico","automatico"),
    # Ford
    ("Ford Ka {}","Ford","Economico",2014,2024,25000,55000,12.0,14.5,80,95,999,4,5,"flexivel","manual"),
    ("Ford EcoSport {}","Ford","SUV",2013,2024,40000,85000,8.5,11.0,100,140,1598,4,5,"flexivel","automatico"),
    ("Ford Ranger {}","Ford","Picape",2012,2024,120000,210000,7.0,9.5,160,200,1996,4,5,"diesel","automatica"),
    ("Ford Transit {}","Ford","Comercial",2015,2024,140000,200000,6.0,8.0,130,170,2198,2,3,"diesel","manual"),
    ("Ford Territory {}","Ford","SUV",2020,2024,120000,160000,8.5,11.0,150,175,1498,4,5,"flexivel","cvt"),
    # Mitsubishi
    ("Mitsubishi L200 {}","Mitsubishi","Picape",2010,2024,110000,240000,6.0,8.5,160,190,2442,4,5,"diesel","automatica"),
    ("Mitsubishi Pajero Sport {}","Mitsubishi","SUV",2015,2024,180000,280000,6.5,9.0,160,200,2442,4,7,"diesel","automatica"),
    ("Mitsubishi Eclipse Cross {}","Mitsubishi","SUV",2019,2024,100000,150000,9.0,11.5,165,170,1498,4,5,"flexivel","cvt"),
    # Land Rover
    ("Land Rover Discovery {}","Land Rover","SUV",2015,2024,250000,400000,6.0,8.5,240,360,2993,4,7,"diesel","automatica"),
    ("Land Rover Evoque {}","Land Rover","SUV",2015,2024,180000,280000,8.0,10.5,150,240,1997,4,5,"flexivel","automatica"),
    ("Range Rover Sport {}","Land Rover","SUV",2015,2024,350000,550000,5.5,8.0,250,400,2993,4,5,"diesel","automatica"),
    # Volvo
    ("Volvo XC40 Recharge {}","Volvo","Eletrico",2022,2024,210000,250000,42,48,400,415,0,4,5,"eletrico","automatico"),
    ("Volvo XC60 {}","Volvo","SUV",2017,2024,200000,320000,7.5,10.5,190,310,1969,4,5,"flexivel","automatica"),
    ("Volvo XC90 {}","Volvo","SUV",2015,2024,250000,420000,6.5,9.0,250,400,1969,4,7,"flexivel","automatica"),
    # Porsche
    ("Porsche Cayenne {}","Porsche","SUV",2015,2024,350000,550000,6.5,9.5,300,440,2995,4,5,"flexivel","automatica"),
    ("Porsche Macan {}","Porsche","SUV",2018,2024,280000,450000,7.0,10.0,250,380,1984,4,5,"flexivel","automatica"),
    ("Porsche Taycan {}","Porsche","Eletrico",2022,2024,450000,600000,35,42,450,580,0,4,4,"eletrico","automatico"),
]

geracoes_sufixos = ["", "1.0", "1.4", "1.6", "2.0", "GT", "Sport", "Premium", "LS", "LT", "LTZ", "Advantage", "SPORT", "GTS", "RS", "S", "SE", "TDI", "GLX", "DX", "GL", "LX"]
cores = ["branco", "preto", "prata", "vermelho", "azul", "cinza", "verde", "bege", "marrom", "laranja"]
cambios_por_tipo = {
    "flexivel": ["manual", "automatico", "cvt"],
    "diesel": ["manual", "automatica"],
    "eletrico": ["automatico"]
}

rows = []
id_counter = 1

for base in veiculos:
    nome_base, marca, categoria, ano_min, ano_max, preco_min, preco_max, cons_cid_min, cons_cid_max, pot_min, pot_max, cilindradas, portas, lugares, combustivel, cambio = base
    qtd_por_base = random.randint(3, 6)
    for _ in range(qtd_por_base):
        ano = random.randint(ano_min, ano_max)
        preco = round(random.uniform(preco_min, preco_max), -2)
        if preco < 5000: preco = 5000
        consumo_cidade = round(random.uniform(cons_cid_min, cons_cid_max), 1)
        consumo_estrada = round(consumo_cidade * random.uniform(1.15, 1.35), 1)
        potencia = random.randint(pot_min, pot_max)
        cor = random.choice(cores)
        km = random.randint(0, 200000) if ano <= 2021 else 0
        sufixo = random.choice(geracoes_sufixos)
        nome = f"{nome_base.format(sufixo)}".strip()
        if nome.count(" ") == 0:
            nome = nome_base.split("{}")[0].strip()
        
        if combustivel == "eletrico":
            cambio_val = "automatico"
        elif combustivel == "diesel":
            cambio_val = random.choice(cambios_por_tipo["diesel"])
        else:
            cambio_val = random.choice(cambios_por_tipo["flexivel"])
        
        rows.append([
            id_counter, nome, marca, categoria, ano, preco, preco * 1.025,
            consumo_cidade, consumo_estrada, potencia, cilindradas,
            portas, lugares, combustivel, cambio_val, cor, km
        ])
        id_counter += 1

with open("dataset/vehicles.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["id","nome","marca","categoria","ano","preco","preco_medio","km_por_litro_cidade","km_por_litro_estrada","potencia_cv","cilindradas","portas","lugares","tipo_combustivel","cambio","cor","km_medio"])
    writer.writerows(rows)

print(f"Gerados {len(rows)} veículos!")
