# 🐟 Boids — Simulation de Banc de Poissons

![Aperçu de la simulation](misc/Enregistrement%202026-08-03%20183639.gif)

Cette simulation repose sur l'algorithme des **Boids** (*Craig Reynolds, 1986*). Chaque agent (poisson) ajuste sa trajectoire selon des règles locales simples, faisant émerger un comportement collectif complexe au sein d'un espace 2D de $1600 \times 1200$ pixels.

---

## 📐 Modélisation Mathématique

### 1. Intégration Temporelle
Pour garantir l'indépendance de la simulation vis-à-vis du taux de rafraîchissement (FPS), le déplacement est calculé via un schéma d'Euler explicite :

$$\mathbf{p}(t + \Delta t) = \mathbf{p}(t) + \mathbf{v}(t) \cdot \Delta t$$

où $\mathbf{p} = (x, y)^T$ est la position, $\mathbf{v} = (v_x, v_y)^T$ le vecteur vitesse et $\Delta t = \frac{\text{tick}}{1000}$ le temps écoulé en secondes.

### 2. Optimisation des Distances
Afin d'éviter le coût calculatoire de la racine carrée $\sqrt{x}$, la proximité entre deux poissons $i$ et $j$ est évaluée via la distance euclidienne au carré :

$$d^2(i, j) = (x_j - x_i)^2 + (y_j - y_i)^2$$

Un poisson $j$ appartient au voisinage $\mathcal{N}_i$ du poisson $i$ si $d^2(i, j) \le R_{\text{align}}^2$ (avec $R_{\text{align}} = 100\text{ px}$).

### 3. Orientation et Transformation
La géométrie locale du poisson est orientée selon son vecteur vitesse :

$$\theta = \arctan2(v_y, v_x)$$

Chaque sommet local $\mathbf{p}_{\text{local}}$ subit une rotation 2D puis une translation vers la position absolue sur l'écran :

$$\mathbf{p}_{\text{écran}} = \begin{pmatrix} \cos\theta & -\sin\theta \\ \sin\theta & \cos\theta \end{pmatrix} \mathbf{p}_{\text{local}} + \mathbf{p}$$

### 4. Force d'Attraction vers la Cible (*Seeking*)
Chaque poisson vise une cible dynamique $\mathbf{c} = (x_{\text{target}}, y_{\text{target}})^T$. Le vecteur direction unitaire $\hat{\mathbf{u}}_{\text{target}}$ et la force associée s'écrivent :

$$\hat{\mathbf{u}}_{\text{target}} = \frac{\mathbf{c} - \mathbf{p}}{\|\mathbf{c} - \mathbf{p}\|}$$

$$\mathbf{F}_{\text{target}} = \hat{\mathbf{u}}_{\text{target}} \cdot k_{\text{target}} \cdot \|\mathbf{v}\|$$

### 5. Règle d'Alignement Local
Chaque poisson adapte sa vitesse à la vitesse moyenne de son voisinage $\mathcal{N}_i$ ($N = |\mathcal{N}_i|$) :

$$\bar{\mathbf{v}} = \frac{1}{N} \sum_{j \in \mathcal{N}_i} \mathbf{v}_j$$

La force de correction d'alignement (*steering*) est déterminée par un contrôle proportionnel :

$$\mathbf{F}_{\text{align}} = \alpha \cdot (\bar{\mathbf{v}} - \mathbf{v}_i) \quad \text{avec } \alpha = 0.05$$

### 6. Superposition et Borne de Vitesse (*Clamping*)
Le nouveau vecteur vitesse résulte de la somme vectorielle des forces :

$$\mathbf{v}' = \mathbf{v} + \mathbf{F}_{\text{align}} + \mathbf{F}_{\text{target}}$$

Sa norme est contrainte dans l'intervalle $[v_{\min}, v_{\max}] = [50, 300]\text{ px/s}$ tout en conservant sa direction :

$$\mathbf{v}_{\text{final}} = \begin{cases} 
v_{\max} \cdot \dfrac{\mathbf{v}'}{\|\mathbf{v}'\|} & \text{si } \|\mathbf{v}'\| > v_{\max} \\[10pt]
v_{\min} \cdot \dfrac{\mathbf{v}'}{\|\mathbf{v}'\|} & \text{si } \|\mathbf{v}'\| < v_{\min} \\[10pt]
\mathbf{v}' & \text{sinon}
\end{cases}$$

---

## 🚀 Perspectives : Complétion du Modèle de Reynolds

L'implémentation actuelle repose sur l'**alignement** et la poursuite d'une cible individuelle. Pour obtenir un modèle complet de boids, deux règles clés seront intégrées prochainement :

1. **Séparation (Répulsion localisée) :** Force répulsive inversement proportionnelle à la distance pour éviter les chevauchements et collisions entre poissons proches :
   $$\mathbf{F}_{\text{sepa}} = \sum_{j \in \mathcal{N}_{\text{proche}}} \frac{\mathbf{p}_i - \mathbf{p}_j}{\|\mathbf{p}_i - \mathbf{p}_j\|^2}$$

2. **Cohésion (Attraction vers le centre de masse) :** Force d'attraction dirigée vers le barycentre $\mathbf{g}_i$ des voisins pour maintenir la cohérence du groupe sans cible artificielle :
   $$\mathbf{g}_i = \frac{1}{N} \sum_{j \in \mathcal{N}_i} \mathbf{p}_j \implies \mathbf{F}_{\text{cohes}} = \beta \cdot (\mathbf{g}_i - \mathbf{p}_i)$$
