import sys
import pygame
from graphics import initialize, update_thing_pos, move_sprite_to
import game_class


def main():
    tile_dict = dict()
    graphics_dict, screen = initialize()
    width, height = 6, 6
    tile = game_class.Thing(width, height, image=graphics_dict['tile'])
    tile_dict['1'] = tile
    tile = game_class.Thing(width, height, image=graphics_dict['tile'])
    tile_dict['2'] = tile
    for n, flise in enumerate(tile_dict):
        print(n, (n+5)*30, 5)
        tile_dict[flise].place_here(n, 5)
        update_thing_pos(tile_dict[flise],screen)
        # move_sprite_to((n + 5) * 30, 5, tile_dict[flise].rect, graphics_dict['tile'], screen)
        # update_thing_pos(flise, screen)

    pygame.display.flip()
    pygame.time.delay(1000)

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
