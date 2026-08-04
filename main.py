import pygame as pg
import random
import time
import math


class Fish:
    """
    Représente un poisson (boid) : sa position, sa vitesse et son
    comportement de déplacement (recherche de cible + alignement
    avec les voisins).
    """

    def __init__(self):
        # Position initiale aléatoire dans la fenêtre
        self.pos= (random.randint(20, WIDTH), random.randint(20, HEIGHT))

        # Vitesse scalaire (norme du vecteur vitesse), en pixels/seconde
        self.speed = random.randint(90, 300)

        # Point que le poisson essaie de rejoindre
        self.target_x = random.randint(20, WIDTH)
        self.target_y = random.randint(20, HEIGHT)

        # Angle d'orientation du poisson, en degrés
        self.angle = 0

        # Vecteur vitesse (vx, vy)
        self.vector = (0, 0)

        self.close_dx = 0
        self.close_dy = 0

    def draw_fish(self, screen):
        """Dessine le poisson comme un petit polygone orienté selon self.angle,
        plus deux cercles (repères visuels) centrés sur un des sommets."""
        # Points du poisson définis dans un repère local (poisson orienté vers la droite)
        base_points = [
            (0, 0),
            (-15, -7),
            (-9, 0),
            (-15, 7)
        ]

        # On fait pivoter chaque point local selon l'angle du poisson,
        # puis on le translate à la position (self.x, self.y) du poisson
        self.rotated_points = []
        for px, py in base_points:
            v = pg.Vector2(px, py).rotate(self.angle)
            self.rotated_points.append((self.pos[0] + v.x, self.pos[1] + v.y))

        # Corps du poisson
        pg.draw.polygon(screen, (80, 200, 235), self.rotated_points)

        # Cercles de debug: rayon de détection de collision (blanc, 15px)
        # et rayon de détection des voisins pour l'alignement (vert, 100px)
        pg.draw.circle(screen, (255, 255, 255), self.rotated_points[2], 15.0, 2)
        # pg.draw.circle(screen, (10, 180, 10), self.rotated_points[2], 100.0, 2)

    def detect_collision(self, screen, boids: list):
        """Colore le poisson en rouge si un autre boid est trop proche
        (simple détection visuelle, pas d'évitement réel de collision)."""
        count = 0
        for boid in boids:
            if boid is self:
                continue
            dist2 = get_dist2(self, boid)
            if dist2 <= 40.0 * 40.0:
                pg.draw.polygon(screen, (200, 10, 10), self.rotated_points)
                self.close_dx += self.pos[0] - boid.pos[0]
                self.close_dy += self.pos[1] - boid.pos[1]
                count += 1
        if count > 0:
            self.close_dx /= count
            self.close_dy /= count


    def get_average_neigh_speed(self, neighboors):
        """Calcule le vecteur vitesse moyen d'une liste de voisins
        (utilisé pour la règle d'alignement du boid)."""
        sum_x = 0
        sum_y = 0
        count = 0

        for boid in neighboors:
            sum_x += boid.vector[0]
            sum_y += boid.vector[1]
            count += 1

        if count == 0:
            return (0, 0)

        return (sum_x / count, sum_y / count)

    def get_average_pos(self, neighboors):
        sum_x = 0
        sum_y = 0
        count = 0

        for boid in neighboors:
            sum_x += boid.pos[0]
            sum_y += boid.pos[1]
            count += 1

        if count == 0:
            return (0, 0)

        return (sum_x / count, sum_y / count)
        
    def get_neighboor(self, radius, boids) :
        neighboors = []
        for boid in boids:
            if boid is self:
                continue
            dist2 = get_dist2(self, boid)
            if dist2 <= radius:
                neighboors.append(boid)
        return neighboors
    def move_fish(self, dt, boids):
        """Met à jour la position et la vitesse du poisson à chaque frame :
        - se dirige vers sa cible (target_x, target_y)
        - s'aligne avec la vitesse moyenne de ses voisins proches
        - change de cible de temps en temps (aléatoirement)
        """
        # Vecteur et distance vers la cible actuelle
        dx_target = self.target_x - self.pos[0]
        dy_target = self.target_y - self.pos[1]
        distance = math.sqrt(dx_target**2 + dy_target**2)

        

        # Recalcule le vecteur vitesse à partir de l'angle courant

        # Si la cible est atteinte, on en choisit une nouvelle au hasard
        if distance < 5:
            self.target_x = random.randint(20, WIDTH - 20)
            self.target_y = random.randint(20, HEIGHT - 20)

        # Recherche des voisins proches (rayon de 100px, car 10000 = 100^2).
        # Ce rayon correspond au cercle vert dessiné dans draw_fish.
        

        # Vitesse moyenne des voisins -> règle d'alignement
        align_neighboors = self.get_neighboor(10000, boids)
        avg_neighbor_vector = self.get_average_neigh_speed(align_neighboors)

        coh_neighboors = self.get_neighboor(50000, boids)
        avg_pos = self.get_average_pos(coh_neighboors)

        align_factor = 0.08   # poids de l'alignement avec les voisins
        cohesion_factor = 0.05 
        avoid_factor = 0.3
        target_factor = 0.03  # poids de l'attraction vers la cible
        turn_factor = 50
        steer_x = 0
        steer_y = 0
        
        if avg_neighbor_vector != (0, 0):
            steer_x = (avg_neighbor_vector[0] - self.vector[0]) * align_factor
            steer_y = (avg_neighbor_vector[1] - self.vector[1]) * align_factor

        dx = dx_target / distance
        dy = dy_target / distance

        cohesion_vector = (avg_pos[0] - self.pos[0], avg_pos[1] - self.pos[1])

        vx = self.vector[0] + steer_x + dx + self.close_dx * avoid_factor * target_factor * self.speed
        vy = self.vector[1] + steer_y + dy + self.close_dy * avoid_factor * target_factor * self.speed

        vx += cohesion_factor * cohesion_vector[0]
        vy += cohesion_factor * cohesion_vector[1]

        new_speed = math.sqrt(vx * vx + vy * vy)
        max_speed = 300
        min_speed = 170

        if new_speed > max_speed:
            factor = max_speed / new_speed
            vx *= factor
            vy *= factor
            new_speed = max_speed
        elif 0 < new_speed < min_speed:
            factor = min_speed / new_speed
            vx *= factor
            vy *= factor
            new_speed = min_speed

        self.speed = new_speed
        self.vector = (vx, vy)
        self.angle = math.degrees(math.atan2(vy, vx))

        if self.pos[0] < 50 :
            vx += turn_factor
        if self.pos[0] > WIDTH - 50 :
            vx -= turn_factor
        if self.pos[1] < 50 :
            vy += turn_factor
        if self.pos[1] > HEIGHT - 50 :
            vy -= turn_factor

        self.vector = (vx, vy)


        # Mise à jour de la position avec le vecteur vitesse actualisé
        x = self.pos[0] + self.vector[0] * dt
        y = self.pos[1] + self.vector[1] * dt

        
        self.pos = (x,y)

        self.close_dx = 0
        self.close_dy = 0 
        # 1 chance sur 10 à chaque frame de dévier légèrement la cible,
        # pour un mouvement moins prévisible
        if random.randint(1, 10) == 1:
            self.target_x += random.randint(-150, 150)
            self.target_y += random.randint(-150, 150)


def generate_fishes(number):
    """Crée une liste de `number` poissons à des positions aléatoires."""
    fishes = []
    for _ in range(number):
        fishes.append(Fish())
    return fishes


def get_dist2(boid1, boid2):
    """Distance au carré entre deux boids (évite un sqrt inutile pour
    les comparaisons de distance)."""
    dx = boid2.pos[0] - boid1.pos[0]
    dy = boid2.pos[1] - boid1.pos[1]
    return dx * dx + dy * dy


# --- Initialisation de pygame et de la fenêtre ---
pg.init()

WIDTH = 1600
HEIGHT = 1200

screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Fish")

clock = pg.time.Clock()
running = True

fishes = generate_fishes(150)

# --- Boucle principale ---
while running:
    dt = clock.tick(60) / 1000  # delta time en secondes, limité à 60 FPS
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    screen.fill((10, 15, 25))  

    for fish in fishes:
        fish.move_fish(dt, fishes)
        fish.draw_fish(screen)
        fish.detect_collision(screen, fishes)

    pg.display.flip()

pg.quit()
