# import sys
import pygame
from graphics import initialize


# import game_class


def main():
    graphics_dict, screen = initialize()
    pygame.font.init()
    font_object = pygame.font.Font('freesansbold.ttf', 50)
    text_object = font_object.render('Test', False, (255, 255, 0))
    screen.blit(text_object, (100, 100))

    pygame.display.flip()
    x = 100

    while True:
        #     time_to_move = next(cool_down_number())
        #     print(time_to_move)
        text_object = font_object.render('Rap', False, (255, 255, 0))
        screen.blit(text_object, (x, 200))
        x += 100
        pygame.display.flip()
        pygame.time.delay(500)


# def cool_down_number():
#     value = 0
#     while value < 10:
#         return_value = value % 4
#         yield return_value
#         value += 1
#         print('rap', return_value)

# tile_dict = dict()
# graphics_dict, screen = initialize()
# width, height = 6, 6
# tile = game_class.Thing(width, height, image=graphics_dict['tile'])
# tile_dict['1'] = tile
# tile = game_class.Thing(width, height, image=graphics_dict['tile'])
# tile_dict['2'] = tile
# for n, flise in enumerate(tile_dict):
#     print(n, (n+5)*30, 5)
#     tile_dict[flise].place_here(n, 5)
#     update_thing_pos(tile_dict[flise],screen)
#     # move_sprite_to((n + 5) * 30, 5, tile_dict[flise].rect, graphics_dict['tile'], screen)
#     # update_thing_pos(flise, screen)
#
# pygame.display.flip()
# pygame.time.delay(1000)

# draw_board(6, 6, graphics_dict['tile'], screen)
# red = (255, 0, 0)
# block = Block(red, 50, 50)
# screen.blit(block.image, block.rect)
# print(block.image, block.rect, block.image.fill(red))
#
# while True:
#     screen.blit(block.image, block.rect)
#     for event in pygame.event.get():  # Close nicely and display changes
#         if event.type == pygame.QUIT:
#             sys.exit()
#     pygame.display.flip()
#     pygame.time.delay(150)


if __name__ == '__main__':
    main()
