<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a id="readme-top"></a>
<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->



<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->


<!-- PROJECT LOGO -->




<!-- TABLE OF CONTENTS -->
<!--
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>
-->


<!-- ABOUT THE PROJECT -->

## À propos du projet FabLab Horaire

Le projet **FabLab Horaire** est une application web conçue pour faciliter la gestion des plages horaires, des réservations et des activités d’un laboratoire de fabrication (FabLab).

---

## Objectifs du projet

Ce projet vise à :

- Automatiser la gestion des réservations  
- Réduire les conflits d’horaire  
- Offrir une interface intuitive pour les utilisateurs et les administrateurs  

### Technologies utilisées


* [![Django][Django]][Django-url]
* [![Svelte][Svelte.dev]][Svelte-url]
* [![Playwright][Playwright.dev]][Playwright-url]


<!-- GETTING STARTED -->
## Mise en route

Il suffit de cloner le projet et suivre les documentations ci-dessous

- [Documentation Configuration Environnement Developpement](./Docs/READMEENVDEV.MD)
- [Documentation Frontend](./FabLab/README.MD)
- [Documentation Backend](./API/README.MD)
- [Documentation Playwright](./Playwright/README.MD)

<!-- USAGE EXAMPLES -->
## Screenshot (À venir)

<!-- ROADMAP -->
## Roadmap – FabLab Horaire

 
- [x] Initialisation du projet Django (Backend)
- [x] Initialisation du projet Svelte (Frontend)
- [x] Configuration de la base de données
- [x] Mise en place des modèles principaux (Users TimeSlots, Reservations)
- [x] API CRUD de base
- [x] Interface de connexion
- [x] Authentification sécurisée
- [x] Tests E2E avec Playwright
- [ ] Gestion des rôles (Admin / Utilisateur)
- [ ] Création et modification des plages horaires
- [ ] Système complet de réservation
- [ ] Tableau de bord administrateur
- [ ] Logs d’activité
- [ ] Design responsive complet
- [ ] Messages de confirmation
- [x] Configuration Nginx
- [x] Service systemd pour Django
- [x] Variables d’environnement sécurisées
- [ ] Support multi-FabLab


<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
<!-- LINKS -->
[Django]: https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white
[Django-url]: https://www.djangoproject.com/

[Svelte.dev]: https://img.shields.io/badge/Svelte-FF3E00?style=for-the-badge&logo=svelte&logoColor=white
[Svelte-url]: https://svelte.dev/

[Playwright.dev]: https://img.shields.io/badge/Playwright-2EAD33?style=for-the-badge&logo=playwright&logoColor=white
[Playwright-url]: https://playwright.dev/