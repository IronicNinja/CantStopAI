import random
from tkinter import *

class CantStop():
    def __init__(self):
        self.pieces = 3
        self.tkroot = Tk()
        self.color = '#a6a48f'
        self.canvas = Canvas(self.tkroot, width=950, height=350)
        self.canvas.pack(expand=True, fill=BOTH)
        self.canvas.configure(bg=self.color)
        self.canvas.create_window(450, 150, anchor=CENTER)
        self.player_A = {k: 0 for k in range(2, 13)}
        self.player_B = {k: 0 for k in range(2, 13)}
        self.board_end = [3, 5, 7, 9, 11, 13, 11, 9, 7, 5, 1]

    def random_roll(self):
        return [random.randint(1, 6) + random.randint(1, 6), random.randint(1, 6) + random.randint(1, 6)]

    def button_press(self, player, num1, num2):
        player[num1] += 1
        player[num2] += 1
        self.canvas.pack_forget()
        button_cont = Button(self.tkroot, text="Continue", command=self.player_move())
        button_end = Button(self.tkroot, text="End Turn")
        button_cont.place(x=150, y=150)
        button_end.place(x=650, y=150)

    def player_move(self):
        rolls_list = [self.random_roll(), self.random_roll(), self.random_roll()]
        for i in range(len(rolls_list)):
            roll = rolls_list[i]
            button = Button(self.tkroot, text=f"Rolls: {roll[0]} {roll[1]}", command=self.button_press(self.player_A, roll[0], roll[1]))
            button.place(x=50+300*i, y=150)

    def run(self):
        while True:
            self.pieces = 3
            # Every person's move
            while True:
                # Every move
                self.player_move()
                    
                break
            break
        self.tkroot.mainloop()      

bot = CantStop()      
bot.player_move()              

