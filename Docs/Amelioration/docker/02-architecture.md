# Architecture Docker proposée


## Environnements et différences

### Local (développeur)

**Objectif :** Développer rapidement avec hot-reload, sans rien installer sur sa machine.

```yaml
# docker-compose.yml (local)
services:
  api:
    build: ./API           # Build depuis le code source local
    volumes:
      - ./API:/app         # Hot-reload : le code est monté en direct
    environment:
      - DJANGO_DEBUG=True
      - DJANGO_ENV=development

  frontend:
    build: ./FabLab
    volumes:
      - ./FabLab:/app      # Vite hot-reload
    ports:
      - "5173:5173"

  db:
    image: mysql:8.0       # Base de données locale dans un container
    environment:
      MYSQL_DATABASE: fablab_dev
      MYSQL_ROOT_PASSWORD: devpassword
    volumes:
      - db_data:/var/lib/mysql  # Persistance entre les redémarrages
```

Le développeur n'installe **rien** sur sa machine hormis Docker Desktop.

---

### Dev

**Objectif :** Valider les fonctionnalités dans un environnement proche de la prod avant de merger.

```yaml
# docker-compose.dev.yml
services:
  api:
    image: ghcr.io/ecoleduweb/fablab-api:${IMAGE_TAG}   # Image pré-construite par CI
    env_file: .env.dev
    restart: unless-stopped

  frontend:
    image: ghcr.io/ecoleduweb/fablab-frontend:${IMAGE_TAG}
    env_file: .env.dev
    restart: unless-stopped

  db:
    image: mysql:8.0       # MySQL en container pour le dev — pas besoin d'une vraie DB
    env_file: .env.dev
    volumes:
      - db_dev_data:/var/lib/mysql
```

---

### Prod

**Objectif :** Haute disponibilité, base de données externe, Nginx comme reverse proxy.

```yaml
# docker-compose.prod.yml
services:
  api:
    image: ghcr.io/ecoleduweb/fablab-api:${IMAGE_TAG}
    env_file: .env.prod
    restart: always
    # Pas de port exposé directement — Nginx gère le trafic

  frontend:
    image: ghcr.io/ecoleduweb/fablab-frontend:${IMAGE_TAG}
    env_file: .env.prod
    restart: always

  
  db:
    image: mysql:8.0       # MySQL en container pour le dev — pas besoin d'une vraie DB
    env_file: .env.dev
    volumes:
      - db_dev_data:/var/lib/mysql

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./ssl:/etc/nginx/ssl:ro
    depends_on:
      - api
      - frontend

```

---

## Gestion des variables d'environnement

```
projet/
├── .env.example          template avec des valeurs vides
├── .env.local            Ignoré par git — valeurs locales du dev
├── .env.dev              Ignoré par git — injecté par CI sur le serveur dev
└── .env.prod             Ignoré par git — injecté par CI sur le serveur prod
```

Le fichier `.env.example` sert de documentation vivante : un nouveau développeur sait exactement quelles variables configurer.

---

## Nouveau workflow GitHub Actions

```yaml
# .github/workflows/deploy.yml
name: Build & Deploy

on:
  push:
    branches: [main]        # → déploie en DEV
    tags: ['*']             # → déploie en PROD

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Build & push API image
        run: |
          docker build -t ghcr.io/ecoleduweb/fablab-api:${{ github.sha }} ./API
          docker push ghcr.io/ecoleduweb/fablab-api:${{ github.sha }}

      - name: Build & push Frontend image
        run: |
          docker build -t ghcr.io/ecoleduweb/fablab-frontend:${{ github.sha }} ./FabLab
          docker push ghcr.io/ecoleduweb/fablab-frontend:${{ github.sha }}

  test:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - name: Run Playwright tests
        run: |
          IMAGE_TAG=${{ github.sha }} docker compose -f docker-compose.test.yml up --abort-on-container-exit

  deploy-dev:
    needs: test
    if: github.ref == 'refs/heads/main'
    # SSH vers serveur dev → docker compose pull && docker compose up -d

  deploy-prod:
    needs: test
    if: startsWith(github.ref, 'refs/tags/')
    # SSH vers serveur prod → docker compose pull && docker compose up -d
```

Le serveur **ne construit plus rien** — il télécharge et exécute des images déjà validées.