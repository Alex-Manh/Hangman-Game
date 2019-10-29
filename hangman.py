
"""
    Assignment 3
    CSSE1001/7030
    Semester 2, 2018
"""

__author__ = "Minh Anh Bui 45041899"

import random
import tkinter as tk
from tkinter import messagebox
from PIL import ImageTk
import functools
import string
alphabet = string.ascii_lowercase


def hang_man_game():
    '''
        Control the Hangman Game holistically
    '''
    
    root = tk.Toplevel()

    class tool_manager(object):
        '''
        A class to manage supporting tools for the game
        '''
        def __init__(self):
            '''
                Construct the supporting 
            '''
            self._list_word = self.read_words('words.txt')
            self._secret_word = self.generate_word(self._list_word)

        def get_word(self):
            '''
                Return the secret word(list)
            '''
            return self._secret_word

        def read_words(self, text):
            '''
                Read the text file and insert all words to a list

                Parameter:
                    text(text): The file containing words
                Return:
                    word_list(list): The list consisting of words in the text file
            '''
            word_list = []
            with open(text) as text_word:
                for line in text_word:
                    word = line.strip()
                    word_list.append(word)
            return word_list

        def generate_word(self, words):
            '''
                Randomly choose a word from a list of words

                Parameter:
                    words(list): A list of words to choose from
                    
                Return
                    word(list): The word converted to list form
            '''
            word=words[random.randint(0, len(words) - 1)]
            return list(word)


    class Hangman(object):
        '''
            A class to manage the main App
        '''
        def __init__(self, master):
            '''
                Construct the main app
            '''
            self._master = master
            self._tool = tool_manager()
            self._word = self._tool.get_word()
            self._master.title('Hangman Game')
            self._master.geometry('800x600')
            self._canvas = tk.Canvas(self._master, height=300, width=400)
            self._canvas.pack(side=tk.TOP)
            
            #Image being displayed at the top of the App
            self._image_list = []
            self._image_list.append(ImageTk.PhotoImage(file="pyimage1.png"))
            self._image_list.append(ImageTk.PhotoImage(file="pyimage2.png"))
            self._image_list.append(ImageTk.PhotoImage(file="pyimage3.png"))
            self._image_list.append(ImageTk.PhotoImage(file="pyimage4.png"))
            self._image_list.append(ImageTk.PhotoImage(file="pyimage5.png"))
            self._image_num = 0
            self._image_display=self._canvas.create_image(200, 150, image=self._image_list[self._image_num])
            note = "Welcome to the Hangman Game! \nYou need to guess the word in green box within 5 trials"

            #Instruction for player
            self._instruction = tk.Label(self._master, text=note, font="Courier 10")
            self._instruction.pack(side=tk.TOP, ipadx=2)

            #The secret word being hidden under blank label
            self._secret_frame = tk.Frame(self._master, width=200, height=300, bg='yellow')
            self._secret_frame.pack(side=tk.TOP, pady=20)
            self._hidden_label = hidden(self._secret_frame, self._word)

            #Interactive keyboard for player 
            self._interact_frame1 = tk.Frame(self._master, bg='cyan')
            self._interact_frame1.pack(side=tk.TOP, pady=20)
            self._interact_frame2 = tk.Frame(self._master, bg='cyan')
            self._interact_frame2.pack(side=tk.TOP)
            self.key_board(self._interact_frame1, self._interact_frame2)

            #Check if the player has won or not
            self.win()

        def get_secret_word(self):
            '''
                Return the secret word generated(list)
            '''
            return self._word

        def change_image(self):
            '''
                Change the image displayed accordingly to the number of trials
                the player has left
            '''
            self._image_num+=1
            if self._image_num == len(self._image_list):
                self._image_num = 0
                self.fail()
            else:
                self._canvas.itemconfig(self._image_display, image=self._image_list[self._image_num])

        def key_board(self, parent1, parent2):
            '''
                Construct the interactive keyboard for player
            '''
            for letter in alphabet[:13]:
                letter_button = tk.Button(parent1, command=functools.partial(self.check, letter), font="Courier 10", bg="#ccccff", text=letter, width=5, height=2)
                letter_button.pack(side=tk.LEFT)
            for letter in alphabet[13:]:
                letter_button = tk.Button(parent2, command=functools.partial(self.check, letter), font="Courier 10", bg="#ccccff", text=letter, width=5, height=2)
                letter_button.pack(side=tk.LEFT)

        def check(self, letter):
            '''
                Parameter:
                    letter(str): A letter in alphabet, inserted by player from the app's keyboard

                Check if the letter is in the secret word
                    If True: Reaveal
                    If False: Minus a trial, change image displayed 
            '''
            word = self.get_secret_word()
            guessed_list = []
            if letter in word:
                trial = True
                while trial:
                    if letter in word:
                        guessed_index = word.index(letter)
                        guessed_list.append(guessed_index)
                        self._hidden_label.reveal(guessed_index)
                        word[guessed_index] = ''
                    else:
                        break
            elif letter not in word:
                self.change_image()

        def fail(self):
            '''
                Announce that the player runs out of trials and lose the game
            '''
            messagebox.showinfo("Notification", "You lose")
            self.quit()

        def win(self):
            '''
                Announce that the player has won the game
            '''
            check_win = self._hidden_label.check_win()
            if check_win:
                messagebox.showinfo("Notification", "You win")
                self.quit()
            self._master.after(50, self.win)

        def quit(self):
            '''
                Stop the app
            '''
            root.destroy()

    class hidden(tk.Frame):
        '''
           A class to mangage the hidden word's label underneath blank label
        '''
        def __init__(self, parent, word):
            '''
                Construct the hidden word's label
            '''
            super().__init__()
            self._hidden_list = []
            self._number_letters = len(word)
            for column_index, character in enumerate(word):
                hidden_label = tk.Label(parent, text=character, width=3, height=1, font=("Courier",20), bg='#ffff99', borderwidth=2, relief='solid')
                hidden_label.grid(row=2, column=column_index)
                hidden_label.lower()
                self._hidden_list.append(hidden_label)
                blank_label = tk.Label(parent, width=3, height=1, font=("Courier",20), bg='#99ff99', borderwidth=2, relief='solid')
                blank_label.grid(row=2, column=column_index)

        def reveal(self, index):
            '''
                Reveal the hidden letters of secret word
            '''
            self._hidden_list[index].lift()
            self._number_letters -= 1

        def check_win(self):
            '''
                Check if all letters in secret word has been discoverd
            '''
            if not self._number_letters:
                return True



    app = Hangman(root)
    root.mainloop()


