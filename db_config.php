<?php
// ============================================
// AutoMatch - Conexão com Banco de Dados
// Ajuste as credenciais conforme seu ambiente
// ============================================

define('DB_HOST', 'localhost');
define('DB_USER', 'root');
define('DB_PASS', '');
define('DB_NAME', 'automatch');

function getConnection() {
    try {
        $conn = new mysqli(DB_HOST, DB_USER, DB_PASS, DB_NAME, DB_PORT);
        if ($conn->connect_error) {
            throw new Exception("Falha na conexão: " . $conn->connect_error);
        }
        $conn->set_charset("utf8mb4");
        return $conn;
    } catch (Exception $e) {
        die("Erro de conexão: " . $e->getMessage());
    }
}

// ============================================
// Funções auxiliares para o recomendador
// ============================================

function getVeiculos($conn, $filtros = []) {
    $sql = "SELECT * FROM veiculos WHERE 1=1";
    $params = [];
    $types = "";

    if (!empty($filtros['preco_min'])) {
        $sql .= " AND preco >= ?";
        $params[] = $filtros['preco_min'];
        $types .= "d";
    }
    if (!empty($filtros['preco_max'])) {
        $sql .= " AND preco <= ?";
        $params[] = $filtros['preco_max'];
        $types .= "d";
    }
    if (!empty($filtros['categoria'])) {
        $sql .= " AND categoria = ?";
        $params[] = $filtros['categoria'];
        $types .= "s";
    }
    if (!empty($filtros['ano_min'])) {
        $sql .= " AND ano >= ?";
        $params[] = $filtros['ano_min'];
        $types .= "i";
    }
    if (!empty($filtros['marca'])) {
        $sql .= " AND marca = ?";
        $params[] = $filtros['marca'];
        $types .= "s";
    }

    $sql .= " ORDER BY score_total DESC LIMIT 50";

    $stmt = $conn->prepare($sql);
    if ($params) {
        $stmt->bind_param($types, ...$params);
    }
    $stmt->execute();
    return $stmt->get_result()->fetch_all(MYSQLI_ASSOC);
}

function calcularScore($veiculo, $preferencias) {
    $score = 0;
    $pesos = [
        'preco' => $preferencias['prioridade_custo'] ?? 5,
        'consumo' => $preferencias['prioridade_economia'] ?? 5,
        'potencia' => $preferencias['prioridade_desempenho'] ?? 5
    ];
    $totalPeso = array_sum($pesos);
    if ($totalPeso == 0) $totalPeso = 1;

    // Score de preço (quanto menor, melhor)
    $precoMax = 500000;
    $scorePreco = max(0, (1 - ($veiculo['preco'] / $precoMax)) * 10);
    $score += $scorePreco * ($pesos['preco'] / $totalPeso);

    // Score de consumo
    $consumoMax = 60;
    $scoreConsumo = min(10, ($veiculo['km_por_litro_cidade'] / $consumoMax) * 10);
    $score += $scoreConsumo * ($pesos['consumo'] / $totalPeso);

    // Score de potência
    $potenciaMax = 400;
    $scorePotencia = min(10, ($veiculo['potencia_cv'] / $potenciaMax) * 10);
    $score += $scorePotencia * ($pesos['desempenho'] / $totalPeso);

    return round($score * 10, 2);
}
