# FabLab Scheduling API

API REST développée avec **Django** et **Django REST Framework** permettant la gestion d’horaires pour un FabLab.  
Le système permet de gérer des événements, des plages horaires et des réservations.

L’authentification est réalisée avec **JWT (JSON Web Tokens)** stockés dans des **cookies HttpOnly** afin d’améliorer la sécurité.

---

## Table des matières

- [Présentation](#présentation)
- [Architecture](#architecture)
- [Technologies utilisées](#technologies-utilisées)
- [Installation](#installation)
- [Configuration](#configuration)
- [Base de données](#base-de-données)
- [Lancement du projet](#lancement-du-projet)
- [Authentification](#authentification)
- [Tests](#tests)
- [Auteur](#auteur)

---

## Présentation

Cette API permet de :

- gérer des **événements**
- créer des **plages horaires**
- générer des **slots de réservation**
- réserver un slot pour un client
- authentifier un administrateur via **JWT**

Le projet suit une architecture claire basée sur :

```sh
Controller
   ↓
Service
   ↓
Repository
```

Cette séparation permet :

- une meilleure maintenabilité
- un code plus testable
- une séparation claire des responsabilités

---

## Architecture

Le projet suit une architecture **layered**.

### Controllers

Gestion des requêtes HTTP et des réponses API.

### Services

Contiennent la logique métier.

### Repositories

Responsables de l'accès aux données.

### Authentication

Gestion des JWT via cookies sécurisés.

### Tests unitaires

Tests unitaires des endpoints critiques.

---

## Technologies utilisées

- Python 3.13
- Django 6
- Django REST Framework
- SimpleJWT
- MariaDB
- Docker
- JWT cookies (HttpOnly)
- Django Test Framework

---

## Installation

### 1. Cloner le projet

```bash
   git clone https://github.com/ecoleduweb/HoraireFabLab.git
   cd HoraireFabLab/API
```

---

### 2. Installer python (S'il ne l'est pas déjà)

- Rechercher "python download" sur internet
- Télécharger l'outil d'installation de python
- Ouvrir l'outil d'installation et installer python

---

### 3. Créer un environnement virtuel

```bash
   cd HoraireFabLab/API
   python -m venv venv
```

#### Activation

##### Windows

```bash
   venv\Scripts\activate
```

##### Linux / Mac

```bash
   source venv/bin/activate
```

---

### 4. Installer les dépendances

```bash
   pip install -r requirements.txt
```

---

### 5. Installer les packages nécessaires

```bash
   pip install django djangorestframework django-cors-headers python-decouple nh3
```

---

## Configuration

Créer un fichier `.env`.

Exemple :

```bash
DJANGO_ENV=
DJANGO_DEBUG=
DJANGO_SECRET_KEY=

DB_NAME=
DB_USER=
DB_PASSWORD=
DB_HOST=
DB_PORT=

JWT_COOKIE_SECURE=
JWT_COOKIE_SAMESITE=
```

---

## Base de données

### Migrations

```bash
   python manage.py migrate
```

---

### Créer un utilisateur admin

```bash
   python manage.py shell
```

```python
   from django.contrib.auth.hashers import make_password
   from api.models import User

   User.objects.create(
      username="admin1",
      password_hash=make_password("pass123"),
      email="admin1@test.com"
   )
```

---

## Lancement du projet

```bash
   python manage.py runserver
```

L'API sera accessible à :

```sh
   http://localhost:8000
```

---

## Authentification

Le projet utilise **JWT avec cookies HttpOnly**.

Cookies générés :

```sh
   access_token
   refresh_token
```

### Avantages

- protection contre les attaques **XSS**
- authentification **stateless**
- sécurité améliorée

---

## Tests

Lancer les tests :

```bash
   python manage.py test
```

Les tests couvrent :

- login
- authentification JWT
- endpoint `/me`
- logout

- Création d'un événement répare tes trucs

---

## Auteur

Étudiant : **Cedric Tresor**
Reviewers : **Christophe Gilbert et Hélène Caron**
Supervision : **Antoine Chagnon Michaud**

Projet pédagogique et d'application  
Québec, 2026
