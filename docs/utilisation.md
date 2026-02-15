# Introduction

Notre logiciel propose 3 modes différents (hors la page d'accueil) :

1. Édition d'un questionnaire
2. Remplissage d'un formulaire
3. Correction d'un formulaire rempli

## Remarques

Le logiciel dans l'état actuel n'est pas terminé.
En particulier, l'interface utilisateur pourrait être embellie,
les opérations davantage sécurisées (contre la perte de données sans enregistrement par exemple),
les actions proposées plus nombreuses.

En revanche, nous nous sommes concentrés sur la propreté du code.

## Notions de questionnaire, formulaire

Un questionnaire est composé d'un titre et d'une liste de questions.
Chaque question possède un énoncé et un espace de réponse.
Notre logiciel propose 3 types de questions :

- À réponse libre (textuelle courte)
- À choix multiples (plusieurs choix possibles)
- À choix unique (un choix parmi plusieurs propositions)

Un formulaire permet de répondre au questionnaire en renseignant une
réponse à chaque question du questionnaire.
Un questionnaire peut avoir plusieurs formulaires de réponse.

Il est possible de sauvegarde un questionnaire, ses formulaires, et
toutes les données qui leur sont subordonnées dans un fichier, afin de ne pas
perdre le travail entre les différentes sessions d'utilisation, ou de partager
le questionnaire ou ses résultats.

# Interface

L'interface se compose de 3 éléments principaux :

- Un menu déroulant, en haut
- L'espace central de la fenêtre, où sont affichée la pluspart des informations
- D'éventuelles fenêtres "pop-up"

## Mode édition d'un questionnaire

Dans ce mode, l'utilisateur peut éditer un questionnaire.

Le titre est édité dans le petit encadré tout en haut de la page d'édition.
Chaque question est éditée dans un éditeur de question, décrit plus bas.

L'utilisateur peut ajouter une question supplémentaire en utilisant le bouton adéquat, tout en bas de l'éditeur.
Il peut aussi modifier leur ordre ou en supprimer grâce aux boutons "flèches" et "croix",
qui apparaissent en bas à droite de chaque éditeur de question.

### Éditeurs de question

L'éditeur de question est divisé en trois parties principales :

- La partie supérieure :
  - Renseigne l'énoncé de la question (encadré à gauche)
  - Le type de question (menu déroulant au milieu)
  - Le nombre de points qu'elle rapporte (encadré à droite)
- La partie centrale :
  - Définit les possibilités de réponse ainsi que la bonne réponse.
    Cette partie est spécifique à chaque type de question.
- La partie inférieure :
  - Indicateur de question obligatoire (remarque : non-fonctionnel actuellement)
  - Permet de déplacer ou supprimer la question au sein du questionnaire (boutons à droite).

#### Question libre

La réponse attendue est décrite dans un espace de saisie textuelle.

#### Question à choix unique et multiples

La liste des proposition est définie de manière similaire à celle des questions au sein du questionnaire.
Une interface avec des boutons à cocher (multiples) ou à choisir (unique) permet la sélection de la ou des bonnes réponses.

## Mode remplissage d'un formulaire

Dans ce mode, l'utilisateur peut remplir le formulaire d'un questionnaire.

L'utilisateur est invité à donner un nom à sa tentative tout en haut de la page.
Chaque question est présentée dans un encadré similaire à ceux de l'éditeur.

Une fois le formulaire complété, l'utilisateur peut demander sa correction avec le bouton "envoyer", tout en bas.

## Mode correction d'un formulaire rempli

Dans ce mode, l'utilisateur peut avoir la correction de sa tentative.
Cette page est en mode lecture seule.

Le nom de la tentative est renseigné en haut.
Chaque question est présentée dans un encadré similaire à ceux de l'éditeur de questionnaire et de formulaire.
Elle informe désormais de la correctitude de la réponse fournie, et indique la réponse attendue.

## Menu déroulant

Le menu déroulant présente plusieurs volets, dont :

- Questionnaire
- Formulaire

### Questionnaire

#### Nouveau

Permet la création d'un nouveau questionnaire vide.

#### Ouvrir

Permet l'ouverture d'un qcm depuis un fichier de sauvegarde.

#### Enregistrer

Permet la sauvegarde d'un qcm.

#### Enregistrer sous

Permet la sauvegarde d'un qcm dans un autre fichier.

#### Fermer

Permet la fermeture du questionnaire affiché ; l'interface revient au menu d'accueil.

### Formulaire

#### Commencer

Permet l'ouverture d'un nouveau formulaire pour
- Le questionnaire actuellement en édition dans l'éditeur de questionnaire
- Le questionnaire trouvé dans un fichier alors choisi pour ouverture par l'utilisateur

#### Corriger

Permet l'affichage de la correction du formulaire.

#### Enregistrer

Enregistre le formulaire dans un fichier.

#### Enregistrer sous

Enregistre le formulaire dans un autre fichier.

#### Fermer

Permet la fermeture du formulaire affiché ; l'interface revient au menu d'accueil.

# Utilisation

L'utilisation se fait en plusieurs étapes, dont certaines peuvent être omises.

1. Édition d'un nouveau questionnaire
2. Ouverture d'un questionnaire dans un formulaire
3. Remplissage d'un formulaire
4. Ouverture du formulaire rempli dans le correcteur
5. Affichage des résultats et de la correction

Questionnaire et formulaire peuvent être sauvegardés dans un fichier.
Voir les explications sur le menu déroulant.
