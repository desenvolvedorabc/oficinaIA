
/*
================================================================================
STAR SCHEMA TRANSFORMATION FOR SAEV EDUCATIONAL ASSESSMENT DATA
================================================================================

OBJETIVO:
Transformar a tabela única 'avaliacao' (resultado do ETL) em um modelo 
Star Schema otimizado para análises de Business Intelligence.

ESTRUTURA CRIADA:
- 3 Tabelas de Dimensão: dim_aluno, dim_escola, dim_descritor
- 1 Tabela Fato: fato_resposta_aluno  
- 1 Tabela Auxiliar: teste (versão normalizada da tabela original)

BENEFÍCIOS:
- Consultas mais rápidas para dashboards e relatórios
- Modelo otimizado para ferramentas de BI
- Redução de redundância de dados
- Facilita análises agregadas e drill-down

AUTOR: SAEV Dashboard Project
DATA: 2025
VERSÃO: 1.0
================================================================================
*/

-- ============================================================================
-- ETAPA 1: LIMPEZA DE ESTRUTURAS EXISTENTES
-- ============================================================================
.print "🧹 Removendo tabelas fato e dimensão existentes..."

DROP TABLE IF EXISTS dim_aluno;
DROP TABLE IF EXISTS dim_escola; 
DROP TABLE IF EXISTS dim_descritor;
DROP TABLE IF EXISTS teste; 
DROP TABLE IF EXISTS fato_resposta_aluno;

-- Tabelas futuras (comentadas para referência)
-- DROP TABLE IF EXISTS resposta_escola;
-- DROP TABLE IF EXISTS resposta_municipio;   

-- ============================================================================
-- ETAPA 2: CRIAÇÃO DAS TABELAS DE DIMENSÃO
-- ============================================================================
.print "📊 Criando tabelas de dimensão..."

-- ----------------------------------------------------------------------------
-- DIMENSÃO ALUNO (dim_aluno)
-- Contém dados únicos de cada aluno
-- ----------------------------------------------------------------------------
.print "👤 Criando dimensão de alunos..."
CREATE TABLE dim_aluno (
    ALU_ID INTEGER PRIMARY KEY,    -- Chave primária - ID único do aluno
    ALU_NOME VARCHAR(60),          -- Nome do aluno (pode estar criptografado)
    ALU_CPF CHAR(11)               -- CPF do aluno (pode estar criptografado)
);

-- Popula a dimensão com alunos únicos
INSERT INTO dim_aluno (ALU_ID, ALU_NOME, ALU_CPF)  
SELECT DISTINCT ALU_ID, ALU_NOME, ALU_CPF 
FROM avaliacao; 

SELECT COUNT(*) FROM dim_aluno;
.print "✅ Dimensão aluno criada com sucesso!"

-- ----------------------------------------------------------------------------
-- DIMENSÃO ESCOLA (dim_escola)
-- Contém dados únicos de cada escola
-- ----------------------------------------------------------------------------
.print "🏫 Criando dimensão de escolas..."
CREATE TABLE dim_escola (
    ESC_INEP CHAR(8) PRIMARY KEY,  -- Chave primária - Código INEP da escola
    ESC_NOME VARCHAR(60)           -- Nome da escola (pode estar criptografado)
);

-- Popula a dimensão com escolas únicas
INSERT INTO dim_escola (ESC_INEP, ESC_NOME) 
SELECT DISTINCT ESC_INEP, ESC_NOME 
FROM avaliacao;

SELECT COUNT(*) FROM dim_escola;
.print "✅ Dimensão escola criada com sucesso!"

-- ----------------------------------------------------------------------------
-- DIMENSÃO DESCRITOR (dim_descritor)
-- Contém dados únicos de cada descritor/competência com estatísticas de uso
-- ----------------------------------------------------------------------------
.print "🎯 Criando dimensão de descritores..."
CREATE TABLE dim_descritor (
    MTI_CODIGO VARCHAR(15) PRIMARY KEY,  -- Chave primária - Código do descritor
    MTI_DESCRITOR VARCHAR(512),          -- Descrição completa do descritor
    QTD INTEGER                          -- Quantidade de questões usando este descritor
); 

-- Popula a dimensão com descritores únicos e suas estatísticas
-- Usa MAX() para pegar uma versão da descrição quando há variações
INSERT INTO dim_descritor (MTI_CODIGO, MTI_DESCRITOR, QTD) 
SELECT 
    MTI_CODIGO, 
    MAX(MTI_DESCRITOR) AS MTI_DESCRITOR,  -- Pega uma versão da descrição
    COUNT(*) AS QTD 
FROM avaliacao 
GROUP BY MTI_CODIGO;

SELECT COUNT(*) FROM dim_descritor;
.print "✅ Dimensão descritor criada com sucesso!"

-- ============================================================================
-- ETAPA 3: CRIAÇÃO DA TABELA AUXILIAR NORMALIZADA
-- ============================================================================
.print "📋 Criando tabela auxiliar 'teste'..."

