# CHANGELOG - SAEV Dashboard

## [2.1.0] - 2025-07-24

### 🎯 Nova Funcionalidade Principal

#### Processamento Automático de Múltiplos Arquivos CSV
- **Pasta fixa**: Todos os arquivos CSV em `data/raw/` são processados automaticamente
- **Simplificação de uso**: Não é mais necessário especificar arquivos individuais
- **Processamento sequencial**: Arquivos são carregados em ordem alfabética
- **Consolidação**: Todos os dados são combinados em um único banco otimizado

### 📝 Mudanças nos Scripts

#### Script de Produção (`carga.py`)
**Antes:**
```bash
python carga.py arquivo.csv [banco.db]
```

**Agora:**
```bash
python carga.py [banco.db]
```

#### Script de Teste (`carga_teste.py`)
**Antes:**
```bash
python carga_teste.py arquivo.csv cidade_teste.txt [banco.db]
```

**Agora:**
```bash
python carga_teste.py cidade_teste.txt [banco.db]
```

### 🚀 Melhorias Implementadas

#### Módulo ETL Aprimorado
- **Novo método**: `load_csv_data()` com suporte a `csv_folder`
- **Compatibilidade**: Mantém suporte a arquivo único (`csv_path`)
- **Logs detalhados**: Mostra progresso de cada arquivo processado
- **Consolidação inteligente**: Combina DataFrames com otimização de memória

#### Interface de Usuário
- **Mensagens informativas**: Lista todos os arquivos que serão processados
- **Validação aprimorada**: Verifica existência da pasta e arquivos CSV
- **Feedback em tempo real**: Progresso de cada arquivo durante o carregamento

#### Performance
- **Processamento batch**: Carrega todos os arquivos antes de aplicar filtros
- **Otimização de memória**: Usa pandas para concatenação eficiente
- **Logs estruturados**: Contadores detalhados por arquivo e total

### 📊 Exemplo de Execução

```
📁 Pasta de origem: data/raw
📄 Arquivos encontrados: 5
   • es_1_serie.csv
   • es_2_serie.csv
   • es_3_serie.csv
   • es_4_serie.csv
   • es_5_serie.csv

📥 Carregando: es_1_serie.csv
   📊 2,235,036 registros em es_1_serie.csv
📥 Carregando: es_2_serie.csv
   📊 3,650,432 registros em es_2_serie.csv
...
📄 Total combinado: 16,739,644 registros
✅ Dados carregados com sucesso: 137,578 registros
```

### 🔧 Compatibilidade

#### Mantida
- ✅ Suporte a arquivo único (modo legado)
- ✅ Todas as funcionalidades de anonimização
- ✅ Star Schema automático
- ✅ Validação de dados

#### Nova
- 🆕 Processamento automático de pasta
- 🆕 Consolidação de múltiplos arquivos
- 🆕 Interface simplificada
- 🆕 Logs detalhados por arquivo

---

## [2.0.0] - 2025-07-24

### 🎯 Melhorias Principais

#### ETL Integrado com Star Schema
- **Processo automatizado**: ETL + Star Schema executados em uma única operação
- **Scripts reformulados**: `carga.py` e `carga_teste.py` com nova arquitetura modular
- **Logs detalhados**: Acompanhamento completo de cada etapa do processo
- **Validação automática**: Verificação de integridade e estatísticas dos dados
- **Sobrescrita controlada**: Recriação segura de bancos existentes

#### Star Schema Otimizado
- **Aplicação automática**: Transformação integrada ao processo de carga padrão
- **Script utilitário**: `apply_star_schema.py` para aplicação em bancos existentes
- **Performance validada**: Melhorias de 10-100x em consultas de BI
- **Documentação completa**: Guias detalhados e exemplos práticos

#### Segurança e Conformidade
- **Anonimização MD5**: Proteção de dados sensíveis no ambiente de teste
- **Filtragem por município**: Controle granular dos dados de teste
- **Confirmações de segurança**: Proteção contra execução acidental em produção

### 📁 Arquivos Modificados

#### Novos Arquivos
- `apply_star_schema.py` - Utilitário para aplicar Star Schema em bancos existentes

#### Arquivos Reformulados
- `src/data/etl.py` - Módulo ETL integrado com Star Schema
- `carga.py` - Script de carga para produção com nova arquitetura
- `carga_teste.py` - Script de carga para teste com anonimização integrada

#### Documentação Atualizada
- `README.md` - Documentação completa do novo processo ETL e Star Schema

### 🚀 Novos Recursos

#### Classe SAEVDataProcessor
- `create_database_structure(overwrite=False)` - Criação controlada de estrutura
- `load_csv_data(csv_path, test_mode=False, allowed_cities=None)` - Carga inteligente de dados
- `apply_star_schema()` - Aplicação da transformação Star Schema
- `validate_data()` - Validação completa de qualidade dos dados
- `full_etl_process()` - Processo completo integrado

#### Scripts de Linha de Comando
- Mensagens coloridas e informativas
- Confirmações de segurança para produção
- Validação de arquivos e parâmetros
- Logs estruturados com emojis

### 🔧 Melhorias Técnicas

#### Performance
- Índices otimizados criados automaticamente
- Transformação Star Schema com performance 10-100x melhor
- Queries de validação otimizadas

#### Robustez
- Tratamento de erros abrangente
- Validação de integridade de dados
- Logs detalhados para debugging
- Confirmações de segurança

#### Usabilidade
- Interface de linha de comando amigável
- Documentação completa com exemplos
- Processo automatizado end-to-end
- Mensagens de status claras

### 📊 Compatibilidade

#### Mantida
- ✅ Estrutura da tabela `avaliacao` inalterada
- ✅ Compatibilidade com dados existentes
- ✅ Interface dos scripts mantida (com melhorias)
- ✅ Funcionalidades do dashboard preservadas

#### Nova
- ⭐ Tabelas Star Schema (`dim_*` e `fato_*`)
- 🔧 Módulo ETL integrado
- 📊 Consultas otimizadas disponíveis
- 🚀 Processo automatizado

### 🧪 Validação

#### Testes Realizados
- ✅ Carregamento de módulos Python
- ✅ Criação de estrutura de banco
- ✅ Validação de scripts de linha de comando
- ✅ Aplicação do Star Schema
- ✅ Compatibilidade com dados existentes

#### Performance
- ✅ Transformação Star Schema: ~1.5s para ~100k registros
- ✅ Consultas agregadas: Melhoria de 10-100x
- ✅ Validação de dados: <1s para conjuntos típicos

---

**Nota**: Esta versão mantém total compatibilidade com dados e processos existentes, adicionando melhorias significativas de performance e usabilidade.
