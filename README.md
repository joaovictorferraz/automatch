# AutoMatch 🚗

Sistema de recomendação inteligente de veículos desenvolvido como projeto do **6º semestre** do curso de **Análise e Desenvolvimento de Sistemas**.

**Link para teste:** [https://automatch-29ds.onrender.com/](https://automatch-29ds.onrender.com/)

---

## Sobre o projeto

O AutoMatch é uma aplicação web que ajuda o usuário a encontrar o veículo ideal com base em suas preferências pessoais. Diferente de filtros tradicionais (onde você apenas seleciona marca/modelo), o AutoMatch calcula um **score de compatibilidade** entre o usuário e cada veículo do dataset, considerando múltiplos critérios simultaneamente.

Os preços são 100% reais obtidos da **Tabela FIPE** oficial via [api.fipe.online](https://fipe.online), garantindo que as recomendações reflitam o valor real de mercado dos veículos.

---

## Funcionalidades

### Recomendação inteligente (score)
O usuário informa suas preferências (faixa de preço, categorias, marcas, ano, prioridade para consumo, potência etc.) e o sistema calcula um **score de 0 a 100** para cada veículo, ordenando do mais ao menos compatível. O score leva em conta:

- **Aderência à faixa de preço** — quão próximo o veículo está do valor ideal do usuário
- **Consumo (km/l)** — prioridade configurável para economia de combustível
- **Potência (cv)** — prioridade configurável para desempenho
- **Ano de fabricação** — filtro por ano mínimo e máximo
- **Categoria** — Hatch, Sedan, SUV, Picape
- **Marca, combustível e câmbio** — filtros exatos

### Clusterização (K-Means)
Os veículos são agrupados em **5 clusters** com base em preço, ano, consumo, potência e cilindrada. O sistema sugere veículos similares aos que o usuário mais gostou, mesmo que estejam em posições diferentes no ranking.

### Dashboard / Estatísticas
- Total de veículos, marcas e categorias
- Preço médio, consumo médio, potência média
- Distribuição por marca, categoria e combustível
- Resumo de cada cluster

### API REST
Endpoints públicos disponíveis:
- `GET /api/veiculos` — lista completa de veículos
- `GET /api/marcas` — marcas disponíveis
- `GET /api/categorias` — categorias disponíveis
- `GET /api/clusters` — resumo dos clusters
- `GET /api/dashboard` — estatísticas gerais

---

## Dataset

- **400 veículos** com preços reais da Tabela FIPE (junho/2026)
- **10 marcas:** Fiat, Volkswagen, Chevrolet, Toyota, Honda, Hyundai, Renault, Jeep, Nissan, Ford
- **4 categorias:** Hatch, Sedan, SUV, Picape
- As especificações técnicas (potência, consumo, cilindrada, câmbio) são baseadas em dados reais de fábrica / INMETRO
- Fonte dos preços: `Tabela FIPE` via api.fipe.online
- Fonte das especificações: `Fabricante / INMETRO`

---

## Tecnologias utilizadas

| Tecnologia | Finalidade |
|---|---|
| **Python 3 / Flask** | Backend e API REST |
| **Pandas / NumPy** | Processamento e análise dos dados |
| **Scikit-learn** | Clusterização K-Means e escalonamento |
| **HTML / CSS / JavaScript** | Frontend responsivo |
| **Render** | Hospedagem (deploy contínuo via GitHub) |
| **Git / GitHub** | Versionamento |

---

## Como executar localmente

```bash
# Clone o repositório
git clone https://github.com/joaovictorferraz/automatch.git
cd automatch

# Crie um ambiente virtual
python -m venv venv
venv\Scripts\activate   # Windows
# source venv/bin/activate  # Linux/Mac

# Instale as dependências
pip install -r requirements.txt

# Execute a aplicação
python app.py
```

Acesse em [http://localhost:5000](http://localhost:5000).

---

## Scripts

- `scripts/gerar_dataset.py` — gera o dataset com preços da API FIPE (requer token de [fipe.online](https://fipe.online))
- `scripts/fipe_client.py` — cliente utilitário para consulta individual de preço FIPE

---

## Estrutura do projeto

```
automatch/
├── app.py                   # Aplicação Flask principal
├── wsgi.py                  # Ponto de entrada para produção (gunicorn)
├── requirements.txt         # Dependências
├── database.sql             # Schema do banco de dados (MySQL)
├── db_config.php            # Configuração de banco (legado)
├── dataset/
│   └── vehicles.csv         # Dataset com 400 veículos
├── scripts/
│   ├── gerar_dataset.py     # Gerador do dataset via API FIPE
│   └── fipe_client.py       # Cliente de consulta FIPE
└── templates/
    └── index.html           # Frontend da aplicação
```

---

## Licença

Projeto acadêmico sem fins comerciais.
