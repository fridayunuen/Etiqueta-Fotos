import os
from tkinter import Tk, filedialog
from numpy import repeat
import cv2
from win32con import (SW_SHOW, SW_RESTORE)
import win32gui
import win32ui
#
inicio=win32ui.MessageBox("Para reetiquetar las imagenes de acuerdo a la posición del item, utiliza las teclas: \n\n W: Frontal \n S: Trasera \n A: Izquierda \n D: Derecha", "Instrucciones Generales",1)
if inicio==2:
    exit()

consideraciones = win32ui.MessageBox("La carpeta debe contener archivos JPG ya etiquetados\n\nEl nombre de la carpeta no debe contener ( _ )\n\nUna ventana emergente mostrará la vista elegida, si desea cambiarla presione la opción Cancelar y escoja nuevamente entre W,A,S o D\n\nUna vez inciado el programa podrá salir hasta que se hayan reetiquetado todas las imagenes de la carpeta", "Consideraciones",1)
if consideraciones==2:
    exit()
#
root = Tk() 
root.withdraw() 
root.attributes('-topmost', True) 
carpeta = filedialog.askdirectory()
#
base_name_carpeta = os.path.basename(carpeta)
if "_" in base_name_carpeta:
    d=win32ui.MessageBox("El nombre de la carpeta contiene ( _ ) desea cambiarlo? ", "Error", 1) #1 Aceptar 2 Cancelar
    if d==1:
        os.rename(carpeta, carpeta.replace("_", ""))
        carpeta=carpeta.replace("_", "")
    elif d==2:
        exit()
#
os.chdir(carpeta) 
files = os.listdir()
if len(files) == 0:
    win32ui.MessageBox("La carpeta esta vacia", "Error",0)
    exit()
if not all(file.endswith('.jpg') for file in files):
    win32ui.MessageBox("La carpeta solo debe de contener archivos JPG", "Error",0)
    exit()       
#
paths = [os.path.join(carpeta, file) for file in files]
principales = [path for path in paths if "515Wx515" in path]
#
def get_subset(string, start, end):
    return string[start:end]    

def detect_char(string, char):
    return [i for i, letter in enumerate(string) if letter == char]  

def get_windows_placement(window_id):
    return win32gui.GetWindowPlacement(window_id)[1]

def set_active_window(window_id):
    if get_windows_placement(window_id) == 2:
        win32gui.ShowWindow(window_id, SW_RESTORE)
    else:
        win32gui.ShowWindow(window_id, SW_SHOW)
    win32gui.SetForegroundWindow(window_id)
    win32gui.SetActiveWindow(window_id)
#
def seleccion(imagen): 
    img = cv2.imread(imagen)
    cv2.imshow('Imagen',img) 
    cv2.setWindowProperty('Imagen', cv2.WND_PROP_TOPMOST, 1)
    window_id = win32gui.GetActiveWindow()
    set_active_window(window_id)
    tecla=cv2.waitKey(0) 
    
    while tecla != ord('a') and tecla != ord('d') and tecla != ord('w') and tecla != ord('s'):
        win32ui.MessageBox("Recuerda que para etiquetar las fotos debes de presionar las teclas \t W A S D", "Cuidado", 0)
        img = cv2.imread(imagen)
        cv2.imshow('Imagen',img) 
        cv2.setWindowProperty('Imagen', cv2.WND_PROP_TOPMOST, 1)
        window_id = win32gui.GetActiveWindow()
        set_active_window(window_id)
        tecla=cv2.waitKey(0) 
        cv2.destroyAllWindows() 

    if tecla == ord('a'):
        new_label="_Izquierda-new_"
    elif tecla == ord('d'):
        new_label="_Derecha-new_" 
    elif tecla == ord('w'):
        new_label="_Frontal-new_"
    elif tecla == ord('s'):
        new_label="_Trasera-new_"
    
    return new_label    
 #
for i in range(len(principales)):
    imagen = principales[i]
    new_label=seleccion(imagen)
    continuar = win32ui.MessageBox(new_label, "Seleccion", 1) #?

    while continuar == 2:
        new_label=seleccion(imagen)
        continuar = win32ui.MessageBox(new_label, "Seleccion", 1)

    cv2.destroyAllWindows() 
      
    tipo=get_subset( imagen, detect_char(imagen, '_')[0], detect_char(imagen, '_')[1]+1) #_Derecha_
    sku =get_subset( imagen, detect_char(imagen, '_')[1]+1, detect_char(imagen, '_')[2]) #1700490094
    no_vista=get_subset(imagen, detect_char(imagen, '_')[2], detect_char(imagen, '_')[2]+3) #_1.

    item = [path for path in paths if sku in path] 
    vista=[item for item in item if tipo in item] 

    item_vista=[vista for vista in vista if no_vista in vista] 
    
    for j in range(len(item_vista)) :
        imagen2 = item_vista[j]
        if not os.path.exists(imagen2.replace(tipo, new_label)):
            os.rename(imagen2, imagen2.replace(tipo, new_label))
        else:
            if not os.path.exists(imagen2.replace(no_vista, "_1.")):
                os.rename(imagen2, imagen2.replace(no_vista, "_1."))
            else:
                if not os.path.exists(imagen2.replace(no_vista, "_2.")):
                    os.rename(imagen2, imagen2.replace(no_vista, "_2.")) 
                else:
                    print("Ya existe")
                    
files=os.listdir()
for i in range(len(files)):
    if '-' not in files[i]:
        base_name=carpeta[:-len(os.path.basename(carpeta))]
        if not os.path.exists(base_name+"Repeticiones"):
            os.mkdir(base_name+"Repeticiones")
        os.rename(files[i], base_name+"Repeticiones/"+files[i])
files= os.listdir()
for i in range(len(files)):
    os.rename(files[i],files[i].replace('-new', ''))

del  carpeta, files, paths, principales, imagen, new_label
