# Minecraft Archive (mcarchive)

Plataforma web para preservação e compartilhamento de mods, modpacks, server jars, mapas e tutoriais clássicos de Minecraft (1.4.7 até 1.16.5+).

A imagem oficial é All-in-One: executa o Django (via Gunicorn) e o servidor Nginx integrados dentro de um único container gerenciado pelo Supervisor, eliminando a necessidade de múltiplos containers.

---

## Imagens Docker no GitHub Packages (GHCR)

A imagem Docker deste projeto é publicada automaticamente no GitHub Container Registry:

```text
ghcr.io/thalisonnunes20/mcarchive:latest
```

---

## Como Executar com Docker Compose (Container Unico)

### Opção 1: Stack Simplificada com SQLite (Zero-Config / Sem .env)

Para rodar imediatamente sem banco de dados externo e sem precisar criar `.env`:

```bash
docker compose -f docker-compose.sqlite.yml up -d
```

### Opção 2: Deploy de Produção com Imagem Pronta do GHCR

```bash
docker compose -f docker-compose.prod.yml up -d
```

### Opção 3: Construindo localmente

```bash
cp .env.example .env
docker compose up -d --build
```

O site estará acessível diretamente em `http://localhost` (ou na porta que você mapear no host, ex: `8180:80`).

---

## Painel Administrativo

A rota do painel de administração customizada é:
* `http://SEU_IP_OU_DOMINIO/mca-painel/`

Para criar o primeiro usuário administrador no container:
```bash
docker compose -f docker-compose.sqlite.yml exec mcarchive python manage.py createsuperuser
```

---

## Configuração das Variáveis de Ambiente

* **ALLOWED_HOSTS**: Deve conter o domínio ou IP por onde a aplicação será acessada. Se for expor via Nginx Proxy Manager, coloque o domínio (ex: `mcarchive.tsnunes.lan` ou `mcarchive.seudominio.com`). Usar `*` funciona para testes, mas é menos seguro em produção.
* **DB_NAME / DB_SQLITE_PATH**: Ao utilizar SQLite, o Django precisa do caminho do arquivo. A configuração `DB_SQLITE_PATH=/app/data/db.sqlite3` instrui o container a salvar o banco exatamente na pasta mapeada no host/OMV. Deixe `DB_NAME` vazio, pois as configurações priorizam o SQLite automaticamente quando `DB_NAME` não é definido.
* **SECURE_SSL_REDIRECT, SESSION_COOKIE_SECURE, CSRF_COOKIE_SECURE**:
  * Se o tráfego chegar ao container como HTTP (quando o Nginx Proxy Manager ou Cloudflare gerenciam o certificado SSL antes de repassar ao Django), mantenha como `False`.
  * Se alterar para `True`, o Django pode entrar em loop de redirecionamento, a menos que haja configuração específica de proxy header. Deixar em `False` é o padrão para quem gerencia certificados externamente no NPM.

---

## Banco de Dados (SQLite ou PostgreSQL)

* **SQLite (Padrão / Zero-Config)**: Se nenhuma variável `DB_NAME` for definida no arquivo `.env`, o sistema utiliza SQLite localmente de forma automática.
* **PostgreSQL**: Para utilizar PostgreSQL externo, preencha as variáveis `DB_NAME`, `DB_USER`, `DB_PASSWORD` e `DB_HOST` no arquivo `.env`.

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
