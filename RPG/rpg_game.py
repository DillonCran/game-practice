import pygame, random, math, sys
from pygame.locals import *
from sprites import *
from config import *


class Game:
    def __init__(self):
        pygame.init()
        # Sets screen size, clock, default font, and game loop
        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        self.clock = pygame.time.Clock()  # Sets clock
        self.font = pygame.font.SysFont("Arial", 30)  # Sets font
        self.running = True  # Sets game loop

        # Fonts
        self.font_roboto = pygame.font.Font(
            "D:\\Projects\\Game\\RPG\\images\\img\\img\\fonts\\Roboto\\Roboto-Medium.ttf",
            32,
        )

        # Spritesheets/Backgrounds
        self.character_spritesheet = Spritesheet(
            "D:\\Projects\\Game\\RPG\\images\\img\\img\\character.png"
        )
        self.terrain_spritesheet = Spritesheet(
            "D:\\Projects\\Game\\RPG\\images\\img\\img\\terrain.png"
        )
        self.enemy_spritesheet = Spritesheet(
            "D:\\Projects\\Game\\RPG\\images\\img\\img\\enemy.png"
        )
        self.intro_background = pygame.image.load(
            "D:\\Projects\\Game\\RPG\\images\\img\\img\\introbackground.png"
        )
        self.game_over_background = pygame.image.load(
            "D:\\Projects\\Game\\RPG\\images\\img\\img\\gameover.png"
        )
        self.attack_spritesheet = Spritesheet(
            "D:\\Projects\\Game\\RPG\\images\\img\\img\\attack.png"
        )

    def create_tilemap(self):
        # Creates tilemap
        # Iterates through tilemap, enumerating gives row number
        for row, tiles in enumerate(tilemap):
            for col, tile in enumerate(tiles):
                Ground(self, col, row)
                if tile == "B":
                    Block(self, col, row)
                if tile == "P":
                    self.player = Player(self, col, row)  # Creates player object
                if tile == "E":
                    Enemy(self, col, row)
                    """
                if tile == " ":
                    Grass(self, col, row)
                    """

    def camera(self, target):
        def __init__(self, width, height):
            self.rect = pygame.Rect(0, 0, width, height)
            self.width = width
            self.height = height

        def update(self, target):
            x = target.rect.centerx - int(width / 2)
            y = target.rect.centery - int(height / 2)

            # limit scrolling
            x = max(0, x)  # left
            y = max(0, y)  # top

            x = min((bg_width - width), x)
            y = min((bg_height - height), y)

            self.rect = pygame.Rect(x, y, self.width, self.height)

    def new(self):
        # New game starts
        self.playing = True

        # Sprite groups
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.LayeredUpdates()
        self.attacks = pygame.sprite.LayeredUpdates()

        # Creates tilemap
        self.create_tilemap()

    def events(self):
        # game loop events
        # gets every event in pygame, iterates through them
        for event in pygame.event.get():
            # Check for closing window
            if event.type == pygame.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False

    def update(self):
        # game loop update
        self.all_sprites.update()
        self.camera(self.player)

    def draw(self):
        # draws and renders game objects
        self.screen.fill(BLACK)  # fills screen with black
        self.all_sprites.draw(self.screen)  # draws sprites on screen
        self.clock.tick(FPS)  # sets game FPS
        pygame.display.update()  # updates screen

    def main(self):
        # game loop
        while self.playing:
            self.events()  # Listening for inputs
            self.update()  # Updating sprites
            self.draw()  # Drawing sprites

    def game_over(self):
        game_over = True
        end_text = self.font.render("Game Over", True, WHITE)
        end_text_rect = end_text.get_rect(center=(WIN_WIDTH / 2, WIN_HEIGHT / 2))

        restart_button = Button(100, 150, 120, 50, WHITE, BLACK, "Restart", 32)

        for sprite in self.all_sprites:
            sprite.kill()

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            mouse_pos = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()

            if restart_button.is_pressed(mouse_pos, click):
                self.new()
                self.main()

            self.screen.blit(self.game_over_background, (0, 0))
            self.screen.blit(end_text, end_text_rect)
            self.screen.blit(
                restart_button.image, (restart_button.rect.x, restart_button.rect.y)
            )
            self.clock.tick(FPS)
            pygame.display.update()

    def intro_screen(self):
        # Intro screen
        # temp variable for loop
        intro = True
        # Creates title and play button
        title = self.font.render("RPG Game", True, BLACK)
        # Gets rect of title and centers it
        title_rect = title.get_rect(center=(WIN_WIDTH / 2, WIN_HEIGHT - 500))
        # Creates play button
        play_button = Button(10, 15, 100, 50, WHITE, BLACK, "Play", 32)
        #
        while intro:
            # Checks for quit event
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    intro = False
                    self.running = False

            # assign variable for mouse position and click
            mouse_pos = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()

            # Closes intro screen if play button is pressed
            if play_button.is_pressed(mouse_pos, click):
                intro = False

            # Update the position of the button to center it on the intro screen
            play_button.update_position(WIN_WIDTH, WIN_HEIGHT)

            # Draws intro screen
            self.screen.blit(self.intro_background, (0, 0))
            self.screen.blit(title, title_rect)
            self.screen.blit(
                play_button.image, (play_button.rect.x, play_button.rect.y)
            )

            self.clock.tick(FPS)
            pygame.display.update()


# Creates game object
g = Game()
g.intro_screen()
g.new()
# Game loop
while g.running:
    g.main()
    g.game_over()

# Quits game when game loop is broken
pygame.quit()
sys.exit()
