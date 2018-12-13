import sys
import game_class
import pygame
from graphics import draw_board, initialize


def main():
    width, height = 6, 6
    pygame.init()
    graphics_dict, screen = initialize()  # Initialize graphics: graphics_dict hold all sprites with their names as keys

    board_tile_group = draw_board(screen, graphics_dict)
    block_group = pygame.sprite.Group()

    ghost_group = make_ghosts(width, height, graphics_dict)

    falling_block_group = pygame.sprite.GroupSingle()
    falling_block_group.add(game_class.Block(width, height, image=graphics_dict['pill_e'], block_group=block_group))
    player = game_class.Player(width, height, image=graphics_dict['blob_e'])
    shadow_tile = game_class.Thing(image=graphics_dict['tile_shadow1'])

    cool_down = 0
    disappear_delay = 0
    while True:
        for event in pygame.event.get():  # Close nicely and display changes
            if event.type == pygame.QUIT:
                sys.exit()

        screen.fill((0, 0, 0))
        board_tile_group.draw(screen)

        cool_down = check_keyboard(player, block_group, cool_down)

        disappear_delay = full_board_loop_check(block_group, disappear_delay)

        update_shadows(block_group, falling_block_group, graphics_dict, screen, shadow_tile)

        block_group.update(screen)
        ghost_group.update(screen, block_group)
        update_player(graphics_dict, player, screen)
        update_falling_block(block_group, falling_block_group, graphics_dict, player, screen, drop_ticks=1)

        pygame.display.flip()
        pygame.time.delay(33)


def update_falling_block(block_group, falling_block_group, graphics_dict, player, screen, drop_ticks=1):
    falling_block = falling_block_group.sprite
    board_width, board_height = falling_block.board_width, falling_block.board_height
    bag, image = falling_block.bag, falling_block.image

    drop_result = falling_block.update_falling(player, block_group, drop_ticks)

    if drop_result == 'Failure':
        end_game(graphics_dict, screen)
    elif drop_result == 'Head_landing':
        player.carried_block_group.add(falling_block)
        player.carried_block().drop_clock = 1
        player.carried_block().letter_direction = player.letter_direction
        falling_block_group.add(game_class.Block(board_width, board_height,
                                                 bag=bag, image=image, block_group=block_group))
    elif drop_result == 'Ground_landing':
        block_group.add(falling_block)
        falling_block_group.add(game_class.Block(board_width, board_height,
                                                 bag=bag, image=image, block_group=block_group))
    falling_block.image = graphics_dict[f'pill_{falling_block.letter_direction}']
    falling_block.update(screen)


def update_player(graphics_dict, player, screen):
    player.image = graphics_dict[f'blob_{player.letter_direction}']
    player.update(screen)
    if player.carried_block():
        player.carried_block().image = graphics_dict[f'pill_{player.carried_block().letter_direction}']
        player.carried_block().update(screen)


def update_shadows(block_group, falling_block_group, graphics_dict, screen, shadow_tile):
    falling_block = falling_block_group.sprite
    shadow_tile.place_here(falling_block.x_pos, falling_block.y_pos)
    shadow_tile.image = graphics_dict[f'tile_shadow{5-int(falling_block.drop_clock/25)}']
    shadow_tile.update(screen)
    for block in block_group:
        block.select_image(graphics_dict, falling_block)


def check_keyboard(player, block_group, cool_down):
    if cool_down == 0:
        pygame.event.pump()
        key = pygame.key.get_pressed()  # checking pressed keys
        if key[pygame.K_SPACE]:
            player.push_block(block_group)
            cool_down = 4
        if key[pygame.K_w]:
            player.take_step('n', block_group)
            cool_down = 4
        elif key[pygame.K_d]:
            player.take_step('e', block_group)
            cool_down = 4
        elif key[pygame.K_s]:
            player.take_step('s', block_group)
            cool_down = 4
        elif key[pygame.K_a]:
            player.take_step('w', block_group)
            cool_down = 4
        elif key[pygame.K_p]:
            cool_down = 4
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
                    pygame.time.delay(200)
                    sys.exit()
        elif key[pygame.K_q]:
            pygame.time.delay(200)
            sys.exit()
    else:
        cool_down -= 1
    return cool_down


def full_board_loop_check(block_group, disappear_delay):
    for block in block_group:
        chain = pygame.sprite.Group()
        chain.add(block)
        loop_or_false = loop_check(chain, block_group)
        if loop_or_false is not False:
            for block_2 in loop_or_false:
                if not block_2.marked:
                    disappear_delay = 6
                block_2.marked = True
    if disappear_delay == 0:
        for block in block_group:
            if block.marked:
                block.kill()
    else:
        disappear_delay -= 1
    return disappear_delay


def loop_check(chain, block_group):
    latest_block = chain.sprites()[-1]
    board_width, board_height = latest_block.board_width, latest_block.board_height
    next_x = (latest_block.x_pos + latest_block.direction()[0]) % board_width
    next_y = (latest_block.y_pos + latest_block.direction()[1]) % board_height
    next_block = game_class.probe(next_x, next_y, block_group, board_width, board_height)
    if not next_block:
        return False

    for block in chain:
        if next_block.x_pos == block.x_pos and next_block.y_pos == block.y_pos:
            for tail_block in chain:
                if next_block.x_pos == tail_block.x_pos and next_block.y_pos == tail_block.y_pos:
                    return chain  # This is the loop it returns
                else:
                    chain.remove(tail_block)
    chain.add(next_block)
    loop_or_false = loop_check(chain, block_group)
    return loop_or_false


def make_ghosts(board_width, board_height, graphics_dict):
    placeholder = graphics_dict['pill_e']
    ghost_group = pygame.sprite.Group()
    for num in range(board_width):
        ghost_group.add(game_class.Ghost(num, -1, board_width, board_height, image=placeholder),
                        game_class.Ghost(num, board_height, board_width, board_height, image=placeholder))
    for num in range(board_height):
        ghost_group.add(game_class.Ghost(-1, num, board_width, board_height, image=placeholder),
                        game_class.Ghost(board_width, num, board_width, board_height, image=placeholder))
    return ghost_group


def end_game(graphics_dict, screen):
    image = graphics_dict['game_over']
    img_rect = image.get_rect(center=(350, 250))
    screen.blit(image, img_rect)
    pygame.display.flip()
    pygame.time.delay(2000)
    sys.exit()


if __name__ == '__main__':
    main()
