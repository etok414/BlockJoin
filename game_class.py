import random


class Game:
    def __init__(self, height, width):
        self.carried_block = False
        self.x_pos = 0
        self.y_pos = 0
        self.number_direction = 0
        self.dir_dict = {0: (0, 1), 1: (1, 0), 2: (0, -1), 3: (-1, 0)}
        self.status = 'Fine'
        # Status is 'Fine' if the player is on the ground, 'Elevated' if it's on a block, and if it's holding a block,
        # that's its status.
        self.bag = [0, 1, 2, 3]
        random.shuffle(self.bag)
        self.blocks = {}
        self.board_height = height
        self.board_width = width

    def direction(self):
        return self.dir_dict[self.number_direction]

    def receive_input(self, received_input):
        pass

    def move(self, movement_direction):
        # TODO: Movement animation.
        if self.number_direction != movement_direction:
            self.number_direction = movement_direction
            if self.status != 'Fine' and self.status != 'Elevated':
                self.status.orientation = movement_direction
        else:
            moved_coors = (self.x_pos + self.direction()[0], self.y_pos + self.direction()[1])
            probe_result = self.probe(moved_coors)

            if probe_result:
                if probe_result == 'Occupied':
                    if self.status == 'Fine':
                        self.status = 'Elevated'
                        # TODO: Animation for jumping onto blocks.
                    elif self.status != 'Elevated':
                        return
                        # If it goes here, it's because it's holding a block, and therefore can't jump.
                elif self.status == 'Elevated' and probe_result == 'Empty':
                    # TODO: Animation for jumping off blocks.
                    self.status = 'Fine'
                self.x_pos, self.y_pos = moved_coors

    def push(self):
        direction = self.direction()
        if self.status == 'Fine':
            # TODO: Punch animation.
            pf_space = (self.x_pos + direction[0], self.y_pos + direction[0])  # pf: push from
            pt_space = (self.x_pos + direction[0] * 2, self.y_pos + direction[0] * 2)  # pt: push to
            if self.probe(pf_space) == 'Occupied' and self.probe(pt_space) == 'Empty':
                self.blocks[pt_space] = self.blocks[pf_space]
                self.blocks[pf_space] = None
        elif self.status == 'Elevated':
            pass
            # TODO: Punch animation.
        else:
            # If self.status isn't 'Fine' or 'Elevated', it's the block it's carrying.
            self.blocks[(self.x_pos, self.y_pos)] = self.status
            moved_coors = (self.x_pos - direction[0], self.y_pos - direction[0])
            if self.probe(moved_coors):
                self.x_pos, self.y_pos = moved_coors

            if self.probe((self.x_pos, self.y_pos)) == 'Occupied':
                self.status = 'Elevated'
            else:
                self.status = 'Fine'

    def make_block(self, orientation, is_ghost=False):
        pass

    def update(self):
        pass

    def ghosts(self):
        pass

    def gridlock_check(self):
        pass

    def compare(self):
        pass

    def probe(self, coordinate):
        # Returns 'Occupied' if the space is occupied, 'Empty' if it's empty, and None if it doesn't exist
        if 0 <= coordinate[0] <= self.board_width and 0 <= coordinate[1] <= self.board_height:
            if self.blocks.get(coordinate):
                return 'Occupied'
            else:
                return 'Empty'
