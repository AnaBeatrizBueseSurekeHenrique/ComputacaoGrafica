import filtros

import cv2
import numpy as np
from tkinter import Label, Tk, Canvas, Menu, NW, CENTER, filedialog as fidia
from PIL import ImageTk  
import inspect
from skimage.segmentation import flood_fill, flood
import suporteImg
import operacoes
import random

def imagem(imagemInicio):
    global imagemCanvas
    
    global entrada
    entrada = [5,6]
    
    global itens
    itens = []
    
    global img
    
    img = cv2.imread(imagemInicio)
    
    global novaImg
    
    novaImg = img
    
    # responsavel por inserir a imagem no canva
    def uploadImagem(imagem, width, height):
        global imagemCanvas
        alturaImagem, larguraImagem = imagem.shape[:2]
        imagem, alturaImagem, larguraImagem = suporteImg.mudarTamImg(imagem, width-10, height-100, alturaImagem , larguraImagem)
        imagemCanvas = suporteImg.converteImagem(imagem)
        canvas.delete("all")
        canvas.configure(width=larguraImagem, height=alturaImagem)
        canvas.create_image((0,0), anchor="nw", image=imagemCanvas)
    
    # imagem sem filtros.
    def imagemInicial(width, height):
        global itens
        itens =  suporteImg.removerItens(itens)        
        global img
        global novaImg
        novaImg = img
        uploadImagem(novaImg, width, height)
    
    # insere uma novo foto
    def inserirFoto(width, height):
        global novaImg
        global img
        global itens
        itens =  suporteImg.removerItens(itens)
        fileName = fidia.askopenfilename(filetypes=[("Png Pictures", "*.png"),("Jpg Pictures", "*.jpg"), ("Jpeg Pictures", "*.jpeg")])
        img = cv2.imread(fileName)
        novaImg = img
        uploadImagem(img, width, height)
    
    # salva a imagem como png
    def salvarImagem():
        fileName = fidia.asksaveasfilename(initialdir = "/",title = "Selecionar Arquivo", confirmoverwrite=True, filetypes=[("Fotos Png", "*png")])
        fileName += ".png"
        img = ImageTk.getimage(imagemCanvas)
        npImagem = np.array(img)
        imagemCv = cv2.cvtColor(npImagem, cv2.COLOR_RGB2BGR)
        cv2.imwrite(fileName, imagemCv)
    
    def histograma(width, height):
        global itens
        itens = suporteImg.removerItens(itens)
        global novaImg
        opencvImage, novaImg = operacoes.calcHistograma(novaImg)
        uploadImagem(opencvImage, width, height)  
    
    def area():
        global root
        w = root.winfo_screenwidth()
        h = root.winfo_screenheight()
        uploadImagem(img, w, h)
        imagemInicial(width, height)
        global itens
        itens = suporteImg.removerItens(itens)
        itens = operacoes.calcArea(root, itens, img)
        
    def calcPerimetro():
        global root
        w = root.winfo_screenwidth()
        h = root.winfo_screenheight()
        uploadImagem(img, w, h)
        global itens
        itens =  suporteImg.removerItens(itens)
        thresh = filtros.filtroOtsu(img) 
        contours, hierarchy = cv2.findContours(thresh, 1, 2)
        perimetro = 0
        for cnt in contours:
            perimetro += cv2.arcLength(cnt, True)
        label = Label(root, text="Valor do Perimetro: " + str(perimetro) + " pixels", bg="#37353e", fg='#d3dad9', font=("Arial", 10, "bold"))
        label.grid(row=0, column=1, padx=(10))        
        itens.append(label)
    
    def calcDiametro():    
        global root
        w = root.winfo_screenwidth()
        h = root.winfo_screenheight()
        uploadImagem(img, w, h)
        global itens
        itens =  suporteImg.removerItens(itens)
        thresh = filtros.filtroOtsu(img) 
        contours,hierarchy = cv2.findContours(thresh,1,2)
        diametro = 0
        for i in contours:
            (x,y),radius = cv2.minEnclosingCircle(i)
            radius = int(radius)
            diametro += (radius*radius)*4.13
        label = Label(root, text="Valor do Diametro: " + str(diametro) + " pixels", bg="#37353e", fg='#d3dad9', font=("Arial", 10, "bold"))
        label.grid(row=0, column=1, padx=(10))        
        itens.append(label)
    
    def contarObjetos():
        global root
        w = root.winfo_screenwidth()
        h = root.winfo_screenheight()
        global itens
        
        itens =  suporteImg.removerItens(itens)
        qntd = 0
        height, weight = img.shape[:2]
        mask = np.zeros((height + 2, weight + 2), np.uint8)
        auxImg = img.copy()
        colorirImg = img.copy()
        auxImg = filtros.filtroOtsu(auxImg)
           
        if np.sum(auxImg == 255) > np.sum(auxImg == 0):
            auxImg = filtros.filtroNegativo(auxImg)
            
        for i in range(0,height):
            for j in range(0,weight):
                if(auxImg[i][j] == 255):
                    qntd += 1
                    mask = flood(auxImg, (i, j), tolerance=20)
                    auxImg = flood_fill(auxImg, (i, j), 0, tolerance=20)
                    
                    blue = random.randint(0, 255)
                    green = random.randint(0, 255)
                    red = random.randint(0, 255)

                    corAtual = (blue, green, red)
                    colorirImg[mask] = corAtual
                    
        uploadImagem(colorirImg,w, h)     
        label = Label(root, text="Quantidade de Objetos = " + str(qntd), bg="#37353e", fg='#d3dad9', font=("Arial", 10, "bold"))
        label.grid(row=0, column=1, padx=(10))        
        itens.append(label)
    
    def addValor(i, filtro, qntdBotoes, width, height, minVal, maxVal, texto):

        if(entrada[i]+1 < maxVal[i]):
            entrada[i] += 1
            if(len(maxVal) == 1):
                filtrar(filtro, qntdBotoes, width, height, minVal,maxVal, texto)
            else:
                if(i != 0):
                    filtrar(filtro, qntdBotoes, width, height, minVal, [entrada[1], 255], texto)
                else:
                    filtrar(filtro, qntdBotoes, width, height, [0, entrada[0]], maxVal, texto)
    
    def diminuiValor(i, filtro, qntdBotoes, width, height, minVal, maxVal, texto):

        if(entrada[i]-1 > minVal[i]):
            entrada[i] -= 1
            if(len(minVal) == 1):
                filtrar(filtro, qntdBotoes, width, height, minVal,maxVal, texto)
            else:
                if(i != 0):
                    filtrar(filtro, qntdBotoes, width, height, minVal, [entrada[0], 255], texto)
                else:
                    filtrar(filtro, qntdBotoes, width, height, [0, entrada[1]], maxVal, texto)
    
    def filtrar(filtro, qntdBotoes, width, height, valMin, valMax, texto):
        global itens
        itens =  suporteImg.removerItens(itens)
        global novaImg
        global img
      
        if(qntdBotoes > 0):
            
            botao = []
            botao2 = []
            label = []
            
            def executarAdd():
                caller = inspect.stack()[1].frame
                localvars = caller.f_locals
                self = localvars['self']
                i = (self.widget.grid_info()['column'])
                i = int((i-1)/3)
                
                addValor(i, filtro=filtro, qntdBotoes=qntdBotoes, width=width, height=height, minVal=valMin, maxVal=valMax, texto=texto)
                return executarAdd
            
            def executarDiminui():
                caller = inspect.stack()[1].frame
                localvars = caller.f_locals
                self = localvars['self']
                i = (self.widget.grid_info()['column'])
                i = int((i-3)/3)
                
                diminuiValor(i, filtro=filtro, qntdBotoes=qntdBotoes, width=width, height=height, minVal=valMin, maxVal=valMax, texto=texto)
                return executarDiminui
            
            for i in range(0, qntdBotoes):
                botao, botao2, label, itens =  suporteImg.criacaoBotoes(botao, botao2, itens, label, executarAdd, executarDiminui, i, root, texto, entrada)            
            novaImg = filtro(img, entrada)
        else:
            
            novaImg = filtro(img)
        
        uploadImagem(novaImg, width, height)
     
    def filtroInicial(filtro, qntdBotoes, width, height, valMin, valMax, texto):
        for i in range(0, qntdBotoes):
            entrada[i] = 5+i
        filtrar(filtro, qntdBotoes, width, height, valMin, valMax, texto)
    global root 
    root = Tk()
    root.title("Imagens")
    root.geometry()
    root.state('zoomed')
    width = root.winfo_screenwidth()
    height = root.winfo_screenheight()
    
  
    canAux = Canvas(root, bg='#44444E', width=width, height=height)
    canAux.place(relx=0,rely=0, anchor=NW)
    
    canvas = Canvas(root)
    canvas.place(relx=0.5, rely=0.5, anchor=CENTER)
    
    canSuperior = Canvas(root, bg = "#37353e", height=40, width=width)
    canSuperior.grid(row= 0, column= 0, sticky='nsew', columnspan=10)
    
    root.grid_columnconfigure(9, weight=1)
    uploadImagem(img, width, height)
    
    menu = Menu(root)
    
    item1 = Menu(menu)
    item1.add_command(label="Inserir Nova Foto", command= lambda : inserirFoto(width, height))
    item1.add_command(label="Salvar Foto", command=salvarImagem)
    item1.add_command(label="Voltar ao Menu", command=lambda : suporteImg.menuVoltar(root))
    
    
    item2 = Menu(menu)
    item2.add_command(label='Imagem Original', command= lambda : imagemInicial(width, height))
    item2.add_command(label="Preto e Branco", command= lambda : filtroInicial(filtro=filtros.filtrosDeCinza, qntdBotoes=0, width=width, height=height, valMin=[0], valMax=[0], texto=[]))
    item2.add_command(label="Negativo", command=lambda : filtroInicial(filtro=filtros.filtroNegativo, qntdBotoes=0, width=width, height=height,valMin=[0], valMax=[0], texto=[]))
    item2.add_command(label='Otsu', command=lambda : filtroInicial(filtro=filtros.filtroOtsu,qntdBotoes=0, width=width, height=height, valMin=[0], valMax=[0], texto=[]))
    item2.add_command(label="Suavização por Média", command=lambda : filtroInicial(filtro=filtros.suavizacaoMedia, qntdBotoes=1, width=width, height=height, valMin=[0], valMax=[25], texto=['Kernel: ']))
    item2.add_command(label="Suavização por Mediana", command=lambda : filtroInicial(filtro=filtros.suavizacaoMediana, qntdBotoes=1, width=width, height=height, valMin=[0], valMax=[25], texto=['Kernel: ']))
    item2.add_command(label="Canny", command=lambda : filtroInicial(filtro=filtros.detectorBordasCanny, qntdBotoes=2, width=width, height=height, valMin=[0, entrada[0]],valMax=[entrada[1], 255], texto=['Threshold 1: ', 'Threshold 2: ']))
    item2.add_command(label="Erosão", command=lambda : filtroInicial(filtro=filtros.filtroErosao, qntdBotoes=1, width=width, height=height, valMin=[0], valMax=[25], texto=['Qntd Iterações: ']))
    item2.add_command(label="Dilatação", command=lambda : filtroInicial(filtro=filtros.filtroDilatacao, qntdBotoes=1, width=width, height=height, valMin=[0], valMax=[25], texto=['Qntd Iterações: ']))
    item2.add_command(label="Abertura", command=lambda : filtroInicial(filtro=filtros.abertura, qntdBotoes=1, width=width, height=height, valMin=[0], valMax=[25], texto=['Qntd Iterações: ']))
    item2.add_command(label="Fechamento", command=lambda : filtroInicial(filtro=filtros.fechamento, qntdBotoes=1, width=width, height=height, valMin=[0], valMax=[25], texto=['Qntd Iterações: ']))
    
    
    item3 = Menu(menu)
    item3.add_command(label='Histograma', command=lambda : histograma(width, height))
    item3.add_command(label="Calculo Área", command=area)
    item3.add_command(label="Calculo Diametro", command=calcDiametro)
    item3.add_command(label="Calculo Perimetro", command=calcPerimetro)    
    item3.add_cascade(label="Contador de Objetos", command=contarObjetos)
    
    
    menu.add_cascade(label="Arquivos", menu=item1)
    menu.add_cascade(label="Filtros", menu=item2)
    menu.add_cascade(label="Operações", menu=item3)
    
    root.config(menu=menu)
    
    root.mainloop()