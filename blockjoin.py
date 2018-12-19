import sys
import game_class
import pygame
from graphics import draw_board, initialize_graphics
from start_end_messages import display_score, end_game, welcome


# TODO Make levels and level counter
# TODO Make welcome screen with instructions
# TODO Refactor program and move methods to modules

def main(display_welcome):
    width, height = 6, 6
    graphics_dict, screen = initialize_graphics()  # graphics_dict hold all sprite with their names as keys
    if display_welcome:
        welcome(screen)

    block_group = pygame.sprite.Group()
    board_tile_group = draw_board(graphics_dict, width, height, screen)
    ghost_group = make_ghosts(width, height, graphics_dict)
    falling_block_group = pygame.sprite.GroupSingle()

    falling_block_group.add(game_class.Block(width, height, image=graphics_dict['pill_e'], block_group=block_group))

    player = game_class.Player(width, height, image=graphics_dict['blob_e'])
    shadow_tile = game_class.Thing(image=graphics_dict['tile_shadow1'])

    cool_down = 0
    disappear_delay = 0
    score = 0
    while True:
        for event in pygame.event.get():  # Close nicely and display changes
            if event.type == pygame.QUIT:
                sys.exit()

        screen.fill((0, 0, 0))
        board_tile_group.draw(screen)

        cool_down = check_keyboard(player, block_group, cool_down)

        disappear_delay, score = full_board_loop_check(block_group, disappear_delay, score)
        display_score(score, screen)

        update_shadows(falling_block_group, graphics_dict, screen, shadow_tile)
        for block in block_group:
            block.select_image(graphics_dict, falling_block_group.sprite)
        block_group.update(screen)
        ghost_group.update(screen, block_group, graphics_dict)
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
        if not end_game():
            main(display_welcome=False)
        else:
            sys.exit()
    elif drop_result == 'Head_landing':
        player.carried_block_group.add(falling_block)
        player.carried_block().drop_clock = 1
        if player.turn_carried_block:
            player.carried_block().letter_direction = player.letter_direction
        else:
            bag = None
        falling_block_group.add(game_class.Block(board_width, board_height,
                                                 bag=bag, image=image, block_group=block_group, orders='Fall'))
    elif drop_result == 'Ground_landing':
        block_group.add(falling_block)
        if not player.turn_carried_block:
            bag = None
        falling_block_group.add(game_class.Block(board_width, board_height,
                                                 bag=bag, image=image, block_group=block_group, orders='Fall'))
    falling_block.image = graphics_dict[f'pill_{falling_block.letter_direction}']
    falling_block.update(screen)


def update_player(graphics_dict, player, screen):
    player.image = graphics_dict[f'blob_{player.letter_direction}']
    player.update(screen)
    if player.carried_block():
        player.carried_block().image = graphics_dict[f'pill_{player.carried_block().letter_direction}']
        player.carried_block().update(screen)


def update_shadows(falling_block_group, graphics_dict, screen, shadow_tile):
    falling_block = falling_block_group.sprite
    shadow_tile.place_here(falling_block.x_pos, falling_block.y_pos)
    shadow_tile.image = graphics_dict[f'tile_shadow{5-int(falling_block.drop_clock/25)}']
    shadow_tile.update(screen)


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


def full_board_loop_check(block_group, disappear_delay, score):
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
        clear_counter = 0
        for block in block_group:
            if block.marked:
                clear_counter += 1
                block.kill()
        score += clear_counter * (5 * (10 + clear_counter))
    else:
        disappear_delay -= 1
    return disappear_delay, score


def loop_check(chain, block_group):
    latest_block = chain.sprites()[-1]
    board_width, board_height = latest_block.board_width, latest_block.board_height

    next_x = (latest_block.x_pos + latest_block.direction()[0]) % board_width
    next_y = (latest_block.y_pos + latest_block.direction()[1]) % board_height
    for block in chain:
        if next_x == block.x_pos and next_y == block.y_pos:
            for tail_block in chain:
                if next_x == tail_block.x_pos and next_y == tail_block.y_pos:
                    return chain  # This is the loop it returns
                else:
                    chain.remove(tail_block)

    next_block = game_class.probe(next_x, next_y, block_group, board_width, board_height)
    if not next_block:
        return False
    chain.add(next_block)
    loop_or_false = loop_check(chain, block_group)
    return loop_or_false


