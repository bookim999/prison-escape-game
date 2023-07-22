# Nikki Kim

# creation of class game_map
class game_map:
    # remembering content of map_file and guard_file
    # creation of variables for future use
    def __init__(self, map_file, guard_file):
        self.map_file = map_file
        self.guard_file = guard_file
        self.current_grid = []
        self.guard_list = []

        try:
            # creating 2D list of 12 rows x 16 characters from map_file content
            # opening map_file to read from it
            map_opener = open(self.map_file)
            for count in range(12):
                # reading each line in map_file and turning it into a list
                line = map_opener.readline()
                list_line = list(line)
                # removing new line character in each line
                if "\n" in list_line:
                    list_line.remove("\n")

                # ensuring that each sublist has 16 characters
                if len(list_line) < 16:
                    difference = 16 - len(list_line)
                    spaces = " "
                    list_line.extend(spaces * difference)

                    self.current_grid.append(list_line)

                else:
                    self.current_grid.append(list_line)

            # closing map_file
            map_opener.close()

            # opening guard_file to read from it
            guard_opener = open(self.guard_file)
            # creating guard object for every guard (each line) in guard_file
            # calculating the guard's row, col, attack_range, and movements for later use
            # storing created guard object in guard_list
            for line in guard_opener:
                each_guard = line.split()
                row = int(each_guard[0])
                col = int(each_guard[1])
                attack_range = int(each_guard[2])
                movements = each_guard[3:]
                guard_object = guard(row, col, attack_range, movements)
                self.guard_list.append(guard_object)

            # putting guard on game map
            for each_guard in self.guard_list:
                self.current_grid[each_guard.guard_row][each_guard.guard_col] = "G"

            # finding player position on game map
            for row in range(len(self.current_grid)):
                for col in range(len(self.current_grid[0])):
                    if self.current_grid[row][col] == "P":
                        self.player_row = row
                        self.player_col = col

            # finding exit position on game map
            for row in range(len(self.current_grid)):
                for col in range(len(self.current_grid[0])):
                    if self.current_grid[row][col] == 'E':
                        self.exit_row = row
                        self.exit_col = col

            # closing guard_file
            guard_opener.close()

        # exception code to run when IO error encountered
        except IOError as io_error:
            print("IOError:", io_error)
            exit()

        # exception code to run when index error encountered
        except IndexError as index_error:
            print("IndexError:", index_error)
            exit()

        # exception code to run when value error encountered
        except ValueError as value_error:
            print("ValueError:", value_error)
            exit()

    # retrieves the game map
    def get_grid(self):
        current_grid = self.current_grid
        return current_grid

    # retrieves the list of guard objects
    def get_guards(self):
        return self.guard_list

    # for updating new player position
    def update_player(self, direction):
        # empty grid in location of player
        self.current_grid[self.player_row][self.player_col] = ' '

        # update player position depending on direction parameter
        # ensure player cannot walk into wall, guard, or off-grid
        if direction == 'U' and self.player_row == 0:
            pass

        elif direction == 'D' and self.player_row == 11:
            pass

        elif direction == 'L' and self.player_col == 0:
            pass

        elif direction == 'R' and self.player_col == 15:
            pass

        elif direction == 'U' and self.current_grid[self.player_row - 1][self.player_col] != '#' \
                and self.current_grid[self.player_row - 1][self.player_col] != 'G':
            self.player_row = self.player_row - 1

        elif direction == 'D' and self.current_grid[self.player_row + 1][self.player_col] != '#' \
                and self.current_grid[self.player_row + 1][self.player_col] != 'G':
            self.player_row = self.player_row + 1

        elif direction == 'L' and self.current_grid[self.player_row][self.player_col - 1] != '#' \
                and self.current_grid[self.player_row][self.player_col - 1] != 'G':
            self.player_col = self.player_col - 1

        elif direction == 'R' and self.current_grid[self.player_row][self.player_col + 1] != '#' \
                and self.current_grid[self.player_row][self.player_col + 1] != 'G':
            self.player_col = self.player_col + 1

        # assign new updated position for player
        self.current_grid[self.player_row][self.player_col] = 'P'

    # for updating each guard position
    def update_guards(self):
        for each_guard in self.guard_list:
            # find current position of each guard
            guard_pos = each_guard.get_location()
            guard_row = guard_pos[0]
            guard_col = guard_pos[1]
            # empty current guard location in grid
            self.current_grid[guard_row][guard_col] = ' '
            # find the new row and column that the guard will move into
            new_r, new_c = each_guard.move(self.current_grid)
            # update grid with new position of guard
            self.current_grid[new_r][new_c] = 'G'

    # for determining whether player won by reaching the exit
    def player_wins(self):
        if self.player_row == self.exit_row and self.player_col == self.exit_col:
            return True

        else:
            return False

    # for determining whether player loses by being in the attack range of guard
    def player_loses(self):
        for each_guard in self.guard_list:
            if each_guard.enemy_in_range(self.player_row, self.player_col):
                return True
        return False


