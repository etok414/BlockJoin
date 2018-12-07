import sys
import game_class
import pygame
from graphics import draw_board, initialize, update_thing_pos


def main():
    width, height = 6, 6
    pygame.init()
    graphics_dict, screen = initialize()  # Initialize graphics: graphics_dict hold all sprites with their names as keys
    board_tile_group = draw_board(screen, graphics_dict)

    block_list = []
    falling_block = game_class.Block(width, height, image=graphics_dict['pill_e'])
    player = game_class.Player(width, height, image=graphics_dict['blob_e'])

    shadow_tile = game_class.Thing(image=graphics_dict['tile_shadow1'])  # TODO: Properly implement shadows.

    counter = 0
    while True:
        screen.fill((0, 0, 0))
        board_tile_group.draw(screen)

        if counter >= 3:
            check_keyboard(player, block_list)
        counter = (counter + 1) % 4

        # TODO: Properly implement shadows.
        shadow_tile.x_pos, shadow_tile.y_pos = falling_block.x_pos, falling_block.y_pos
        shadow_tile.image = graphics_dict[f'tile_shadow{5-int(falling_block.drop_clock/30)}']
        update_thing_pos(shadow_tile, screen)
        # TODO: Properly implement shadows.

        for block in block_list:
            update_thing_pos(block, screen)
        player.image = graphics_dict[f'blob_{player.letter_direction}']
        update_thing_pos(player, screen)
        if player.carried_block:
            player.carried_block.image = graphics_dict[f'pill_{player.carried_block.letter_direction}']
            update_thing_pos(player.carried_block, screen)

        falling_block = block_drop(falling_block, player, block_list, 1)
        falling_block.image = graphics_dict[f'pill_{falling_block.letter_direction}']
        update_thing_pos(falling_block, screen)

        full_board_loop_check(block_list)

        pygame.display.flip()
        pygame.time.delay(33)


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
            return chain[num:]  # This is the gridlock it returns
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
        player.carried_block.letter_direction = player.letter_direction
        return game_class.Block(width, height, bag=bag, image=image)
    elif drop_result == 'Ground_landing':
        # block_list.append(game_class.Block(width, height, bag, direction, x_pos, y_pos, image=image))
        block_list.append(falling_block)
        return game_class.Block(width, height, bag=bag, image=image)
    else:
        return falling_block


if __name__ == '__main__':
    main()
