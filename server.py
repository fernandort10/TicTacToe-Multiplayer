import pygame
from grid import Cuadricula

import os
os.environ['SDL_VIDEO_WINDOW_POS'] = '200,100'

surface = pygame.display.set_mode((600,600))
pygame.display.set_caption('CherryMataHaraka')

import threading
def create_thread(target):
    thread = threading.Thread(target=target)
    thread.daemon = True
    thread.start()

#Crear el TCP socket para el server
import socket
HOST = '127.0.0.1'
PUERTO = 65432
conexion_establecida = False
conn, addr = None, None

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((HOST, PUERTO))
sock.listen(1)

def recibir_data():
    global turn
    while True:
        data = conn.recv(1024).decode()
        data = data.split('-')
        x, y = int(data[0]), int(data[1])
        if data[2] == 'yourturn':
            turn = True
        if data[3] == 'False':
            grid.game_over = True
        if grid.get_valor_celda(x, y) == 0:
            grid.set_valor_celda(x, y, 'Haraka')

def esperando_conexion():
    global conexion_establecida, conn, addr
    conn, addr = sock.accept()
    print('client is connected')
    conexion_establecida = True
    recibir_data()


create_thread(esperando_conexion)

grid = Cuadricula()
encendido = True
jugador = "Cherry"
turn = True
jugando = 'True'

while encendido:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            encendido = False
        if event.type == pygame.MOUSEBUTTONDOWN and conexion_establecida:
            if pygame.mouse.get_pressed()[0]:
                if turn and not grid.game_over:
                    pos = pygame.mouse.get_pos()
                    cellX, cellY = pos[0] // 200, pos[1] // 200
                    grid.get_mouse(cellX, cellY, jugador)
                    if grid.game_over:
                        jugando = 'False'
                    send_data = '{}-{}-{}-{}'.format(cellX, cellY, 'yourturn', jugando).encode()
                    conn.send(send_data)
                    turn = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and grid.game_over:
                grid.limpiar_cuadricula()
                grid.game_over = False
                jugando = 'True'
            elif event.key == pygame.K_ESCAPE:
                encendido = False


    surface.fill((0,0,0))

    grid.dibujar(surface)

    pygame.display.flip()