# Importing useful modules.
import tkinter as tk
import tkinter.simpledialog as simpledialog
import tkinter.messagebox as tkMessageBox
import random

class BattleshipGUI:
    def __init__(self, master, grid_size, num_4_long, num_3_long, num_2_long):
        self.master = master
        self.master.title("Battleship")

        self.playfield_size = grid_size

        # Creating ship sizes based on user input.
        self.ship_sizes = [4] * num_4_long + [3] * num_3_long + [2] * num_2_long
        self.ships = []
        self.total_guesses = 0
        self.available_tiles = [(i, j) for i in range(self.playfield_size) for j in range(self.playfield_size)]

        # Check if grid size can accommodate all ships.
        if sum(self.ship_sizes) > self.playfield_size**2:
            tkMessageBox.showerror("Error", "Grid too small for the total number of ships. Please choose a larger grid or fewer ships.")
            self.master.destroy()  # Close the game window
            return

        self.create_playfield()
        self.place_ships()

    # Creating the grid.
    def create_playfield(self):
        self.cells = []
        for i in range(self.playfield_size):
            row = []
            for j in range(self.playfield_size):
                cell = tk.Label(self.master, width=2, height=1, relief="ridge", bg="dodger blue")
                cell.grid(row=i, column=j)
                cell.bind("<Button-1>", lambda event, row=i, col=j: self.check_guess(row, col))
                row.append(cell)
            self.cells.append(row)

    # Placing ships on the grid.
    def place_ships(self):
        for ship_size in self.ship_sizes:
            while True:
                # Randomizing vertical or horizontal ships.
                direction = random.choice(["horizontal", "vertical"])
                if direction == "horizontal":
                    row = random.randint(0, self.playfield_size - 1)
                    col = random.randint(0, self.playfield_size - ship_size)
                    # Checking if any cell in the ship's path is already occupied.
                    ship_tiles = [(row, col+i) for i in range(ship_size)]
                    if all(tile in self.available_tiles for tile in ship_tiles):
                        self.ships.append(ship_tiles)
                        for tile in ship_tiles:
                            # Removing ship tiles from available tiles.
                            self.available_tiles.remove(tile)
                        break
                else:
                    row = random.randint(0, self.playfield_size - ship_size)
                    col = random.randint(0, self.playfield_size - 1)
                    # Checking if any cell in the ship's path is already occupied.
                    ship_tiles = [(row+i, col) for i in range(ship_size)]
                    if all(tile in self.available_tiles for tile in ship_tiles):
                        self.ships.append(ship_tiles)
                        for tile in ship_tiles:
                            # Removing ship tiles from available tiles.
                            self.available_tiles.remove(tile)
                        break
    
    # Checking user's guesses. If correct, turn a tile red until the entire ship is found, then turn it black. If wrong, turn it white.
    def check_guess(self, row, col):
        self.total_guesses += 1
        if (row, col) in [(r, c) for ship in self.ships for (r, c) in ship]:
            self.cells[row][col]["bg"] = "red"
            self.check_ship_sunk()
        else:
            self.cells[row][col]["bg"] = "white"
        if self.check_game_over():
            self.display_game_over()

    # Turns the ship black when the entire thing is sunk.
    def check_ship_sunk(self):
        for ship in self.ships:
            if all(self.cells[r][c]["bg"] == "red" for (r, c) in ship):
                for (r, c) in ship:
                    self.cells[r][c]["bg"] = "black"

    # Checking if the game is over by checking the total number of black cells.
    def check_game_over(self):
        black_count = sum([1 for row in self.cells for cell in row if cell["bg"] == "black"])
        return black_count == sum(self.ship_sizes)

    # Displaying results and total guesses.
    def display_game_over(self):
        tkMessageBox.showinfo("Game Over", f"All ships sunk! Total guesses: {self.total_guesses}")
        self.reset_game()

    # Resetting the game so that the user can keep playing.
    def reset_game(self):
        self.ships = []
        for i in range(self.playfield_size):
            for j in range(self.playfield_size):
                self.cells[i][j].config(bg="dodger blue")
        self.place_ships()
        self.total_guesses = 0

# Running the program.
def main():
    root = tk.Tk()

    # Function to get valid integer input from user
    def get_user_input(prompt, min_value=None):
        while True:
            try:
                value = simpledialog.askinteger("Input", prompt)
                if value is None:
                    tkMessageBox.showerror("Input Error", "Input canceled. Exiting game.")
                    root.destroy()
                    return None
                if min_value is not None and value < min_value:
                    tkMessageBox.showerror("Input Error", f"Please enter a number greater than or equal to {min_value}.")
                    continue
                return value
            except ValueError:
                tkMessageBox.showerror("Input Error", "Invalid input. Please enter a valid integer.")

    # Getting user input for grid size with minimum value of 2.
    grid_size = get_user_input("Enter the size of the grid (must be at least 4):", min_value=4)
    if grid_size is None:
        return  # If input is canceled, exit the program

    # Getting user input for number of ships with at least one ship.
    num_4_long = get_user_input("Enter the number of 4-long ships (must have at least 1 ship total):", min_value=0)
    if num_4_long is None:
        return  # If input is canceled, exit the program

    num_3_long = get_user_input("Enter the number of 3-long ships (must have at least 1 ship total):", min_value=0)
    if num_3_long is None:
        return  # If input is canceled, exit the program

    num_2_long = get_user_input("Enter the number of 2-long ships (must have at least 1 ship total):", min_value=0)
    if num_2_long is None:
        return  # If input is canceled, exit the program

    # Ensuring that at least one ship is present.
    if num_4_long + num_3_long + num_2_long < 1:
        tkMessageBox.showerror("Input Error", "You must have at least one ship.")
        root.destroy()
        return

    # Start the game with user input.
    battleship_gui = BattleshipGUI(root, grid_size, num_4_long, num_3_long, num_2_long)
    root.mainloop()

if __name__ == "__main__":
    main()