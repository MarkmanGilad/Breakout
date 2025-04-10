import pygame
from Constants import*

class Block(pygame.sprite.Sprite):
    def __init__(self, image) -> None:
        super().__init__()
        self.image=image
        self.rect=self.image.get_rect()

    def move(self,dx):
        x, y = self.rect.midbottom

        # Predict next position
        next_x = x + dx

        # Define boundaries with some buffer (here ±50 px, wall margin = 70)
        left_limit = 70 + 50
        right_limit = WIDTH - 70 - 50

        # Apply movement if within bounds, else clamp
        if left_limit <= next_x <= right_limit:
            x = next_x
        elif next_x < left_limit:
            x = left_limit  # Clamp to left
        else:
            x = right_limit  # Clamp to right

        self.rect.midbottom = x, y

    def draw(self,surface):
        surface.blit(self.image,self.rect)