# 📊 SAEV Dashboard - Sistema de Análise de Avaliações Educacionais

Este projeto desenvolve uma solução completa de Business Intelligence para análise de dados de avaliações diagnósticas aplicadas em escolas da rede municipal e estadual, utilizando tecnologias modernas e inteligência artificial.

## 🎯 Objetivos do Projeto

- **Visualização Interativa**: Dashboards dinâmicos para análise de desempenho educacional
- **Relatórios Automatizados**: Geração de relatórios detalhados em Excel
- **Análises Avançadas**: Clustering, análise de tendências e correlações
- **Monitoramento de Equidade**: Identificação de gaps educacionais
- **Interface Intuitiva**: Painel web responsivo e fácil de usar

## 🚀 Funcionalidades Principais

### 📈 Dashboard Interativo
- Visão geral de desempenho por município e escola
- Análise por competências e descritores
- Filtros dinâmicos por ano, disciplina, teste e série
- Gráficos interativos com Plotly

### 📋 Sistema de Relatórios
- Relatórios municipais comparativos
- Análise de desempenho por escola
- Relatórios de competências e descritores
- Análises comparativas entre anos
- Exportação automática para Excel

### 🔬 Análises Avançadas
- Clustering de escolas por perfil de desempenho
- Análise de equidade educacional
- Correlação entre competências
- Análise de tendências temporais
- Identificação de gaps entre séries

## 🛠️ Tecnologias Utilizadas

- **Python 3.8+**: Linguagem principal
- **Streamlit**: Framework para dashboard web
- **Plotly**: Visualizações interativas
- **Pandas**: Manipulação de dados
- **SQLite**: Banco de dados local
- **Scikit-learn**: Análises de machine learning
- **SciPy**: Análises estatísticas

## 📁 Estrutura do Projeto

```
oficinaIA/
├── README.md
├── requirements.txt
├── .env.example                   # Exemplo de configuração
├── run_dashboard.py              # Script principal Python
├── manage_env.py                 # Utilitário de gerenciamento
├── iniciar.sh                    # Script interativo com menu
├── iniciar_teste.sh              # Script para ambiente de teste
├── iniciar_prod.sh               # Script para ambiente de produção
├── carga.py                      # Script de carga original
├── carga_teste.py                # Script de carga para teste
├── data/
│   ├── raw/                      # Dados CSV originais
│   └── test/                     # Dados de teste
├── db/
│   ├── avaliacao_teste.db        # Banco de teste (pode estar no repo)
│   └── avaliacao_prod.db         # Banco de produção (não vai pro repo)
├── src/
│   ├── config.py                 # Configurações e gerenciamento de ambientes
│   ├── data/
│   │   └── etl.py               # Processos de ETL melhorados
│   ├── dashboard/
│   │   └── main.py              # Dashboard principal
│   ├── reports/
│   │   └── generator.py         # Gerador de relatórios
│   └── analytics/
│       └── advanced.py          # Análises estatísticas avançadas
├── reports/                      # Relatórios gerados
└── tests/                        # Testes unitários
```

## 🚀 Como Executar

### 1. Preparação do Ambiente

```bash
# Instalar dependências
pip install -r requirements.txt

# Ou criar ambiente virtual (recomendado)
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows

pip install -r requirements.txt
```

### 2. Carregar Dados

```bash
# Para dados de produção
python carga.py arquivo_dados.csv db/avaliacao_prod.db

# Para dados de teste (com ofuscação)
python carga_teste.py arquivo_dados.csv cidade_teste.txt db/avaliacao_teste.db
```

### 3. Gerenciar Ambientes

```bash
# Verificar status dos ambientes
python manage_env.py status

# Detectar ambiente atual
python manage_env.py detect

# Validar ambiente específico
python manage_env.py validate teste
python manage_env.py validate producao

# Configurar ambiente (criar estrutura se necessário)
python manage_env.py setup teste
python manage_env.py setup producao
```

### 4. Executar Dashboard

#### Métodos Simplificados (Scripts Shell)

```bash
# Script interativo com menu
./iniciar.sh

# Direto para ambiente de teste
./iniciar_teste.sh

# Direto para ambiente de produção (com confirmação)
./iniciar_prod.sh

# Com porta customizada
./iniciar_teste.sh 8502
./iniciar_prod.sh 8503
```

#### Método Avançado (Python)

```bash
# Detecção automática do ambiente
python run_dashboard.py

# Forçar ambiente de teste
python run_dashboard.py --env teste

# Forçar ambiente de produção
python run_dashboard.py --env producao

# Especificar porta customizada
python run_dashboard.py --port 8502

# Listar ambientes disponíveis
python run_dashboard.py --list

# Mostrar informações do ambiente
python run_dashboard.py --info

# Ou diretamente com Streamlit (detecta automaticamente)
streamlit run src/dashboard/main.py
```

### 5. Acessar a Aplicação

Abra seu navegador em: **http://localhost:8501** (ou a porta especificada)

