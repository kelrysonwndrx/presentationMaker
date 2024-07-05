from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import xml.etree.ElementTree as et

import customtkinter
import tkinter as tk
from tkinter import StringVar
from tkinter import *
from tkinter.filedialog import askopenfilename
import Elements as el

def getSlideInThePosition(self, position):
    if(position<len(self.slide)):
        return self.slides[position]
    else: print("Posição maior que o número de slides dessa apresentação")
#--------------------------------------------------------------------------------
#----To improve implementation------------------------------------
class PresentationFile():
    def __init__(self, framePrincipal, framePreview, fileName='', numDeSlides=1, autor = '', dateOfCreation=''):
        self.presentation = et.Element('presentation')
        self.presentation.attrib = {'id': '0', 'fileName': str(fileName), 'numDeSlides': str(numDeSlides), 'autor': str(autor), 'dateOfCreation': str(dateOfCreation)}
        self.slides = []
        self.framePrincipal = framePrincipal
        self.framePreview = framePreview
        self.currentSlide = None

        if(numDeSlides>0):
            for i in range(1, numDeSlides+1):
                canvasPrincipal = customtkinter.CTkCanvas(self.framePrincipal, width = 400, height = 300, bg = 'white')
                canvasPreview = customtkinter.CTkCanvas(self.framePreview, width = 150, height = 100, bg = 'white')
                slide = (Slide(canvasPrincipal, canvasPreview, i, [300, 200], 'white'))

                (self.slides).append(slide)
                (self.presentation).append(slide.getSlide())
                self.currentSlide = slide
                canvasPreview.grid(row=i-1, column=0, padx=2.5, pady=2.5)
            ((self.currentSlide).getCanvasPrincipal()).pack()

        else:
            print('Número de slides menor que 1')
    
    def getPresentation(self):
        return self.presentation

    def getSlides(self):
        return (self.slides)

    def getInformations(self, info=None):
        if(info == 'autor'):
            return (self.presentation).attrib['autor']
        elif(info == 'numDeSlides'):
            return (self.presentation).attrib['numDeSlides']
        elif(info == 'dateOfCreation'):
            return (self.presentation).attrib['dateOfCreation']
        elif(info == None):
            informations = {'autor': (self.presentation).attrib['autor'], 'numDeSlides': (self.presentation).attrib['numDeSlides'], 'dateOfCreation': (self.presentation).attrib['dateOfCreation']}
            return informations

    def addNewSlide(self, tamanho, color='white', btAddNewSlide=None, position=None):
        if(position == None):
            (self.presentation).attrib['numDeSlides'] = str(int((self.presentation).attrib['numDeSlides'])+1)
            canvasPrincipal = customtkinter.CTkCanvas(self.framePrincipal, width = 400, height = 300, bg = 'white')
            canvasPreview = customtkinter.CTkCanvas(self.framePreview, width = 150, height = 100, bg = 'white')

            slide = Slide(canvasPrincipal, canvasPreview, (self.presentation).attrib['numDeSlides'], tamanho, color)
            
            (self.slides).append(slide)
            (self.presentation).append(slide.getSlide())

            btAddNewSlide.grid_forget()
            btAddNewSlide = customtkinter.CTkButton(self.framePreview, text="+", command= lambda: self.addNewSlide([300, 200], 'white', btAddNewSlide=btAddNewSlide), width=150)
            btAddNewSlide.grid(row=int((self.presentation).attrib['numDeSlides']), column=0, padx=0, pady=5, sticky=N)

            ((self.currentSlide).getCanvasPrincipal()).pack_forget()

            canvasPrincipal.pack()

            canvasPreview.grid(row=int((self.presentation).attrib['numDeSlides'])-1, column=0, padx=2.5, pady=2.5)

            self.currentSlide = slide
        else:

            (self.presentation).attrib['numDeSlides'] = str(int((self.presentation).attrib['numDeSlides'])+1)
            canvasPrincipal = customtkinter.CTkCanvas(self.framePrincipal, width = 300, height = 200, bg = 'white')
            canvasPreview = customtkinter.CTkCanvas(self.framePreview, width = 150, height = 100, bg = 'white')
            slide = Slide(canvasPrincipal, canvasPreview, position, tamanho, color)
            self.currentSlide = slide
            aux = self.slides[position-1]
            self.slides[position-1] = slide
            (self.slides).append((self.slides)[-1])

            for j in range(position, int((self.presentation).attrib['numDeSlides'])-1):

                self.slides[j] = aux
                aux = self.slides[j+1]

            for s in (self.presentation):
               if(int(s.attrib['id']) > position-1):
                    s.attrib['id'] = str(int(s.attrib['id'])+1)
            
            (self.presentation).append(slide.getSlide())
            ((self.currentSlide).getCanvasPrincipal()).pack_forget()
            canvasPrincipal.pack()

    #Method to implement
    def deleteSlide(self, position):
        if(position < int((self.presentation).attrib['numDeSlides']) and position > 0):
            (self.slides).pop(position-1)
            for s in (self.presentation):
               if(int(s.attrib['id']) == position):
                    (self.presentation).remove(s)
            (self.presentation).attrib['numDeSlides'] = str(int((self.presentation).attrib['numDeSlides'])-1)

            for s in (self.presentation):
               if(int(s.attrib['id']) > position-1):
                    s.attrib['id'] = str(int(s.attrib['id'])-1)
        
        else:
            print("Posição indicada fora do número de Slides")

    #Checar método
    def moveSlide(self, position1, position2):
        if((position1 < int((self.presentation).attrib['numDeSlides']) and position1 > 0)):
            if((position2 < int((self.presentation).attrib['numDeSlides']) and position2 > 0)):
                aux1 = self.slides[position1-1]
                aux2 = self.slides[position2-1]
                self.slides[position1-1] = aux2
                self.slides[position2-1] = aux1

            for s in (self.presentation):
                if((int(s.attrib['id']) == position1)):
                    s.attrib['id'] = str(int(position2))
                elif((int(s.attrib['id']) == position2)):
                    s.attrib['id'] = str(int(position1))

    def save(self, caminho):
        tree = et.ElementTree(self.presentation)
        tree.write(caminho, encoding = 'utf-16')

    def showXMLFile(self):
        et.dump(et.ElementTree(self.presentation))

