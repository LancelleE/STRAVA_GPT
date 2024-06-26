# STRAVA ROASTER
Author: Etienne LANCELLE 

Date: 2024-06

## To-do

- Intégrer mécanique de refresh de token.
- Stockage de l'historique des refresh de token ?
- Stockage de tous les logs ? A chaque Run :
    - Si la GitHub action n'a pas repéré de nouvelles activités, juste une ligne de log
    - Si activité, alors noter : timestamp, activity_id, type (run, bad, vélo ?), changement (titre ? description ?)
    - Si refresh token, préciser
- Définir la fréquence de Run
- Construire la mécanique de pattern dans le titre
    - J-X avant un évènement, 
    - Emojis à mettre sur une période donnée en premier caractère
        - Et définir à partir de combien de jours avant l'afficher
    - Emoji si je suis avec Enora (règle métier : si nb_athlete = 2, faute de mieux)
- Construire la définition de description via un LLM
    - Quel modèle employer ? OpenAI ?
    - Quelles métriques donner au prompt ?
        - Exploiter les segments, dans un autre call API.
    - Quel prompt employer ?
    - Quel ton ?

- Rédiger documentation

## Idées pêle-mêle

- Laisser 1h à l'utilisateur (moi) pour mettre mon titre, titre qui pourra servir au modèle pour comprendre la séance que je souhaitais réaliser.
- Idem pour la description.
- Pourquoi pas mettre en description des métriques rigolotes ? 
    - si je fais plus de 1000 déniv sur l'année, alors "Barre des 1000m de D+ atteinte en 2024 !"
    - barres kilométriques, tous les 100 bornes par exemple, avec un rappel de "combien de jours de 0 à 100, de 100 à 200, etc ?"
    - volume de kudos
    - volume de calories
    - temps passé à courir sur l'année

Il faudra bien que le LLM **AJOUTE** de la description, il ne la remplace pas.