"""
Conway's Game of Life, recreation by me.
"""
import os
import random
from time import sleep

try:
    from termcolor import colored
except ImportError:
    print("termcolor module not detected. Using default colors...")

class GameOfLife:
    """
    Rules
    -----
    For each space that is populated:
        -> each cell with one or no neighbors dies, as if by solitude
        -> each cell with four or more neighbors dies, as if by overpopulation
        -> each cell with two or three neighbors survives.
    For a space that is empty or unpopulated:
        -> each cell with three neighbors becomes populated
    """

    def __init__(self):
        self.map_height = 0
        self.map_width = 0
        self.print_speed = 0.5
        self.frequency = 0
    
        self.cell_string = "#"
        self.empty_tile_string = "."
    
        self.custom = False


    def setup(self):
        """
        First prompt the user if they want to enter custom values for the intial state
        or use the default map that was hard-coded onto here.
        """
        print("Conway's Game of Life")
        print("---------------------")
        print("Set custom values or use the default map from the source code?")
        print("1: custom 2: default")
        while True:
            user_selection = input(">> ")
            if user_selection == "1":
                self.custom = True
                try:
                    self.map_height = int(input("Enter map height: "))
                    self.map_width = int(input("Enter map width: "))
                    self.frequency = int(input("(0% - 100%) Enter frequency of cells in initial state: "))
                    self.cell_string = input("Enter symbol for cell: ")
                    self.empty_tile_string = input("Enter symbol for empty tile: ")
                except ValueError:
                    raise Exception("Inappropriate values.")
                break
            elif user_selection == "2":
                self.map_height = len(self._get_starting_map())
                self.map_width = len(self._get_starting_map()[0])
                break
            else:
                print("Unknown input")

        self._game_of_life()


    def _print_map(self, game_map: list) -> None:
        """
        Prints map to the terminal for every generation using custom values from user selection
        ::params::
            game_map (list) - 2d list filled with 1's and 0's
        """
        print("Conway's Game Of Life")
        for row in game_map:
            for tile in row:
                if tile != 1:
                    print(colored(self.empty_tile_string, 'white'), end="  ")
                    # print(self.empty_tile_string, end="  ")
                    continue
                print(colored(self.cell_string, 'green'), end="  ")
                # print(self.cell_string, end="  ")
            print()


    def _game_of_life(self) -> None:
        """Main logic of the game"""
        # (Needed) Create duplicate map as to not mess up cell interactions at a time.
        game_map = self._get_starting_map()
        game_map_temp = self._get_starting_map()

        self._print_map(game_map_temp)
        print()

        while True:
            sleep(self.print_speed)
            os.system("clear")

            # Check each tile in the map one at a time.
            for i in range(self.map_height):
                for j in range(self.map_width):

                    # Check the 3x3 adjacent tiles around current
                    # tile not including itself and track neighbors.
                    num_neighbors = 0
                    for k in range(i - 1, i + 2):
                        for l in range(j - 1, j + 2):
                            
                            # Prevent going out of map range and even wrapping around.
                            if ((k < 0 or k > self.map_height - 1) and (l < 0 or l > self.map_width - 1)):
                                continue
                            elif (k < 0 or k > self.map_height - 1 or l < 0 or l > self.map_width - 1):
                                continue
                            # Skip if current tile in the 3x3 iteration is itself.
                            elif i == k and j == l:
                                continue
                            # Add to number of neighbors if current tile is a cell.
                            elif game_map[k][l] == 1:
                                num_neighbors += 1

                    # Apply the rules for cell growth/death.
                    if game_map_temp[i][j] == 1:
                        # Cell survives.
                        if num_neighbors == 2 or num_neighbors == 3:
                            pass
                        # Cell fucking dies.
                        elif num_neighbors <= 1 or num_neighbors >= 4:
                            game_map_temp[i][j] = 0
                    else:
                        # Cell emerges.
                        if num_neighbors == 3:
                            game_map_temp[i][j] = 1

            # Set our original map into the updated one.
            for i in range(self.map_height):
                for j in range(self.map_width):
                    game_map[i][j] = game_map_temp[i][j]

            self._print_map(game_map)


    def _get_starting_map(self) -> list:
        """
        Return the initial state for the game which is a 2d list of 1's and 0's
        0 = empty tile, 1 = cell
        """
        if self.custom:
            generated_list = [[0 for j in range(self.map_width)] for i in range(self.map_height)]
            self.frequency /= 100.0
            for i in range(self.map_height):
                for j in range(self.map_width):
                    random_cell_chance = random.uniform(0, 1)
                    if random_cell_chance <= self.frequency:
                        generated_list[i][j] = 1
                    else:
                        generated_list[i][j] = 0
            return generated_list

        # You can edit this here if you want! It will automatically detect
        # the map dimensions, but make sure to keep it rectangular and use 1's and 0's!
        else:
            return [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]


if __name__ == "__main__":
    cgol = GameOfLife()
    cgol.setup()
