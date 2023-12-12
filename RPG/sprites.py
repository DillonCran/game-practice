from typing import Any
import pygame
from pygame.sprite import Group, Group
from config import *
import sys
import math
import random

# SPRITES NEEDED:
# Player (DONE)
# Enemy (DONE)
# Block
# Grass (DONE)
# Attack
# Item
# NPC
# Door
# Chest
# Sign
# Portal
# Stairs
# Trap
# Water
# Lava
# Ladder
# Bridge
# Tree
# Bush
# Rock


class Spritesheet:
    def __init__(self, file):
        # loads spritesheet
        self.sheet = pygame.image.load(file).convert()

    def get_sprite(self, x, y, width, height):
        # gets sprite from sheet
        sprite = pygame.Surface([width, height])
        # blits sprite from sheet to sprite surface
        # (x,y) is the top left corner of the sprite on the sheet, using the width and height of the sprite
        sprite.blit(self.sheet, (0, 0), (x, y, width, height))
        # sets colorkey of sprite to black
        sprite.set_colorkey(BLACK)
        # returns sprite
        return sprite


class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = PLAYER_LAYER  # Sets player layer
        self.groups = self.game.all_sprites  # Sets player sprite group
        pygame.sprite.Sprite.__init__(self, self.groups)  # Initializes player sprite

        # Set player x/y by tiles
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        # temp variables for player movement
        self.x_change = 0
        self.y_change = 0

        self.facing = "down"  # Sets default player facing direction for animation
        self.animation_loop = 1  # Sets default player animation frame

        # Set player image
        # This calls the spritesheet class and gets the sprite from the sheet
        # There is some empty space on the sheet, so the width and height are multiplied by 2
        self.image = self.game.character_spritesheet.get_sprite(
            3, 2, self.width, self.height
        )

        # Set player rect
        # This is used for collision detection (hitboxes)
        self.rect = self.image.get_rect()
        # Set player rect x/y to match player x/y
        self.rect.x = self.x
        self.rect.y = self.y

        # set player animation cells (for animation strips)
        # each sprite is loaded from pixel coordinates on the spritesheet, using the width and height of the sprite
        self.down_animations = [
            self.game.character_spritesheet.get_sprite(3, 2, self.width, self.height),
            self.game.character_spritesheet.get_sprite(35, 2, self.width, self.height),
            self.game.character_spritesheet.get_sprite(68, 2, self.width, self.height),
        ]

        self.up_animations = [
            self.game.character_spritesheet.get_sprite(3, 34, self.width, self.height),
            self.game.character_spritesheet.get_sprite(35, 34, self.width, self.height),
            self.game.character_spritesheet.get_sprite(68, 34, self.width, self.height),
        ]

        self.left_animations = [
            self.game.character_spritesheet.get_sprite(3, 98, self.width, self.height),
            self.game.character_spritesheet.get_sprite(35, 98, self.width, self.height),
            self.game.character_spritesheet.get_sprite(68, 98, self.width, self.height),
        ]

        self.right_animations = [
            self.game.character_spritesheet.get_sprite(3, 66, self.width, self.height),
            self.game.character_spritesheet.get_sprite(35, 66, self.width, self.height),
            self.game.character_spritesheet.get_sprite(68, 66, self.width, self.height),
        ]

    # This is the game loop update function for the player
    def update(self):
        # Update player x/y
        self.movement()
        # animates player
        self.animate()
        # checks for collision with enemies
        self.collide_enemy()

        # Set player rect x/y to match player x/y
        self.rect.x += self.x_change
        self.collide_blocks("x")  # checks for collision with blocks on x axis
        self.rect.y += self.y_change
        self.collide_blocks("y")  # checks for collision with blocks on y axis

        # reset player movement change variables
        self.x_change = 0
        self.y_change = 0

    # This is where the player movement is handled
    def movement(self):
        keys = pygame.key.get_pressed()  # creates instance of keys pressed

        # Sprinting
        if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
            sprint_multiplier = 1.5
        else:
            sprint_multiplier = 1

        # Damping factor for momentum
        damping = 1  # You can adjust this value to control the momentum effect

        # Diagonal movement math
        diagonal_move = (keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]) and (
            keys[pygame.K_UP] or keys[pygame.K_DOWN]
        )
        # Diagonal movement multiplier
        diagonal_multiplier = 1 / math.sqrt(2)

        # character movement with arrow keys
        if keys[pygame.K_LEFT]:
            if diagonal_move:
                self.x_change = -PLAYER_SPEED * sprint_multiplier * diagonal_multiplier
            else:
                self.x_change = -PLAYER_SPEED * sprint_multiplier
            self.facing = "left"

        if keys[pygame.K_RIGHT]:
            if diagonal_move:
                self.x_change = PLAYER_SPEED * sprint_multiplier * diagonal_multiplier
            else:
                self.x_change = PLAYER_SPEED * sprint_multiplier
            self.facing = "right"

        if keys[pygame.K_UP]:
            if diagonal_move:
                self.y_change = -PLAYER_SPEED * sprint_multiplier * diagonal_multiplier
            else:
                self.y_change = -PLAYER_SPEED * sprint_multiplier
            self.facing = "up"

        if keys[pygame.K_DOWN]:
            if diagonal_move:
                self.y_change = PLAYER_SPEED * sprint_multiplier * diagonal_multiplier
            else:
                self.y_change = PLAYER_SPEED * sprint_multiplier
            self.facing = "down"

        # Apply damping to simulate momentum
        self.x_change *= damping
        self.y_change *= damping

        # Update player position
        self.rect.x += self.x_change
        self.rect.y += self.y_change

    # This is where the player collision is handled
    def collide_blocks(self, direction):
        if direction == "x":
            # checks for collision with blocks on x axis by comparing the player rect to the block rect
            # The False argument is for the sprite kill argument, which we don't want to use for blocks
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                # if the player is moving right
                if self.x_change > 0:
                    for sprite in self.game.all_sprites:
                        sprite.rect.x += self.x_change
                    # if there is a collision, stop the player rect from moving beyond the opposite side of the block rect
                    self.rect.right = hits[0].rect.left
                # if the player is moving left
                if self.x_change < 0:
                    for sprite in self.game.all_sprites:
                        sprite.rect.x += self.x_change
                    # if there is a collision, stop the player rect from moving beyond the opposite side of the block rect
                    self.rect.left = hits[0].rect.right

        if direction == "y":
            # checks for collision with blocks on y axis
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                # if player is moving down
                if self.y_change > 0:
                    # move all sprites with the player rect, stopping on collision
                    for sprite in self.game.all_sprites:
                        sprite.rect.y += self.y_change
                    # if there is a collision, stop the player rect from moving beyond the opposite side of the block rect
                    self.rect.bottom = hits[0].rect.top
                # if the player is moving up
                if self.y_change < 0:
                    for sprite in self.game.all_sprites:
                        sprite.rect.y += self.y_change
                    # if there is a collision, stop the player rect from moving beyond the opposite side of the block rect
                    self.rect.top = hits[0].rect.bottom

    # This is where the player animation is handled, including the animation strips and logic
    def animate(self):
        # Animation
        # Animates player based on direction
        if self.facing == "down":
            # if the player is not moving, set the player image to the first frame of the animation
            if self.x_change == 0 and self.y_change == 0:
                self.image = self.down_animations[0]
            else:
                # sets the player image to the current frame of the animation
                self.image = self.down_animations[math.floor(self.animation_loop)]
                # adds to the animation loop
                self.animation_loop += 0.1
                # if the animation loop is greater than the length of the animation, reset the animation loop
                if self.animation_loop >= len(self.down_animations):
                    self.animation_loop = 1

        if self.facing == "up":
            if self.x_change == 0 and self.y_change == 0:
                self.image = self.up_animations[0]
            else:
                self.image = self.up_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= len(self.up_animations):
                    self.animation_loop = 1

        if self.facing == "left":
            if self.x_change == 0 and self.y_change == 0:
                self.image = self.left_animations[0]
            else:
                self.image = self.left_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= len(self.left_animations):
                    self.animation_loop = 1

        if self.facing == "right":
            if self.x_change == 0 and self.y_change == 0:
                self.image = self.right_animations[0]
            else:
                self.image = self.right_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= len(self.right_animations):
                    self.animation_loop = 1

    #
    def collide_enemy(self):
        # checks for collision with enemies between the player and sprites in the enemies group
        hits = pygame.sprite.spritecollide(self, self.game.enemies, False)
        if hits:
            # if there is a collision, kill the player and end the game
            self.kill()
            self.game.playing = False


