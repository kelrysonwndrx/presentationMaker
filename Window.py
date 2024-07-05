import customtkinter
import tkinter as tk
from tkinter import StringVar
from tkinter import *
from tkinter.filedialog import askopenfilename
from xmlParserV2 import PresentationFile

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
    c.tag_bind(text, '<Enter>', lambda event: change_cursor(c, event, cursor))
    c.tag_bind(text, '<Leave>', lambda event: restore_cursor(c, event))
    c.update()

def delete(c):
    c.delete('all')

def setAddTextVisible():
    f2.grid_forget()
    frameAddText.grid(row=0, column=1, padx=15, pady=15, sticky=W+N)
    frameAddText.update()

def setAddDrawVisible():
    frameAddText.grid_forget()
    f2.grid(row=0, column=1, padx=15, pady=15, sticky=W+N)
    f2.update()

def addNewSlide(frame1, frame2=None):
    global numDeSlides, btAddNewSlide, canvas

    btAddNewSlide.grid_forget()
    btAddNewSlide = customtkinter.CTkButton(frameOPresentationTimeLine, text="+", command= lambda: addNewSlide(frameOPresentationTimeLine, f1), width=150)
    btAddNewSlide.grid(row=numDeSlides+1, column=0, padx=0, pady=5, sticky=N)

    slide = customtkinter.CTkCanvas(frame1, borderwidth=0, width = 150, height = 100, bg = 'white')
    slide.grid(row=(numDeSlides), column=0, padx=2.5, pady=2.5)
    canvas.pack_forget()
    canvas = customtkinter.CTkCanvas(frame2, width = 400, height = 300, bg = 'white')
    canvas.pack()

    numDeSlides += 1

caminhoParaArquivo = ''

def retornaCaminho():
    global aux 
    caminhoParaArquivo = askopenfilename()

app = customtkinter.CTk()
app.title("my app")
app.geometry("800x600")
app.grid_columnconfigure((0), weight=1)

# Definição da barra de menus----------------------------------------------------------------------------------

menu = Menu(app, title='Menu principal', type='normal', tearoff=0, relief='raised')

file = Menu(menu, tearoff=0)
file.add_command(label='Salvar')
file.add_command(label='Salvar como')
file.add_separator()
file.add_command(label='Abrir arquivo', command=retornaCaminho)
file.add_command(label='Abrir arquivos recentes')
file.add_separator()
file.add_command(label='Sair', command=app.quit)

menu.add_cascade(label='Arquivo', menu=file)

edit = Menu(menu, tearoff=0)
edit.add_command(label='opção1')
edit.add_command(label='opção2')
edit.add_command(label='opção3')
edit.add_command(label='opção4')
edit.add_command(label='opção5')
edit.add_command(label='opção6')

menu.add_cascade(label='Editar', menu=edit)

biblioteca = Menu(menu, tearoff=0)
biblioteca.add_command(label='opção1')
biblioteca.add_command(label='opção2')
biblioteca.add_command(label='opção3')
biblioteca.add_command(label='opção4')
biblioteca.add_command(label='opção5')
biblioteca.add_command(label='opção6')

menu.add_cascade(label='Biblioteca', menu=biblioteca)

view = Menu(menu, tearoff=0)
view.add_command(label='opção1')
view.add_command(label='opção2')
view.add_command(label='opção3')
view.add_command(label='opção4')
view.add_command(label='opção5')
view.add_command(label='opção6')

menu.add_cascade(label = 'Janela', menu = view)

imagem = Menu(menu, tearoff=0)
imagem.add_command(label='opção1')
imagem.add_command(label='opção2')
imagem.add_command(label='opção3')
imagem.add_command(label='opção4')
imagem.add_command(label='opção5')
imagem.add_command(label='opção6')

menu.add_cascade(label = 'Imagem', menu = imagem)

