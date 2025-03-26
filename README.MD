# Sistema de Cotações de Moedas

Um projeto full-stack para visualização de cotações de moedas estrangeiras em relação ao dólar americano (USD), com backend em Django/PostgreSQL e frontend em React.

## Funcionalidades:

* **Consulta em tempo real** de cotações (USD → BRL, EUR, JPY)
* **Gráfico interativo** com histórico de até 5 dias úteis
* **Persistência em banco de dados** PostgreSQL
* **API RESTful** com Django REST Framework
* **Interface responsiva** com React e Recharts

## Tecnologias:

### Backend

* **Python 3.10+**
* Django 4.2
* Django REST Framework
* PostgreSQL
* psycopg2 (adaptador PostgreSQL)
* django-cors-headers

### Frontend

* React 18
* Axios (client HTTP)
* Recharts (visualização de dados)
* Vite (build tool)

## Como Executar:

### Pré-requisitos

* Python 3.10+
* Node.js 16+
* PostgreSQL 14+
* pgAdmin 4 (opcional)

### Configuração do Backend:

1. **Configure o ambiente virtual**

   ```
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate   
   ```
2. **Instale as dependências**

   ```
   pip install -r requirements.txt
   ```
3. **Configure o banco de dados**

   * Crie um banco chamado `cotacoes_db` no PostgreSQL
   * Atualize as credenciais em `backend/settings.py`
4. **Aplique as migrações**
   

   ```
   python manage.py migrate
   ```
5. **Inicie o servidor**


   ```
   python manage.py runserver
   ```

### Configuração do Frontend:

1. **Acesse a pasta do frontend**

   ```
   cd ../frontend
   ```
2. **Instale as dependências**

   ```
   npm install
   ```
3. **Inicie o aplicativo**

   ```
   npm run dev
   ```

## API:

* `GET /api/cotacoes/buscar/?moeda=BRL&dias=5`
  Retorna cotações históricas da moeda especificada

## Estrutura do Banco de Dados:

Tabela `cotacoes_cotacao`:

* `id` (PK)
* `data` (date)
* `moeda` (varchar)
* `valor` (decimal)

## Fluxo de Dados:

1. Frontend solicita cotações via API
2. Backend verifica se os dados existem no PostgreSQL
3. Se não existirem, consulta a API externa (VatComply)
4. Armazena novos dados no banco
5. Retorna os dados formatados para o frontend
6. React renderiza o gráfico com Recharts

## Solução de Problemas:

**Dados não aparecendo?**

* Verifique se o backend está rodando (`http://127.0.0.1:8000/api/cotacoes/buscar/?moeda=BRL&dias=5`)
* Confira os logs do Django para erros
* Verifique as permissões do usuário PostgreSQL

**Problemas de CORS?**

* Confira se `django-cors-headers` está configurado corretamente
* Verifique as configurações em `settings.py`
