import math
from tkinter import *
from sys import platform
from node import Node

master = Tk()

canvas_width = 800
canvas_height = 400
w = Canvas(master,
           width=canvas_width,
           height=canvas_height)
w.pack()

start_x = 0
start_y = 0
shape = []
cursor_size = 5
current_x = 0
current_y = 0
roots = []
selected = None


def update():
    w.delete('all')
    if roots:
        for root in roots:
            root.draw()
    w.create_oval(current_x - cursor_size, current_y - cursor_size,
                  current_x + cursor_size, current_y + cursor_size)


def button1(event):
    global roots, selected

    clicked = []
    if not selected:
        for root in roots:
            # print(root.all())
            clicked += [a for a in root.all() if a.check_for_click(event.x, event.y)]
        if clicked:
            # print('clicked', clicked)
            selected = clicked[0]
            selected.selected = True
        else:
            roots.append(Node(event.x, event.y, cursor_size, w))
    else:
        for root in roots:
            # print(root.all())
            clicked += [a for a in root.all() if a.check_for_click(event.x, event.y)]
        if selected not in clicked:
            if clicked:
                selected.append(Node(clicked[0].x, clicked[0].y, clicked[0].r, w))
            else:
                selected.append(Node(event.x, event.y, cursor_size, w))
            selected.selected = False
            selected = None
    w.delete('all')
    # print(roots)
    [root.draw() for root in roots]


def move_cursor(event):
    global current_x, current_y
    current_x = event.x
    current_y = event.y
    update()


def drag(event):
    pass


def keypress(event):
    global cursor_size
    if event.char == '[':
        if cursor_size > 5:
            cursor_size -= 1

    if event.char == ']':
        if cursor_size < 100:
            cursor_size += 1
    update()


w.focus_set()

w.bind('<Button-1>', button1)
w.bind('<B1-Motion>', drag)
w.bind('<Motion>', move_cursor)
w.bind('<KeyPress>', keypress)


def toggleanimation():
    print('starting')


playbutton = Button(master, text="⏯️", command=toggleanimation)
playbutton.pack()


master.mainloop()
