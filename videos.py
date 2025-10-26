from tkinter import Canvas, Tk, Menu, NW, CENTER
from PIL import Image, ImageTk
import cv2
import numpy as np
import filtros
from tkinter import filedialog as fidia
import suporteImg
import inspect

global cap

image_id = None
def videos(inserida):
    
    global filtro 
    global qntdButoes
   
    global entrada
    entrada = [5,5]
    global itens
    itens = []
    
    filtro = 0
    
    def show_frame():
        global image_id
        ret, frame = cap.read()
        global width
        global height
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            alturaImagem, larguraImagem = frame.shape[:2]
            frame, alturaImagem, larguraImagem = suporteImg.mudarTamImg(frame, width-10, height-200, alturaImagem, larguraImagem)
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
                img = suporteImg.converteImagem(opencv_image)
                photo = img
            canvas.photo = photo
            if image_id:       
                canvas.itemconfig(image_id, image=photo)
            else:
                image_id = canvas.create_image((0,0), image=photo, anchor='nw')
                canvas.configure(width=photo.width(), height=photo.height())
            root.after(20, show_frame)
        else:
            suporteImg.menuVoltar(root)   
        
        
    global minVal
    global maxVal
    def mudarFiltros(valor, qntdBotoes, minV, maxV, texto):
        global itens
        itens =  suporteImg.removerItens(itens)
        global filtro
        filtro = valor
        def executarAdd():
            caller = inspect.stack()[1].frame
            localvars = caller.f_locals
            self = localvars['self']
            i = (self.widget.grid_info()['column'])
            i = int((i-1)/3)
            
            addValor(i, texto)
            return executarAdd
        
        def executarDiminui():
            caller = inspect.stack()[1].frame
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

    cap = cv2.VideoCapture(inserida)
    
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
    global root
    
    root = Tk()
    root.state('zoomed')
    root.title("Videos")
  
    global width
    global height
    
    width= root.winfo_screenwidth()               
    height= root.winfo_screenheight()   
    root.geometry()
    
    can = Canvas(root, bg = '#44444E', width=width, height=height)
    can.place(relx=0,rely=0, anchor=NW)
  
    can1 = Canvas(root, bg='#37353e', height=50)
    can1.grid(row=0, column=0, sticky='nsew', columnspan=10)
    root.grid_columnconfigure(9, weight=1)
    
    canvas = Canvas(root)
    canvas.place(relx=0.5, rely=0.53, anchor=CENTER)
    
    menu = Menu(root)
    
    item1 = Menu(menu)
    item1.add_command(label="Voltar ao Menu", command=lambda : suporteImg.menuVoltar(root))
    
    item2 = Menu(menu)
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

    menu.add_cascade(label="Arquivo", menu=item1)
    menu.add_cascade(label="Filtros", menu=item2)
    root.config(menu=menu)
    
    show_frame()

    root.mainloop()