ajuda = Menu(menu, tearoff=0)
ajuda.add_command(label='opção1')
ajuda.add_command(label='opção2')
ajuda.add_command(label='opção3')
ajuda.add_command(label='opção4')
ajuda.add_command(label='opção5')
ajuda.add_command(label='opção6')

menu.add_cascade(label = 'Ajuda', menu = ajuda)

sobre = Menu(menu, tearoff=0)
sobre.add_command(label='opção1')
sobre.add_command(label='opção2')
sobre.add_command(label='opção3')
sobre.add_command(label='opção4')
sobre.add_command(label='opção5')
sobre.add_command(label='opção6')

menu.add_cascade(label = 'Sobre', menu = sobre)

app.config(menu=menu)

#-----------------------------------------------------------------------------------------------------------

frameTools = tk.Frame(app, borderwidth=2, relief= tk.GROOVE)
frameTools.grid(row=0, column=0, padx=5, pady=5, sticky=N)

frameWorkstation = tk.Frame(app, borderwidth=2, relief= tk.GROOVE, width=50, height=100)
frameWorkstation.grid(row=1, column=0, padx=5, pady=5, sticky=N)

#-----Slide TimeLine ---------------------------------------------------------

frameOPresentationTimeLine = customtkinter.CTkScrollableFrame(frameWorkstation, width=160, height=600)
frameOPresentationTimeLine.grid(row=0, column=0, padx=5, pady=5, sticky=W)

#slide1 = customtkinter.CTkCanvas(frameOPresentationTimeLine, borderwidth=0, width = 150, height = 100, bg = 'white')
#slide1.grid(row=0, column=0, padx=2.5, pady=2.5)

framePresentationEdition = tk.Frame(frameWorkstation, borderwidth=2, relief= tk.GROOVE)
framePresentationEdition.grid(row=0, column=1, padx=5, pady=5, sticky=NE)

frameOptions = tk.Frame(framePresentationEdition, borderwidth=2, relief= tk.GROOVE)
frameOptions.grid(row=0, column=0, padx=10, pady=10, sticky=NE)

frameworkArea = tk.Frame(framePresentationEdition, borderwidth=2, relief= tk.GROOVE)
frameworkArea.grid(row=1, column=0, padx=15, pady=15, sticky=NE)

f1 = tk.Frame(frameworkArea, borderwidth=2, relief= tk.GROOVE)
f1.grid(row=0, column=0, padx=10, pady=10, sticky=NE)

f2 = tk.Frame(frameworkArea, borderwidth=2, height = 30, width=80, relief= tk.GROOVE)

#f2.grid(row=0, column=1, padx=15, pady=15)


pres = PresentationFile(f1, frameOPresentationTimeLine, fileName='Arquivo de teste', numDeSlides=1, autor = 'Kelryson', dateOfCreation='04/07/2024')

btAddNewSlide = customtkinter.CTkButton(frameOPresentationTimeLine, text="+",  width=150, command=lambda: pres.addNewSlide([400, 300], color='white', btAddNewSlide=btAddNewSlide))
btAddNewSlide.grid(row=int((pres.getPresentation()).attrib['numDeSlides']), column=0, padx=0, pady=5, sticky=N)

#canvas = customtkinter.CTkCanvas(f1,width = 400,height = 300,bg = 'white')

#canvas.pack()
#canvas.grid(row=0, column=0, padx=20, pady=20, sticky="w", columnspan=2)

optionsAddDraw = customtkinter.CTkButton(frameTools, text="Retângulo", command=setAddDrawVisible)
optionsAddDraw.grid(row=0, column=0, padx=10, pady=5, columnspan=1)

optionsAddText = customtkinter.CTkButton(frameTools, text="Texto", command=setAddTextVisible)
optionsAddText.grid(row=0, column=1, padx=10, pady=5, columnspan=1)

optionsAdicionarImagem = customtkinter.CTkButton(frameTools, text="Adicionar Imagem", command=None)
optionsAdicionarImagem .grid(row=0, column=2, padx=10, pady=5, columnspan=1)

