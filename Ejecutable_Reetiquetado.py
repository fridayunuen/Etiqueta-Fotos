import os
from tkinter import Tk, filedialog
from numpy import repeat
import cv2
from win32con import (SW_SHOW, SW_RESTORE)
import win32gui
import win32ui
import shutil
import zipfile
import datetime

root = Tk() # pointing root to Tk() to use it as Tk() in program.
root.withdraw() # Hides small tkinter window.
root.attributes('-topmost', True) # Opened windows will be active. above all windows despite of selection.
carpeta = filedialog.askdirectory() # Returns opened path as str

# get base name of carpeta
base_name_carpeta = os.path.basename(carpeta)

#base_name_carpeta contains "_"
if "_" in base_name_carpeta:
    d=win32ui.MessageBox("El nombre de la carpeta contiene ( _ ) desea cambiarlo? ", "Error", 1) #1 Aceptar 2 Cancelar
    if d==1:
        #rename carpeta path
        os.rename(carpeta, carpeta.replace("_", ""))
        carpeta=carpeta.replace("_", "")
        #base_name_carpeta = base_name_carpeta.replace("_", "")
    elif d==2:
        exit()
    

os.chdir(carpeta) # Changes directory to opened path.
files = os.listdir()

# if the folder is empty, the program will exit
if len(files) == 0:
    win32ui.MessageBox("La carpeta esta vacia", "Error",0)
    exit()

if not all(file.endswith('.jpg') for file in files):
    win32ui.MessageBox("La carpeta solo debe de contener archivos JPG", "Error",0)
    exit()    

# get path of all files
paths = [os.path.join(carpeta, file) for file in files]

# this function ditects a string inside a string
def detect_string(string, substring):
    return substring in string

error_paths = [path for path in paths if detect_string(path, "Error")]    

# if error_paths is not empty, the program will exit
if len(error_paths) == 0:
    win32ui.MessageBox("La carpeta no contiene archivos con error :)", "Mensaje",0)
    exit()

inicio=win32ui.MessageBox("Para reetiquetar las imagenes de acuerdo a la posición del item, utiliza las teclas: \n\n W: Frontal \n S: Trasera \n A: Izquierda \n D: Derecha", "Instrucciones Generales",1)
if inicio==2:
    exit()

consideraciones = win32ui.MessageBox("Asegurate de tener acceso a la carpeta compartida en donde se guardarán los cambios realizados\n\nLa carpeta debe contener archivos JPG ya etiquetados\n\nEl nombre de la carpeta no debe contener ( _ )\n\nUna ventana emergente mostrará la vista elegida, si desea cambiarla presione la opción Cancelar y escoja nuevamente entre W,A,S o D\n\nUna vez inciado el programa podrá salir hasta que se hayan reetiquetado todas las imagenes de la carpeta", "Consideraciones",1)
if consideraciones==2:
    exit()

#Functions --------------------------------------------------------------------------------------------------
# this function is used to create a subset from a string
def get_subset(string, start, end):
    return string[start:end]    

# this function detects the position of a  character in a string
def detect_char(string, char):
    return [i for i, letter in enumerate(string) if letter == char]  

# With these functions we can activate the window and bring it to the front.
def get_windows_placement(window_id):
    return win32gui.GetWindowPlacement(window_id)[1]

def set_active_window(window_id):
    if get_windows_placement(window_id) == 2:
        win32gui.ShowWindow(window_id, SW_RESTORE)
    else:
        win32gui.ShowWindow(window_id, SW_SHOW)
    win32gui.SetForegroundWindow(window_id)
    win32gui.SetActiveWindow(window_id)

# now we use the previous function to get all '_'
error_paths_positions = [detect_char(path, '_') for path in error_paths]
#select the first position of each path
error_paths_positions_1 = [path[1] for path in error_paths_positions]
error_paths_positions_1 = [int(path) + 1 for path in error_paths_positions_1]

error_paths_positions_2 = [path[2] for path in error_paths_positions]

# get the subset of the paths
error_paths_subset = [get_subset(path, error_paths_positions_1[i], error_paths_positions_2[i]) for i, path in enumerate(error_paths)]

# unique values of error_paths_subset
skue = list(set(error_paths_subset))

productos_error = []
for path in paths:
    for j in range(len(skue)):
        if detect_string(path, skue[j]):
            # save the path in the new variable
            productos_error.append(path)
            
carpeta = os.getcwd()

# if not exists the folder 'error', the program will create it
if not os.path.exists(carpeta + '\\Errores'):
    os.mkdir("Errores")

for path in productos_error:
    name = os.path.basename(path)
    os.rename(path, carpeta+"/Errores/" + name) 

# files in the folder 'error'
error_files = os.listdir(carpeta + '\\Errores')
# change directory to 'error'
os.chdir(carpeta + '\\Errores')

# get all paths in directory
files = os.listdir()
# get all paths of files
paths = [os.path.join(carpeta + '\\Errores', file) for file in files]

error_paths = [path for path in paths if detect_string(path, "_Error_")]  

no_error_paths = [path for path in paths if not detect_string(path, "_Error_")]  

for i in range(len(no_error_paths)):
    imagen = no_error_paths[i]
    tipo = (get_subset(imagen, detect_char(imagen, '_')[0]+1, detect_char(imagen, '_')[1]+1) )
    
    tipo2 = tipo.replace("_", "-new_")
    os.rename(imagen, imagen.replace(tipo, tipo2))
        
principales = [error_paths for error_paths in error_paths if "515Wx515" in error_paths]

