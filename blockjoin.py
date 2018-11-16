import sys
import game_class
import pygame
from graphics import draw_board, initialize, move_sprite_to


def main():
    width, height = 6, 6
    pygame.init()
    graphics_dict, screen = initialize()  # Initialize graphics: graphics_dict hold all sprites with their names as keys
    draw_board(width, height, graphics_dict['tile'], screen)
    game = game_class.Game(width, height)

    base_x, base_y = 337, 222
    blob_img = graphics_dict['blob_e']
    pill_img = graphics_dict['pill_e']
    blob = blob_img.get_rect(center=(base_x, base_y))
    pill = pill_img.get_rect(center=(400, 250))

    move_sprite_to(base_x, base_y, blob, blob_img, screen)

    while True:
        draw_board(width, height, graphics_dict['tile'], screen)

        check_keyboard(game)

        blob_img = graphics_dict[f'blob_{game.letter_direction}']
        move_sprite_to(base_x + (game.x_pos * 50), base_y - (game.y_pos * 50), blob, blob_img, screen)

        pygame.display.flip()

        for _ in range(4):
            pygame.time.delay(33)
            block_drop(game)


def check_keyboard(game):
    for event in pygame.event.get():  # Close nicely and display changes
        if event.type == pygame.QUIT:
            sys.exit()
    pygame.event.pump()
    key = pygame.key.get_pressed()  # checking pressed keys
    if key[pygame.K_w]:
        game.move('n')
    elif key[pygame.K_d]:
        game.move('e')
    elif key[pygame.K_s]:
        game.move('s')
    elif key[pygame.K_a]:
        game.move('w')
    elif key[pygame.K_q]:
        sys.exit()


def block_drop(game):
    result = game.update_falling_block()
    if result == 'failure':
        sys.exit()
    else:
        pass
    # TODO: Make the dropping animations, and make the things land.


if __name__ == '__main__':
    main()