def make_garbage(block_group, board_width, board_height, graphics_dict, player, falling_block=None, garbage_count=1):
    if falling_block:
        falling_block.drop_clock = 124
    if garbage_count > board_width * board_height - (len(block_group.sprites) + 10):
        garbage_count = board_width * board_height - (len(block_group.sprites) + 10)
    if garbage_count < 0:
        return

    bag = None
    placeholder = graphics_dict['pill_e']
    for _ in range(garbage_count):
        new_block = game_class.Block(board_width, board_height,
                                     bag=bag, image=placeholder, block_group=block_group, orders='Garbage')
        if game_class.probe(new_block.x_pos, new_block.y_pos, block_group, board_width, board_height):
            if not end_game():
                main(display_welcome=False)
            else:
                sys.exit()
        if player.x_pos == new_block.x_pos and player.y_pos == new_block.y_pos:
            player.status = 'Elevated'


def make_ghosts(board_width, board_height, graphics_dict):
    placeholder = graphics_dict['pill_e_ghost']
    for modifier in ['', '_inv']:
        for letter in ['n', 'e', 's', 'w']:
            graphics_dict[f'pill_{letter}{modifier}_ghost'].set_alpha(100)
    ghost_group = pygame.sprite.Group()
    for num in range(board_width):
        ghost_group.add(game_class.Ghost(num, -1, board_width, board_height, image=placeholder),
                        game_class.Ghost(num, board_height, board_width, board_height, image=placeholder))
    for num in range(board_height):
        ghost_group.add(game_class.Ghost(-1, num, board_width, board_height, image=placeholder),
                        game_class.Ghost(board_width, num, board_width, board_height, image=placeholder))
    return ghost_group


# def display_score(score, screen):
#     font_object = pygame.font.Font('freesansbold.ttf', 50)
#     text_object = font_object.render(str(score), False, (255, 255, 0))
#     screen.blit(text_object, (35, 25))
#
#
# def display_text(text, x_pos, y_pos, screen, height_in_pixels=50, colour=(255, 255, 0)):
#     font_object = pygame.font.Font('freesansbold.ttf', height_in_pixels)
#     text_object = font_object.render(text, False, colour)
#     screen.blit(text_object, (x_pos, y_pos))
#     pygame.display.flip()
#
#
# def check_for_space_bar():
#     pygame.time.delay(5)
#     pygame.event.pump()
#     key = pygame.key.get_pressed()
#     if key[pygame.K_SPACE]:
#         return True
#
#
# def welcome(screen):
#     screen.fill((0, 0, 0))
#     the_text, y_pos = '', 25
#     for letter in 'Welcome to BlockJoin| |The goal is to join blocks end-to-end or in a loop|' \
#                   'Use <a><s><d><w> to move|You can carry blocks and drop them with <space>|' \
#                   'You can push blocks with <space>|Press <q> to quit| |Press <space> to close this screen':
#         if letter == '|':
#             the_text = ''
#             y_pos += 45
#             continue
#         the_text += letter
#         display_text(the_text, 50, y_pos, screen, 25, (0, 255, 255))
#         if check_for_space_bar():
#             break
#     for _ in range(1000):
#         if check_for_space_bar():
#             break
#
#
# def end_game():
#     size = 700, 500
#     screen = pygame.display.set_mode(size)
#     pygame.display.set_caption('BlockJoin')
#     display_text('GAME OVER', 200, 75, screen)
#     pygame.time.delay(2000)
#
#     screen.fill((0, 0, 0))
#     display_text('Play again? (y/n)', 150, 75, screen)
#
#     while True:
#         pygame.event.pump()
#         key = pygame.key.get_pressed()  # checking pressed keys
#         if key[pygame.K_n]:
#             screen.fill((0, 0, 0))
#             the_text, y_pos = '', 175
#             for letter in 'Lead programmer: Toke |Graphics, programming: Mads _*_':
#                 if letter == '|':
#                     the_text = ''
#                     y_pos += 100
#                     continue
#                 the_text += letter
#                 display_text(the_text, 100, y_pos, screen, 25, (0, 255, 255))
#                 if check_for_space_bar():
#                     sys.exit()
#                 pygame.time.delay(75)
#             for _ in range(1000):
#                 if check_for_space_bar():
#                     sys.exit()
#         elif key[pygame.K_y]:
#             main(display_welcome=False)
#
#         pygame.time.delay(50)


if __name__ == '__main__':
    main(display_welcome=True)
