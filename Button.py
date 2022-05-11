from tkinter import *
import pygame

class Question:
    def __init__(self, question):
        self.state = None
        self.question = question
        self.root = Tk()
        self.root.title("Dialog window")
        self.root.geometry("400x300")

        message = StringVar()

        Message(self.root, text=self.question, font=50).pack()

        message_entry = Entry(textvariable=message)
        message_entry.place(relx=.3, rely=.50)

        message_button = Button(text="Apply", font=50, command=lambda: self.get_message(message))
        message_button.place(relx=.3, rely=.60)

        self.root.mainloop()

    def get_message(self, message, flag = True):
        self.state = message.get()
        self.root.destroy()

class Report:
    def __init__(self, report):
        self.state = None
        self.report = report
        self.root = Tk()
        self.root.title("Dialog window")
        self.root.geometry("400x300")

        Message(self.root, text=self.report, font=50).pack()

        click_button = Button(text="OK", font=50, command=self.click)
        click_button.place(relx=.3, rely=.60)

        self.root.mainloop()

    def click(self):
        self.root.destroy()