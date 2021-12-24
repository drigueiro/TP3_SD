from circle import *
import sys
import time
import multiprocessing as mp
#!pip install pickle-mixin
import _pickle as cPickle

import os
os.environ['SDL_VIDEO_CENTERED'] = '1'
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'
#!pip install pygame
import pygame as gui
import socket

Mensagem01 = "Desejo Ingressar na rede"
Mensagem02 = "Desejo Sair da Rede"
Messagem05= "Topic Mudou"

# Inicializacao da GUI
gui.init()
font = gui.font.SysFont('arial', 8)
gui.display.set_caption('TP3')
#icon = gui.image.load('icon.png')
#gui.display.set_icon(icon)
screen = gui.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGTH))
screen.fill(WHITE)
gui.display.update()
# Lista de circulos
circle_list = []
qtCircles = 0;
NUMBER_CIRCLES = 10
myport = 7070
port=7171
topic = "200.239.138.122"

# Desenha o circulo na tela da GUI
def draw_circle(circle):
    gui.draw.circle(screen, circle.color, circle.pos, circle.size)
    number = font.render(str(circle.id), False, BLACK)
    screen.blit(number, circle.pos)

# Inicializacao da lista de circulos
circle_list =  []


#data = cPickle.dumps(list(circle_list))
print("vai mandar a mensagem para entrar na rede")
tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
dest = (topic, int(myport))
tcp.connect(dest)
data = cPickle.dumps(Mensagem01)
tcp.send(data)
msg = tcp.recv(10000)
print(msg)
if len(msg)>0:
    data = cPickle.loads(msg)

print(data)
for circle in (data):
    draw_circle(Circle(circle));

tcp.close();
flag = 0 ;

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
dest = ("0.0.0.0", int(port))
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(dest)

s.listen(50)
print("pronto para escutar atualizações")


while(flag<=10):
    conexao, ipConexao = s.accept()
    msg = conexao.recv(8096)
    data = cPickle.loads(msg)
    #caso mude de topic Ele manda mensagem e o subscriber manda de volta peqindo

    for circle in (data):
        draw_circle(Circle(circle));

    flag = flag + 1;
    gui.display.update()
    conexao.close()


     # Verifica fim de execucao
    for event in gui.event.get():
      if event.type == gui.QUIT:
        flag = 60
      elif event.type == gui.KEYDOWN:
        if event.key == gui.K_ESCAPE:
          flag = 60
s.close()

print("TOPIC", topic)
finaliza = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
finaliza.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#finaliza.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
print(socket.getaddrinfo(topic, myport))

dest = (topic, int(myport))
finaliza.connect(dest)
data = cPickle.dumps(Mensagem02)
finaliza.send(data)
finaliza.close();
