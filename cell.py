from tkinter import Button, Label
import settings
import random
import ctypes
import sys

class Cell:
    all = []
    cell_count_label_object = None
    cell_count = settings.CELL_COUNT
    def __init__(self, x, y, is_mine=False):
        self.is_mine = is_mine
        self.is_opened = False
        self.is_mine_candidate = False
        self.cell_btn_object = None
        self.x = x
        self.y = y

        #append the object to the cell.all[]
        Cell.all.append(self)

    def create_btn_object(self, location):
        btn = Button(
            location,
            width=12,
            height=4
            #text=f"{self.x},{self.y}"
        )
        btn.bind('<Button-1>', self.left_click_actions) #left click
        btn.bind('<Button-3>', self.right_click_actions) #right click
        self.cell_btn_object = btn

    @staticmethod
    def create_cell_count_label(location):
        lbl = Label(
            location,
            bg=settings.BG_COLOR,
            fg='white',
            text=f"Cells Left:{Cell.cell_count}",
            font=("",30)
        )
        Cell.cell_count_label_object = lbl

    def left_click_actions(self, event):
        #this while loop prevents hitting the first cell as a mine
        #while self.cell_count == settings.CELL_COUNT and self.is_mine:
         #   Cell.randomize_mines()
        if self.is_mine:
            self.show_mine()
        else:
            if self.surrounded_cells_mines_length == 0:
                for cell_obj in self.surrounded_cells:
                    cell_obj.show_cell()
            self.show_cell()
        
        #cancel events if cell is already opened
        self.cell_btn_object.unbind('<Button-1>')
        self.cell_btn_object.unbind('<Button-3>')

        #if mines count is equal to cells left count player won
        if Cell.cell_count == settings.MINES_COUNT:
            ctypes.windll.user32.MessageBoxW(0, 'Congratulations! You won!', 'Game Over',0)

    def right_click_actions(self, event):
        if not self.is_mine_candidate:
            self.cell_btn_object.configure(bg='orange')
            self.is_mine_candidate = True
        else:
            self.cell_btn_object.configure(bg='SystemButtonFace')
            self.is_mine_candidate = False

    def get_cell_by_axis(self, x, y):
        # return a cell object based on x,y value
        for cell in Cell.all:
            if cell.x == x and cell.y == y:
                return cell

    def show_mine(self):
        # login to interrup game and displa lost message
        self.cell_btn_object.configure(bg='red')
        ctypes.windll.user32.MessageBoxW(0, 'You clicked on a mine', 'Game Over',0)
        sys.exit()

    def show_cell(self):
        if not self.is_opened:
            Cell.cell_count -= 1
            self.cell_btn_object.configure(text=self.surrounded_cells_mines_length)
            #replace text of cell count label with newer count
            if Cell.cell_count_label_object:
                Cell.cell_count_label_object.configure(text = f"Cells Left:{Cell.cell_count}")

            self.cell_btn_object.configure(bg='SystemButtonFace')
        #mark cell as opened
        self.is_opened = True

        #print(self.surrounded_cells_mines_length)
        #print (self.surrounded_cells)
        #print (self.get_cell_by_axis(0,0))

    @property
    def surrounded_cells(self):
        cells = [
            self.get_cell_by_axis(self.x - 1, self.y - 1),
            self.get_cell_by_axis(self.x - 1, self.y),
            self.get_cell_by_axis(self.x - 1, self.y + 1),
            self.get_cell_by_axis(self.x, self.y - 1),
            self.get_cell_by_axis(self.x + 1, self.y - 1),
            self.get_cell_by_axis(self.x + 1, self.y),
            self.get_cell_by_axis(self.x + 1, self.y + 1),
            self.get_cell_by_axis(self.x, self.y + 1)
        ]

        cells = [cell for cell in cells if cell is not None]
        return cells

    @property
    def surrounded_cells_mines_length(self):
        counter = 0
        for cell in self.surrounded_cells:
            if cell.is_mine:
                counter+=1

        return counter

    @staticmethod
    def randomize_mines():
        picked_cells = random.sample(Cell.all, settings.MINES_COUNT)
        for picked_cell in picked_cells:
            picked_cell.is_mine = True

    def __repr__(self):
        return f"Cell({self.x}, {self.y})"