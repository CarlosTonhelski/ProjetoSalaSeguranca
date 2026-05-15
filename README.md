SecureRoom: Sistema de controle de acesso utilizando Raspberry Pi 4, RFID, Flask, PostgreSQL e monitoramento web em tempo real.

Funcionalidades
leitura RFID;
controle de entrada e saída;
acessos autorizados e negados;
detecção de invasão;
monitoramento em tempo real;
gerenciamento de colaboradores;
exportação CSV;
análise de dados com Pandas.

Tecnologias Utilizadas:
Backend:
Python;
Flask;
PostgreSQL;

Frontend:
HTML;
CSS;
JavaScript;

Hardware:
Raspberry Pi 4;
RFID RC522
LEDs;
Buzzer;

Análise de Dados:
Pandas;
Jupyter Notebook;

Estrutura do Projeto:
backend/      API Flask + PostgreSQL
frontend/     Interface web
analise/      Pandas + Jupyter Notebook
ProjetoTag.py Raspberry Pi + RFID

Como Executar:
Backend:
cd backend
python app.py

Frontend:
Abrir o arquivo:
frontend/index.html

Raspberry Pi:
python3 ProjetoTag.py

Infraestrutura
Serviço	Endereço:
Backend Flask	10.1.25.110:5000
PostgreSQL	10.1.25.39:5432


Integrantes:
Júlia Wonsick Pazzinatto RA 1136562. Responsável pelo Backend, Flask, PostgreSQL e integração da API.
Carlos Eduardo Tonhelski RA: 1137093. Responsável pela Raspberry Pi, RFID e hardware.
João Vinicius Lago dos Santos RA: 1136868. Responsável pelo Frontend e monitoramento em tempo real.

Disciplina:
Hardware Architecture — Atitus Educação

Professor: Me. Fernando Posser Pinheiro
