import sys
from game_class import Game
import pygame
from graphics import draw_board, initialize


def main():
    pygame.init()
    graphics_dict, screen = initialize()
    draw_board(6, 6, graphics_dict['tile'], screen)

    while True:
        for event in pygame.event.get():  # Close nicely and display changes
            if event.type == pygame.QUIT:
                sys.exit()
        pygame.display.flip()
        pygame.time.delay(150)


if __name__ == '__main__':
    main()
