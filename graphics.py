import os
import sys
import pygame
import game_class

BLACK = (0, 0, 0)


def initialize_graphics():
    pygame.init()
    pygame.font.init()

    size = 700, 500
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('BlockJoin')

    graphics_dict = dict()  # A dictionary for all images with their filename as keys

    base_folder = os.path.dirname(__file__)
    folder = 'graphics'  # All graphics for the game have to go into this folder as .png or .PNG
    _path = os.path.join(base_folder, folder)
    path = os.path.normpath(_path)

    file_list = os.listdir(path)  # All files in the graphics directory is read into a list...

    for file_name in file_list:  # ...and only the .png files are loaded and stored in a dict with filename as key
        if file_name[-4:].lower() == '.png':
            _full_path = os.path.join(base_folder, folder, file_name)
            full_path = os.path.normpath(_full_path)

            graphics_dict[file_name[:-4]] = pygame.image.load(full_path).convert()
            graphics_dict[file_name[:-4]].set_colorkey(BLACK)  # Pseudo alpha channel. All black (RGB(0,0,0)) is ignored

    return graphics_dict, screen


def draw_board(graphics_dict, width, height, screen):
    # TODO Is it necessary to pass in screen if drawing is delegated to board_tile_group(screen) later?
    screen.fill(BLACK)
    board_tile_group = pygame.sprite.Group()
    for x_c in range(width):
        for y_c in range(height):
            tile = game_class.Thing(x_c, y_c, image=graphics_dict['tile'])
            tile.update(screen)
            board_tile_group.add(tile)

    return board_tile_group


def main():
    """ Just for testing purposes """
    pass
    # graphics_dict, screen = initialize()
    # width, height = 6, 6

    while True:
        for event in pygame.event.get():  # Close nicely and display changes
            if event.type == pygame.QUIT:
                sys.exit()
        pygame.display.flip()
        pygame.time.delay(150)


if __name__ == '__main__':
    main()
