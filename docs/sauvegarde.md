# Fonctionnement de la sauvegarde

La sauvegarde se fait dans une base de données au format SQL.
Elle est assurée par le module `qcm.control.db` qui se sert du modèle défini dans `qcm.db`.

Le fichier de sauvegarde est choisi arbitrairement par l'utilisateur.
Il prend l'extension `.qdb`.

Un fichier d'exemple est proposé dans le dossier `examples` à la racine de ce projet.

# Contenu

La base de données de chaque fichier contient :

- Un unique `Qcm`
- Une liste de `Tentative` reliées toutes au même qcm
- Tous les objets qui sont subordonnés au `Qcm` et aux `Tentatives`

Il représente ainsi un questionnaire et toutes les réponses qui lui ont été collectées.

# Améliorations possibles

- Stocker des informations de version
- Stockage des dates
- Mode "réponse uniquement", qui empêche l'utilisateur de voir les réponses correctes avant d'avoir rempli le formulaire.

Dans une optique à plus grande échelle, il serait aussi envisageable de stocker toutes les informations d'une session
dans une unique base de donnée (donc un unique fichier), au lieu d'émettre un fichier par projet.