optionsButton2 = customtkinter.CTkButton(frameTools, text="Button2", command=None)
optionsButton2.grid(row=0, column=3, padx=10, pady=5, columnspan=1)

optionsButton3 = customtkinter.CTkButton(frameTools, text="Button3", command=None)
optionsButton3.grid(row=0, column=4, padx=10, pady=5, columnspan=1)

optionsButton4 = customtkinter.CTkButton(frameTools, text="Adicionar Slide", command= None)
optionsButton4.grid(row=0, column=4, padx=10, pady=5, columnspan=1)

button = customtkinter.CTkButton(f2, text="Criar retângulo", command= lambda: pres.currentSlide.addNewElement('blue', x1=float(E1.get()), y1=float(E2.get()), x2=float(E3.get()), y2=float(E4.get()), type='rectangle', position=None))
button.grid(row=0, column=0, padx=10, pady=10, columnspan=2)  

buttonDelete = customtkinter.CTkButton(f2, text="Deletar", command= lambda: delete((pres.currentSlide).getCanvasPrincipal()))
buttonDelete.grid(row=1, column=0, padx=15, pady=10, columnspan=2)

#button = customtkinter.CTkButton(f2, text="Delete", command=delete(canvas))
#button.grid(row=1, column=0, padx=15, pady=10, columnspan=2)

#canvas.create_rectangle(60, 40, 100, 100, fill=None)

#canvas.create_text(80, 80, text='Isto é apenas um teste', fill='black', width=60)
 
#pc = canvas.create_rectangle(80-60, 80-40, 80+60, 80+40, fill=None)

vare1 = tk.StringVar()

E1 = customtkinter.CTkEntry(f2, placeholder_text="Posição x1")
E1.grid(row=2, column=0, padx=15, pady=10)

vare2 = tk.StringVar()

E2 = customtkinter.CTkEntry(f2, placeholder_text="Posição y1")
E2.grid(row=3, column=0, padx=15, pady=10)

vare3 = tk.StringVar()

E3 = customtkinter.CTkEntry(f2, placeholder_text="Posição x2")
E3.grid(row=4, column=0, padx=15, pady=10)

vare4 = tk.StringVar()

E4 = customtkinter.CTkEntry(f2, placeholder_text="Posição y2")
E4.grid(row=5, column=0, padx=15, pady=10)

#----------------------------------------------------------------------------------------

frameAddText = tk.Frame(frameworkArea, borderwidth=2, height = 30, relief= tk.GROOVE)
#frameAddText.grid(row=0, column=1, padx=15, pady=15)

buttonText = customtkinter.CTkButton(frameAddText, text="Criar texto", command= lambda: pres.currentSlide.addNewElement(string=str(R1.get()),  x1 = float(R2.get()), y1 = float(R3.get()), type='textBox'))
buttonText.grid(row=2, column=0, padx=15, pady=10, columnspan=2)  

vare1 = tk.StringVar()

R1 = customtkinter.CTkEntry(frameAddText, placeholder_text="Posição x1")
R1.grid(row=3, column=0, padx=15, pady=10)

vare2 = tk.StringVar()

R2 = customtkinter.CTkEntry(frameAddText, placeholder_text="Posição y1")
R2.grid(row=4, column=0, padx=15, pady=10)

vare3 = tk.StringVar()

R3 = customtkinter.CTkEntry(frameAddText, placeholder_text="Posição x2")
R3.grid(row=5, column=0, padx=15, pady=10)

#checkbox_1 = customtkinter.CTkCheckBox(f2, text="checkbox 1")
#checkbox_1.grid(row=6, column=0, padx=15, pady=10)

#checkbox_2 = customtkinter.CTkCheckBox(f2, text="checkbox 2")
#checkbox_2.grid(row=7, column=0, padx=15, pady=10)

app.mainloop()


