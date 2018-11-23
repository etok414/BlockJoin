import sys
import game_class
import pygame
from graphics import draw_board, initialize, move_sprite_to

""" Three coordinate systems are used: 
        * A cartesian keeping track of the position on the board
        * A cartesian blown up to fit the screen
        * An isometric to position sprites in 2.5D
"""


# TODO Merge the last two coordinate systems. Blowing up and transforming to isometric should be one process


def main():
    width, height = 6, 6
    pygame.init()
    graphics_dict, screen = initialize()  # Initialize graphics: graphics_dict hold all sprites with their names as keys
    draw_board(width, height, graphics_dict['tile'], screen)

    base_x, base_y = 337, 222

    block_list = []
    falling_block = game_class.Block(width, height)
    player = game_class.Player(width, height)

    player_img = graphics_dict['blob_e']
    player_sprite = player_img.get_rect(center=(base_x, base_y))
    move_sprite_to(base_x, base_y, player_sprite, player_img, screen)

    block_img = graphics_dict['pill_e']
    block_sprite = block_img.get_rect(center=(base_x, base_y))
    real_pos = falling_block.get_real_pos(base_x, base_y)
    move_sprite_to(real_pos[0], real_pos[1], block_sprite, block_img, screen)

    while True:
        draw_board(width, height, graphics_dict['tile'], screen)

        check_keyboard(player, block_list)

        player_img = graphics_dict[f'blob_{player.letter_direction}']
        real_pos = player.get_real_pos(base_x, base_y)
        move_sprite_to(real_pos[0], real_pos[1], player_sprite, player_img, screen)

        for _ in range(4):
            pygame.time.delay(33)
            falling_block = block_drop(falling_block, player, block_list)

            block_img = graphics_dict[f'pill_{falling_block.letter_direction}']
            real_pos = falling_block.get_real_pos(base_x, base_y)
            move_sprite_to(real_pos[0], real_pos[1], block_sprite, block_img, screen)


def check_keyboard(player, block_list):
    for event in pygame.event.get():  # Close nicely and display changes
        if event.type == pygame.QUIT:
            sys.exit()
    pygame.event.pump()
    key = pygame.key.get_pressed()  # checking pressed keys
    if key[pygame.K_w]:
        player.move('n', block_list)
    elif key[pygame.K_d]:
        player.move('e', block_list)
    elif key[pygame.K_s]:
        player.move('s', block_list)
    elif key[pygame.K_a]:
        player.move('w', block_list)
    elif key[pygame.K_SPACE]:
        player.push(block_list)
    elif key[pygame.K_q]:
        sys.exit()


def block_drop(falling_block, player, block_list):
    drop_result = falling_block.update_falling(player, block_list)

    width, height = falling_block.board_width, falling_block.board_height
    bag, direction = falling_block.bag, falling_block.direction
    x_pos, y_pos = falling_block.x_pos, falling_block.y_pos

    if drop_result == 'Failure':
        print('Failure')
        sys.exit()
    elif drop_result == 'Head_landing':
        player.carried_block = game_class.Block(width, height, bag, direction, x_pos, y_pos)
        falling_block = game_class.Block(width, height, bag=bag)
    elif drop_result == 'Ground_landing':
        block_list.append(game_class.Block(width, height, bag, direction, x_pos, y_pos))
        falling_block = game_class.Block(width, height, bag=bag)
    return falling_block
    # TODO: Make the dropping animations, and make the things land.


if __name__ == '__main__':
    main()
