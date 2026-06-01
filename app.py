import os
import numpy as np
import pandas as pd
from flask import Flask, render_template, request, jsonify
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import json

app = Flask(__name__)
app.secret_key = 'automatch-super-secret-key-2024'

DATA_PATH = os.path.join(os.path.dirname(__file__), 'dataset', 'vehicles.csv')

def carregar_dados():
    df = pd.read_csv(DATA_PATH, sep=',', encoding='utf-8')
    return df

def tratar_dados(df):
    cols_numericas = ['ano', 'preco', 'km_por_litro_cidade', 'km_por_litro_estrada',
                      'potencia_cv', 'cilindradas', 'portas', 'lugares']
    for col in cols_numericas:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    df = df.fillna({
        'km_por_litro_cidade': df['km_por_litro_cidade'].median(),
        'km_por_litro_estrada': df['km_por_litro_estrada'].median(),
        'potencia_cv': df['potencia_cv'].median(),
        'preco': df['preco'].median()
    })
    return df

def aplicar_clusterizacao(df, n_clusters=5):
    features_cluster = ['preco', 'ano', 'km_por_litro_cidade', 'potencia_cv', 'cilindradas']
    X = df[features_cluster].copy()
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    df['cluster_id'] = kmeans.fit_predict(X_scaled)
    centros = scaler.inverse_transform(kmeans.cluster_centers_)
    resumo = []
    for i in range(n_clusters):
        cluster_df = df[df['cluster_id'] == i]
        resumo.append({
            'cluster_id': int(i),
            'count': len(cluster_df),
            'preco_medio': round(cluster_df['preco'].mean(), 2),
            'ano_medio': round(cluster_df['ano'].mean(), 1),
            'consumo_medio': round(cluster_df['km_por_litro_cidade'].mean(), 2),
            'potencia_media': round(cluster_df['potencia_cv'].mean(), 1),
            'principais_marcas': cluster_df['marca'].value_counts().head(3).to_dict(),
            'principais_categorias': cluster_df['categoria'].value_counts().head(3).to_dict()
        })
    return df, kmeans, scaler, resumo, X_scaled

