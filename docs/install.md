# Installation du projet

## Prérequis

Pour installer le projet, vous aurez besoin de :

- git ([documentation officielle](https://git-scm.com/book/fr/v2/D%C3%A9marrage-rapide-Installation-de-Git))
- Python 3.11 ([documentation officielle](https://docs.python.org/fr/3.11/using/index.html))
- Poetry ([documentation officielle](https://python-poetry.org/docs/#installation))
- PostgreSQL ([documentation officielle](https://www.postgresql.org/download/))

## Installation sur une distribution Linux

Commencez par cloner le projet :

```bash
git clone  
```

Puis, pour créer la base de données :

```bash
sudo su - postgres

psql

CREATE DATABASE buckutt;
CREATE USER buckutt WITH PASSWORD 'choississez un mot de passe';
GRANT ALL PRIVILEGES ON DATABASE buckutt TO buckutt;
ALTER ROLE buckutt SET client_encoding TO 'utf8';
ALTER ROLE buckutt SET default_transaction_isolation TO 'read committed';
ALTER ROLE buckutt SET timezone TO 'UTC';
\q
```

Une fois la base de données créée, vous pouvez renommer le fichier `.env.example`
en `.env` et le modifier pour qu'il corresponde à votre configuration.
Commencez par renseigner le clef secrète de Django (`SECRET_KEY`).
Pour ça, vous pouvez utiliser le site [djecrety.ir](https://djecrety.ir/).
Renseignez ensuite les informations de connexion à la base de données (`DB_NAME` et `DB_PASSWORD`).

Ensuite, installez les dépendances du projet :

```bash
poetry install

# Ou bien, si vous voulez installer le moins de dépendances possible :
poetry install --without docs,dev
```

Puis, créez les tables de la base de données :

```bash
poetry run ./manage.py migrate
poetry run loaddata fixtures.json
```

Enfin, lancez le serveur de développement :

```bash
poetry run ./manage.py runserver
```


## Windows

PTDR t'utilises Windows ? Bah écris les instructions toi-même.

