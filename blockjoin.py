import sys
import game_class
import pygame
from graphics import draw_board, initialize, move_sprite_to, update_thing_pos

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
    # draw_board(width, height, graphics_dict['tile'], screen)

    block_list = []
    falling_block = game_class.Block(width, height, image=graphics_dict['pill_e'])
    player = game_class.Player(width, height, image=graphics_dict['blob_e'])
    board = game_class.Thing(-2, 0, image=graphics_dict['board'])

    # tile = game_class.Thing(0, 0, image=graphics_dict['tile'])

    # player_img = graphics_dict['blob_e']
    # player_sprite = player_img.get_rect()
    # move_sprite_to(0, 0, player.rect, player.image, screen)
    update_thing_pos(board, screen)
    # board = get_rect(center=(x_i * 50 + 400, y_i * 50 + 200))
    update_thing_pos(player, screen)  # Is these two lines necessary?
    update_thing_pos(falling_block, screen)

    while True:
        # draw_board(tile, screen)
        update_thing_pos(board, screen)

        check_keyboard(player, block_list)

        for block in block_list:
            update_thing_pos(block, screen)
        player.image = graphics_dict[f'blob_{player.letter_direction}']
        update_thing_pos(player, screen)
        if player.carried_block:
            player.carried_block.image = graphics_dict[f'pill_{player.carried_block.letter_direction}']
            update_thing_pos(player.carried_block, screen)

        falling_block = block_drop(falling_block, player, block_list, 4)
        falling_block = block_drop(falling_block, player, block_list)

        falling_block.image = graphics_dict[f'pill_{falling_block.letter_direction}']
        update_thing_pos(falling_block, screen)
        pygame.time.delay(150)
# TODO Update via pygame's sprite engine
# TODO Put shadows under falling blocks


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
        player.carried_block = None
    elif key[pygame.K_p]:
        while True:
            pygame.time.delay(150)
            for event in pygame.event.get():  # Close nicely and display changes
                if event.type == pygame.QUIT:
                    sys.exit()
            pygame.event.pump()
            key = pygame.key.get_pressed()  # checking pressed keys
            if key[pygame.K_p] or key[pygame.K_o]:
                break
    elif key[pygame.K_q]:
        sys.exit()


def full_board_loop_check(block_list):
    for block in block_list:
        loop_or_false = loop_check([block], block_list)
        if loop_or_false:
            pass  # TODO: Getting rid of the blocks involved in the gridlock.


def loop_check(chain, block_list):
    latest_block = chain[-1]
    board_width, board_height = latest_block.board_width, latest_block.board_height
    next_x = (latest_block.x_pos + latest_block.direction()[0]) % board_width
    next_y = (latest_block.y_pos + latest_block.direction()[1]) % board_height
    next_block = game_class.probe(next_x, next_y, block_list, board_width, board_height)
    if not next_block:
        return False
    for num, block in enumerate(chain):
        if next_block.x_pos == block.x_pos and next_block.y_pos == block.y_pos:
            return chain[num:] # This is the gridlock it returns
    chain.append(next_block)
    loop_or_false = loop_check(chain, block_list)
    return loop_or_false


def block_drop(falling_block, player, block_list, drop_ticks=1):
    drop_result = falling_block.update_falling(player, block_list, drop_ticks)

    width, height = falling_block.board_width, falling_block.board_height
    bag, direction = falling_block.bag, falling_block.direction
    x_pos, y_pos = falling_block.x_pos, falling_block.y_pos
    image = falling_block.image

    if drop_result == 'Failure':
        print('Failure')
        sys.exit()
    elif drop_result == 'Head_landing':
        # player.carried_block = game_class.Block(width, height, bag, direction, x_pos, y_pos, image=image)
        player.carried_block = falling_block
        player.carried_block.drop_clock = 1
        return game_class.Block(width, height, bag=bag, image=image)
    elif drop_result == 'Ground_landing':
        # block_list.append(game_class.Block(width, height, bag, direction, x_pos, y_pos, image=image))
        block_list.append(falling_block)
        return game_class.Block(width, height, bag=bag, image=image)
    else:
        return falling_block
    # TODO: Make the dropping animations, and make the things land.


if __name__ == '__main__':
    main()
