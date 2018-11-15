import sys
from game_class import Game
import pygame
from graphics import draw_board, initialize, move_sprite


def main():
    width, height = 6, 6
    pygame.init()
    graphics_dict, screen = initialize()  # Initialize graphics: graphics_dict hold all sprites with their names as keys
    draw_board(width, height, graphics_dict['tile'], screen)
    game = game_class.Game(width, height)

    x_c, y_c = 387, 222
    blob_img = graphics_dict['blob_e']
    pill_img = graphics_dict['pill_e']
    blob = blob_img.get_rect(center=(x_c, y_c))
    pill = pill_img.get_rect(center=(400, 250))

    while True:
        draw_board(width, height, graphics_dict['tile'], screen)

        move_sprite(x_c, y_c, blob, blob_img, screen)

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
