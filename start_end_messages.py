import sys
import pygame


def display_score(score, screen):
    font_object = pygame.font.Font('freesansbold.ttf', 50)
    text_object = font_object.render(str(score), False, (255, 255, 0))
    screen.blit(text_object, (50, 50))


def display_text(text, x_pos, y_pos, screen, height_in_pixels=50, colour=(255, 255, 0)):
    font_object = pygame.font.Font('freesansbold.ttf', height_in_pixels)
    text_object = font_object.render(text, False, colour)
    screen.blit(text_object, (x_pos, y_pos))
    pygame.display.flip()


def check_for_space_bar():
    pygame.time.delay(5)

    pygame.event.pump()
    key = pygame.key.get_pressed()
    if key[pygame.K_SPACE] or key[pygame.K_q]:
        return True


def check_for_1_2():
    pygame.time.delay(5)

    pygame.event.pump()
    key = pygame.key.get_pressed()
    if key[pygame.K_1] or key[pygame.K_SPACE] or key[pygame.K_q]:
        return 1
    elif key[pygame.K_2]:
        return 2


def welcome(screen):
    screen.fill((0, 0, 0))
    the_text, y_pos = '', 25
    for letter in 'Welcome to BlockJoin| |The goal is to join blocks end-to-end or in a loop|' \
                  'Use <a><s><d><w> to move|You can carry blocks and drop them with <space>|' \
                  'You can push blocks with <space>|Press <q> to quit| |Press <space> to close this screen':
        if letter == '|':
            the_text = ''
            y_pos += 45
            continue
        the_text += letter
        display_text(the_text, 50, y_pos, screen, 25, (0, 255, 255))
        if check_for_space_bar():
            break
    while True:
        if check_for_space_bar():
            break


def choose_game_mode(screen):
    screen.fill((0, 0, 0))
    the_text, y_pos = '', 25
    pygame.time.delay(100)
    for letter in 'Please choose game mode|' \
                  '<1> The carried block turn with the player (default)|' \
                  '<2> The carried block have the original direction|        at all times':
        if letter == '|':
            the_text = ''
            y_pos += 45
            continue
        the_text += letter
        display_text(the_text, 50, y_pos, screen, 25, (0, 255, 255))
        pygame.time.delay(50)
        if check_for_1_2() == 1:
            return True
        elif check_for_1_2() == 2:
            return False
    while True:
        pygame.time.delay(50)
        if check_for_1_2() == 1:
            return True
        elif check_for_1_2() == 2:
            return False


def end_game():
    size = 700, 500
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('BlockJoin')

    display_text('GAME OVER', 150, 75, screen)
    pygame.time.delay(500)

    display_text('Play again? (y/n)', 150, 200, screen)
    while True:
        pygame.event.pump()
        key = pygame.key.get_pressed()  # checking pressed keys
        if key[pygame.K_n]:
            show_credits(screen)
        elif key[pygame.K_y]:
            return False

        pygame.time.delay(50)


def show_credits(screen):
    screen.fill((0, 0, 0))
    the_text, y_pos = '', 175
    for letter in 'Lead programmer: Toke |Graphics, programming: Mads _*_':
        if letter == '|':
            the_text = ''
            y_pos += 100
            continue
        the_text += letter
        display_text(the_text, 100, y_pos, screen, 25, (0, 255, 255))
        if check_for_space_bar():
            sys.exit()
        pygame.time.delay(75)
    for _ in range(1000):
        if check_for_space_bar():
            sys.exit()
