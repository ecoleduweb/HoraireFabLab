# Préparer environnement développement

## But de la documentation
Cette documentation va servir à préparer votre environnement de développement.

Avoir un docker MariaDB.
## Installation


### 1 -Valider que la virtualisation est activé sur l'ordinateur
```bash
# Powershell en admin
wsl --install
```
Cela va installer un WSL de Ubuntu, au premier démarrage il va demander de mettre un username et un mot de passe.
### 2- Télécharger et installer Docker Desktop
 - Docker Desktop
[Lien pour DockerDesktop](https://www.docker.com/products/docker-desktop/)

### 3- Configurer Docker Desktop
Se rendre dans paramètre

Dans general s'assurer que cette case est coché :

**Use the WSL 2 based engine (Windows Home can only run the WSL 2 backend)**

Ensuite, se rendre dans Ressources -> WSL integration :

Activé ces 2 choses :

**Enable integration with my default WSL distro**
**Ubuntu**

Cela va reloader Docker Desktop

### 4- Configurer pour démarrer MariaDB

 1. Ouvrir Powershell en admin
 2. ```bash
 	cd C:/
	```
 3. ```bash
 	mkdir docker/mariadb3308/
	```
 4. ```bash
	cd .\docker\mariadb3308\ 
	```
 5. Copié ceci en ligne de commande 
	 ```bash
	@"
	services:
	  mariadb:
	    image: mariadb:11
	    container_name: mariadb
	    command: --port=3308
	    environment:
	      MARIADB_ROOT_PASSWORD: RootPass123!
	      MARIADB_DATABASE: FabLab
	      MARIADB_USER: fablab_user
	      MARIADB_PASSWORD: FabLab123!
	    ports:
	      - "3308:3308"
	    volumes:
	      - mariadb_data:/var/lib/mysql
	    restart: unless-stopped

	volumes:
	  mariadb_data:
	"@ | Set-Content docker-compose.yml
	  ```

 6. Toujours dans le dossier exécuter ceci (Cela initialise MariaDB) :
	 ```bash
	 docker  compose  up  -d
	 ```
### Point important  :
Regarder le script pour créer le mariadb pour savoir quoi mettre dans le .env
Pour utiliser le docker MariaDB, il faut que l'application Docker Desktop soit ouverte.

#### Pour se connecter à la bd :
En powershell admin :

	docker exec -it mariadb mariadb -u root -p -P 3308
