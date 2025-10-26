from tkinter import Canvas, Tk, Menu
from PIL import Image, ImageTk
import cv2
import numpy as np
import filtros
from inspect import stack
import suporteImg

image_id = None

def camera():
    
    global detectFrontal
    detectFrontal = cv2.CascadeClassifier('cascades\\haarcascade_frontalface_default.xml')    
    
    global detectProfile
    detectProfile = cv2.CascadeClassifier('cascades\\haarcascade_profileface.xml')  
      
    global filtro 
    filtro = 0
    

  
    global entrada
    entrada = [5,5]
    
    global itens
    itens = []
    

    def showFrame():
        global image_id

        ret, frame = cap.read()
    
        if ret:
            
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)
            
            if filtro == 0:
                photo = ImageTk.PhotoImage(image=img)
            else:
                numpy_image = np.array(img)
                opencv_image = cv2.cvtColor(numpy_image, cv2.COLOR_RGB2BGR)   
                
                
                if filtro == 1:
                    opencv_image = filtros.filtrosDeCinza(opencv_image)
                
                elif filtro == 2: 
                    opencv_image = filtros.filtroNegativo(opencv_image)
                
                elif filtro == 3:
                    opencv_image = filtros.filtroOtsu(opencv_image)
                
                elif filtro == 4:
                    opencv_image = filtros.suavizacaoMedia(opencv_image, entrada)
                
                elif filtro == 5:
                    opencv_image = filtros.suavizacaoMediana(opencv_image, entrada)
                
                elif filtro == 6:
                    opencv_image = filtros.detectorBordasCanny(opencv_image, entrada)
                
                elif filtro == 7:
                    opencv_image = filtros.filtroErosao(opencv_image, entrada)
                
                elif filtro == 8:
                    opencv_image = filtros.filtroDilatacao(opencv_image, entrada)
                
                elif filtro == 9:
                    opencv_image = filtros.abertura(opencv_image, entrada)
                
                elif filtro == 10:
                    opencv_image = filtros.fechamento(opencv_image, entrada)
                
                elif filtro == 11:
                    opencv_image = detectRosto(opencv_image)
                
                img = suporteImg.converteImagem(opencv_image)
                photo = img
            
            canvas.photo = photo
            
            # verifica se há imagem, se não há, cria uma nova.
            if image_id:       
                canvas.itemconfig(image_id, image=photo)
            else:
                image_id = canvas.create_image((0,0), image=photo, anchor='nw')
                canvas.configure(width=photo.width(), height=photo.height())
            
            root.after(20, showFrame)
            
    def detectRosto(frame):
        global detectFrontal
        global detectProfile
        
        #detecta rosto frontal e lateral
        face = detectFrontal.detectMultiScale(filtros.filtrosDeCinza(frame), 1.3, 3)
        for (x, y, larg, alt) in face:  
            ret = cv2.rectangle(frame, (x, y), (x + larg, y + alt), (0, 255, 0), 3)
        
        face = detectProfile.detectMultiScale(filtros.filtrosDeCinza(frame), 1.3, 3)
        for (x, y, larg, alt) in face:
            ret = cv2.rectangle(frame, (x, y), (x + larg, y + alt), (0, 255, 0), 3)
        
        return frame
    
    global minVal
    global maxVal
    
    def mudarFiltros(valor, qntdBotoes, minV, maxV, texto):
        global itens
        itens =  suporteImg.removerItens(itens)
        
        global filtro
        filtro = valor
        
        def executarAdd():
            caller = stack()[1].frame
            localvars = caller.f_locals
            self = localvars['self']
            
            i = (self.widget.grid_info()['column'])
            i = int((i-1)/3)
            
            addValor(i, texto)
            return executarAdd
        
        def executarDiminui():
            caller = stack()[1].frame
            localvars = caller.f_locals
            self = localvars['self']
            
            i = (self.widget.grid_info()['column'])
            i = int((i-3)/3)
            
            diminuiValor(i, texto)
            return executarDiminui
            
        global minVal
        minVal = minV
        global maxVal
        maxVal = maxV
        
        if(qntdBotoes > 0):
            botao = []
            botao2 = []
            label = []
            
            for i in range(0, qntdBotoes):
                botao, botao2, label, itens =  suporteImg.criacaoBotoes(botao, botao2, itens, label, executarAdd, executarDiminui, i, root, texto, entrada)            

    cap = cv2.VideoCapture(0)
    
    def addValor(i, texto):
        global itens
        global maxVal
        global minVal
        
        if(entrada[i]+1 < maxVal[i]):
            entrada[i] += 1
            if(len(maxVal) != 1):
                if(i != 0):
                    maxVal = [entrada[1],255]
                else:
                    minVal = [0, entrada[0]]
        
        itens[1+i*3].config(text=texto[i]+str(entrada[i]))
      
                
    def diminuiValor(i, texto):
        global minVal
        global maxVal
       
        if(entrada[i]-1 > minVal[i]):
            entrada[i] -= 1
            if(len(minVal) != 1):
                if(i != 0):
                    maxVal = [entrada[0], 255]
                else:
                    minVal =  [0, entrada[1]]
       
        itens[1+i*3].config(text=texto[i]+str(entrada[i]))
        
    def inserirFiltro(valor, qntdBotoes, valMin, valMax, texto):
        for i in range(0, qntdBotoes):
            entrada[i] = 5+i
        
        mudarFiltros(valor, qntdBotoes, valMin, valMax, texto)
       
    
    root = Tk()
    root.resizable(width=False, height=False)
    root.title("Camera")
    
    can1 = Canvas(root, bg='#37353e', height=50)
    can1.grid(row=0, column=0, sticky='nsew', columnspan=10)
    root.grid_columnconfigure(9, weight=1)

    canvas = Canvas(root)
    canvas.grid(row=1, column=1, sticky='nsew', columnspan=10)
            
    menu = Menu(root)
    item1 = Menu(menu)
    item1.add_command(label="Voltar ao Menu", command=lambda : suporteImg.menuVoltar(root))

    item2 = Menu(menu)
    item2.add_command(label="Ver Original", command=lambda : inserirFiltro(0,0, valMin=[0], valMax=[0], texto=[]))
    item2.add_command(label="Preto e Branco", command=lambda : inserirFiltro(1,0, valMin=[0], valMax=[0], texto=[]))
    item2.add_command(label="Negativo", command=lambda : inserirFiltro(2,0, valMin=[0], valMax=[0], texto=[]))
    item2.add_command(label="Otsu", command=lambda : inserirFiltro(3,0,valMin=[0], valMax=[0], texto=[]))
    item2.add_command(label="Suavização por Media", command=lambda : inserirFiltro(4,1, valMin=[0], valMax=[25], texto=['Kernel: ']))
    item2.add_command(label="Suavização pela Mediana", command=lambda : inserirFiltro(5,1, valMin=[0], valMax=[25], texto=['Kernel: ']))
    item2.add_command(label="Canny", command=lambda : inserirFiltro(6,2, valMin=[0, entrada[0]],valMax=[entrada[1], 255], texto=['Threshold 1: ', 'Threshold 2: ']))
    item2.add_command(label="Erosão", command=lambda : inserirFiltro(7,1,  valMin=[0], valMax=[25], texto=['Qntd Iterações: ']))
    item2.add_command(label="Dilatação", command=lambda : inserirFiltro(8,1,  valMin=[0], valMax=[25], texto=['Qntd Iterações: ']))
    item2.add_command(label="Abertura", command=lambda : inserirFiltro(9,1,  valMin=[0], valMax=[25], texto=['Qntd Iterações: ']))
    item2.add_command(label="Fechamento", command=lambda : inserirFiltro(10,1,  valMin=[0], valMax=[25], texto=['Qntd Iterações: ']))
    
    item3 = Menu(menu)
    item3.add_cascade(label="Detectar Faces", command=lambda : inserirFiltro(11,0, valMin=[0], valMax=[0], texto=[]))
    menu.add_cascade(label='Menu', menu=item1)
    menu.add_cascade(label="Filtros", menu=item2)
    menu.add_cascade(label="Detecção", menu=item3)
    root.config(menu=menu)

    showFrame()

    root.mainloop()