class Slide():

    def __init__(self, canvasPrincipal, canvasPreview, id, tamanho, color='white'):
        self.slide = et.Element('slide')
        self.elements = []
        self.id = id
        self.slide.attrib = {'id': str(id), 'numDeElements': str(0), 'width': str(tamanho[0]), 'height': str(tamanho[1]), 'background_color': str(color)}
        self.canvasPrincipal = canvasPrincipal
        self.canvasPreview = canvasPreview
        self.ratioWidth = 150/int(self.slide.attrib['width'])
        self.rationHeight = 100/int(self.slide.attrib['height'])

    def getSlide(self):
        return self.slide

    def getInfo(self, info=None):
        if(info == 'id'):
            return (self.slide).attrib['id']
        elif(info == 'width'):
            return (self.slide).attrib['width']
        elif(info == 'height'):
            return (self.slide).attrib['height']
        elif(info == 'background_color'):
            return (self.slide).attrib['background_color']
        elif(info == None):
            return self.slide.attrib

    def getCanvasPrincipal(self):
        return self.canvasPrincipal

    def getCanvasPreview(self):
        return self.canvasPreview

    def addNewElement(self, string, x1, y1, x2=None, y2=None, type=None, position=None):

        if(type == 'textBox'):
            if(position == None):
                (self.slide).attrib['numDeElements'] = str(int((self.slide).attrib['numDeElements'])+1)
                textPrincipal = el.DraggableText(self.canvasPrincipal, x1, y1, text=string, fill='black', width=80)
                textPreview = el.DraggableText(self.canvasPreview, round(self.ratioWidth*x1), round(self.rationHeight*y1), text=string, fill='black', width=80)
                text = TextBox((self.slide).attrib['numDeElements'], string, x1, y1, textPrincipal, textPreview)
                (self.elements).append(text)
                (self.slide).append(text.getElement())
            else:

                (self.slide).attrib['numDeElements'] = str(int((self.slide).attrib['numDeElements'])+1)
                text = textBox(position, string, x1, y1)
                aux = self.elements[position-1]
                self.elements[position-1] = text
                (self.elements).append((self.elements)[-1])

                for j in range(position, int((self.slide).attrib['numDeElements'])-1):

                    self.elements[j] = aux
                    aux = self.elements[j+1]

                for s in (self.slide):
                    if(int(s.attrib['id']) > position-1):
                            s.attrib['id'] = str(int(s.attrib['id'])+1)
                    
                (self.slide).append(text.getElement())

        elif(type == 'rectangle'):

            if(position == None):
                (self.slide).attrib['numDeElements'] = str(int((self.slide).attrib['numDeElements'])+1)
                dRectPrincipal = el.DraggableRectangle(self.canvasPrincipal, x1, y1, x2, y2, fill=string)
                dRectPreview = el.DraggableRectangle(self.canvasPreview, round(self.ratioWidth*x1), round(self.rationHeight*y1), round(self.ratioWidth*x2), round(self.rationHeight*y2), fill=string)
                rectangle = Rectangle((self.slide).attrib['numDeElements'], x1, y1, x2, y2, string)
                (self.elements).append(rectangle)
                (self.slide).append(rectangle.getElement())
            else:

                (self.slide).attrib['numDeElements'] = str(int((self.slide).attrib['numDeElements'])+1)
                rectangle = Rectangle(position, x1, y1, x2, y2, string)
                aux = self.elements[position-1]
                self.elements[position-1] = rectangle
                (self.elements).append((self.elements)[-1])

                for j in range(position, int((self.slide).attrib['numDeElements'])-1):

                    self.elements[j] = aux
                    aux = self.elements[j+1]

                for s in (self.slide):
                    if(int(s.attrib['id']) > position-1):
                            s.attrib['id'] = str(int(s.attrib['id'])+1)
                        
                (self.slide).append(rectangle.getElement())

        elif(type == 'image'):
            pass


    #To check implmentation
    def deleteElement(self, position):
        if(position < int((self.slide).attrib['numDeElements']) and position > 0):
            (self.elements).pop(position-1)
            for s in (self.slide):
               if(int(s.attrib['id']) == position):
                    (self.slide).remove(s)
            (self.slide).attrib['numDeElements'] = str(int((self.slide).attrib['numDeElements'])-1)

            for s in (self.slide):
               if(int(s.attrib['id']) > position-1):
                    s.attrib['id'] = str(int(s.attrib['id'])-1)


    #To check implmentation
    def moveElement(self, position1, position2):
        if((position1 < int((self.slide).attrib['numDeElements']) and position1 > 0)):
            if((position2 < int((self.slide).attrib['numDeElements']) and position2 > 0)):
                aux1 = self.elements[position1-1]
                aux2 = self.elements[position2-1]
                self.elements[position1-1] = aux2
                self.elements[position2-1] = aux1

            for s in (self.slide):
                if((int(s.attrib['id']) == position1)):
                    s.attrib['id'] = str(int(position2))
                elif((int(s.attrib['id']) == position2)):
                    s.attrib['id'] = str(int(position1))
        
    def getElements(self):
        return self.elements

