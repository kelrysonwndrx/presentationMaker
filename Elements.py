import customtkinter
import tkinter as tk
from tkinter import StringVar
from tkinter import *
from tkinter.filedialog import askopenfilename

from reportlab.lib.pagesizes import letter
#from reportlab.pdfgen import canvas
import xml.etree.ElementTree as et

numDeSlides = 1

class DraggableRectangle:
    def __init__(self, canvas, x, y, width, height, **kwargs):
        self.canvas = canvas
        self.rect = self.canvas.create_rectangle(x, y, x+width, y+height, **kwargs)
        self.start_x = None
        self.start_y = None
        self.canvas.tag_bind(self.rect, '<ButtonPress-1>', self.on_press)
        self.canvas.tag_bind(self.rect, '<B1-Motion>', self.on_move)
        self.canvas.tag_bind(self.rect, '<ButtonRelease-1>', self.on_release)

    def on_press(self, event):
        self.start_x = event.x
        self.start_y = event.y

    def on_move(self, event):
        if self.start_x is not None and self.start_y is not None:
            dx = event.x - self.start_x
            dy = event.y - self.start_y
            self.canvas.move(self.rect, dx, dy)
            self.start_x = event.x
            self.start_y = event.y
    
    def on_release(self, event):
        self.start_x = None
        self.start_y = None

class DraggableText:
    def __init__(self, canvas, x, y,  **kwargs):
        self.canvas = canvas
        self.rect = self.canvas.create_text(x, y, **kwargs)
        self.start_x = None
        self.start_y = None
        self.canvas.tag_bind(self.rect, '<ButtonPress-1>', self.on_press)
        self.canvas.tag_bind(self.rect, '<B1-Motion>', self.on_move)
        self.canvas.tag_bind(self.rect, '<ButtonRelease-1>', self.on_release)

    def on_press(self, event):
        self.start_x = event.x
        self.start_y = event.y

    def on_move(self, event):
        if self.start_x is not None and self.start_y is not None:
            dx = event.x - self.start_x
            dy = event.y - self.start_y
            self.canvas.move(self.rect, dx, dy)
            self.start_x = event.x
            self.start_y = event.y
    
    def on_release(self, event):
        self.start_x = None
        self.start_y = None

cursor = 'hand2'

def change_cursor(c, event, cursor):
    c.config(cursor=cursor)

def restore_cursor(c, event):
    c.config(cursor='')

def createRect(c, x1, x2, y1, y2):
    dRect = DraggableRectangle(c, x1, x2, y1, y2, fill="blue")
    #rect = c.create_rectangle(x1, x2, y1, y2, fill=None)
    c.tag_bind(dRect, '<Enter>', lambda event: change_cursor(c, event, cursor))
    c.tag_bind(dRect, '<Leave>', lambda event: restore_cursor(c, event))
    c.update()

def createText(c, text, x1, x2):
    text = DraggableText(c, x1, x2, text=text, fill='black', width=80)
    c.tag_bind(rect, '<Enter>', lambda event: change_cursor(c, event, cursor))
    c.tag_bind(rect, '<Leave>', lambda event: restore_cursor(c, event))
    c.update()

def delete(c):
    c.delete('all')