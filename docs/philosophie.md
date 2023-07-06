# Philosophie du projet

Ce projet est une preuve de concept de réécriture de l'API BuckUTT.
Son but n'est pas de remplacer l'API actuelle, mais de servir de base
pour la réécriture.
Il n'est cependant pas exclu de garder le code actuel et de l'étoffer 
jusqu'à ce qu'il soit utilisable en production.

L'emphase est mise sur la vitesse et la facilité de développement.
De ce point de vue, Django est un choix idéal.

Le deuxième point important est la documentation.
Le code est commenté et documenté, et la documentation est générée
par MkDocs.
En outre, les schémas de validation permettent à django-ninja
de générer une documentation de l'API REST à travers une interface Swagger.

Le troisième point est la pertinence des codes HTTP retournés.
La version actuelle de l'API retourne presque toujours des codes 500
en cas d'erreur, quelle qu'elle soit.
Le code actuel essaie donc de retourner des codes HTTP pertinents,
même si cela implique d'effectuer des requêtes supplémentaires à la base de données.

La performance n'est pas le souci principal pour le moment.