# Oficina de IA

Este projeto visa desenvolver um projeto de BI utilizando o Copilot Github






## Mapa de extração de carga de dados

### Estruturas de dados


#### Tabela "avaliacao"


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
