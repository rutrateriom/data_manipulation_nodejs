# Projet de manipulation de data avec nodejs

## Introduction

Ce projet utilise des scripts en Python et Node.js pour générer et analyser des données clients fictives. L'objectif est de simuler des transactions et de calculer des statistiques intéressantes comme le chiffre d'affaires, la dépense moyenne par client, l'age le plus représenté chez les clients, les produits les plus commandés, etc...

## Prérequis

Avant de commencer, assurez-vous d'avoir les logiciels suivants installés :

- [Node.js](https://nodejs.org/)
- [Python](https://www.python.org/)
- npm
- [git](https://git-scm.com/downloads)

## Installation

Clonez le dépôt et installez les dépendances nécessaires en vous plaçant dans le répertoire désiré.
```bash
git clone https://github.com/rutrateriom/data_manipulation_nodejs.git
cd data_manipulation_nodejs
npm install
```

## Utilisation
### Génération des données
le script python permet de générer des données fictives grace au module faker, il créera un csv de 100 000 lignes, une pour chaque client, qui contiennent chacune leur id, prénom,nom,age, etc ... ainsi que des informations concernant leurs achats.
Pour cela, il faut lancer le script python en se placant dans le répértoire python_scripts et en faisant 
```bash
python generate_data.py
```
attention si le fichier csv clients.csv existe déjà, il ne peut pas être écrasé, pour en créer un nouveau, il faut le supprimer.
Aussi, pas besoin d'installer faker sur sa machine, elle est déjà installée dans le projet.
### Analyse des données
L'analyse des données se fait avec le script extract.js, qui est dans src, il doit y avoir le csv dans le même dossier pour qu'il fonctionne correctement, il faut donc se placer dans src avec un invite de commande et faire:
```bash
node extract.js
```
pour lire un autre fichier csv, disons clients2.csv, il faut l'appeler avec l'argument en plus
```bash
node extract.js --file=clients2.csv
```
les résultats seront affichés directement dans l'invite de commande
## Auteur
Arthur Moiret Bisiaux (arthur59400@hotmail.com)
