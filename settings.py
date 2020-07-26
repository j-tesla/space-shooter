from os import path

WIDTH = 480
HEIGHT = 600
FPS = 60

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# set up assets folders
game_dir = path.dirname(__file__)
img_dir = path.join(game_dir, 'img')
snd_dir = path.join(game_dir, 'snd')
retro = path.join(img_dir, 'retro.ttf')
