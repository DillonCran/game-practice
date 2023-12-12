WIN_SIZE = WIN_WIDTH, WIN_HEIGHT = 960, 540  # 30 tiles
TILESIZE = 32  # Sets the sprite resolution
FPS = 60  # Sets the game FPS
PLAYER_SPEED = 1  # Sets the player speed
ENEMY_SPEED = 1  # Sets the enemy speed
# Layers (for sprite groups, not for the screen, which is always 0)
PLAYER_LAYER = 4
ENEMY_LAYER = 3
BLOCK_LAYER = 2
GROUND_LAYER = 1

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)
PINK = (255, 192, 203)
BROWN = (165, 42, 42)
GREY = (128, 128, 128)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)

world_map = []

tilemap = [
    "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBB",
    "B                            B",
    "B     E                      B",
    "B    BBB                     B",
    "B                            B",
    "B                            B",
    "B                  E         B",
    "B                            B",
    "B              P             B",
    "B     BBB                    B",
    "B       B                    B",
    "B       B                    B",
    "B                            B",
    "B                            B",
    "B                            B",
    "B                            B",
    "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBB",
]
