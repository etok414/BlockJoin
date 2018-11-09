import random


class Player:
    def __init__(self):
        self.carried_block = False
        self.x_pos = 0
        self.y_pos = 0
        self.direction = 0
        self.dir_dict = {0: (0, 1), 1: (1, 0), 2: (0, -1), 3: (-1, 0)}
        self.status = 'Fine'
        # Status is 'Fine' if the player is on the ground, 'Elevated' if it's on a block, and if it's holding a block,
        # that's its status.

    def receive_input(self, recieved_input, board):
        pass

    def move(self, direction, board):
        # TODO: Movement animation.
        moved_coors = (self.x_pos + self.dir_dict[direction][0], self.y_pos + self.dir_dict[direction][0])
        probe_result = board.probe(moved_coors)

        if probe_result and self.direction == direction:
            if probe_result == 'Occupied':
                if self.status == 'Fine':
                    self.status = 'Elevated'
                    # TODO: Animation for jumping onto blocks.
                elif self.status != 'Elevated':
                    return
                    # If it goes here, it's because it's holding a block, and therefore can't jump.
            elif self.status == 'Elevated':
                # TODO: Animation for jumping off blocks.
                self.status = 'Fine'
            self.x_pos, self.y_pos = moved_coors

        else:
            self.direction = direction
            if self.status != 'Fine' and self.status != 'Elevated':
                self.status.orientation = direction

    def push(self, board):
        if self.status == 'Fine':
            # TODO: Punch animation.
            relevant_dir = (self.dir_dict[self.direction][0], self.dir_dict[self.direction][0])
            if board.probe((self.x_pos + relevant_dir[0], self.y_pos + relevant_dir[1])) == 'Occupied' \
                    and board.probe((self.x_pos + relevant_dir[0]*2, self.y_pos + relevant_dir[1]*2)) == 'Empty':
                board.blocks[(self.x_pos + relevant_dir[0]*2, self.y_pos + relevant_dir[1]*2)] = board.blocks[
                    (self.x_pos + relevant_dir[0], self.y_pos + relevant_dir[1])]
                board.blocks[(self.x_pos + relevant_dir[0], self.y_pos + relevant_dir[1])] = None
        elif self.status == 'Elevated':
            pass
            # TODO: Punch animation.
        else:
            board.blocks[(self.x_pos, self.y_pos)] = self.status
            moved_coors = (self.x_pos - self.dir_dict[self.direction][0], self.y_pos - self.dir_dict[self.direction][0])
            probe_result = board.probe(moved_coors)
            if probe_result:
                self.x_pos, self.y_pos = moved_coors

            if board.probe((self.x_pos, self.y_pos)) == 'Occupied':
                self.status = 'Elevated'
            else:
                self.status = 'Fine'



class Board:
    def __init__(self, height, width):
        self.bag = [0, 1, 2, 3]
        random.shuffle(self.bag)
        self.blocks = {}
        self.height = height
        self.width = width

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
        if 0 <= coordinate[0] <= self.width and 0 <= coordinate[1] <= self.height:
            if self.blocks.get(coordinate):
                return 'Occupied'
            else:
                return 'Empty'


def main():
    pass


if __name__ == '__main__':
    main()
