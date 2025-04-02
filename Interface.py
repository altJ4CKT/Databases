from _musicQuizDatabase import Reader
import os
import tkinter as tk

test: Reader = Reader((os.path.dirname(os.path.realpath(__file__))+"/Quiz Songs.db"))

class QuizFrame(tk.Frame):
    def __init__(self, windowRef: tk.Tk, oldFrame: tk.Frame, packId: int):

        if oldFrame is not None:
            oldFrame.destroy()

        self.quizId = packId

        super().__init__(windowRef)
        self.SetupLayout()
        self.pack(fill="both", expand=True)

    def SetupLayout(self):
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(4, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)

        self.configure(bg="black")

        tk.Label(self, text=f"{" - ".join(test.GetPackMetadata(self.quizId))}",
                 font=["Century Gothic", 30],
                 width = 40).grid(row=0, column=1, padx=10, pady=10)
        tk.Label(self, text="Question Number 1",
                 font=["Century Gothic", 15],
                 width=20).grid(row=1, column=1, padx=10, pady=10)
        tk.Button(self, text="Next Question",
                  command=lambda: QuizFrame(self.master, self),
                  font=["Century Gothic", 15],
                  width=20).grid(row=4, column=2, padx=10, pady=10)


class MusicQuizFrame(tk.Frame):
    def __init__(self, windowRef: tk.Tk, oldFrame: tk.Frame = None):

        if oldFrame is not None:
            oldFrame.destroy()

        super().__init__(windowRef)
        self.SetupLayout()
        self.pack(fill="both", expand=True)

    def SetupLayout(self):
        self.configure(bg="#ff0000")

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(4, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        tk.Label(self, text="MusicQuiz", width=10, font=["Century Gothic", 20]).grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        packIds = test.GetAllPacks()

        # Go through each pack in the database
        for i in range(len(packIds)):

            packId = packIds[i]

            tk.Button(self, text=" - ".join(test.GetPackMetadata(packId)), command=lambda tempId=packId: QuizFrame(self.master, self, tempId),
                      font=["Century Gothic", 20],
                      width = 20).grid(row=1+i, column=0, columnspan=2, padx=10, pady=10)
            # tk.Button(self, text="2010's Pop - JWitham", command=lambda: print("2010's Pop - Jwitham"),
            #           font=["Century Gothic", 20],
            #           width=20).grid(row=2, column=0, columnspan=2, padx=10, pady=10)
            # tk.Button(self, text="Dad Songs - MWitham", command=lambda: print("Dad Songs - MWitham"),
            #           font=["Century Gothic", 20],
            #           width=20).grid(row=3, column=0, columnspan=2, padx=10, pady=10)

class MainProgram(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("Main Window")

        self.configure(bg="#ff8000")

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        MusicQuizFrame(self)
        self.mainloop()

x: MainProgram = MainProgram()

