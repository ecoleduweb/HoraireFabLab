# Comparaison : Script SSH vs Docker

## Le problème actuel

Le workflow de déploiement actuel fonctionne en production, mais chaque étape du script SSH peut apporter des problèmes.

---

## Analyse point par point

### 1."Ça marche sur mon poste" —  Environnements toutes pareil.

**Problème actuel**

Chaque développeur installe Python, Node.js et mariadb directement sur sa machine. Le script prod fais la "même" chose.

Les versions peuvent différés, même si on les "contrôles".

**Solution Docker**

```dockerfile
#Exemple
FROM python:3.12
# La version est fixée dans l'image — identique partout
```

Tout le monde fait tourner exactement le même environnement.

---

### 2. Arrivé d'un nouveau développeur

**Problème actuel**

Un nouveau dev doit :
- Installer Python dans la bonne version
- Installer Node.js dans la bonne version
- Installer mariadb
- Créer son `.env` manuellement
- Déboguer les incompatibilités de sa machine (Clin d'oeil à Hélène)

Cela peut prendre une demi-journée ou plus.

**Solution Docker**

```bash
git clone https://github.com/ecoleduweb/HoraireFabLab.git
cp .env.example .env.local   # remplir ses valeurs
docker compose up
```

L'application tourne en quelques minutes.

---

### 3. Le déploiement supprime tout avant de tout réinstaller

**Problème actuel**

```bash
rm -rf fablab
git clone https://github.com/ecoleduweb/HoraireFabLab.git fablab
pip install -r requirements.txt   # réinstalle tout
npm install                        # réinstalle tout
npm run build
```

Chaque déploiement est une reconstruction complète depuis zéro. Si `npm install` échoue à mi-chemin (réseau instable, package retiré de npm), le serveur se retrouve dans un état cassé et les services ne redémarrent pas.

**Solution Docker**

```bash
docker pull ghcr.io/ecoleduweb/fablab-api:v1.2.0
docker compose up -d
```

L'image est construite une seule fois dans GitHub Actions et téléchargée sur le serveur. Si le pull échoue, l'ancienne image est toujours là — le serveur reste opérationnel.

---

### 4. Rollback en cas de problème

**Problème actuel**

Si un bug critique arrive en production après un déploiement, revenir en arrière implique de relancer manuellement tout le script SSH avec le bon tag Git. Pendant ce temps, le service est dégradé.

**Solution Docker**

```bash
# Revenir à la version précédente en 10 secondes
docker compose down
docker compose up -d
docker pull ghcr.io/ecoleduweb/fablab-api:v1.1.9
# Modifier le tag dans docker-compose.prod.yml et relancer
docker compose up -d
```

Chaque image taguée est un snapshot immuable de l'application. On peut revenir à **n'importe quelle** version déployée.

---

### 5. Tests Playwright

**Problème actuel**

 Les navigateurs installés peuvent différer.

**Solution Docker**

```yaml
# docker-compose.test.yml
playwright:
  image: mcr.microsoft.com/playwright:v1.49.0-jammy
  depends_on:
    - api
    - frontend
```

Les tests tournent dans le container officiel Playwright de Microsoft, avec les navigateurs précis requis. Les résultats sont fiables et reproductibles.

---

### 6. Gestion des secrets et du `.env`

**Problème actuel**

Le script SSH génère le `.env` directement dans la commande, avec les secrets exposés en clair dans les logs GitHub Actions si `set -x` est activé :

```bash
cat > .env << EOF
DB_USER=${{ secrets.PROD_DB_USERNAME }}
...
EOF
```

**Solution Docker**

Les secrets GitHub Actions sont passés comme variables d'environnement au container au moment du `docker compose up`, sans jamais être écrits dans un fichier sur le disque pendant le déploiement. En local, un `.env.local` ignoré par git est utilisé.

---

## Résumé des risques

| Risque | Script SSH | Docker |
|--------|-----------|--------|
| Déploiement partiel (npm crash) | Marche pu | Rollback automatique |