## 🗃️ Gerenciamento de Ambientes

### Ambientes Disponíveis

| Ambiente | Descrição | Arquivo | Repositório |
|----------|-----------|---------|-------------|
| **teste** | Dados ofuscados com MD5 | `avaliacao_teste.db` | ✅ Permitido |
| **producao** | Dados reais sensíveis | `avaliacao_prod.db` | ❌ Não permitido |

### Detecção Automática

O sistema detecta automaticamente qual ambiente usar baseado em:

1. **Variável de ambiente** `SAEV_ENVIRONMENT` (teste/producao)
2. **Existência do banco de produção** - se existe, usa produção
3. **Fallback para teste** - caso contrário, usa teste

### Configuração por Variável de Ambiente

```bash
# Forçar ambiente de teste
export SAEV_ENVIRONMENT=teste
python run_dashboard.py

# Forçar ambiente de produção
export SAEV_ENVIRONMENT=producao
python run_dashboard.py
```

### Segurança

- 🔒 **Banco de produção**: Nunca incluído no repositório Git
- 🧪 **Banco de teste**: Dados ofuscados com MD5, seguro para repositório
- 🛡️ **Validação automática**: Sistema verifica integridade dos ambientes

## 🖥️ Scripts Shell Simplificados

Para facilitar o uso, foram criados scripts shell que automatizam a execução:

### 📋 Scripts Disponíveis

| Script | Descrição | Uso |
|--------|-----------|-----|
| `./iniciar.sh` | Menu interativo para escolher ambiente | `./iniciar.sh` |
| `./iniciar_teste.sh` | Execução direta do ambiente de teste | `./iniciar_teste.sh [porta]` |
| `./iniciar_prod.sh` | Execução direta do ambiente de produção | `./iniciar_prod.sh [porta]` |

### 🎯 Características dos Scripts

#### `iniciar_teste.sh`
- ✅ **Seguro**: Ambiente com dados ofuscados
- 🔧 **Auto-configuração**: Cria estrutura se necessário
- 🟢 **Sem confirmação**: Inicia diretamente
- 📁 **Banco**: `db/avaliacao_teste.db`

#### `iniciar_prod.sh`  
- ⚠️ **Cuidado**: Ambiente com dados reais
- 🔐 **Confirmação obrigatória**: Solicita confirmação antes de iniciar
- 🔍 **Validação rigorosa**: Verifica integridade antes da execução
- 📁 **Banco**: `db/avaliacao_prod.db`

#### `iniciar.sh`
- 🎨 **Interface amigável**: Menu colorido e interativo
- 📊 **Status em tempo real**: Mostra disponibilidade dos ambientes
- 🛠️ **Ferramentas**: Acesso rápido a configurações e validações
- 💡 **Ajuda integrada**: Explicações e exemplos de uso

### 🚀 Exemplos de Uso dos Scripts

```bash
# Menu interativo - escolha visual do ambiente
./iniciar.sh

# Teste rápido na porta padrão (8501)
./iniciar_teste.sh

# Teste em porta customizada
./iniciar_teste.sh 8502

# Produção com confirmação (porta padrão)
./iniciar_prod.sh

# Produção em porta específica
./iniciar_prod.sh 8503
```

## 📊 Estrutura dos Dados 

## 📊 Estrutura dos Dados

### Tabela "avaliacao"

A tabela a seguir apresenta a estrutura de dados da tabela avaliacao que armazena os microdados do sistema SAEV.

| Nome da Coluna  | Tipo de Dados  | Tamanho | Descrição |  
| ----------------| -------------- | ------- | --------- |
| MUN_UF          | CHAR(2)        |    2    | SIGLA DA UNIDADE DA FEDERAÇÃO |       
| MUN_NOME        | VARCHAR(60)    |   60    | NOME DO MUNICÍPIO |
| ESC_INEP        | CHAR(8)        |    8    | CÓDIGO INEP DA ESCOLA |
| ESC_NOME        | VARCHAR(80)    |   80    | NOME DA ESCOLA |
| SER_NUMBER      | INTEGER        |         | NÚMERO DO ANO/SÉRIE |
| SER_NOME        | VARCHAR(30)    |   30    | NOME DA SÉRIE |
| TUR_PERIODO     | VARCHAR(15)    |   15    | TURNO DE ATIVIDADE (Manhã, Tarde) |
| TUR_NOME        | VARCHAR(15)    |   20    | NOME DO TURNO |
| ALU_ID          | LONG           |         | IDENTIFICAÇÃO DO ALUNO |  
| ALU_NOME        | VARCHAR(80)    |   80    | NOME DO ALUNO |
| ALU_CPF         | VARCHAR(11)    |   15    | CPF DO ALUNO  |
| AVA_NOME        | VARCHAR(50)    |   50    | NOME DA AVALIAÇÃO |  
| AVA_ANO         | INTEGER        |         | ANO DA AVALIAÇÃO |
| DIS_NOME        | VARCHAR(30)    |   30    | NOME DA DISCIPLINA  |
| TES_NOME        | VARCHAR(30)    |   30    | NOME DO TESTE |
| TEG_ORDEM       | INTEGER        |         | ORDEM DA QUESTÃO DO TESTE |
| ATR_RESPOSTA    | CHAR(1)        |    1    | RESPOSTA DO ALUNO NA QUESTÃO |
| ATR_CERTO       | INTEGER        |         | SE 1 ACERTOU SE 0 ERROU |   
| MTI_CODIGO      | VARCHAR(15)    |   15    | CÓDIGO DO DESCRITOR |
| MTI_DESCRITOR   | VARCHAR(512)   |   512   | DESCRIÇÃO DO DESCRITOR | 

