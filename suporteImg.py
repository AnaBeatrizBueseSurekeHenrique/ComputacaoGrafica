import cv2
from tkinter import *
from PIL import Image, ImageTk  
import menu as m
import inspect
def converteImagem(img):
    if(len(img.shape)==3):
        b,g,r = cv2.split(img)
        img = cv2.merge((r,g,b))
    imgtk = ImageTk.PhotoImage((Image.fromarray(img)))
    return imgtk


def mudarTamImg(imagem, width, height, altImg, larImg):
    while(larImg > width or altImg > height):
        if(altImg > (height)):
            proporcao = height/(altImg)
            altImg = height
            larImg = int(larImg*proporcao)
        if(larImg > (width)):
            proporcao = width/(larImg)
            larImg = width
            altImg = int(altImg*proporcao)
    imagem = cv2.resize(imagem, (larImg, altImg))
    return imagem, altImg, larImg

def menuVoltar(root):
    root.destroy()    
    m.menu()

def removerItens(itens):
    while(itens):
        itens[0].destroy()
        itens.remove(itens[0])
    return itens

def criacaoBotoes(botao, botao2, itens, label, executarAdd, executarDiminui, i, root, texto, entrada):
    botao.append(Button(text="+", width=10, command=executarAdd, activebackground="#d3dad9"))
    botao[i].grid(row=0, column=1+(i)*(3), padx=(10))

    itens.append(botao[i])
    
    label.append(Label(root, text=texto[i]+str(entrada[i]), bg="#37353e", fg='#d3dad9', font=("Arial", 10, "bold")))
    label[i].grid(row=0, column=2+(i)*(3), padx=0)
    
    itens.append(label[i])
    
    botao2.append(Button(text="-", width=10, command=executarDiminui, activebackground="#d3dad9"))
    botao2[i].grid(row=0, column=3+(i)*3)
    
    itens.append(botao2[i])
    return botao, botao2, label, itens