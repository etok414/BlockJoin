import random


class Player:
    def __init__(self):
        self.carried_block = False
        self.x_pos = 0
        self.y_pos = 0
        self.direction = 0
        self.dir_dict = {0: (0, 1), 1: (1, 0), 2: (0, -1), 3: (-1, 0)}
        self.status = 'Fine'

    def receive_input(self, recieved_input, board):
        pass

    def move(self, direction, board):
        moved_coors = (self.x_pos + self.dir_dict[direction][0], self.y_pos + self.dir_dict[direction][0])
        probe_result = board.probe(moved_coors)

        if probe_result and self.direction == direction:
            if probe_result == 'Occupied':
                if self.status == 'Holding':
                    return
                else:
                    self.status = 'Elevated'
            self.x_pos, self.y_pos = moved_coors

        else:
            self.direction = direction

    def push(self, board):
        if self.status == 'Holding':
            pass
        else:
            # TODO: punch animation
            relevant_dir = (self.dir_dict[self.direction][0], self.dir_dict[self.direction][0])
            if board.probe((self.x_pos + relevant_dir[0], self.y_pos + relevant_dir[1])) == 'Occupied' \
                    and board.probe((self.x_pos + relevant_dir[0]*2, self.y_pos + relevant_dir[1]*2)) == 'Empty':
                pass



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
    print('AAA')