class TextBox():
    def __init__(self, id, text, x, y, elementPrincipal, elementPreview):
        self.textBox = et.Element('textBox')
        self.textBox.attrib = {'id': str(id), 'text': str(text), 'x':str(x), 'y':str(y)}
        self.elementPrincipal = elementPrincipal
        self.elementPreview = elementPreview

    def getElement(self):
        return self.textBox

    def getInfo(self, attrib):
        if(str(attrib) == None):
            return (self.texBox.attrib)
        else:
            return (self.texBox.attrib)[str(attrib)]

    def getElementPrincipal(self):
        return self.elementPrincipal

    def getElementPreview(self):
        return self.elementPreview

    def setPosition(self, x, y):
        self.textBox.attrib['x'] = str(x)
        self.textBox.attrib['y'] = str(y)
    
    def setText(self, text):
        self.textBox.attrib['text'] = str(text)

class Rectangle():
    def __init__(self, id, x1, y1, x2, y2, color, elementPrincipal, elementPreview):
        self.rectangle = et.Element('Rectangle')
        self.rectangle.attrib = {'id': str(id),'x1': str(x1), 'y1': str(x2), 'x2': str(x2), 'y2': str(y2), 'color': str(color)}
        self.elementPrincipal = elementPrincipal
        self.elementPreview = elementPreview

    def getElement(self):
        return self.rectangle

    def getElementPrincipal(self):
        return self.elementPrincipal

    def getElementPreview(self):
        return self.elementPreview

    def getInfo(self, attrib):
        if(str(attrib) == None):
            return self.rectangle.attrib
        else:
            return self.rectangle.attrib[str(attrib)]

    def setPosition(self, x1, y1, x2, y2):
        (self.rectangle.attrib)['x1'] = str(x1)
        (self.rectangle.attrib)['y1'] = str(y1)
        (self.rectangle.attrib)['x2'] = str(x2)
        (self.rectangle.attrib)['y2'] = str(y2)

    def setColor(self, color):
        (self.rectangle.attrib)['color'] = str(color)

#Image (To implement after all)
class Image():
    def __init__(self, elementPrincipal, elementPreview):
        self.textBox = et.Element('Image')
        self.elementPrincipal = elementPrincipal
        self.elementPreview = elementPreview

    def getElement(self):
        return self.textBox

    def getElementPrincipal(self):
        return self.elementPrincipal

    def getElementPreview(self):
        return self.elementPreview

#--------TESTS-----------------------------------------------------------------------------------