def seleccion(imagen): 
    img = cv2.imread(imagen)
    cv2.imshow('Imagen',img) #
    cv2.setWindowProperty('Imagen', cv2.WND_PROP_TOPMOST, 1)
    window_id = win32gui.GetActiveWindow()#
    set_active_window(window_id)#
    #detecting which key is pressed 
    tecla=cv2.waitKey(0) # waits until a key is pressed
    
    # Pressing only keys predefined
    while tecla != ord('a') and tecla != ord('d') and tecla != ord('w') and tecla != ord('s'):
        win32ui.MessageBox("Recuerda que para etiquetar las fotos debes de presionar las teclas \t W A S D", "Cuidado", 0)
        img = cv2.imread(imagen)
        cv2.imshow('Imagen',img) #
        cv2.setWindowProperty('Imagen', cv2.WND_PROP_TOPMOST, 1)
        window_id = win32gui.GetActiveWindow()#
        set_active_window(window_id)#
        tecla=cv2.waitKey(0) 
        cv2.destroyAllWindows() 

    # Conditional statement to detect which key is pressed
    if tecla == ord('a'):
        new_label="_Izquierda-new_"
    elif tecla == ord('d'):
        new_label="_Derecha-new_" 
    elif tecla == ord('w'):
        new_label="_Frontal-new_"
    elif tecla == ord('s'):
        new_label="_Trasera-new_"
    
    return new_label
for i in range(len(principales)):
    imagen = principales[i]

    new_label=seleccion(imagen)
    
    #Now, if the user wants to change his/her selection, he/ she can select the option "Cancel"
    continuar = win32ui.MessageBox(new_label, "Seleccion", 1) #?

    while continuar == 2:
        new_label=seleccion(imagen)
        continuar = win32ui.MessageBox(new_label, "Seleccion", 1)

    cv2.destroyAllWindows() # destroys the window showing image  
      
    # Elements of the path 
    tipo=get_subset( imagen, detect_char(imagen, '_')[0], detect_char(imagen, '_')[1]+1) #_Derecha_
    sku =get_subset( imagen, detect_char(imagen, '_')[1]+1, detect_char(imagen, '_')[2]) #1700490094
    no_vista=get_subset(imagen, detect_char(imagen, '_')[2], detect_char(imagen, '_')[2]+3) #_1.

    item = [path for path in paths if sku in path] 
    vista=[item for item in item if tipo in item] 

    # Selecting all paths with sku in them and with determinated vista
    item_vista=[vista for vista in vista if no_vista in vista] 
    
    # if imagen2.replace(tipo, new_label) does not exist, rename imagen2 to imagen2.replace(tipo, new_label)
    for j in range(len(item_vista)) :
        imagen2 = item_vista[j]
        
        if not os.path.exists(imagen2.replace(tipo, new_label)):
            os.rename(imagen2, imagen2.replace(tipo, new_label))
            
            
        else:
            if not os.path.exists(imagen2.replace(no_vista, "_1.")):
                imagen3 = imagen2.replace(no_vista, "_1.")
                imagen3 = imagen3.replace(tipo, new_label)
                os.rename(imagen2, imagen3)
                
            else:
                if not os.path.exists(imagen2.replace(no_vista, "_2.")):
                    imagen3 = imagen2.replace(no_vista, "_2.")
                    imagen3 = imagen3.replace(tipo, new_label)
                    os.rename(imagen2, imagen3)

ec = "S:\TOM CARGAS MASIVAS\ErroresCorregidos"
if not os.path.exists(ec):
    os.mkdir(ec)

files=os.listdir()
for i in range(len(files)):
    if '-' not in files[i]:
        #base_name=carpeta[:-len(os.path.basename(carpeta))]
        if not os.path.exists(ec+"/Repeticiones"):
            os.mkdir(ec+"/Repeticiones")
        os.rename(files[i], ec+"/Repeticiones/"+files[i])
        
        
files= os.listdir()
for i in range(len(files)):
    os.rename(files[i],files[i].replace('-new', ''))

# if there exists a folder called "Repeticiones" show a message
if os.path.exists(base_name_carpeta+"Repeticiones"):
    win32ui.MessageBox("Existen Archivos con mas de 2 vistas, revisar carpeta repeticiones", "Error", 0)

files= os.listdir()
files
error_files
import pandas as pd
# create a table with files and error files as columns
table = pd.DataFrame(columns=['Files', 'Error Files'])
table['Files'] = files
table['Error Files'] = error_files


# if table has same value in both columns and in the same row, delete that row
table = table.drop_duplicates(subset=['Files', 'Error Files'], keep='first')


day = datetime.datetime.now().strftime("%d-%m-%Y")  
hour = datetime.datetime.now().strftime("%H-%M-%S")

if not os.path.exists(ec+"\\Transformaciones("+day+"_"+hour+").csv"):    
    table.to_csv(ec+"\\Transformaciones("+day+"_"+hour+").csv", index=False)

# get all paths in directory
files = os.listdir()
# get all paths of files    
paths = [os.path.join(carpeta + '\\Errores', file) for file in files]


# move all files to carpeta
for i in range(len(paths)):
    os.rename(paths[i], carpeta + "\\" + files[i])

os.chdir(carpeta)

# if Errores folder empty, delete it
if os.listdir(carpeta + "\\Errores") == []:    
    os.rmdir(carpeta + "\\Errores")
else:
    win32ui.MessageBox("Hubo un error, revisar carpeta", "Error", 0)

del  carpeta, files, paths, principales, imagen, new_label        