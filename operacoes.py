from matplotlib import pyplot as plt
from PIL import Image  
import cv2
import io
import numpy as np
import suporteImg
import filtros
from tkinter import Label

def calcHistograma(novaImg):
    
    plt.clf()
    color = ('b', 'g', 'r')
    plt.xlabel('Bins')
    plt.ylabel("# de Pixels")
    plt.title("Histograma")
    
    if(len(novaImg.shape) > 2):
        for i, col in enumerate(color):
            histr = cv2.calcHist([novaImg],[i],None,[256],[0,256])
            plt.plot(histr,color = col)
    else:
        hist = cv2.calcHist([novaImg], [0], None, [256], [0, 256])        
        plt.plot(hist)
        
    plt.xlim([0,256])
    img_buf = io.BytesIO() 
    plt.savefig(img_buf, format='png')
    novaImg = Image.open(img_buf)
    opencvImage = cv2.cvtColor(np.array(novaImg), cv2.COLOR_RGB2BGR)
    return opencvImage, novaImg

def calcArea(root, itens, img):
    itens =  suporteImg.removerItens(itens)
    thresh = filtros.filtroOtsu(img)
    contours, hierarchy = cv2.findContours(thresh, 1, 2)
    area = 0
    for cnt in contours:       
        area += cv2.contourArea(cnt)
    label = Label(root, text="Valor da Área: " + str(area) + " pixels", bg="#37353e", fg='#d3dad9', font=("Arial", 10, "bold"))
    label.grid(row=0, column=1, padx=(10))
    itens.append(label)
    return itens