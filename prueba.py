import win32ui

inicio=win32ui.MessageBox("Para reetiquetar las imagenes de acuerdo a la posición del item, utiliza las teclas: \n\n W: Frontal \n S: Trasera \n A: Izquierda \n D: Derecha", "Instrucciones Generales",1)
if inicio==2:
    exit()

consideraciones = win32ui.MessageBox("La carpeta debe contener archivos JPG ya etiquetados\n\nEl nombre de la carpeta no debe contener ( _ )\n\nUna ventana emergente mostrará la vista elegida, si desea cambiarla presione la opción Cancelar y escoja nuevamente entre W,A,S o D\n\nUna vez inciado el programa podrá salir hasta que se hayan reetiquetado todas las imagenes de la carpeta", "Consideraciones",1)
if consideraciones==2:
    exit()