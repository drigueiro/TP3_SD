# Instanciacao da classe Circulo
# e de variaveis uteis para o programa
import random

# Cores para a GUI
BLACK  = (  0,   0,   0)
WHITE  = (255, 255, 255)
RED    = (255,  63,  63)
GREEN  = (  0, 240,  15)
BLUE   = ( 64, 127, 255)
YELLOW = (255, 239,   0)
PURPLE = (200,  15, 255)
CYAN   = (  0, 239, 255)
ORANGE = (239, 127,   0)
COLORS = [RED, GREEN, BLUE, YELLOW, PURPLE, CYAN, ORANGE]

# Tamanho da tela
SCREEN_WIDTH  = 1000
SCREEN_HEIGTH = 640

# Raio minimo e maximo dos circulos
MIN_RADIUS = 2
MAX_RADIUS = 12

# Classe circulo, possui cor, raio,
# identificador e posicao X e Y

def CreateCircle(id):
    color = random.choice(COLORS)
    pos = (random.randint(MAX_RADIUS, SCREEN_WIDTH  - MAX_RADIUS),
                random.randint(MAX_RADIUS, SCREEN_HEIGTH - MAX_RADIUS))
    size = random.randint(MIN_RADIUS, MAX_RADIUS)
    return (id,color,pos, size)

class Circle():
  def __init__(self,circle):

    self.id = circle[0] + 1
    self.color = circle[1]
    self.pos = circle[2]
    self.size = circle[3]

  # Troca a cor do circulo
  def update_color(self):
    self.color = random.choice(COLORS)

  # Troca a posicao do circulo
  def update_position(self):
    self.pos = (random.randint(MAX_RADIUS, SCREEN_WIDTH  - MAX_RADIUS),
                random.randint(MAX_RADIUS, SCREEN_HEIGTH - MAX_RADIUS))

  # Troca o raio do circulo
  def update_size(self):
    self.size = random.randint(MIN_RADIUS, MAX_RADIUS)

  # Lista das funcoes de update
  update_functions = [update_color, update_position, update_size]
