import random


class Actor:
    def __init__(self, board_width, board_height, direction, x_pos, y_pos):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.letter_direction = direction
        self.board_width = board_width
        self.board_height = board_height

    def direction(self, direction=None):
        if direction is None:
            return {'n': (0, 1), 'e': (1, 0), 's': (0, -1), 'w': (-1, 0)}[self.letter_direction]
        else:
            return {'n': (0, 1), 'e': (1, 0), 's': (0, -1), 'w': (-1, 0)}[direction]

    def receive_input(self, received_input):
        pass

    def move(self, movement_direction, block_list, can_jump=False):
        # TODO: Movement animation.
        moved_coors = (self.x_pos + self.direction(movement_direction)[0],
                       self.y_pos + self.direction(movement_direction)[1])
        probe_result = self.probe(moved_coors[0], moved_coors[1], block_list)

        if probe_result and (probe_result == 'Empty' or can_jump):
            self.x_pos, self.y_pos = moved_coors

    def probe(self, x_coor, y_coor, block_list):
        # Returns the block that occupies the space if it's occupied, 'Empty' if it's empty, and
        # None if it's outside the board
        if 0 <= x_coor < self.board_width and 0 <= y_coor < self.board_height:
            for block in block_list:
                if block.x_pos == x_coor and block.y_pos == y_coor:
                    return block
            return 'Emtpy'

    def get_real_pos(self, x, y):
        x += self.x_pos * 50
        y += self.y_pos * 50

        y = -y  # This is because pygame's coordinate system is upside down
        return x, y


class Player(Actor):
    def __init__(self, board_width, board_height):
        super().__init__(board_width, board_height, 'e', 0, 0)
        self.status = 'Fine'
        # Status is 'Fine' if the actor can jump, 'Elevated' if it's atop a block, and 'Grounded' if it can't jump.
        # TODO: Status currently only serves to tell the animation if the player should be elevated.
        self.carried_block = False

    def move(self, movement_direction, block_list, turn_to_face=True):
        if self.letter_direction != movement_direction and turn_to_face:
            self.letter_direction = movement_direction
            if self.carried_block:
                self.carried_block.letter_direction = movement_direction
        else:
            super().move(movement_direction, block_list, can_jump=False if self.carried_block else True)
            if self.carried_block:
                self.status = 'Grounded'
            elif self.probe(self.x_pos, self.y_pos, block_list) != 'Empty':
                self.status = 'Elevated'
                # TODO: Animation for jumping onto blocks.
            else:
                # TODO: Animation for jumping off blocks.
                self.status = 'Fine'

    def push(self, block_list):
        direction = self.direction()
        if self.carried_block:
            block_list.append(Block(self.carried_block.board_width, self.carried_block.board_height,
                                    self.carried_block.bag , self.carried_block.direction, self.carried_block.x_pos,
                                    self.carried_block.y_pos))
            self.carried_block = None
            reversal_dict = {'n': 's', 'e': 'w', 's': 'n', 'w': 'e'}
            self.move(reversal_dict[self.letter_direction], block_list, turn_to_face=False)
        else:
            if self.status == 'Fine':
                probe_result = self.probe(self.x_pos + direction[0], self.y_pos + direction[0], block_list)
                if probe_result and probe_result != 'Empty':
                    probe_result.move(self.letter_direction, block_list)
            # TODO: Punch animation.

    def get_real_pos(self, x, y):
        if self.status == 'Elevated':
            x -= 25
            y += 25
        return super().get_real_pos(x, y)


class Block(Actor):
    def __init__(self, board_width, board_height, bag=None, direction=None, x_pos=None, y_pos=None):
        if self.x_pos is None and self.y_pos is None:
            self.drop_clock = 150
        else:
            self.drop_clock = 0
        if self.x_pos is None:
            self.x_pos = random.randrange(1, self.board_width - 2)
        if self.y_pos is None:
            self.y_pos = random.randrange(1, self.board_height - 2)
        if self.letter_direction is None:
            if bag is None:
                bag = ['n', 'e', 's', 'w']
                random.shuffle(bag)
            self.letter_direction = bag.pop(0)
        self.bag = bag
        super().__init__(board_width, board_height, direction, x_pos, y_pos)

    def update_falling(self, player, block_list, clock_ticks=1):
        self.drop_clock -= clock_ticks
        if self.drop_clock <= 0:
            if self.probe(self.x_pos, self.y_pos, block_list) != 'Empty':
                return 'Failure'
            elif self.x_pos == player.x_pos and self.y_pos == player.y_pos:
                if player.carried_block:
                    return 'Failure'
                return 'Head_landing'
            else:
                return 'Ground_landing'

    def get_real_pos(self, x, y):
        if self.drop_clock > 0:
            x -= 25
            y += 25
            x -= self.drop_clock
            y += self.drop_clock
        return super().get_real_pos(x, y)


def ghosts(self):
    pass


def gridlock_check(self):
    pass


def compare(self):
    pass
