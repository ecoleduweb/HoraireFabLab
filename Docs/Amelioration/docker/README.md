# Proposition : Dockerisation du FabLab

## Résumé

Le but est de démontrer **l'avantage** d'utiliser docker, dans un but éducatif, pratique et cool.
---

## Documents de cette section

1. **[Comparaison avant/après](./01-comparaison.md)** — Pourquoi le script actuel pose problème et comment Docker règle chacun des points.
2. **[Architecture proposée](./02-architecture.md)** — Comment structurer les environnements local, dev et prod avec Docker.
3. **[Outils selon le rôle](./03-outils.md)** — Docker Desktop pour les devs, Dockhand pour les DevOps.

---

## Comparaison

| Critère | Avant (SSH) | Après (Docker) |
|---------|------------|----------------|
| Ressemblance local/prod |  Aucunement | Identique |
| Réglage de bug | Tannant | `docker compose` avec image précédente |