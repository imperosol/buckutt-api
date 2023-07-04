# BuckUTT API

BuckUTT est le système de paiement dématérialisé
du BDE de l'UTT, hébergé par l'[UTT Net Group](https://ung.utt.fr).

La conception originelle de l'API remonte à 2014.
Depuis, il n'y a pas eu de maintenance ni de mise à jour.
Certaines dépendances sont devenues obsolètes et
personne n'est actuellement en mesure de résoudre les bugs qui surviennent.
Le code n'est pas documenté, pas testé et peu commenté.

Ce projet a pour but de réécrire l'API, en l'améliorant,
en la documentant et en la testant.

Le code actuel est une preuve de concept qui n'a pas (encore)
vocation à être utilisé en production.
Il est écrit en Python 3.11 avec le framework Django 4.2.
La rapidité et la facilité de développement avec Django
en font un choix idéal pour ce genre de prototype.

## Organisation du projet

Le projet est organisé en plusieurs applications Django.
Chacune est organisée de la manière suivante :

    application/
        tests/     # Tests unitaires
            __init__.py
            test_model.py  # tests liés directement aux modèles et à l'ORM
            test_api.py    # tests liés à l'API REST
        __init__.py
        admin.py   # Administration Django
        api.py     # API REST
        apps.py    # Configuration de l'application
        models.py  # Modèles de l'ORM
        schemas.py # Schémas de validation des données

Il y a au total 4 applications :

- `article` : gestion des articles, de leurs catégories et de leur prix
- `selling_points` : gestion des points de vente et des machines
- `transaction` : gestion des achats et des rechargements de compte
- `users` : gestion des utilisateurs

Le dossier `buckutt/` contient les fichiers de configuration
de Django et les fichiers communs à toutes les applications.

Le projet contient également un dossier `docs/` qui contient
la documentation du projet. Elle est écrite en Markdown
et compilée en HTML avec [MkDocs](https://www.mkdocs.org/).

