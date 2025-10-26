import cv2
import numpy as np
def filtrosDeCinza(img):
    cinzaImg = img[:,:,0]/3+ img[:,:,1]/3+img[:,:,2]/3
    cinzaImg = cinzaImg.astype('uint8')
    return cinzaImg
def filtroNegativo(img):
    negativoImg = cv2.bitwise_not(img)
    return negativoImg

def filtroOtsu(img):
    img = filtrosDeCinza(img)
    ret,th = cv2.threshold(img,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    return th

def suavizacaoMedia(img, val):
    k = int(val[0])
    media = cv2.blur(img,(k,k))
    return media


def suavizacaoMediana(img, val):
    k = int(val[0])
    for i in range(1, k, 2):
        blurImg = cv2.medianBlur(img, i)
    return blurImg

def detectorBordasCanny(img, val):
    edges = cv2.Canny(img, val[0], val[1])
    return edges

def filtroErosao(img, val):
    iteracoes = val[0]
    img = filtrosDeCinza(img)
    array = np.array([[255, 255, 255],
                   [255, 255, 255],
                   [255, 255, 255]], np.uint8)
    erosao = cv2.erode(img, array, iterations=iteracoes)
    return erosao

    
def filtroDilatacao(img, val):
    iteracoes = val[0]
    img = filtrosDeCinza(img)
    array = np.array([[255, 255, 255],
                   [255, 255, 255],
                   [255, 255, 255]], np.uint8)
    dilatacao  = cv2.dilate(img, array, iterations=iteracoes)
    return dilatacao
    
def abertura(img, val):
    it = val[0]
    img = filtrosDeCinza(img)

    opening = cv2.morphologyEx(img, cv2.MORPH_OPEN, np.ones((3, 11), np.uint8), iterations=it)
    return opening

def fechamento(img, val):
    it = val[0]
    img = filtrosDeCinza(img)
    closing =  cv2.morphologyEx(img, cv2.MORPH_CLOSE, np.ones((3, 11), np.uint8), iterations=it)
    return closing