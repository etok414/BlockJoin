import sys
import game_class
import pygame
from graphics import draw_board, initialize


def main():
    width, height = 6, 6
    pygame.init()
    graphics_dict, screen = initialize()
    draw_board(width, height, graphics_dict['tile'], screen)
    game = game_class.Game(width, height)

    while True:
        for event in pygame.event.get():  # Close nicely and display changes
            if event.type == pygame.QUIT:
                sys.exit()
        pygame.event.pump()
        key = pygame.key.get_pressed()  # checking pressed keys
        if key[pygame.K_a]:
            game.move(0)
        elif key[pygame.K_d]:
            game.move(1)
        elif key[pygame.K_s]:
            game.move(2)
        elif key[pygame.K_w]:
            game.move(3)
        elif key[pygame.K_q]:
            sys.exit()
        pygame.display.flip()
        pygame.time.delay(150)


if __name__ == '__main__':
    main()
