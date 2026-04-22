# Fichiers Docker — Guide d'intégration

Ce dossier contient tous les fichiers Docker prêts à intégrer dans le projet FabLab.

## Structure à adopter dans le projet

```
HoraireFabLab/
├── API/
│   ├── Dockerfile                ← Copier depuis API/Dockerfile
│   ├── requirements.txt
│   └── ...
├── FabLab/
│   ├── Dockerfile                ← Copier depuis FabLab/Dockerfile
│   ├── package.json
│   └── ...
├── nginx/
│   └── nginx.conf                ← À créer (exemple ci-dessous)
├── docker-compose.yml            ← Local / développement
├── docker-compose.prod.yml       ← Production
├── .env.example                  ← Committer ce fichier
├── .env.local                    ← Ne pas committer (gitignore)
├── .env.dev                      ← Ne pas committer (injecté par CI)
├── .env.prod                     ← Ne pas committer (injecté par CI)
└── .gitignore
```

## Fichiers fournis

| Fichier | Destination dans le projet | Description |
|---------|---------------------------|-------------|
| `API/Dockerfile` | `API/Dockerfile` | Image multi-stage pour Django |
| `FabLab/Dockerfile` | `FabLab/Dockerfile` | Image multi-stage pour Svelte |
| `docker-compose.yml` | `docker-compose.yml` | Compose local avec hot-reload |
| `docker-compose.prod.yml` | `docker-compose.prod.yml` | Compose prod avec Nginx |
| `.env.example` | `.env.example` | Template de variables d'env |

## Ajouter au .gitignore

```gitignore
# Environnements Docker
.env.local
.env.dev
.env.prod

# Données locales
db_local_data/
```

## Exemple de configuration Nginx minimale

```nginx
# nginx/nginx.conf
events {}

http {
    upstream api {
        server api:8000;
    }

    upstream frontend {
        server frontend:8001;
    }

    server {
        listen 80;
        server_name fablab.example.com;

        location /api/ {
            proxy_pass http://api;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }

        location / {
            proxy_pass http://frontend;
            proxy_set_header Host $host;
        }
    }
}
```

## Première utilisation (développeur)

```bash
# 1. Cloner le projet
git clone https://github.com/ecoleduweb/HoraireFabLab.git
cd HoraireFabLab

# 2. Préparer l'environnement local
cp .env.example .env.local
# Éditer .env.local avec vos valeurs locales

# 3. Démarrer
docker compose up

# L'API est sur http://localhost:8000
# Le frontend est sur http://localhost:5173
```

## Lancer les tests Playwright

```bash
docker compose --profile test run playwright npx playwright test
```