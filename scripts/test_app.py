import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Test by importing app module
import app as auto_app
app = auto_app.app

with app.test_client() as client:
    r = client.get("/api/dashboard")
    print(f"Status: {r.status_code}")
    d = r.get_json()
    print(f"Veiculos: {d['total_veiculos']}, Marcas: {d['total_marcas']}, Categorias: {d['total_categorias']}")
    print(f"Preco medio: R$ {d['preco_medio']}")
    
    r2 = client.post("/recomendar", json={
        "preco_min": 50000, "preco_max": 120000,
        "categoria": "SUV", "top_n": 5
    })
    print(f"Recomendar Status: {r2.status_code}")
    d2 = r2.get_json()
    print(f"Resultados: {len(d2['resultados'])}")
    for v in d2['resultados'][:3]:
        print(f"  {v['nome']} - R$ {v['preco']:.0f} - Score: {v['score']}")
    print("OK - Tudo funcionando!")
