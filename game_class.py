import random
import pygame


class Thing(pygame.sprite.Sprite):
    def __init__(self, x_pos=0, y_pos=0, image=None):
        super().__init__()
        self.pos = self.x_pos, self.y_pos = x_pos, y_pos
        self.image = image
        self.rect = self.image.get_rect()

    def calc_screen_pos(self):
        x_c = self.x_pos * 50
        y_c = -self.y_pos * 50
        x_i, y_i = x_c - y_c, (x_c + y_c) / 2
        return x_i, y_i

    def place_here(self, x, y):
        self.x_pos, self.y_pos = x, y

    def update(self, screen):
        x_i, y_i = self.calc_screen_pos()
        self.rect.centerx, self.rect.centery = 100 + x_i, 300 + y_i
        screen.blit(self.image, self.rect)


class Actor(Thing):
    def __init__(self, board_width, board_height, direction='e', x_pos=0, y_pos=0, image=None):
        super().__init__(x_pos, y_pos, image)
        self.letter_direction = direction
        self.board_width = board_width
        self.board_height = board_height

    def direction(self, direction=None):
        """ Translate direction string n, e, w, s to direction vector i, j, -i, -j """
        if direction is None:
            direction = self.letter_direction

        return {'n': (0, 1), 'e': (1, 0), 'w': (-1, 0), 's': (0, -1)}[direction]

    def take_step(self, movement_direction, block_group, can_jump=False):
        delta_x, delta_y = self.direction(movement_direction)
        moved_x = self.x_pos + delta_x
        moved_y = self.y_pos + delta_y
        probe_result = probe(moved_x, moved_y, block_group, self.board_width, self.board_height)

        if probe_result is not None and (probe_result is False or can_jump):
            self.place_here(moved_x, moved_y)


class Player(Actor):
    def __init__(self, board_width, board_height, image):
        super().__init__(board_width, board_height, 'e', 0, 0, image)

        self.turn_carried_block = False
        self.status = 'Fine'
        # Status is 'Fine' if the actor can jump, 'Elevated' if it's atop a block, and 'Grounded' if it can't jump.
        # TODO: Status currently only serves to tell the animation if the player should be elevated.
        self.carried_block_group = pygame.sprite.GroupSingle()

    def carried_block(self):
        return self.carried_block_group.sprite

    def take_step(self, movement_direction, block_group, back_jump=False):
        if self.letter_direction != movement_direction and not back_jump:
            self.letter_direction = movement_direction
            if self.carried_block() and self.turn_carried_block:
                self.carried_block().letter_direction = movement_direction
        else:
            can_jump = False if self.carried_block() and not back_jump else True
            super().take_step(movement_direction, block_group, can_jump=can_jump)
            if probe(self.x_pos, self.y_pos, block_group, self.board_width, self.board_height):
                self.status = 'Elevated'
            else:
                self.status = 'Fine'
            if self.carried_block() and not back_jump:
                self.carried_block().place_here(self.x_pos, self.y_pos)
                self.status = 'Grounded'

    def push_block(self, block_group):
        if self.carried_block():
            self.carried_block().drop_clock = 0
            block_group.add(self.carried_block())
            reversal_dict = {'n': 's', 'e': 'w', 's': 'n', 'w': 'e'}
            self.take_step(reversal_dict[self.letter_direction], block_group, back_jump=True)
            self.carried_block_group.empty()
        else:
            delta_x, delta_y = self.direction()
            if not probe(self.x_pos, self.y_pos, block_group, self.board_width, self.board_height):
                probe_result = probe(self.x_pos + delta_x, self.y_pos + delta_y,
                                     block_group, self.board_width, self.board_height)
                if probe_result:
                    probe_result.take_step(self.letter_direction, block_group)
            # TODO: Punch animation.
            # TODO: Check line above. It says "unresolved attribute error"

    def calc_screen_pos(self):
        x_i, y_i = super().calc_screen_pos()
        if self.status == 'Elevated':
            y_i -= 25
        return x_i, y_i


