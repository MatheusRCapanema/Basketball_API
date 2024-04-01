# Basketball API

## Descrição

Este sistema disponibiliza funcionalidades para o quarto árbitro do basquete, além de informações sobre a Olimpíadas internas da materia PI.

## Início Rápido

### Pré-requisitos
- flask
- pathlib
- python-dotenv
- PyJWT
- Flask-SQLAlchemy
- Flask-Migrate
- flask-bcrypt
- mysqlclient
- pymysql

### Instalação

Clone o repositório para a sua máquina local:

git clone https://seu-repositorio/basketball-api.git
cd basketball-api


### Instale as dependências:

pip install -r requirements.txt

### Faça e Configure o arquivo `.env` com as suas variáveis de ambiente:

SQLALCHEMY_DATABASE_URI_DEV='mysql+pymysql://SEU_USUARIO:SUASENHA@SEU_HOST/BASE_DE_DADOS'
SQLALCHEMY_TRACK_MODIFICATIONS=False
SECRET_KEY='sua_secret_key_super_secreta'

### Inicialize o banco de dados:

- flask db init
- flask db migrate -m "Initial migration."
- flask db upgrade


### Executando a Aplicação

Para iniciar o servidor, execute:

- flask run





