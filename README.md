# 🐟 Boids — Simulation de Banc de Poissons

![Aperçu de la simulation](misc/Enregistrement%202026-08-03%20183639.gif)

Ce projet propose une simulation du comportements d'un banc poissons, développée à l'aide de la bibliothèque Pygame. Chaque individu ajuste son déplacement en temps réel afin de naviguer de manière fluide dans son environnement tout en interagissant avec ses congénères.

---

## ⚙️ Principe de l'Algorithme

Le déplacement de chaque poisson est régi par des règles simples de cinématique et d'interaction de voisinage. Chaque poisson est défini par sa position $P = (x, y)$, son vecteur vitesse $\vec{v}$, et un angle d'orientation $\theta$.

Le mouvement se décompose en deux forces principales :

1. 🎯 **L'attraction vers une cible** : Chaque poisson se dirige vers une coordonnée cible $T = (x_{target}, y_{target})$ qui lui est propre. Dès qu'un poisson s'approche suffisamment de sa cible, une nouvelle destination est définie aléatoirement sur la carte.
2. 🔄 **L'alignement avec le voisinage** : C'est le premier principe de comportement de groupe. Chaque poisson scrute son environnement dans un rayon d'interaction $R$. Il calcule le vecteur vitesse moyen $\vec{v}_{\mathrm{moyen}}$ de tous les voisins situés dans cette zone :

$$
\vec{v}_{\mathrm{moyen}} = \frac{1}{N} \sum_{i=1}^{N} \vec{v}_{\mathrm{voisin}, i}
$$

Le poisson applique ensuite une force de correction pour harmoniser sa propre direction avec celle du groupe.

Les vitesses minimale $s_{min}$ et maximale $s_{max}$ sont encadrées à chaque étape temporelle $\Delta t$ afin de garantir la stabilité visuelle de la simulation.

---

## 🎨 Représentation Visuelle

Chaque poisson est modélisé par un polygone orienté selon son angle de déplacement $\theta$. Pour faciliter l'observation et le débogage de la simulation, deux zones d'influence sont dessinées autour de chaque individu :

* 🟢 **Le cercle vert de rayon $R = 100$** : Représente la limite de perception sensorielle du poisson. C'est à l'intérieur de cette zone que les voisins sont pris en compte pour calculer l'alignement.
* ⚪ **Le cercle blanc de rayon $r = 15$** : Représente la zone de sécurité immédiate. Si un autre poisson pénètre dans ce cercle, le poisson change de couleur et devient rouge, signalant graphiquement une situation de collision.

---

## 🚀 Perspectives d'Évolution

Afin d'obtenir une simulation de groupe plus complète et réaliste, le modèle actuel (qui repose uniquement sur l'alignement et la recherche de cible) est conçu pour intégrer prochainement les deux autres forces :

* 🛡️ **La Séparation** : Ajout d'une force répulsive active. Lorsque le cercle de collision blanc ($r = 15$) est violé, le poisson appliquera une force opposée à la direction du voisin trop proche pour s'en écarter et éviter les superpositions.
* 🤝 **La Cohésion** : Ajout d'une force attractive vers le centre de masse du groupe. Le poisson calculera la position moyenne de ses voisins dans le cercle vert ($R = 100$) et cherchera à s'en rapprocher, évitant ainsi que les individus ne s'isolent de manière isolée.
