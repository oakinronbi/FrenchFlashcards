from tkinter import *
from random import choice
from tkinter import Canvas
import pandas

BACKGROUND_COLOR = "#B1DDC6"
word = {}
translate_dict = {}

try:
    data = pandas.read_csv("words_to_learn.csv")
except FileNotFoundError:
    data = pandas.read_csv("1000 Spanish Words.csv")
    translate_dict = data.to_dict(orient="records")
else:
    translate_dict = data.to_dict(orient="records")


def generate_word():
    global word, flip_timer
    window.after_cancel(flip_timer)
    word = choice(translate_dict)
    canvas.itemconfig(word_text, text=word["Spanish"], fill="black")
    canvas.itemconfig(word_lang, text="Spanish", fill="black")
    canvas.itemconfig(canvas_image, image=img)
    flip_timer = window.after(3000, func=flip_over)


def flip_over():
    canvas.itemconfig(canvas_image, image=new_img)
    canvas.itemconfig(word_lang, text="English", fill="white")
    canvas.itemconfig(word_text, text=word["English"], fill="white")


def is_known():
    translate_dict.remove(word)
    print(len(translate_dict))
    new_data = pandas.DataFrame(translate_dict)
    new_data.to_csv("words_to_learn.csv", index=False)
    generate_word()


window = Tk()
window.title("Flash Card")
window.configure(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, func=flip_over)

canvas = Canvas(width=800, height=526, highlightthickness=0, bg="#B1DDC6")
img = PhotoImage(file="card_front.png")
new_img = PhotoImage(file="card_back.png")
canvas_image = canvas.create_image(400, 263, image=img)
word_lang = canvas.create_text(400, 150, text="Spanish", fill="black", font=("Ariel", 40, "italic"))
word_text = canvas.create_text(400, 263, text="word", fill="black", font=("Ariel", 60, "bold"))
canvas.grid(column=0, row=0, columnspan=2)


wrong_image = PhotoImage(file="right.png")
unknown_button = Button(command=generate_word, image=wrong_image, bg="#B1DDC6", highlightthickness=0)
unknown_button.grid(column=0, row=1)


right_image = PhotoImage(file="right.png")
known_button = Button(command=is_known, image=right_image, bg="#B1DDC6", highlightthickness=0)
known_button.grid(column=1, row=1)

generate_word()
window.mainloop()
