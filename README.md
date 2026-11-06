# Minecraft Archive (mcarchive)

Plataforma web para preservação e compartilhamento de mods, modpacks, server jars, mapas e tutoriais clássicos de Minecraft (1.4.7 até 1.16.5+).

---

## Imagens Docker no GitHub Packages (GHCR)

A imagem Docker deste projeto é publicada automaticamente no GitHub Container Registry:

```text
ghcr.io/thalisonnunes20/mcarchive:latest
```

---

## Como Executar com Docker Compose

### Opção 1: Stack Simplificada com SQLite (Zero-Config / Sem .env)

Para rodar imediatamente sem banco de dados externo e sem precisar criar `.env`:

```bash
docker compose -f docker-compose.sqlite.yml up -d
```

### Opção 2: Deploy de Produção com GitHub Packages e PostgreSQL

```bash
docker compose -f docker-compose.prod.yml up -d
```

### Opção 3: Construindo localmente

```bash
cp .env.example .env
docker compose up -d --build
```

O site estará acessível em `http://localhost`.

---

## Painel Administrativo

A rota do painel de administração customizada é:
* `http://localhost/mca-painel/`

Para criar o primeiro usuário administrador no container:
```bash
docker compose -f docker-compose.sqlite.yml exec web python manage.py createsuperuser
```

---

## Banco de Dados (SQLite ou PostgreSQL)

* **SQLite (Padrão / Zero-Config)**: Se nenhuma variável `DB_NAME` for definida no arquivo `.env`, o sistema utiliza SQLite localmente de forma automática.
* **PostgreSQL**: Para utilizar PostgreSQL, preencha as variáveis `DB_NAME`, `DB_USER` e `DB_PASSWORD` no arquivo `.env`.

---

## Executando Localmente sem Docker

1. Crie e ative um ambiente virtual:
   ```bash
   python -m venv .venv
   # Windows:
   .venv\Scripts\activate
   # Linux/Mac:
   source .venv/bin/activate
   ```

2. Instale as dependências:
   ```bash
   pip install -r requirements/development.txt
   ```

3. Aplique as migrações e inicie o servidor:
   ```bash
   python manage.py migrate
   python manage.py runserver
   ```

Acesse em `http://127.0.0.1:8000`.

---

## CI/CD com GitHub Actions

O repositório inclui o workflow `.github/workflows/docker-publish.yml`, responsável por compilar e publicar automaticamente as imagens no GHCR a cada push na branch `main` ou criação de tags de versão (`v*.*.*`).
