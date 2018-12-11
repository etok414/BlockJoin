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

    falling_block = game_class.Block(width, height, image=graphics_dict['pill_e'])
    player = game_class.Player(width, height, image=graphics_dict['blob_e'])
    shadow_tile = game_class.Thing(image=graphics_dict['tile_shadow1'])

    cooldown = 0
    while True:
        screen.fill((0, 0, 0))
        board_tile_group.draw(screen)

        if cooldown == 0:
            action = check_keyboard(player, block_group)
            if action:
                cooldown = 4
        else:
            cooldown -= 1

        shadow_tile.place_here(falling_block.x_pos, falling_block.y_pos)
        shadow_tile.image = graphics_dict[f'tile_shadow{5-int(falling_block.drop_clock/30)}']
        shadow_tile.update(screen)
        # TODO: Make block standing on shadow transparent

        block_group.update(screen)

        player.image = graphics_dict[f'blob_{player.letter_direction}']
        player.update(screen)
        if player.carried_block():
            player.carried_block().image = graphics_dict[f'pill_{player.carried_block().letter_direction}']
            player.carried_block().update(screen)

        falling_block = block_drop(falling_block, player, block_group, 1)
        if falling_block == 'stop':
            end_game(graphics_dict, screen)
        falling_block.image = graphics_dict[f'pill_{falling_block.letter_direction}']
        falling_block.update(screen)

        full_board_loop_check(block_group, graphics_dict)

        pygame.display.flip()
        pygame.time.delay(33)


def check_keyboard(player, block_group):
    for event in pygame.event.get():  # Close nicely and display changes # TODO: Move this to main?
        if event.type == pygame.QUIT:
            sys.exit()

    for block in block_group:
        if block.marked:
            block.kill()

    pygame.event.pump()
    key = pygame.key.get_pressed()  # checking pressed keys
    action = False
    if key[pygame.K_SPACE]:
        player.push(block_group)
        action = True
    if key[pygame.K_w]:
        player.step('n', block_group)
        action = True
    elif key[pygame.K_d]:
        player.step('e', block_group)
        action = True
    elif key[pygame.K_s]:
        player.step('s', block_group)
        action = True
    elif key[pygame.K_a]:
        player.step('w', block_group)
        action = True
    elif key[pygame.K_p]:
        action = True
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
    return action


def full_board_loop_check(block_group, graphics_dict):
    for block in block_group:
        chain = pygame.sprite.Group()
        chain.add(block)
        loop_or_false = loop_check(chain, block_group)
        if loop_or_false is not False:
            for block_2 in loop_or_false:
                block_2.marked = True
                block_2.image = graphics_dict[f'pill_{block_2.letter_direction}_inv']


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


def block_drop(falling_block, player, block_group, drop_ticks=1):
    drop_result = falling_block.update_falling(player, block_group, drop_ticks)

    width, height = falling_block.board_width, falling_block.board_height
    bag, direction = falling_block.bag, falling_block.direction
    image = falling_block.image

    if drop_result == 'Failure':
        print('Failure')
        return 'stop'
    elif drop_result == 'Head_landing':
        player.carried_block_group.add(falling_block)
        player.carried_block().drop_clock = 1
        player.carried_block().letter_direction = player.letter_direction
        return game_class.Block(width, height, bag=bag, image=image)
    elif drop_result == 'Ground_landing':
        block_group.add(falling_block)
        return game_class.Block(width, height, bag=bag, image=image)
    else:
        return falling_block


def end_game(graphics_dict, screen):
    image = graphics_dict['game_over']
    img_rect = image.get_rect(center=(350, 250))
    screen.blit(image, img_rect)
    pygame.display.flip()
    pygame.time.delay(2500)
    sys.exit()


if __name__ == '__main__':
    main()
