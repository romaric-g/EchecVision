# EchecsVision

Le but de ce projet est de créer un système capable de suivre les déplacements sur un
plateau d’échecs à l’aide d’une caméra, c’est-à-dire enregistrer un à un les coups joués sur un plateau
d’échecs physique. Ce suivi des déplacements sera ensuite utilisé pour créer un système qui
permet à un joueur de jouer contre une intelligence artificielle sur échiquier physique.

## Prérequis et dépendances

- Avoir un téléphone Android avec l'application [CameraIP](https://play.google.com/store/apps/details?id=com.pas.webcam&hl=fr&gl=US) et un trépied

- Avoir [Stockfish](https://stockfishchess.org/) installé sur votre ordinateur

- Avoir les différentes dépendances python installées sur votre machine :

```
- OpenCV
- Numpy
- Matplotlib (Pour l'affichage des graphiques)
```

## Utilisation

Pour jouer, vous devrez placer une caméra au-dessus du plateau d'échecs. Cela peut être fait avec votre téléphone en installant [CameraIP](https://play.google.com/store/apps/details?id=com.pas.webcam&hl=fr&gl=US) (disponible uniquement sur android)

Une fois cela fait, vous pouvez simplement utiliser ces instructions en ouvrant un terminal sur votre ordinateur :

    git clone https://github.com/romaric-g/EchecVision
    cd EchecVision/echec_vision
    python main.py

Vous devez ensuite ouvrir l'URL local qui vous donnera acces à une interface web.
Dans celle-ci, vous pourrez alors configurer l'IP de la caméra ainsi que l'emplacement de Stockfish sur votre ordinateur (peut également être fait en modifiant settings.json à la racine du projet).

## Les exemples

Afin d'expérimenter le projet, vous pouvez aussi vous référer aux exemples :

    git clone https://github.com/romaric-g/EchecVision
    cd EchecVision/echec_vision
    cd exemples
    python <nom-de-l-exemple>.py

## Organisation du projets

`core/` : Code principal de l'application

`exemples/` : Exemple de l'application montrant les techniques de traitement d'image

`images/` : Images utilisés ou générés par le projet

`notebooks/` : Code utilisés à des fins d'experimentation

`pok/` : Preuves de concept réalisées avant l'assemblage final du projet

`web/` : Code de l'interface web react.js
