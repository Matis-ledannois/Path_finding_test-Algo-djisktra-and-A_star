"""
Visualisation d'algorithmes de pathfinding (Dijkstra et A*)
Conversion depuis JavaScript vers Python avec Pygame

Dépendances :
    pip install pygame

Contrôles :
    i : Réinitialiser l'algorithme
    n : Générer une nouvelle map
    s : Changer d'algorithme
"""

import pygame
import random
import math
import time
from typing import List, Tuple, Dict, Optional
from dataclasses import dataclass

# Configuration
FPS = 120
GRID_WIDTH = 50
GRID_HEIGHT = 40
CELL_SIZE = 20
CANVAS_WIDTH = GRID_WIDTH * CELL_SIZE
CANVAS_HEIGHT = GRID_HEIGHT * CELL_SIZE

# Couleurs
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)


@dataclass
class Coord:
    """Structure pour stocker des coordonnées"""
    x: int
    y: int


@dataclass
class Node:
    """Structure pour les nœuds dans A*"""
    x: int
    y: int
    cout: float = 0.0
    heuristique: float = 0.0


class PathfindingVisualizer:
    """Classe principale pour la visualisation des algorithmes"""
    
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((CANVAS_WIDTH, CANVAS_HEIGHT))
        pygame.display.set_caption("Algorithmes de Pathfinding")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 24)
        
        # Variables globales
        self.map = self.create_array(GRID_WIDTH, GRID_HEIGHT)
        self.type_algo = 0  # 0=Dijkstra, 1=A*
        self.tps_touche = self.get_time_milli()
        
        # Variables pour Dijkstra
        self.distance = self.create_array(GRID_WIDTH, GRID_HEIGHT)
        self.Q = self.create_array(GRID_WIDTH, GRID_HEIGHT)
        self.predecesseur = self.create_array(GRID_WIDTH, GRID_HEIGHT)
        self.pos_depart = 0
        self.pos_fin = 0
        self.chemin_trouve = False
        
        # Variables pour A*
        self.g_score = self.create_array(GRID_WIDTH, GRID_HEIGHT)
        self.f_score = self.create_array(GRID_WIDTH, GRID_HEIGHT)
        self.open_set: List[Coord] = []
        
        # État des touches
        self.key_presses = {}
        self.running = True
        
        # Initialisation
        self.init()
    
    def create_array(self, *dimensions) -> List:
        """Crée un tableau multidimensionnel (équivalent createArray)"""
        if len(dimensions) == 1:
            return [0] * dimensions[0]
        else:
            return [self.create_array(*dimensions[1:]) for _ in range(dimensions[0])]
    
    def get_random(self, min_val: int, max_val: int) -> int:
        """Retourne un nombre aléatoire entre min et max inclus"""
        return random.randint(min_val, max_val)
    
    def get_time_milli(self) -> int:
        """Retourne le temps en millisecondes"""
        return int(time.time() * 1000)
    
    def init(self):
        """Initialisation de la map et des algorithmes"""
        # Remise à zéro de la map
        for i in range(GRID_WIDTH):
            for j in range(GRID_HEIGHT):
                self.map[i][j] = 0
                # Génération des murs sur les bords
                if i == 0 or j == 0 or i == GRID_WIDTH - 1 or j == GRID_HEIGHT - 1:
                    self.map[i][j] = 9
        
        # Position aléatoire du départ et de la fin
        self.pos_depart = self.get_random(1, GRID_HEIGHT - 2)
        self.pos_fin = self.get_random(1, GRID_HEIGHT - 2)
        self.map[1][self.pos_depart] = 1
        self.map[GRID_WIDTH - 2][self.pos_fin] = 2
        
        # Génération des obstacles
        for _ in range(15):
            x = self.get_random(5, GRID_WIDTH - 6)
            y = self.get_random(5, GRID_HEIGHT - 6)
            taille = self.get_random(2, 5)
            
            for j in range(x - taille, x + taille + 1):
                for k in range(y - taille, y + taille + 1):
                    # Pas d'obstacle sur le départ ou l'arrivée
                    if (j != 1 and j != GRID_WIDTH - 2 and 
                        0 <= j < GRID_WIDTH and 0 <= k < GRID_HEIGHT):
                        self.map[j][k] = 9
        
        # Initialisation des algorithmes
        self.dijkstra_init()
        self.astar_init()
        self.tps_touche = self.get_time_milli()
    
    # ========== DIJKSTRA ==========
    
    def dijkstra_init(self):
        """Initialisation de l'algorithme de Dijkstra"""
        self.chemin_trouve = False
        for i in range(GRID_WIDTH):
            for j in range(GRID_HEIGHT):
                self.distance[i][j] = 99999
                self.Q[i][j] = True
                if self.map[i][j] == 8:
                    self.map[i][j] = 0
        
        self.distance[1][self.pos_depart] = 0
        self.predecesseur = self.create_array(GRID_WIDTH, GRID_HEIGHT)
    
    def dijkstra_trouve_min(self) -> Optional[Coord]:
        """Trouve le sommet avec la distance minimale"""
        mini = 99999
        sommet_x, sommet_y = -1, -1
        
        for i in range(GRID_WIDTH):
            for j in range(GRID_HEIGHT):
                if self.Q[i][j] and self.map[i][j] <= 2:
                    if self.distance[i][j] < mini:
                        mini = self.distance[i][j]
                        sommet_x, sommet_y = i, j
        
        return Coord(sommet_x, sommet_y) if sommet_x != -1 else None
    
    def dijkstra_poids(self, x1: int, y1: int, x2: int, y2: int) -> float:
        """Calcule le poids entre deux points"""
        if self.map[x2][y2] > 2:
            return 99999  # Impossible de passer
        elif x1 == x2 or y1 == y2:
            return 1  # Case adjacente
        else:
            return 1.5  # Diagonale (favorise chemin droit)
    
    def dijkstra_maj_distances(self, x1: int, y1: int, x2: int, y2: int):
        """Met à jour les distances"""
        poids = self.dijkstra_poids(x1, y1, x2, y2)
        if self.distance[x2][y2] > self.distance[x1][y1] + poids:
            self.distance[x2][y2] = self.distance[x1][y1] + poids
            self.predecesseur[x2][y2] = Coord(x1, y1)
    
    def dijkstra_tout_parcouru(self) -> bool:
        """Vérifie si tous les nœuds ont été parcourus"""
        for i in range(GRID_WIDTH):
            for j in range(GRID_HEIGHT):
                if self.Q[i][j]:
                    return False
        return True
    
    def dijkstra(self):
        """Exécution d'une itération de Dijkstra"""
        if not self.dijkstra_tout_parcouru() and not self.chemin_trouve:
            paire = self.dijkstra_trouve_min()
            
            if paire and paire.x != -1:
                self.Q[paire.x][paire.y] = False
                
                # Exploration des voisins (8 directions)
                for i in range(-1, 2):
                    for j in range(-1, 2):
                        if not (i == 0 and j == 0):
                            nx, ny = paire.x + i, paire.y + j
                            if 0 <= nx < GRID_WIDTH and 0 <= ny < GRID_HEIGHT:
                                self.dijkstra_maj_distances(paire.x, paire.y, nx, ny)
        
        # Reconstruction du chemin
        cur_x, cur_y = GRID_WIDTH - 2, self.pos_fin
        if self.predecesseur[cur_x][cur_y] != 0:
            self.chemin_trouve = True
            while not (cur_x == 1 and cur_y == self.pos_depart):
                if (not (cur_x == GRID_WIDTH - 2 and cur_y == self.pos_fin) and 
                    not (cur_x == 1 and cur_y == self.pos_depart)):
                    self.map[cur_x][cur_y] = 8
                
                pred = self.predecesseur[cur_x][cur_y]
                if isinstance(pred, Coord):
                    cur_x, cur_y = pred.x, pred.y
                else:
                    break
    
    # ========== A* ==========
    
    def astar_init(self):
        """Initialisation de l'algorithme A*"""
        self.chemin_trouve = False
        for i in range(GRID_WIDTH):
            for j in range(GRID_HEIGHT):
                self.g_score[i][j] = 99999
                self.f_score[i][j] = 99999
                self.Q[i][j] = True
                if self.map[i][j] == 8:
                    self.map[i][j] = 0
        
        self.g_score[1][self.pos_depart] = 0
        self.f_score[1][self.pos_depart] = self.astar_h(1, self.pos_depart)
        self.predecesseur = self.create_array(GRID_WIDTH, GRID_HEIGHT)
        self.open_set = [Coord(1, self.pos_depart)]
    
    def astar_h(self, x: int, y: int) -> float:
        """Fonction heuristique (distance euclidienne à l'arrivée)"""
        return math.sqrt(
            (GRID_WIDTH - 2 - x) ** 2 + (self.pos_fin - y) ** 2
        )
    
    def astar_recherche(self) -> Optional[Dict]:
        """Recherche du nœud avec le plus petit fScore dans openSet"""
        if not self.open_set:
            return None
        
        mini = 99999
        sommet_x, sommet_y, indice = -1, -1, -1
        
        for i, node in enumerate(self.open_set):
            if self.f_score[node.x][node.y] < mini:
                mini = self.f_score[node.x][node.y]
                sommet_x, sommet_y = node.x, node.y
                indice = i
        
        return {'x': sommet_x, 'y': sommet_y, 'i': indice}
    
    def astar_pas_present(self, x: int, y: int) -> bool:
        """Vérifie si un nœud n'est pas dans openSet"""
        return not any(node.x == x and node.y == y for node in self.open_set)
    
    def astar(self):
        """Exécution d'une itération de A*"""
        if self.open_set and not self.chemin_trouve:
            current = self.astar_recherche()
            
            if current and current['x'] != -1:
                # Arrivée trouvée ?
                if current['x'] == GRID_WIDTH - 2 and current['y'] == self.pos_fin:
                    # Reconstruction du chemin
                    cur_x, cur_y = GRID_WIDTH - 2, self.pos_fin
                    self.chemin_trouve = True
                    
                    while not (cur_x == 1 and cur_y == self.pos_depart):
                        if (not (cur_x == GRID_WIDTH - 2 and cur_y == self.pos_fin) and 
                            not (cur_x == 1 and cur_y == self.pos_depart)):
                            self.map[cur_x][cur_y] = 8
                        
                        pred = self.predecesseur[cur_x][cur_y]
                        if isinstance(pred, Coord):
                            cur_x, cur_y = pred.x, pred.y
                        else:
                            break
                    
                    self.open_set.clear()
                    return
                
                # Retirer le nœud courant
                self.open_set.pop(current['i'])
                
                # Explorer les voisins
                for i in range(-1, 2):
                    for j in range(-1, 2):
                        if not (i == 0 and j == 0):
                            nx, ny = current['x'] + i, current['y'] + j
                            
                            if 0 <= nx < GRID_WIDTH and 0 <= ny < GRID_HEIGHT:
                                tentative_g = (self.g_score[current['x']][current['y']] + 
                                             self.dijkstra_poids(current['x'], current['y'], nx, ny))
                                
                                if tentative_g < self.g_score[nx][ny]:
                                    self.predecesseur[nx][ny] = Coord(current['x'], current['y'])
                                    self.g_score[nx][ny] = tentative_g
                                    self.f_score[nx][ny] = self.g_score[nx][ny] + self.astar_h(nx, ny)
                                    
                                    if self.astar_pas_present(nx, ny):
                                        self.open_set.append(Coord(nx, ny))
                                        self.Q[nx][ny] = False
    
    # ========== RENDU ==========
    
    def render(self):
        """Fonction de rendu du canvas"""
        # Fond noir
        self.screen.fill(BLACK)
        
        # Grille
        for i in range(GRID_WIDTH + 1):
            pygame.draw.line(self.screen, WHITE, (i * CELL_SIZE, 0), 
                           (i * CELL_SIZE, CANVAS_HEIGHT), 1)
        for i in range(GRID_HEIGHT + 1):
            pygame.draw.line(self.screen, WHITE, (0, i * CELL_SIZE), 
                           (CANVAS_WIDTH, i * CELL_SIZE), 1)
        
        # Exécution de l'algorithme
        if self.type_algo == 0:
            self.dijkstra()
        else:
            self.astar()
        
        # Affichage des éléments de la grille
        for i in range(GRID_WIDTH):
            for j in range(GRID_HEIGHT):
                x, y = i * CELL_SIZE, j * CELL_SIZE
                
                # Départ (bleu avec "D")
                if self.map[i][j] == 1:
                    pygame.draw.rect(self.screen, BLUE, (x + 1, y + 1, 18, 18))
                    text = self.font.render("D", True, WHITE)
                    self.screen.blit(text, (x + 5, y + 2))
                
                # Arrivée (rouge avec "F")
                elif self.map[i][j] == 2:
                    pygame.draw.rect(self.screen, RED, (x + 1, y + 1, 18, 18))
                    text = self.font.render("F", True, WHITE)
                    self.screen.blit(text, (x + 5, y + 2))
                
                # Mur (blanc)
                elif self.map[i][j] == 9:
                    pygame.draw.rect(self.screen, WHITE, (x + 1, y + 1, 18, 18))
                
                # Chemin final (jaune)
                elif self.map[i][j] == 8:
                    pygame.draw.rect(self.screen, YELLOW, (x + 1, y + 1, 18, 18))
                
                # Zones explorées (petits carrés rouges)
                if (not self.Q[i][j] and 
                    not (i == 1 and j == self.pos_depart) and 
                    not (i == GRID_WIDTH - 2 and j == self.pos_fin)):
                    pygame.draw.rect(self.screen, RED, (x + 7, y + 7, 5, 5))
        
        # Affichage du nom de l'algorithme
        algo_name = "Dijkstra" if self.type_algo == 0 else "A Star"
        text = self.font.render(algo_name, True, RED)
        self.screen.blit(text, (5, 5))
        
        pygame.display.flip()
    
    def handle_events(self):
        """Gestion des événements"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            elif event.type == pygame.KEYDOWN:
                self.key_presses[event.key] = True
                
                # Réinitialiser l'algorithme
                if event.key == pygame.K_i:
                    if self.type_algo == 0:
                        self.dijkstra_init()
                    else:
                        self.astar_init()
                
                # Nouvelle map
                elif event.key == pygame.K_n:
                    self.init()
                
                # Changer d'algorithme
                elif event.key == pygame.K_s:
                    if self.get_time_milli() - self.tps_touche > 500:
                        self.tps_touche = self.get_time_milli()
                        self.type_algo = (self.type_algo + 1) % 2
                        if self.type_algo == 0:
                            self.dijkstra_init()
                        else:
                            self.astar_init()
            
            elif event.type == pygame.KEYUP:
                if event.key in self.key_presses:
                    self.key_presses[event.key] = False
    
    def run(self):
        """Boucle principale"""
        while self.running:
            self.handle_events()
            self.render()
            self.clock.tick(FPS)
        
        pygame.quit()


if __name__ == "__main__":
    app = PathfindingVisualizer()
    app.run()