# creation of class guard
class guard:
    def __init__(self, row, col, attack_range, movements):
        # remembering all information given through parameters
        # assign variables for future use
        self.guard_row = row
        self.guard_col = col
        self.attack_range = attack_range
        self.guard_movements = movements
        self.counter = -1
        self.current_grid = []

    # retrieves location of each guard
    def get_location(self):
        return self.guard_row, self.guard_col

    # assigns a new position for each guard based on the guard's movements list
    def move(self, current_grid):
        self.current_grid = current_grid

        # count what move the guard is at in the guard_movements list
        # if guard reaches the last move in the list, it returns to the first move in the list
        self.counter += 1
        if self.counter == len(self.guard_movements):
            self.counter = 0

        move = self.guard_movements[self.counter]

        # update guard position depending on the movement in the guard_movements list
        # guard position is only updated if it is not moving into a wall, player, exit, or off-grid
        if move == 'U' and self.guard_row == 0:
            pass

        elif move == 'D' and self.guard_row == 11:
            pass

        elif move == 'L' and self.guard_col == 0:
            pass

        elif move == 'R' and self.guard_col == 15:
            pass

        elif move == 'U' and self.current_grid[self.guard_row - 1][self.guard_col] != '#' \
                and self.current_grid[self.guard_row - 1][self.guard_col] != 'E' \
                and self.current_grid[self.guard_row - 1][self.guard_col] != 'P' \
                and self.current_grid[self.guard_row - 1][self.guard_col] != 'G':
            self.guard_row = self.guard_row - 1

        elif move == 'D' and self.current_grid[self.guard_row + 1][self.guard_col] != '#' \
                and self.current_grid[self.guard_row + 1][self.guard_col] != 'E' \
                and self.current_grid[self.guard_row + 1][self.guard_col] != 'P' \
                and self.current_grid[self.guard_row + 1][self.guard_col] != 'G':
            self.guard_row = self.guard_row + 1

        elif move == 'L' and self.current_grid[self.guard_row][self.guard_col - 1] != '#' \
                and self.current_grid[self.guard_row][self.guard_col - 1] != 'E' \
                and self.current_grid[self.guard_row][self.guard_col - 1] != 'P' \
                and self.current_grid[self.guard_row][self.guard_col - 1] != 'G':
            self.guard_col = self.guard_col - 1

        elif move == 'R' and self.current_grid[self.guard_row][self.guard_col + 1] != '#' \
                and self.current_grid[self.guard_row][self.guard_col + 1] != 'E' \
                and self.current_grid[self.guard_row][self.guard_col + 1] != 'P' \
                and self.current_grid[self.guard_row][self.guard_col + 1] != 'G':
            self.guard_col = self.guard_col + 1

        # assign new position for guard
        new_pos = self.guard_row, self.guard_col
        return new_pos

    # checking whether player is in range of guard's attack
    def enemy_in_range(self, enemy_row, enemy_col):
        # calculating distance between guard and player through Manhattan distance formula abs(a-x) + abs(b-y)
        # where guard's position is (a,b) and player's position is (x,y)
        enemy_distance = abs(self.guard_row - enemy_row) + abs(self.guard_col - enemy_col)

        # player is attacked by guard if the distance between them is less than or equal to attack range
        if enemy_distance <= self.attack_range:
            return True
        else:
            return False