### DDL para criação da tabela

```sql
CREATE TABLE avaliacao (
    MUN_UF         CHAR(2),              -- SIGLA DA UNIDADE DA FEDERAÇÃO
    MUN_NOME       VARCHAR(60),          -- NOME DO MUNICÍPIO
    ESC_INEP       CHAR(8),              -- CÓDIGO INEP DA ESCOLA
    ESC_NOME       VARCHAR(80),          -- NOME DA ESCOLA
    SER_NUMBER     INTEGER,              -- NÚMERO DO ANO/SÉRIE
    SER_NOME       VARCHAR(30),          -- NOME DA SÉRIE
    TUR_PERIODO    VARCHAR(15),          -- TURNO DE ATIVIDADE (Manhã, Tarde)
    TUR_NOME       VARCHAR(20),          -- NOME DO TURNO
    ALU_ID         INTEGER,              -- IDENTIFICAÇÃO DO ALUNO
    ALU_NOME       VARCHAR(80),          -- NOME DO ALUNO
    ALU_CPF        VARCHAR(15),          -- CPF DO ALUNO
    AVA_NOME       VARCHAR(50),          -- NOME DA AVALIAÇÃO
    AVA_ANO        INTEGER,              -- ANO DA AVALIAÇÃO
    DIS_NOME       VARCHAR(30),          -- NOME DA DISCIPLINA
    TES_NOME       VARCHAR(30),          -- NOME DO TESTE
    TEG_ORDEM      INTEGER,              -- ORDEM DA QUESTÃO DO TESTE
    ATR_RESPOSTA   CHAR(1),              -- RESPOSTA DO ALUNO NA QUESTÃO
    ATR_CERTO      INTEGER,              -- SE 1 ACERTOU, SE 0 ERROU
    MTI_CODIGO     VARCHAR(15),          -- CÓDIGO DO DESCRITOR
    MTI_DESCRITOR  VARCHAR(512)          -- DESCRIÇÃO DO DESCRITOR
);

-- Índices para melhor performance
CREATE INDEX idx_municipio ON avaliacao(MUN_NOME);
CREATE INDEX idx_escola ON avaliacao(ESC_INEP);
CREATE INDEX idx_avaliacao_ano ON avaliacao(AVA_ANO);
CREATE INDEX idx_disciplina ON avaliacao(DIS_NOME);
CREATE INDEX idx_serie ON avaliacao(SER_NUMBER);
CREATE INDEX idx_serie_nome ON avaliacao(SER_NOME);
CREATE INDEX idx_teste_nome ON avaliacao(TES_NOME);
```

## 📈 Exemplos de Uso

### Gerar Relatório Municipal
```python
from src.reports.generator import SAEVReports

reports = SAEVReports("db/avaliacao_teste.db")
arquivo = reports.generate_municipal_report(2023, "Matemática")
print(f"Relatório gerado: {arquivo}")
```

### Análise de Clustering
```python
from src.analytics.advanced import SAEVAnalytics

analytics = SAEVAnalytics("db/avaliacao_teste.db")
resultado = analytics.school_clustering(2023, "Português")
print(f"Identificados {resultado['n_clusters']} grupos de escolas")
```

## 🔄 Próximos Passos

### Melhorias Técnicas
- [ ] Implementar cache para consultas frequentes
- [ ] Adicionar testes unitários abrangentes
- [ ] Configurar CI/CD pipeline
- [ ] Implementar logging estruturado
- [ ] Adicionar validação de dados

### Funcionalidades Futuras
- [ ] API REST para integração externa
- [ ] Sistema de alertas automáticos
- [ ] Análise preditiva de desempenho
- [ ] Integração com outros sistemas educacionais
- [ ] Dashboard mobile-friendly

### Análises Avançadas
- [ ] Análise de redes sociais (correlação entre escolas)
- [ ] Modelos preditivos de desempenho
- [ ] Análise de séries temporais
- [ ] Identificação de outliers automática

## 🤝 Contribuição

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 👥 Equipe

- **Desenvolvedor Principal**: Utilizando GitHub Copilot para IA-assisted development
- **Tecnologias**: Python, Streamlit, Plotly, SQLite
- **Metodologia**: Desenvolvimento orientado por dados

---

**Desenvolvido com ❤️ e inteligência artificial para melhorar a educação brasileira.**


