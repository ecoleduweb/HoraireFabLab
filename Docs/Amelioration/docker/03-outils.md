# Outils selon le rôle

## Philosophie

> Docker est la technologie commune, mais les outils diffèrent selon qu'on est **développeur** ou **DevOps**.

L'objectif est de ne pas rendre la tâche plus difficile.

---

## Développeurs — Docker Desktop

### C'est quoi ?

[Docker Desktop](https://www.docker.com/products/docker-desktop/) est l'interface officielle de Docker pour Windows et macOS. Il installe Docker Engine, Docker Compose, et une interface graphique simple.

### Ce que le dev fait au quotidien

```bash
# Démarrer l'environnement complet
docker compose up

# Voir les logs de l'API en temps réel
docker compose logs -f api

# Accéder au shell du container Django
docker compose exec api bash

# Lancer les migrations
docker compose exec api python manage.py migrate

# Arrêter tout
docker compose down
```


### Interface graphique

Docker Desktop offre une interface pour :
- Voir les containers qui tournent (et les démarrer/arrêter en un clic)
- Consulter les logs sans passer par le terminal

### Installation

| Plateforme | Lien |
|-----------|------|
| Windows | [Docker Desktop for Windows](https://docs.docker.com/desktop/install/windows-install/) |
| macOS | [Docker Desktop for Mac](https://docs.docker.com/desktop/install/mac-install/) |
| Linux | [Docker Desktop for Linux](https://docs.docker.com/desktop/install/linux-install/) |

**Prérequis :** Aucune autre installation nécessaire. Docker Desktop inclut tout.

---

## DevOps — Dockhand

### C'est quoi ?

[Dockhand](https://github.com/nicholaswilde/dockhand) (ou des outils équivalents comme **Portainer**, **Watchtower**, ou des scripts Dockhand custom) sont des outils de gestion de containers orientés opérations.

Pour ce projet, la recommandation est **Dockhand** pour orchestrer les déploiements sur les serveurs dev et prod via les GitHub Actions.

### Rôle du DevOps avec Docker

| Tâche | Outil |
|-------|-------|
| Gérer les images dans le registre| GitHub Container Registry + CLI |


### Pourquoi pas juste `systemctl` comme maintenant ?

| Aspect | systemctl | Docker Compose |
|--------|-----------|----------------|
| Rollback | Réinstaller depuis Git | Changer un tag d'image |
| Logs centralisés | Journald (séparé par service) | `docker compose logs` (tout en un) |


---

## Courbe d'apprentissage

| Rôle | Avant (SSH + systemctl) | Après (Docker) |
|------|------------------------|----------------|
| DevOps | Doit maintenir des scripts fragiles | Gère des fichiers YAML déclaratifs |