class Block(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = BLOCK_LAYER

        self.groups = (
            self.game.all_sprites,
            self.game.blocks,
        )  # Sets wall sprite group both all_sprites and blocks

        pygame.sprite.Sprite.__init__(self, self.groups)  # Initializes wall sprite

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        # sets wall image
        self.image = self.game.terrain_spritesheet.get_sprite(
            960, 448, self.width, self.height
        )

        # sets wall hitbox
        self.rect = self.image.get_rect()  # Sets wall rect
        self.rect.x = self.x
        self.rect.y = self.y


class Ground(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = GROUND_LAYER

        self.groups = self.game.all_sprites

        pygame.sprite.Sprite.__init__(self, self.groups)  # Initializes ground sprite

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        # sets ground image
        self.image = self.game.terrain_spritesheet.get_sprite(
            64, 352, self.width, self.height
        )

        # sets wall hitbox
        self.rect = self.image.get_rect()  # Sets ground rect
        self.rect.x = self.x
        self.rect.y = self.y


class Enemy(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        # Enemy sprite init
        self.game = game
        self._layer = ENEMY_LAYER
        self.groups = (
            self.game.all_sprites,
            self.game.enemies,
        )
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        # temp variables for enemy movement
        self.x_change = 0
        self.y_change = 0

        self.facing = random.choice(
            ["up", "down", "left", "right"]
        )  # Sets default enemy facing direction for animation
        self.animation_loop = 1  # Sets default player animation frame
        self.movement_loop = 0  # Sets default enemy movement loop
        self.max_travel = random.randint(
            1, 200
        )  # Sets default enemy max travel distance

        # sets enemy image
        self.image = self.game.enemy_spritesheet.get_sprite(
            3, 2, self.width, self.height
        )
        # set sprite as transparent
        self.image.set_colorkey(BLACK)

        self.rect = self.image.get_rect()  # Sets enemy rect
        self.rect.x = self.x
        self.rect.y = self.y

        # set enemy animation cells (for animation strips)
        self.up_animations = [
            self.game.enemy_spritesheet.get_sprite(3, 2, self.width, self.height),
            self.game.enemy_spritesheet.get_sprite(35, 2, self.width, self.height),
            self.game.enemy_spritesheet.get_sprite(68, 2, self.width, self.height),
        ]

        self.down_animations = [
            self.game.enemy_spritesheet.get_sprite(3, 34, self.width, self.height),
            self.game.enemy_spritesheet.get_sprite(35, 34, self.width, self.height),
            self.game.enemy_spritesheet.get_sprite(68, 34, self.width, self.height),
        ]

        self.left_animations = [
            self.game.enemy_spritesheet.get_sprite(3, 98, self.width, self.height),
            self.game.enemy_spritesheet.get_sprite(35, 98, self.width, self.height),
            self.game.enemy_spritesheet.get_sprite(68, 98, self.width, self.height),
        ]

        self.right_animations = [
            self.game.enemy_spritesheet.get_sprite(3, 66, self.width, self.height),
            self.game.enemy_spritesheet.get_sprite(35, 66, self.width, self.height),
            self.game.enemy_spritesheet.get_sprite(68, 66, self.width, self.height),
        ]

    def update(self):
        self.movement()
        self.animate()

        self.rect.x += self.x_change
        self.rect.y += self.y_change

        self.x_change = 0
        self.y_change = 0

    def movement(self):
        if self.facing == "down":
            # movement set to enemy speed (neg for down and left)
            self.y_change -= ENEMY_SPEED
            # adds to movement loop to track distance traveled
            self.movement_loop -= 1
            # if the movement loop has hit the threshold, change direction
            # movement threshold is set randomly by the max_travel variable
            if self.movement_loop <= -self.max_travel:
                self.facing = random.choice(["up", "down", "left", "right"])

        if self.facing == "up":
            self.y_change += ENEMY_SPEED
            self.movement_loop += 1
            if self.movement_loop >= self.max_travel:
                self.facing = random.choice(["up", "down", "left", "right"])

        if self.facing == "left":
            self.x_change -= ENEMY_SPEED
            self.movement_loop -= 1
            if self.movement_loop <= -self.max_travel:
                self.facing = random.choice(["up", "down", "left", "right"])

        if self.facing == "right":
            self.x_change += ENEMY_SPEED
            self.movement_loop += 1
            if self.movement_loop >= self.max_travel:
                self.facing = random.choice(["up", "down", "left", "right"])

    def animate(self):
        if self.facing == "down":
            # if the player is not moving, set the player image to the first frame of the animation
            if self.x_change == 0 and self.y_change == 0:
                self.image = self.down_animations[0]
            else:
                # sets the player image to the current frame of the animation
                self.image = self.down_animations[math.floor(self.animation_loop)]
                # adds to the animation loop
                self.animation_loop += 0.1
                # if the animation loop is greater than the length of the animation, reset the animation loop
                if self.animation_loop >= len(self.down_animations):
                    self.animation_loop = 1

        if self.facing == "up":
            if self.x_change == 0 and self.y_change == 0:
                self.image = self.up_animations[0]
            else:
                self.image = self.up_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= len(self.up_animations):
                    self.animation_loop = 1

        if self.facing == "left":
            if self.x_change == 0 and self.y_change == 0:
                self.image = self.left_animations[0]
            else:
                self.image = self.left_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= len(self.left_animations):
                    self.animation_loop = 1

        if self.facing == "right":
            if self.x_change == 0 and self.y_change == 0:
                self.image = self.right_animations[0]
            else:
                self.image = self.right_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= len(self.right_animations):
                    self.animation_loop = 1


class Button:
    def __init__(self, x, y, width, height, fg, bg, content, fontsize):
        # Button init
        # set button font
        self.font = pygame.font.Font(
            "D:\\Projects\\Game\\RPG\\images\\img\\img\\fonts\\Roboto\\Roboto-Medium.ttf",
            fontsize,
        )

        # set button content
        self.content = content
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        # sets background and foreground
        self.fg = fg
        self.bg = bg

        # creates button surface
        self.image = pygame.Surface((width, height))
        self.image.fill(bg)

        # sets button rect
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        # sets button blit
        self.text = self.font.render(self.content, True, self.fg)
        self.text_rect = self.text.get_rect(center=(self.width / 2, self.height / 2))
        self.image.blit(self.text, self.text_rect)

    def is_pressed(self, pos, pressed):
        # checks if button is pressed
        if self.rect.collidepoint(pos):
            # if the button is pressed, return True
            # [0] is the left mouse button, [1] is the middle mouse button, [2] is the right mouse button
            if pressed[0]:
                return True
            return False
        return False

    def update_position(self, screen_width, screen_height):
        # Update the position of the button based on the screen size
        self.rect.x = screen_width / 2 - self.width / 2
        self.rect.y = screen_height / 2 - self.height / 2


class Attack(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        # Attack sprite init
        self.game = game
        self._layer = PLAYER_LAYER
        # sets sprite group
        self.groups = self.game.all_sprites, self.game.attacks
        # initializes sprite
        pygame.sprite.Sprite.__init__(self, self.groups)

        # sets sprite x/y
        self.x = x
        self.y = y
        self.width = TILESIZE
        self.height = TILESIZE

        # sets animation loop
        self.animation_loop = 0

        # sets sprite image
        self.image = self.game.attack_spritesheet.get_sprite(
            3, 2, self.width, self.height
        )

        # sets sprite rect
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        # sets sprite direction
        self.right_animations = [
            self.game.attack_spritesheet.get_sprite(0, 64, self.width, self.height),
            self.game.attack_spritesheet.get_sprite(32, 64, self.width, self.height),
            self.game.attack_spritesheet.get_sprite(64, 64, self.width, self.height),
            self.game.attack_spritesheet.get_sprite(96, 64, self.width, self.height),
            self.game.attack_spritesheet.get_sprite(128, 64, self.width, self.height),
        ]

        self.down_animations = [
            self.game.attack_spritesheet.get_sprite(0, 32, self.width, self.height),
            self.game.attack_spritesheet.get_sprite(32, 32, self.width, self.height),
            self.game.attack_spritesheet.get_sprite(64, 32, self.width, self.height),
            self.game.attack_spritesheet.get_sprite(96, 32, self.width, self.height),
            self.game.attack_spritesheet.get_sprite(128, 32, self.width, self.height),
        ]

        self.left_animations = [
            self.game.attack_spritesheet.get_sprite(0, 96, self.width, self.height),
            self.game.attack_spritesheet.get_sprite(32, 96, self.width, self.height),
            self.game.attack_spritesheet.get_sprite(64, 96, self.width, self.height),
            self.game.attack_spritesheet.get_sprite(96, 96, self.width, self.height),
            self.game.attack_spritesheet.get_sprite(128, 96, self.width, self.height),
        ]

        self.up_animations = [
            self.game.attack_spritesheet.get_sprite(0, 0, self.width, self.height),
            self.game.attack_spritesheet.get_sprite(32, 0, self.width, self.height),
            self.game.attack_spritesheet.get_sprite(64, 0, self.width, self.height),
            self.game.attack_spritesheet.get_sprite(96, 0, self.width, self.height),
            self.game.attack_spritesheet.get_sprite(128, 0, self.width, self.height),
        ]

    def update(self):
        self.animate()
        self.collide()

    def collide(self):
        hits = pygame.sprite.spritecollide(self, self.game.enemies, True)

    def animate(self):
        direction = self.game.player.facing

        if direction == "up":
            self.image = self.up_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.8
            if self.animation_loop >= len(self.up_animations):
                self.kill()

        if direction == "down":
            self.image = self.down_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.8
            if self.animation_loop >= len(self.down_animations):
                self.kill()

        if direction == "left":
            self.image = self.left_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.8
            if self.animation_loop >= len(self.left_animations):
                self.kill()

        if direction == "right":
            self.image = self.right_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.8
            if self.animation_loop >= len(self.right_animations):
                self.kill()