class Block(Actor):
    def __init__(self, board_width, board_height, bag=None, direction=None, x_pos=None, y_pos=None, image=None,
                 block_group=None, orders='Fall'):
        super().__init__(board_width, board_height, direction, x_pos, y_pos, image)
        if orders == 'Fall':
            self.drop_clock = 124
            self.x_pos = random.randrange(1, self.board_width - 2)
            self.y_pos = random.randrange(1, self.board_height - 2)
            if block_group is not None:
                if probe(self.x_pos, self.y_pos, block_group, board_height, board_width):
                    self.x_pos = random.randrange(1, self.board_width - 2)
                    self.y_pos = random.randrange(1, self.board_height - 2)
        elif orders == 'Garbage':
            self.x_pos = random.randrange(1, self.board_width)
            self.y_pos = random.randrange(1, self.board_height)
            if block_group is not None:
                for _ in range(board_width*board_height):
                    if probe(self.x_pos, self.y_pos, block_group, board_height, board_width):
                        self.x_pos = random.randrange(1, self.board_width)
                        self.y_pos = random.randrange(1, self.board_height)
                    else:
                        break
                if probe(self.x_pos, self.y_pos, block_group, board_height, board_width):
                    self.x_pos, self.y_pos = None, None

        if self.x_pos is None and self.y_pos is None:
            for x in range(board_width):
                for y in range(board_height):
                    if not probe(x, y, block_group, board_height, board_width):
                        self.x_pos, self.y_pos = x, y
                        block_group.add(self)
        else:
            self.drop_clock = 0
        if self.letter_direction is None:
            if not bag:
                bag = ['n', 'e', 's', 'w']
                random.shuffle(bag)
            self.letter_direction = bag.pop(0)
        self.marked = False
        self.bag = bag

    def select_image(self, graphics_dict, falling_block=None):
        self.image = graphics_dict[f'pill_{self.letter_direction}']
        if self.marked:
            self.image = graphics_dict[f'pill_{self.letter_direction}_inv']
        elif falling_block:
            if self.x_pos == falling_block.x_pos and self.y_pos == falling_block.y_pos:
                self.image = graphics_dict[f'pill_{self.letter_direction}_shadow{5-int(falling_block.drop_clock/25)}']

    def update_falling(self, player, block_group, clock_ticks=1):
        self.drop_clock -= clock_ticks
        if self.drop_clock <= 0:
            self.drop_clock = 0
            probe_result = probe(self.x_pos, self.y_pos, block_group, self.board_width, self.board_height)
            if probe_result:
                if not probe_result.marked:
                    return 'Failure'
            if self.x_pos == player.x_pos and self.y_pos == player.y_pos:
                if player.carried_block():
                    return 'Failure'
                return 'Head_landing'
            else:
                return 'Ground_landing'

    def calc_screen_pos(self):
        x_i, y_i = super().calc_screen_pos()
        if self.drop_clock > 0:
            y_i -= 25
            y_i -= self.drop_clock
        return x_i, y_i


class Ghost(Thing):
    def __init__(self, x_pos, y_pos, board_width, board_height, image=None):
        super().__init__(x_pos, y_pos, image)
        self.board_width = board_width
        self.board_height = board_height

    def update(self, screen, block_group=None, graphics_dict=None):
        if block_group and graphics_dict:
            probe_result = probe(self.x_pos % self.board_width, self.y_pos % self.board_height,
                                 block_group, self.board_width, self.board_height)
            if probe_result:
                self.image = graphics_dict[f'pill_{probe_result.letter_direction}'
                                           f'{"_inv" if probe_result.marked else ""}_ghost']
                super().update(screen)


def probe(x_coor, y_coor, block_group, board_width, board_height):
    """ Returns the block that occupies the tested space if it's occupied, returns False if it's empty,
    and None if it's outside the board """
    if 0 <= x_coor < board_width and 0 <= y_coor < board_height:
        for block in block_group:
            if block.x_pos == x_coor and block.y_pos == y_coor:
                return block
        return False
    else:
        return None
