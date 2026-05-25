-- ============================================
-- AutoMatch - Sistema de Recomendação de Veículos
-- Script SQL para criação do banco de dados
-- Execute este script no phpMyAdmin ou MySQL CLI
-- ============================================

CREATE DATABASE IF NOT EXISTS automatch;
USE automatch;

-- Tabela de veículos
CREATE TABLE IF NOT EXISTS veiculos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    marca VARCHAR(50) NOT NULL,
    categoria VARCHAR(50) NOT NULL,
    ano INT NOT NULL,
    preco DECIMAL(10,2) NOT NULL,
    preco_medio DECIMAL(10,2) NOT NULL,
    km_por_litro_cidade DECIMAL(4,1) NOT NULL,
    km_por_litro_estrada DECIMAL(4,1) NOT NULL,
    potencia_cv INT NOT NULL,
    cilindradas INT NOT NULL,
    portas INT NOT NULL DEFAULT 4,
    lugares INT NOT NULL DEFAULT 5,
    tipo_combustivel VARCHAR(30) NOT NULL,
    cambio VARCHAR(30) NOT NULL,
    cor VARCHAR(30) NOT NULL DEFAULT 'branco',
    km_medio INT NOT NULL DEFAULT 0,
    cluster_id INT DEFAULT NULL,
    score_total DECIMAL(5,2) DEFAULT NULL,
    data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_categoria (categoria),
    INDEX idx_marca (marca),
    INDEX idx_ano (ano),
    INDEX idx_preco (preco),
    INDEX idx_cluster (cluster_id)
);

-- Tabela para preferências dos usuários
CREATE TABLE IF NOT EXISTS preferencias_usuario (
    id INT AUTO_INCREMENT PRIMARY KEY,
    session_id VARCHAR(64) NOT NULL,
    preco_min DECIMAL(10,2) DEFAULT NULL,
    preco_max DECIMAL(10,2) DEFAULT NULL,
    ano_min INT DEFAULT NULL,
    ano_max INT DEFAULT NULL,
    categoria_preferida VARCHAR(50) DEFAULT NULL,
    marca_preferida VARCHAR(50) DEFAULT NULL,
    tipo_combustivel VARCHAR(30) DEFAULT NULL,
    cambio_preferido VARCHAR(30) DEFAULT NULL,
    potencia_min INT DEFAULT NULL,
    consumo_min DECIMAL(4,1) DEFAULT NULL,
    prioridade_economia INT DEFAULT 5,
    prioridade_desempenho INT DEFAULT 5,
    prioridade_custo INT DEFAULT 5,
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_session (session_id)
);

-- Tabela para recomendações geradas
CREATE TABLE IF NOT EXISTS recomendacoes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    session_id VARCHAR(64) NOT NULL,
    veiculo_id INT NOT NULL,
    score DECIMAL(5,2) NOT NULL,
    cluster_id INT DEFAULT NULL,
    distancia_cluster DECIMAL(10,4) DEFAULT NULL,
    data_recomendacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (veiculo_id) REFERENCES veiculos(id) ON DELETE CASCADE,
    INDEX idx_session_recom (session_id)
);

-- View: veículos com score calculado
CREATE VIEW vw_veiculos_score AS
SELECT 
    v.*,
    CASE 
        WHEN v.preco <= 50000 THEN 10
        WHEN v.preco <= 80000 THEN 8
        WHEN v.preco <= 120000 THEN 6
        WHEN v.preco <= 180000 THEN 4
        ELSE 2
    END AS score_preco,
    CASE 
        WHEN v.km_por_litro_cidade >= 13 THEN 10
        WHEN v.km_por_litro_cidade >= 10 THEN 8
        WHEN v.km_por_litro_cidade >= 8 THEN 6
        ELSE 4
    END AS score_consumo,
    CASE 
        WHEN v.potencia_cv >= 200 THEN 10
        WHEN v.potencia_cv >= 150 THEN 8
        WHEN v.potencia_cv >= 100 THEN 6
        WHEN v.potencia_cv >= 80 THEN 4
        ELSE 2
    END AS score_potencia
FROM veiculos v;