-- ----------------------------------------------------------------------------
-- TABELA TESTE (auxiliar)
-- Versão normalizada da tabela original sem redundâncias de dimensões
-- Mantém apenas as chaves estrangeiras para as dimensões
-- ----------------------------------------------------------------------------
CREATE TABLE teste (
    MUN_UF         CHAR(2),              -- SIGLA DA UNIDADE DA FEDERAÇÃO
    MUN_NOME       VARCHAR(60),          -- NOME DO MUNICÍPIO
    ESC_INEP       CHAR(8),              -- FK para dim_escola - CÓDIGO INEP DA ESCOLA
    SER_NUMBER     INTEGER,              -- NÚMERO DO ANO/SÉRIE
    SER_NOME       VARCHAR(30),          -- NOME DA SÉRIE
    TUR_PERIODO    VARCHAR(15),          -- TURNO DE ATIVIDADE (Manhã, Tarde)
    TUR_NOME       VARCHAR(20),          -- NOME DO TURNO
    ALU_ID         INTEGER,              -- FK para dim_aluno - IDENTIFICAÇÃO DO ALUNO
    ALU_CPF        VARCHAR(15),          -- CPF DO ALUNO (redundante, para compatibilidade)
    AVA_NOME       VARCHAR(50),          -- NOME DA AVALIAÇÃO
    AVA_ANO        INTEGER,              -- ANO DA AVALIAÇÃO
    DIS_NOME       VARCHAR(30),          -- NOME DA DISCIPLINA
    TES_NOME       VARCHAR(30),          -- NOME DO TESTE
    TEG_ORDEM      INTEGER,              -- ORDEM DA QUESTÃO DO TESTE
    ATR_RESPOSTA   CHAR(1),              -- RESPOSTA DO ALUNO NA QUESTÃO
    ATR_CERTO      INTEGER,              -- SE 1 ACERTOU, SE 0 ERROU
    MTI_CODIGO     VARCHAR(15)           -- FK para dim_descritor - CÓDIGO DO DESCRITOR
);

-- Popula a tabela teste com dados normalizados (sem nomes de dimensões)
INSERT INTO teste (
    MUN_UF, MUN_NOME, ESC_INEP, SER_NUMBER, SER_NOME, TUR_PERIODO, TUR_NOME, 
    ALU_ID, ALU_CPF, AVA_NOME, AVA_ANO, DIS_NOME, TES_NOME, TEG_ORDEM, 
    ATR_RESPOSTA, ATR_CERTO, MTI_CODIGO
)
SELECT 
    MUN_UF, MUN_NOME, ESC_INEP, SER_NUMBER, SER_NOME, TUR_PERIODO, TUR_NOME, 
    ALU_ID, ALU_CPF, AVA_NOME, AVA_ANO, DIS_NOME, TES_NOME, TEG_ORDEM, 
    ATR_RESPOSTA, ATR_CERTO, MTI_CODIGO  
FROM avaliacao;

SELECT COUNT(*) FROM teste;
.print "✅ Tabela 'teste' (versão otimizada da fonte) criada e populada!"

-- ============================================================================
-- ETAPA 4: CRIAÇÃO DA TABELA FATO
-- ============================================================================
.print "⭐ Criando tabela fato principal..."

-- ----------------------------------------------------------------------------
-- TABELA FATO: fato_resposta_aluno
-- Agregação por aluno, descritor e contexto, com métricas de acerto/erro
-- É o coração do Star Schema - onde ficam as métricas de negócio
-- ----------------------------------------------------------------------------
CREATE TABLE fato_resposta_aluno AS 
SELECT 
    -- Dimensões geográficas e administrativas
    MUN_UF,           -- Unidade da Federação
    MUN_NOME,         -- Nome do Município
    ESC_INEP,         -- Código da Escola (FK para dim_escola)
    
    -- Dimensões educacionais
    SER_NUMBER,       -- Número da Série
    SER_NOME,         -- Nome da Série
    TUR_PERIODO,      -- Período do Turno
    TUR_NOME,         -- Nome do Turno
    
    -- Dimensão do aluno
    ALU_ID,           -- ID do Aluno (FK para dim_aluno)
    
    -- Dimensões de avaliação
    AVA_NOME,         -- Nome da Avaliação
    AVA_ANO,          -- Ano da Avaliação
    DIS_NOME,         -- Disciplina
    TES_NOME,         -- Nome do Teste
    MTI_CODIGO,       -- Código do Descritor (FK para dim_descritor)
    
    -- MÉTRICAS DE NEGÓCIO (Fatos)
    SUM(CASE WHEN ATR_CERTO = 1 THEN 1 ELSE 0 END) AS ACERTO,  -- Total de acertos
    SUM(CASE WHEN ATR_CERTO = 0 THEN 1 ELSE 0 END) AS ERRO     -- Total de erros
FROM teste
GROUP BY 
    MUN_UF, MUN_NOME, ESC_INEP, SER_NUMBER, SER_NOME, 
    TUR_PERIODO, TUR_NOME, ALU_ID, AVA_NOME, AVA_ANO, 
    DIS_NOME, TES_NOME, MTI_CODIGO;

create index idx_fato_resposta_aluno ON fato_resposta_aluno (AVA_ANO,MUN_UF, MUN_NOME, ESC_INEP, DIS_NOME);

.print "📊 Tabela fato_resposta_aluno criada com agregações de métricas!"


SELECT COUNT(*) FROM fato_resposta_aluno;
.print "✅ Tabela fato_resposta_aluno criada e populada com sucesso!"

-- ============================================================================
-- ETAPA 5: OTIMIZAÇÃO FINAL
-- ============================================================================
.print "🚀 Finalizando otimização..."

-- Comentado para preservar dados originais durante desenvolvimento
DROP TABLE avaliacao;

.print "🎉 Otimização de tabelas concluída - STAR SCHEMA criado com sucesso!"
.print ""
.print "📊 ESTRUTURA FINAL DO STAR SCHEMA:"
.print "   - dim_aluno:           Dimensão de alunos únicos"
.print "   - dim_escola:          Dimensão de escolas únicas"  
.print "   - dim_descritor:       Dimensão de descritores com estatísticas"
.print "   - fato_resposta_aluno: Tabela fato com métricas agregadas"
.print "   - teste:               Tabela auxiliar normalizada"
.print ""
.print "✨ Pronto para análises de BI de alta performance!"

-- Compacta o banco de dados removendo espaços não utilizados
VACUUM;