def calcular_score_compatibilidade(df, preferencias):
    scores = []
    for _, row in df.iterrows():
        score = 0
        pesos = {
            'preco': float(preferencias.get('peso_preco', 5)),
            'consumo': float(preferencias.get('peso_consumo', 5)),
            'potencia': float(preferencias.get('peso_potencia', 5)),
            'ano': float(preferencias.get('peso_ano', 3))
        }
        total_peso = sum(pesos.values())
        if total_peso == 0:
            total_peso = 1
        preco_pref_min = float(preferencias.get('preco_min', 0))
        preco_pref_max = float(preferencias.get('preco_max', 500000))
        preco_ideal = (preco_pref_min + preco_pref_max) / 2 if preco_pref_max > preco_pref_min else preco_pref_max
        faixa_preco = max(1, preco_pref_max - preco_pref_min)
        dist_preco = abs(row['preco'] - preco_ideal) / faixa_preco
        score_preco = max(0, 10 - dist_preco * 10)
        if 'preco_min' in preferencias and row['preco'] < preco_pref_min:
            score_preco *= 0.5
        if 'preco_max' in preferencias and row['preco'] > preco_pref_max:
            score_preco *= 0.5
        score += score_preco * (pesos['preco'] / total_peso)
        consumo_max = df['km_por_litro_cidade'].max()
        if consumo_max > 0:
            score_consumo = (row['km_por_litro_cidade'] / consumo_max) * 10
        else:
            score_consumo = 5
        score += score_consumo * (pesos['consumo'] / total_peso)
        potencia_max = df['potencia_cv'].max()
        if potencia_max > 0:
            score_potencia = (row['potencia_cv'] / potencia_max) * 10
        else:
            score_potencia = 5
        score += score_potencia * (pesos['potencia'] / total_peso)
        if 'ano_min' in preferencias and row['ano'] < float(preferencias['ano_min']):
            score *= 0.6
        if 'ano_max' in preferencias and row['ano'] > float(preferencias['ano_max']):
            score *= 0.7
        if 'categoria' in preferencias and preferencias['categoria']:
            cats_pref = [c.strip() for c in preferencias['categoria'].split(',')]
            if row['categoria'] not in cats_pref:
                score = 0
        if 'marca' in preferencias and preferencias['marca']:
            marcas_pref = [m.strip() for m in preferencias['marca'].split(',')]
            if row['marca'] not in marcas_pref:
                score = 0
        if 'combustivel' in preferencias and preferencias['combustivel']:
            if row['tipo_combustivel'] != preferencias['combustivel']:
                score = 0
        if 'cambio' in preferencias and preferencias['cambio']:
            if row['cambio'] != preferencias['cambio']:
                score = 0
        score_final = round(score * 10, 2)
        scores.append({
            'veiculo_id': int(row['id']),
            'nome': row['nome'],
            'marca': row['marca'],
            'categoria': row['categoria'],
            'ano': int(row['ano']),
            'preco': float(row['preco']),
            'km_por_litro_cidade': float(row['km_por_litro_cidade']),
            'km_por_litro_estrada': float(row['km_por_litro_estrada']),
            'potencia_cv': int(row['potencia_cv']),
            'cilindradas': int(row['cilindradas']),
            'tipo_combustivel': row['tipo_combustivel'],
            'cambio': row['cambio'],
            'cor': row['cor'],
            'km_medio': int(row['km_medio']),
            'fonte_preco': row.get('fonte_preco', 'Tabela FIPE'),
            'fonte_especificacoes': row.get('fonte_especificacoes', 'Fabricante / INMETRO'),
            'cluster_id': int(row['cluster_id']) if pd.notna(row.get('cluster_id')) else None,
            'score': score_final
        })
    scores.sort(key=lambda x: x['score'], reverse=True)
    return scores

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recomendar', methods=['POST'])
def recomendar():
    data = request.get_json()
    if not data:
        return jsonify({'erro': 'Dados inválidos'}), 400
    preferencias = data
    df = carregar_dados()
    df = tratar_dados(df)
    df, kmeans, scaler, resumo_clusters, X_scaled = aplicar_clusterizacao(df)
    resultados = calcular_score_compatibilidade(df, preferencias)
    resultados = [r for r in resultados if r['score'] > 0]
    top_n = min(int(preferencias.get('top_n', 20)), len(resultados))
    top_resultados = resultados[:top_n]
    veiculos_semelhantes = {}
    for r in top_resultados[:5]:
        if r['cluster_id'] is not None:
            cluster_id = r['cluster_id']
            similares = [v for v in resultados if v['cluster_id'] == cluster_id and v['veiculo_id'] != r['veiculo_id']]
            veiculos_semelhantes[r['veiculo_id']] = [s['veiculo_id'] for s in similares[:3]]
    stats = {
        'total_analisados': len(df),
        'num_clusters': len(resumo_clusters),
        'preco_medio_dataset': float(df['preco'].mean()),
        'consumo_medio_dataset': float(df['km_por_litro_cidade'].mean()),
        'potencia_media_dataset': float(df['potencia_cv'].mean()),
        'clusters_resumo': resumo_clusters,
        'score_min': min(r['score'] for r in top_resultados) if top_resultados else 0,
        'score_max': max(r['score'] for r in top_resultados) if top_resultados else 0,
        'score_medio': round(np.mean([r['score'] for r in top_resultados]), 2) if top_resultados else 0
    }
    return jsonify({
        'resultados': top_resultados,
        'stats': stats,
        'veiculos_semelhantes': veiculos_semelhantes
    })

@app.route('/api/veiculos')
def api_veiculos():
    df = carregar_dados()
    df = tratar_dados(df)
    return jsonify(json.loads(df.to_json(orient='records')))

@app.route('/api/marcas')
def api_marcas():
    df = carregar_dados()
    marcas = sorted(df['marca'].unique().tolist())
    return jsonify(marcas)

@app.route('/api/categorias')
def api_categorias():
    df = carregar_dados()
    categorias = sorted(df['categoria'].unique().tolist())
    return jsonify(categorias)

@app.route('/api/clusters')
def api_clusters():
    df = carregar_dados()
    df = tratar_dados(df)
    df, kmeans, scaler, resumo_clusters, X_scaled = aplicar_clusterizacao(df)
    return jsonify(resumo_clusters)

@app.route('/api/dashboard')
def api_dashboard():
    df = carregar_dados()
    df = tratar_dados(df)
    df, kmeans, scaler, resumo_clusters, X_scaled = aplicar_clusterizacao(df)
    dados = {
        'total_veiculos': len(df),
        'total_marcas': df['marca'].nunique(),
        'total_categorias': df['categoria'].nunique(),
        'preco_medio': round(float(df['preco'].mean()), 2),
        'preco_min': float(df['preco'].min()),
        'preco_max': float(df['preco'].max()),
        'consumo_medio': round(float(df['km_por_litro_cidade'].mean()), 2),
        'potencia_media': round(float(df['potencia_cv'].mean()), 1),
        'ano_medio': round(float(df['ano'].mean()), 1),
        'distribuicao_categoria': df['categoria'].value_counts().to_dict(),
        'distribuicao_marca': df['marca'].value_counts().head(10).to_dict(),
        'distribuicao_combustivel': df['tipo_combustivel'].value_counts().to_dict(),
        'clusters_resumo': resumo_clusters,
        'veiculos_por_ano': df['ano'].value_counts().sort_index().to_dict()
    }
    return jsonify(dados)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
