# README – API + RPA Scraper

---

## **Resumo**

A aplicação faz uma coleta de atos publicados no site da **Receita Federal**, registro no banco de dados PostgreSQL e uma **API FastAPI** para gerenciamento, consulta e monitoramento dos atos.

O scraper também pode ser executado **[via scheduler](#6-executar-rpa)** e logs de execução são registrados para monitoramento.

---

## **Tecnologias**
| Finalidade           | Tecnologia              |
| -------------------- | ----------------------- |
| Backend              | FastAPI                 |
| Banco de Dados       | PostgreSQL              |
| RPA                  | Selenium                |
| Container            | Docker / Docker Compose |

--

## **Estrutura**

```text
├── API
│   ├── auth.py             # autenticação
│   ├── database.py         # setup do banco (get_db etc.)
│   ├── main.py             # inicia o API
│   ├── models.py           # contem os modelos para o banco de dados
│   ├── routes
│   │   ├── atos.py         # CRUD de atos
│   │   ├── auth.py         # login, register e JWT
│   │   ├── dashboard.py    # endpoints de dashboard e estatísticas
│   │   └── user.py         # logica de usuário
│   ├── schemas.py          # abstração de modelos
├── RPA
│   ├── logs.py             # gera os logs da aplicação
│   ├── main.py             # dispara scraper
│   ├── scraper.py          # pega os atos do site
└── └── sender.py           # envia os dados e registra logs do api
```

---

## **Setup**

#### 1. **Clonar o repositório:**

```bash
git clone <repo-url>
cd {nome-do-repositorio}
```

#### 2. **Criar e ativar ambiente virtual (recomendado):**


```bash
python -m venv venv
source venv/bin/activate       # Linux / macOS
venv\Scripts\activate          # Windows
```

#### 3. **Instalar dependências:**

```bash
pip install -r requirements.txt
```

#### 4. **Criar uma instância do PostgreSQL no Docker:**

```bash
sudo docker compose up      # Linux
```

#### 5. **Configurar banco de dados PostgreSQL:**

Dentro de `API/.env` adicione sua "DATABASE_URI=" seguido da URI do seu banco de dados. 

Exemplo:

```env
DATABASE_URL="postgresql://postgres:postgres@localhost:5432/app_db"
```

#### 6. **Executar API:**


```bash
cd ./API
uvicorn API.main:app --reload
```

* A API ficará disponível em `http://127.0.0.1:8000/`.
* Documentação FastAPI: `http://127.0.0.1:8000/docs`.

#### 7. **Executar RPA:**

```bash
cd ./RPA
python main.py --schedule <intervalo de execução>
```
 * Com o argumanento `--schedule`, o RPA ira contunuar sendo executado indefinidamente.

---

## **Endpoints Principais**

| Endpoint             | Método              | Descrição                            |
| -------------------- | ------------------- | ------------------------------------ |
| `/`                  | GET                 | Testa se a API está rodando          |
| `/auth/`             | POST                | Retorna token JWT                    |
| `/atos/`             | GET/                | Lista os atos                        |
| `/atos/{id do ato}`  | GET/POST/PUT/DELETE | CRUD de atos                         |
| `/dashboard/`        | GET                 | Estatísticas de atos                 |
| `/user/`             | POST                | Criação de usuário                   |