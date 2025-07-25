# Microdados no formato CSV

Nesta pasta você pode adicionar todos os arquivos extraídos do SAEV no formato de microdados (CSV):  

1) primeira linha contém os nomes dos campos (colunas: "MUN_UF","MUN_NOME","ESC_INEP","ESC_NOME","SER_NUMBER","SER_NOME","TUR_PERIODO","TUR_NOME","ALU_ID","ALU_NOME","ALU_CPF","AVA_NOME","AVA_ANO","DIS_NOME","TES_NOME","TEG_ORDEM","ATR_RESPOSTA","ATR_CERTO","MTI_CODIGO","MTI_DESCRITOR");
2) O separador de coluna utilizado é a ","; 
3) o delimitador de campos texto é o caractere  "aspas duplas" ("); Contudo, alguns campos texto no arquivo csv não possuem este delimitador (isso não é um problema para o ETL).


## Carga completa dos dados

```bash

python carga.py 

```


## Carga de teste (somente alguns muncípio e com criptografia) dos dados

```bash

python carga_teste.py cidade_teste.txt

```