import sys
import pygame
from graphics import draw_board, initialize


class Block(pygame.sprite.Sprite):

    # Constructor. Pass in the color of the block,
    # and its x and y position
    def __init__(self, color, width, height):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)

        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        self.image = pygame.Surface([width, height])
        self.image.fill(color)

        # Fetch the rectangle object that has the dimensions of the image
        # Update the position of this object by setting the values of rect.x and rect.y
        self.rect = self.image.get_rect(center=(400, 400))


def main():
    graphics_dict, screen = initialize()
    draw_board(6, 6, graphics_dict['tile'], screen)
    red = (255, 0, 0)
    block = Block(red, 50, 50)
    screen.blit(block.image, block.rect)
    print(block.image, block.rect, block.image.fill(red))

    while True:
        screen.blit(block.image, block.rect)
        for event in pygame.event.get():  # Close nicely and display changes
            if event.type == pygame.QUIT:
                sys.exit()
        pygame.display.flip()
        pygame.time.delay(150)


if __name__ == '__main__':
    main()
