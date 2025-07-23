# Oficina de IA

Este projeto visa desenvolver um projeto de BI utilizando o Copilot Github


## Artefatos e Tecnologias Envolvidas

* Python 
* Streamlit: Utilizado para fazer a apresentação dos painéis entre outras funções;
* SQLite3: SGBD local utilizado para armazenar os dados tratados pelo processo de carga
* Aquivos csv (microdados do sistema SAEV): Arquivo no formato csv cuja primeira linha contém os nomes dos campos (colunas: "MUN_UF","MUN_NOME","ESC_INEP","ESC_NOME","SER_NUMBER","SER_NOME","TUR_PERIODO","TUR_NOME","ALU_ID","ALU_NOME","ALU_CPF","AVA_NOME","AVA_ANO","DIS_NOME","TES_NOME","TEG_ORDEM","ATR_RESPOSTA","ATR_CERTO","MTI_CODIGO","MTI_DESCRITOR"); O separador de coluna utilizado é a ","; o delimitador de campos texto é o caractere  "aspas duplas" ("); Contudo, alguns campos texto no arquivo não possuem este delimitador. 
* Script python carga.py: Executar o processo de carga dos arquivos de origem (CSVs) para a tabela avaliacao do banco de dados avaliacao_prod.db;
* Script python carga_teste.py: Executar o processo de carga dos arquivos de origem (CSVs) para a tabela avaliacao do banco de dados avaliacao_teste.db. Este processo carrega somente dados de alguns minicípios e ofisca dados sensíveis para evitar identificação de alunos, escolas e municípios. 


#### Dicionário da tabela  "avaliacao" 

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

##### DDL para criação da tabela no banco de dados SQLite (avaliacao_prod.db e avaliacao_teste.db)

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
    ALU_ID         INTEGER,              -- IDENTIFICAÇÃO DO ALUNO (usei INTEGER pois LONG não existe no SQLite)
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
````


