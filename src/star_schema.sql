create table aluno ( ALU_ID integer primary KEY , ALU_NOME varchar(60), ALU_CPF char(11) );

insert into aluno (ALU_ID, ALU_NOME, ALU_CPF )  select distinct a.ALU_ID, a.ALU_NOME, a.ALU_CPF from  avaliacao a; 

select count(*) from aluno;


create table escola ( ESC_INEP CHAR(8) primary key, ESC_NOME varchar (60) );

insert into escola (ESC_INEP, ESC_NOME) select distinct ESC_INEP, ESC_NOME from  avaliacao;

select count(*) from escola;


create table descritor ( MTI_CODIGO varchar(15) primary key, MTI_DESCRITOR varchar(512), QTD integer); 

insert into descritor (MTI_CODIGO, MTI_DESCRITOR, QTD) select  MTI_CODIGO, MTI_DESCRITOR, count(*) as QTD from  avaliacao group by 1;


CREATE TABLE teste (
    MUN_UF         CHAR(2),              -- SIGLA DA UNIDADE DA FEDERAÇÃO
    MUN_NOME       VARCHAR(60),          -- NOME DO MUNICÍPIO
    ESC_INEP       CHAR(8),              -- CÓDIGO INEP DA ESCOLA
    SER_NUMBER     INTEGER,              -- NÚMERO DO ANO/SÉRIE
    SER_NOME       VARCHAR(30),          -- NOME DA SÉRIE
    TUR_PERIODO    VARCHAR(15),          -- TURNO DE ATIVIDADE (Manhã, Tarde)
    TUR_NOME       VARCHAR(20),          -- NOME DO TURNO
    ALU_ID         INTEGER,              -- IDENTIFICAÇÃO DO ALUNO
    ALU_CPF        VARCHAR(15),          -- CPF DO ALUNO
    AVA_NOME       VARCHAR(50),          -- NOME DA AVALIAÇÃO
    AVA_ANO        INTEGER,              -- ANO DA AVALIAÇÃO
    DIS_NOME       VARCHAR(30),          -- NOME DA DISCIPLINA
    TES_NOME       VARCHAR(30),          -- NOME DO TESTE
    TEG_ORDEM      INTEGER,              -- ORDEM DA QUESTÃO DO TESTE
    ATR_RESPOSTA   CHAR(1),              -- RESPOSTA DO ALUNO NA QUESTÃO
    ATR_CERTO      INTEGER,              -- SE 1 ACERTOU, SE 0 ERROU
    MTI_CODIGO     VARCHAR(15)          -- CÓDIGO DO DESCRITOR
);


insert into teste (MUN_UF,MUN_NOME,ESC_INEP,SER_NUMBER,SER_NOME,TUR_PERIODO,TUR_NOME,ALU_ID,ALU_CPF,AVA_NOME,AVA_ANO,DIS_NOME,TES_NOME,TEG_ORDEM,ATR_RESPOSTA,ATR_CERTO,MTI_CODIGO)
select MUN_UF,MUN_NOME,ESC_INEP,SER_NUMBER,SER_NOME,TUR_PERIODO,TUR_NOME,ALU_ID,ALU_CPF,AVA_NOME,AVA_ANO,DIS_NOME,TES_NOME,TEG_ORDEM,ATR_RESPOSTA,ATR_CERTO,MTI_CODIGO  
from avaliacao;

drop table avaliacao;
VACUUM;
