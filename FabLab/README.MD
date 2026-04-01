# Horaire FabLab - Front-End (Application WEB)

## Identification

- Auteure: Hélène Caron
- Date de création: 28/01/2026
- Date de dernière modification: 18/03/2026
- Version: 1.0

## Description

Application WEB développée dans le cadre du cours de Projet d'application pour le projet de gestionnaire d'activité de réparation d'objets du FabLab.

## Prérequis pour installer le projet en local

- Avoir VS Code ou une application similaire

## Installation du projet en local

1. Ouvrir un terminal dans l'application
2. Si le repository global du projet n'est pas déjà clôné en local, effectuer la commande suivante dans le terminal:

```sh
    git clone https://github.com/ecoleduweb/HoraireFabLab.git
```

3. Si le projet est déjà clôné, s'assurer d'avoir la dernière version à jour en effectuant la commande suivante:

```sh
    git pull
```

## Installation des dépendances

Pour installer les différentes dépendances requises pour le projet, exécuter les lignes de commande suivantes dans le dossier "/HoraireFabLab/FabLab":

```sh
    npm i
    npm install yup
    npm install striptags
    npm install svelte-hamburgers
```

## Configuration de l'environnement

1. Créer un fichier appelé ".env" dans le dossier "/HoraireFabLab/FabLab", puis entrer les variables d'environnement dans le fichier nouvellement créé selon le modèle suivant:

```
    #Base URL for API calls
    PUBLIC_BASE_URL=
```

## Démarrage du projet

1. À l'aide du terminal de l'application, se positionner dans le dossier "/HoraireFabLab/FabLab"
2. Exécuter la ligne de commande suivante:

```sh
    npm run dev
```

Le site web peut maintenant être consulté sur votre machine locale à l'adresse indiquée dans le terminal

## Contributeurs

- Hélène Caron: Créatrice et première contributrice
