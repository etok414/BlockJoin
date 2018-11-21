import sys
import game_class
import pygame
from graphics import draw_board, initialize, move_sprite_to


def main():
    width, height = 6, 6
    pygame.init()
    graphics_dict, screen = initialize()  # Initialize graphics: graphics_dict hold all sprites with their names as keys
    draw_board(width, height, graphics_dict['tile'], screen)

    base_x, base_y = 337, 222
    blob_img = graphics_dict['blob_e']
    pill_img = graphics_dict['pill_e']
    blob = blob_img.get_rect(center=(base_x, base_y))
    pill = pill_img.get_rect(center=(400, 250))

    move_sprite_to(base_x, base_y, blob, blob_img, screen)

    block_list = []
    falling_block = game_class.Block(width, height)
    player = game_class.Player(width, height)

    while True:
        draw_board(width, height, graphics_dict['tile'], screen)

        check_keyboard(player, block_list)

        blob_img = graphics_dict[f'blob_{player.letter_direction}']
        real_pos = player.get_real_pos(base_x, base_y)
        move_sprite_to(real_pos[0], real_pos[1], blob, graphics_dict[f'blob_{player.letter_direction}'], screen)

        pygame.display.flip()

        for _ in range(4):
            pygame.time.delay(33)
            block_drop(falling_block, player, block_list)


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
    elif key[pygame.K_q]:
        sys.exit()


def block_drop(falling_block, player, block_list):
    drop_result = falling_block.update_falling(player, block_list)
    if drop_result == 'failure':
        sys.exit()
    elif drop_result == 'head_landing':
        player.carried_block = game_class.Block(falling_block.board_width, falling_block.board_height, falling_block.bag
                                                , falling_block.direction, falling_block.x_pos, falling_block.y_pos)
        falling_block = game_class.Block(falling_block.board_width, falling_block.board_height, bag=falling_block.bag)
    elif drop_result == 'ground_landing':
        block_list.append(game_class.Block(falling_block.board_width, falling_block.board_height, falling_block.bag,
                                           falling_block.direction, falling_block.x_pos, falling_block.y_pos))
        falling_block = game_class.Block(falling_block.board_width, falling_block.board_height, bag=falling_block.bag)
    return falling_block
    # TODO: Make the dropping animations, and make the things land.


if __name__ == '__main__':
    main()
