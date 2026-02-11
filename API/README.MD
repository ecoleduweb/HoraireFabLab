## HoraireFabLab API — Installation

Backend Django pour la gestion du FabLab.
Authentification admin hardcodée (2 comptes).

## Prérequis

-Python 3.11+
-pip
-Git
-virtualenv (optionnel mais recommandé)

1- Vérifier Python :
 'python --version'

2- Cloner le projet 
git clone  https://github.com/ecoleduweb/HoraireFabLab.git
cd HoraireFabLab/API

3- Créer l’environnement virtuel
 # Windows (Git Bash) :
 python -m venv venv
 source venv/Scripts/activate

 # PowerShell
 venv\Scripts\activate

 # Mac / Linux
 python -m venv venv
source venv/bin/activate

4. Installer les packages
pip install django djangorestframework django-cors-headers python-decouple

5. Installer les dépendances
pip install -r requirements.txt

6. Configuration .env
API/.env
Voici un exemple de lignes à insérer dans votre .env: 
/*
DJANGO_SECRET_KEY=django-insecure-dev-key
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
DJANGO_ENV=development
*/

