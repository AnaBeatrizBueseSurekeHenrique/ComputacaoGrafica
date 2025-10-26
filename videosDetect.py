from tkinter import Canvas, Tk, CENTER, NW, Menu, FALSE, filedialog as fidia
from ultralytics import YOLO
from pygame import mixer
import cv2
import suporteImg
import cvzone
import math

image_id = None
global cap

def videos(inserida):
    def inserirFoto():
        global cap
        filename = fidia.askopenfilename(filetypes=[("Videos", "*.mp4")])
        cap = cv2.VideoCapture(filename)

    global filtro 
    global qntdButoes
       
    global entrada
    entrada = [5,5]
    global itens
    itens = []
        
    model = YOLO('best.pt')

    classNames = ["frog"]
    filtro = 0
    def show_frame():
            
        global playback
        global audio
        global width
        global height
        global musicaPausada
        ret, img  =cap.read()
        if(img is not None):

            alturaImagem, larguraImagem = img.shape[:2]
            img, alturaImagem, larguraImagem = suporteImg.mudarTamImg(img, width, height-100, alturaImagem, larguraImagem)
            results = model(img, stream=True)
            for r in results:
                boxes = r.boxes
            
                aux = len(boxes)
                for box in boxes:
                    x1, y1, x2, y2 = box.xyxy[0]
                    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                    w, h = x2-x1, y2-y1
                    cvzone.cornerRect(img, (x1, y1, w, h))

                    conf = math.ceil((box.conf[0]*100))/100

                    cls = box.cls[0]
                    name = classNames[int(cls)]

                    cvzone.putTextRect(img, f'{name} 'f'{conf}', (max(0,x1), max(35,y1)), scale = 2)
                    
        
            global image_id
        
            if ret:
                photo = suporteImg.converteImagem(img)
            
                canvas.photo = photo
                if image_id:       
                    canvas.itemconfig(image_id, image=photo)
                    if(aux == 0 and musicaPausada == False):
                        mixer.music.pause()	
                        musicaPausada = True
                    else:
                        
                        if(musicaPausada == True and aux != 0):
                            musicaPausada = FALSE                        
                            mixer.music.unpause()
                else:
                    image_id = canvas.create_image((0,0), image=photo, anchor='nw')
                    canvas.configure(width=photo.width(), height=photo.height())
                
            root.after(20,show_frame)
        else:
            mixer.music.stop()
            suporteImg.menuVoltar(root)   
             


    cap = cv2.VideoCapture(inserida)

    root = Tk()
    root.title("Detectar Sapos")
  
    global width
    global height
    root.state('zoomed')
    width= root.winfo_screenwidth()               
    height= root.winfo_screenheight()   
    can = Canvas(root, bg = '#37353e', width=width, height=height)
    can.place(relx=0,rely=0, anchor=NW)
    canvas = Canvas(root)
    canvas.place(relx=0, rely=0, anchor=NW)
    canvas.place(relx=0.5, rely=0.5, anchor=CENTER)
    global musicaPausada
    musicaPausada = False
 
    mixer.init()
  
    mixer.music.load('frogs.mp3')


    mixer.music.set_volume(0.2)

    mixer.music.play(-1)
    menu = Menu(root)
    item1 = Menu(menu)
    item1.add_command(label="Inserir novo video", command=inserirFoto)
    item1.add_command(label="Voltar ao Menu", command=lambda : suporteImg.menuVoltar(root))
    root.config(menu=menu)
    show_frame()
  
    root.mainloop()