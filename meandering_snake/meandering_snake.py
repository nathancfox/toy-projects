#!/usr/bin/env python
# This has to come before importing anything else from matplotlib
import matplotlib as mpl
mpl.use('TkAgg')

import time

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as Tk

import snake_classes

# Hacky global variables (shame on you)
root = None
reset_button = None
snake = None
ax = None
canvas = None
trapped_msg = None

def make_snake(body_color = 'viridis'):
    global snake
    snake = snake_classes.Snake((int(((ax.get_xlim()[1] - ax.get_xlim()[0]) / 2)) + 4,
                                 int(((ax.get_ylim()[1] - ax.get_ylim()[0]) / 2))),
                                'right', 16, label='snake1')
    snake.set_body_color(body_color)
    return(snake)

def update_canvas():
    global snake
    global ax
    global canvas
    directions = ('up', 'down', 'left', 'right')
    dir_choices = list(directions)
    new_dir = None
    for i in range(len(dir_choices)):
        # Type conversion is because validation functions are expecting
        # a str type not a numpy.str_ type
        new_dir = str(np.random.choice(dir_choices))
        new_head_pos = snake.get_new_head_pos(new_dir)
        if (ax.get_xlim()[0] ==  new_head_pos[0]
                or ax.get_xlim()[1] + 1 == new_head_pos[0]
                or ax.get_ylim()[0] == new_head_pos[1]
                or ax.get_ylim()[1] + 1 == new_head_pos[1]):
            dir_choices.remove(new_dir)
            new_dir = None
            continue
        try:
            snake.move_snake_one(new_dir)
            break
        except ValueError:
            dir_choices.remove(new_dir)
            new_dir = None
            continue
    if new_dir is None:
        add_trapped_msg()
    else:
        snake.remove_from_axes(ax)
        snake.draw_on_axes(ax)
        canvas.draw()
        root.after(250, update_canvas)

def add_trapped_msg():
    global ax
    global canvas
    global trapped_msg
    width, height = ax.figure.get_size_inches()
    text_height= height * 0.05
    size = text_height * 72
    trapped_msg = ax.text(0.5, 0.5, 'Your snake is trapped!',
                          horizontalalignment='center',
                          verticalalignment='center',
                          transform=ax.transAxes, size=size,
                          bbox=dict(boxstyle='square',
                                    facecolor='#FF8080',
                                    edgecolor='#FFCDCD'))
    canvas.draw()
    reset_button.config(state='active')

def _reset():
    global snake
    global ax
    global canvas
    global trapped_msg
    if trapped_msg is None:
        raise AssertionError('_reset() ran with a trapped_msg!')
    trapped_msg.remove()
    snake.remove_from_axes(ax)
    snake = make_snake()
    snake.draw_on_axes(ax)
    canvas.draw()
    time.sleep(0.25)
    update_canvas()
    reset_button.config(state='disabled')

def _quit():
    root.quit()     # stops mainloop

def main():
    global root
    global reset_button
    global snake
    global ax
    global canvas
    root = Tk.Tk()
    root.wm_title("Meandering Snake")

    fig = plt.figure(figsize=(8, 8), dpi=100)
    ax = fig.add_subplot(111)

    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)

    BOARD_SIZE = (30, 30)

    ax.set_aspect('equal')
    ax.set_xlim(0, BOARD_SIZE[0])
    ax.set_ylim(0, BOARD_SIZE[1])
    ax.set_xticks([i for i in range(BOARD_SIZE[0] + 1)])
    ax.set_yticks([i for i in range(BOARD_SIZE[1] + 1)])
    ax.tick_params(length=0)
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    width, height = ax.figure.get_size_inches()
    spine_lw = min(width, height) * 0.02 * 72
    del width
    del height
    spine_color = '#000000'
    ax.spines['top'].set_linewidth(spine_lw)
    ax.spines['top'].set_edgecolor(spine_color)
    ax.spines['bottom'].set_linewidth(spine_lw)
    ax.spines['bottom'].set_edgecolor(spine_color)
    ax.spines['left'].set_linewidth(spine_lw)
    ax.spines['left'].set_edgecolor(spine_color)
    ax.spines['right'].set_linewidth(spine_lw)
    ax.spines['right'].set_edgecolor(spine_color)
    ax.set_position([0, 0, 1, 1])
    ax.set_facecolor('#C1C1C1')

    quit_button = Tk.Button(master=root, text='Quit', command=_quit)
    quit_button.pack(side=Tk.BOTTOM)
    reset_button = Tk.Button(master=root, text='Reset', command=_reset)
    reset_button.config(state='disabled')
    reset_button.pack(side=Tk.BOTTOM)

    snake = make_snake()
    snake.draw_on_axes(ax)
    canvas.draw()

    root.after(250, update_canvas)
    Tk.mainloop()

if __name__ == '__main__':
    main()
