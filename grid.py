import pygame
import os

Cherry = pygame.image.load(os.path.join('Recursos', 'Cherry.png'))
Haraka = pygame.image.load(os.path.join('Recursos', 'Haraka.png'))


class Cuadricula:
    def __init__(self):
        self.grid_lines = [((0,200), (600,200)), # first horizontal line
                           ((0,400), (600,400)), # second horizontal line
                           ((200,0), (200,600)), # first vertical line
                           ((400,0), (400,600))] # second vertical line

        self.grid = [[0 for x in range(3)] for y in range(3)]
        # search directions  N         NW        W       SW       S       SE      E       NE
        self.search_dirs = [(0, -1), (-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1)]
        self.game_over = False

    def dibujar(self, surface):
        for line in self.grid_lines:
            pygame.draw.line(surface, (200,200,200), line[0], line[1], 2)

        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                if self.get_valor_celda(x, y) == "Cherry":
                    surface.blit(Cherry, (x * 200, y * 200))
                elif self.get_valor_celda(x, y) == "Haraka":
                    surface.blit(Haraka, (x * 200, y * 200))

    def get_valor_celda(self, x, y):
        return self.grid[y][x]

    def set_valor_celda(self, x, y, value):
        self.grid[y][x] = value

    def get_mouse(self, x, y, player):
        if self.get_valor_celda(x, y) == 0:
            self.set_valor_celda(x, y, player)
            self.checkear_cuadricula(x, y, player)

    def está_entre_los_limites(self, x, y):
        return x >= 0 and x < 3 and y >= 0 and y < 3

    def checkear_cuadricula(self, x, y, jugador):
        count = 1
        for index, (dirx, diry) in enumerate(self.search_dirs):
            if self.está_entre_los_limites(x + dirx, y + diry) and self.get_valor_celda(x + dirx, y + diry) == jugador:
                count += 1
                xx = x + dirx
                yy = y + diry
                if self.está_entre_los_limites(xx + dirx, yy + diry) and self.get_valor_celda(xx + dirx, yy + diry) == jugador:
                    count += 1
                    if count == 3:
                        break
                if count < 3:
                    nueva_direc = 0

                    if index == 0:
                        nueva_direc = self.search_dirs[4]
                    elif index == 1:
                        nueva_direc = self.search_dirs[5]
                    elif index == 2:
                        nueva_direc = self.search_dirs[6]
                    elif index == 3:
                        nueva_direc = self.search_dirs[7]
                    elif index == 4:
                        nueva_direc = self.search_dirs[0]
                    elif index == 5:
                        nueva_direc = self.search_dirs[1]
                    elif index == 6:
                        nueva_direc = self.search_dirs[2]
                    elif index == 7:
                        nueva_direc = self.search_dirs[3]

                    if self.está_entre_los_limites(x + nueva_direc[0], y + nueva_direc[1]) \
                            and self.get_valor_celda(x + nueva_direc[0], y + nueva_direc[1]) == jugador:
                        count += 1
                        if count == 3:
                            break
                    else:
                        count = 1

        if count == 3:
            print('Ganó', jugador, 'buen palomo!')
            self.game_over = True
        else:
            self.game_over = self.está_llena_la_cuadricula()


    def está_llena_la_cuadricula(self):
        for fila in self.grid:
            for value in fila:
                if value == 0:
                    return False
        return True

    def limpiar_cuadricula(self):
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                self.set_valor_celda(x, y, 0)

    def imprimir_cuadricula(self):
        for fila in self.grid:
            print(fila)