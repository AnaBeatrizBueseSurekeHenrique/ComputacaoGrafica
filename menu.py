from tkinter import Button, Menu, Tk,Canvas, CENTER, NW, filedialog as fidia
import imagem
import camera
import videos
import videosDetect

def menu():    
    
    def inserirFoto():
        filename = fidia.askopenfilename(filetypes=[("Png Pictures", "*.png"),("Jpg Pictures", "*.jpg"), ("Jpeg Pictures", "*.jpeg")])
        if(filename):
            root.destroy()    
            imagem.imagem(filename)
    
    def iniciaVideo():
        filename = fidia.askopenfilename(filetypes=[("Videos", "*.mp4")])
        if(filename):
            root.destroy()     
            videos.videos(filename)
            
    def iniciaCamera():
        root.destroy()    
        camera.camera()
        
    def iniciaDeteccao():
        filename = fidia.askopenfilename(filetypes=[("Videos", "*.mp4")])
        if(filename):
            root.destroy()     
            videosDetect.videos(filename)
            
    root = Tk()
    root.state('zoomed')            
    root.title("Menu")
    root.geometry()
    
    width= root.winfo_screenwidth()               
    height= root.winfo_screenheight()   
    
    canBg = Canvas(root, bg='#37353e', height=height, width=width)
    canBg.place(relx=0, rely=0, anchor=NW)
    
    can = Canvas(root, bg = '#44444E', height=int(height/2.5), width=int(width/2))
    can.place(relx=0.5, rely=0.5, anchor=CENTER)


    btnFoto = Button(root, text = "Inserir foto" ,fg = "black", command=inserirFoto, width=100, height=3, activebackground="#d3dad9")
    btnFoto.place(relx=0.5, rely=0.35, anchor=CENTER)
    
    btnCamera = Button(root, text = "Abrir Camera" , fg = "black", command=iniciaCamera, width=100, height=3, activebackground="#d3dad9")
    btnCamera.place(relx=0.5, rely=0.45, anchor=CENTER)
    
    btnVideo = Button(root, text = "Ver Video" , fg = "black", command=iniciaVideo, width=100, height=3, activebackground="#d3dad9")
    btnVideo.place(relx=0.5, rely=0.55, anchor=CENTER)
    
    btnDetectar = Button(root, text = "Detectar sapos" , fg = "black", command=iniciaDeteccao, width=100, height=3, activebackground="#d3dad9")
    btnDetectar.place(relx=0.5, rely=0.65, anchor=CENTER)

    root.mainloop()
    