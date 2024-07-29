import pygame
import random

FOOD_COLORS = [
    '#006336',  # Vert Cypres
    '#986B35'  # kuwatya
]

FOOD_POWER = 150
RADIUS_OF_FOOD = 10

# 餌
class Food:
	def __init__(self, x, y, food_power=FOOD_POWER):
		self.x = x
		self.y = y
		self.food_power = food_power
		self.food_radius = RADIUS_OF_FOOD
		self.eaten = False

	def move(self):
		pass

	def display(self, screen):
		pygame.draw.circle(screen, (0, 0, 255), (int(self.x), int(self.y)), RADIUS_OF_FOOD)