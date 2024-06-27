# -- coding: utf-8 --
import tkinter as tk
from tkinter import filedialog, ttk
import urllib.request
import json
import re
#importar clase afd
from CLASES.Afd import Afd
from tkinter import messagebox

filenameAtencion=""
filenameCliente=""
dataAFD1={}
dataAFD2={}

def cargarTextAtencion():
    global filenameAtencion
    filenameAtencion = filedialog.askopenfilename(
        filetypes=[("Archivos de Texto", "*.txt")],
        title="Seleccione un archivo de texto"
    )
    if filenameAtencion:
        with open(filenameAtencion, mode='r', encoding="utf-8") as file:
            content = file.read()
            text_widget.delete(1.0, tk.END)  # Clear
            text_widget.insert(tk.END, content)
    else:
        text_widget.delete(1.0, tk.END)  # Clear
        print ("No seleccionaste nada")

def cargarTextCliente():
    global filenameCliente 
    filenameCliente = filedialog.askopenfilename(
        filetypes=[("Archivos de Texto", "*.txt")],
        title="Seleccione un archivo de texto"
    )
    if filenameCliente:
        with open(filenameCliente,  mode='r', encoding="utf-8") as file:
            content = file.read()
            text_widget2.delete(1.0, tk.END)  # Clear
            text_widget2.insert(tk.END, content)
    else:
        text_widget2.delete(1.0, tk.END)  # Clear
        print ("No seleccionaste nada")

root = tk.Tk()
root.title("NPL - DIEGO DUARTE") #titulo
root.geometry("1024x768") #dimension
root.iconbitmap("call_center_icon.ico") #icono
root.resizable(0,1) #no se puede cambiar el tamaño
root.config(bg="black") #color de fondo

eAtencion = tk.Label(root, text="ENTRADA - ATENCION AL CLIENTE:", font=("Arial", 12), bg="black", fg="white")
eAtencion.place(x=0, y=0)
# Crear un Text widget para mostrar contenido
text_widget = tk.Text(root, wrap="word", width=40, height=10)
#text_widget.pack(pady=10)
text_widget.place(x=0, y=22)

eCliente = tk.Label(root, text="ENTRADA - CLIENTE:", font=("Arial", 12), bg="black", fg="white")
eCliente.place(x=400, y=0)
# Crear un Text widget para mostrar contenido
text_widget2 = tk.Text(root, wrap="word", width=40, height=10)
#text_widget2.pack(pady=10)
text_widget2.place(x=400, y=22)

#boton para seleccionar archivo
botonAbrirAtencion = tk.Button(root, text="Seleccionar Texto\nde Atencion al Cliente", width=20, height=4, command=cargarTextAtencion)
#botonAbrirAtencion.pack(pady=10)
botonAbrirAtencion.place(x=0, y=200)
#boton para seleccionar archivo
botonAbrirCliente = tk.Button(root, text="Seleccionar Texto\ndel Cliente", width=20, height=4, command=cargarTextCliente)
#botonAbrirCliente.pack(pady=10)
botonAbrirCliente.place(x=400, y=200)


def principal():
    afd=Afd()
    afd.leerAFD()
    datos_AFD1=afd.dataAFD1
    datos_AFD2=afd.dataAFD2
    palabras=[]
    
    if filenameAtencion and filenameCliente:
        with open(filenameAtencion,  mode='r', encoding="utf-8") as file:
            contenido = file.read()
            #Eliminar signos de puntuacion con regex
            palabras = sacarPalabras(contenido)

            #por cada palabra vemos el AFD
            tNeutros, tSaludo, tDespedida, tIdentificacion, tCordialidad=simulacionAFD1(datos_AFD1,palabras)
            text_widgetAFD1.delete(1.0, tk.END)  # Clear
            text_widgetAFD1.insert(tk.END, "Neutros:\n"+";".join(tNeutros)+"\n\nSaludos:\n"+";".join(tSaludo)+"\n\nDespedidas:\n"+";".join(tDespedida)+"\n\nIdentificaciones:\n"+";".join(tIdentificacion)+"\n\nCordialidades:\n"+";".join(tCordialidad))
            comboNeutroA["values"]=tNeutros
            comboNeutroA.set('')
            comboAFD1.set('')
            puntajeFinalA.set(puntuarAtencion(tSaludo, tDespedida, tIdentificacion, tCordialidad))
        with open(filenameCliente,  mode='r', encoding="utf-8") as file:
            contenido = file.read()
            #Eliminar signos de puntuacion con regex
            palabras = sacarPalabras(contenido)

            #por cada palabra vemos el AFD
            tNeutros2, tBuenas, tMalas = simulacionAFD2(datos_AFD2,palabras)
            text_widgetAFD2.delete(1.0, tk.END)  # Clear
            text_widgetAFD2.insert(tk.END, "Neutros:\n"+";".join(tNeutros2)+"\n\nBuenas:\n"+";".join(tBuenas)+"\n\nMalas:\n"+";".join(tMalas))
            comboNeutroC["values"]=tNeutros2
            comboNeutroC.set('')
            comboAFD2.set('')
            puntajeFinalC.set(puntuarExpCliente(tBuenas, tMalas))
        
        puntajeGeneral.set((puntajeFinalA.get()+puntajeFinalC.get())/2)
    else:
        if not filenameAtencion:
            messagebox.showinfo(message="Debe seleccionar un archivo de texto de Entrada de Atencion al Cliente", title="Error de Entrada")
        if not filenameCliente:
            messagebox.showinfo(message="Debe seleccionar un archivo de texto de Entrada del Cliente", title="Error de Entrada")    

def puntuarAtencion(tSaludo, tDespedida, tIdentificacion, tCordialidad):
    puntaje=0
    if len(tSaludo)>0:
        puntaje=puntaje+1
    if len(tDespedida)>0:
        puntaje=puntaje+1
    if len(tIdentificacion)>0:
        puntaje=puntaje+1
    if len(tCordialidad)>0:
        if len(tCordialidad)>1:
            puntaje=puntaje+2
        else:
            puntaje=puntaje+1
    return puntaje

def puntuarExpCliente(tBuenas, tMalas):
    puntaje=len(tBuenas)*5/(len(tBuenas)+len(tMalas))
    
    return int(round(puntaje, 0))


#separar las palabras del texto, sin signos de puntuacion
def sacarPalabras(contenido):
    contenido = re.sub(r'[^\w\s]',' ',contenido)
    contenido = contenido.lower()
    tokens=contenido.split()
    return tokens

def simulacionAFD2(datos_AFD2, palabras):
    tNeutros, tBuenas, tMalas=[],[],[]
    estadoActual=datos_AFD2["estadoInicial"]
    agregar="" #palabra final a agregar, puede tener varias palabras
    for palabra in palabras:
        
        conjunto=estadoActual+"_"+palabra

        #si conjunto esta en las transiciones
        if conjunto in datos_AFD2["transiciones"]:
            if agregar=="":
                agregar=agregar+palabra
            else:
                agregar=agregar+" "+palabra

            estadoActual=datos_AFD2["transiciones"][conjunto]

            #si el estado actual es final
            if estadoActual in datos_AFD2["estadosFinales"]:
                print("Palabra aceptada: "+agregar)
                if estadoActual=="bueno":
                    tBuenas.append(agregar)
                elif estadoActual=="malo":
                    tMalas.append(agregar)
                agregar=""
                estadoActual="inicio"
        else:
            #no se encontró camino
            #no es final
            if agregar!="":
                print("Palabra no aceptada: "+agregar)
                if agregar not in tNeutros:
                    tNeutros.append(agregar)

            print("Palabra no aceptada: "+palabra)
            if palabra not in tNeutros:
                tNeutros.append(palabra)
            agregar=""
            estadoActual="inicio"
    return tNeutros, tBuenas, tMalas

def simulacionAFD1(datos_AFD1, palabras):
    tNeutros, tSaludo, tDespedida, tIdentificacion, tCordialidad=[],[],[],[],[]
    estadoActual=datos_AFD1["estadoInicial"]
    agregar="" #palabra final a agregar, puede tener varias palabras
    for palabra in palabras:
        
        conjunto=estadoActual+"_"+palabra.strip()
        print(conjunto)
        #si conjunto sin espacios esta en las transiciones
        if conjunto.strip() in datos_AFD1["transiciones"]:
            if agregar=="":
                agregar=agregar+palabra
            else:
                agregar=agregar+" "+palabra

            estadoActual=datos_AFD1["transiciones"][conjunto]
            print(estadoActual)
            #si el estado actual es final
            if estadoActual in datos_AFD1["estadosFinales"]:
                print("Palabra aceptada: "+agregar)
                if estadoActual=="saludo":
                    tSaludo.append(agregar)
                elif estadoActual=="despedida":
                    tDespedida.append(agregar)
                elif estadoActual=="identificacion":
                    tIdentificacion.append(agregar)
                elif estadoActual=="cordialidad":
                    tCordialidad.append(agregar)
                agregar=""
                estadoActual="inicio"
        else:
            #no se encontró camino
            #no es final
            if agregar!="":
                print("Palabra no aceptada: "+agregar)
                if agregar not in tNeutros:
                    tNeutros.append(agregar)
            print("Palabra no aceptada: "+palabra)
            if palabra not in tNeutros:
                tNeutros.append(palabra)
            agregar=""
            estadoActual="inicio"
    
    return tNeutros, tSaludo, tDespedida, tIdentificacion, tCordialidad





#boton para empezar
botonEmpezar = tk.Button(root, text="Empezar", width=20, height=4, command=principal)
botonEmpezar.place(x=800, y=200)

dAtencion = tk.Label(root, text="DETALLE - ATENCION AL CLIENTE:", font=("Arial", 12), bg="black", fg="white")
dAtencion.place(x=0, y=300)

text_widgetAFD1 = tk.Text(root, wrap="word", width=40, height=10)
text_widgetAFD1.place(x=0, y=322)

dCliente = tk.Label(root, text="DETALLE - CLIENTE:", font=("Arial", 12), bg="black", fg="white")
dCliente.place(x=400, y=300)

text_widgetAFD2 = tk.Text(root, wrap="word", width=40, height=10)
text_widgetAFD2.place(x=400, y=322)

comboNeutroA=ttk.Combobox(
    state="readonly")
comboNeutroA.place(x=0, y=500)

comboAFD1 = ttk.Combobox(
    state="readonly",
    values=["Saludo", "Despedida", "Identificacion", "Cordialidad"])
comboAFD1.place(x=150, y=500)

def agregarAFD1():
    afd=Afd()
    afd.leerAFD()
    datos_AFD1=afd.dataAFD1
    if comboNeutroA.get()!="" and comboAFD1.get()!="":
        datos_AFD1["alfabeto"].append(comboNeutroA.get())
        if not "inicio_"+comboNeutroA.get() in datos_AFD1["transiciones"]:
            if comboAFD1.get()=="Saludo":
                datos_AFD1["transiciones"]["inicio_"+comboNeutroA.get()]="saludo"
            elif comboAFD1.get()=="Despedida":
                datos_AFD1["transiciones"]["inicio_"+comboNeutroA.get()]="despedida"
            elif comboAFD1.get()=="Identificacion":
                datos_AFD1["transiciones"]["inicio_"+comboNeutroA.get()]="identificacion"
            elif comboAFD1.get()=="Cordialidad":
                datos_AFD1["transiciones"]["inicio_"+comboNeutroA.get()]="cordialidad"
        else:
            print("Ya existe")
        #todos los values de comboNeutroA["values"] menos el seleccionado
        comboNeutroA["values"]=list(filter(lambda x: x!=comboNeutroA.get(), comboNeutroA["values"]))
        comboNeutroA.set('')

        afd.dataAFD1=datos_AFD1
        afd.escribirAFD()
        
        comboAFD1.set('')
    else:
        messagebox.showinfo(message="Debe seleccionar una palabra y un tipo", title="No se puede agregar")

botonAgregarAFD1 = tk.Button(root, text="Agregar", width=10, height=1, command=agregarAFD1)
botonAgregarAFD1.place(x=0, y=530)


comboNeutroC=ttk.Combobox(
    state="readonly")
comboNeutroC.place(x=400, y=500)

comboAFD2 = ttk.Combobox(
    state="readonly",
    values=["Malo", "Bueno"])
comboAFD2.place(x=550, y=500)

def agregarAFD2():
    afd=Afd()
    afd.leerAFD()
    datos_AFD2=afd.dataAFD2
    if comboNeutroC.get()!="" and comboAFD2.get()!="":
        datos_AFD2["alfabeto"].append(comboNeutroC.get())
        if not "inicio_"+comboNeutroC.get() in datos_AFD2["transiciones"]:
            if comboAFD2.get()=="Malo":
                datos_AFD2["transiciones"]["inicio_"+comboNeutroC.get()]="malo"
            elif comboAFD2.get()=="Bueno":
                datos_AFD2["transiciones"]["inicio_"+comboNeutroC.get()]="bueno"
        else:
            messagebox.showinfo(message="Esa palabra ya tiene una transición", title="No se puede agregar")
            print("Ya existe")
        #todos los values de comboNeutroA["values"] menos el seleccionado
        comboNeutroC["values"]=list(filter(lambda x: x!=comboNeutroC.get(), comboNeutroC["values"]))
        comboNeutroC.set('')

        afd.dataAFD1=datos_AFD2
        afd.escribirAFD()
        
        comboAFD2.set('')
    else:
        messagebox.showinfo(message="Debe seleccionar una palabra y un tipo", title="No se puede agregar")

botonAgregarAFD2 = tk.Button(root, text="Agregar", width=10, height=1, command=agregarAFD2)
botonAgregarAFD2.place(x=400, y=530)

puntajeFinalA=tk.IntVar()
puntajeFinalA.set(0)

puntaje1 = tk.Label(root, text="Experiencia de Atencion: ", font=("Arial", 12), bg="black", fg="white")
puntaje1.place(x=0, y=600)

puntajeFinal1 = tk.Label(root, textvariable=puntajeFinalA, font=("Arial", 12), bg="black", fg="white")
puntajeFinal1.place(x=190, y=600)

puntajeFinalC=tk.IntVar()
puntajeFinalC.set(0)

puntaje2 = tk.Label(root, text="Experiencia del Cliente: ", font=("Arial", 12), bg="black", fg="white")
puntaje2.place(x=400, y=600)

puntajeFinal2 = tk.Label(root, textvariable=puntajeFinalC, font=("Arial", 12), bg="black", fg="white")
puntajeFinal2.place(x=590, y=600)

puntajeGeneral=tk.IntVar()
puntajeGeneral.set(0)

puntajeG = tk.Label(root, text="Puntaje General: ", font=("Arial", 12), bg="black", fg="white")
puntajeG.place(x=200, y=700)

puntajeFinalG = tk.Label(root, textvariable=puntajeGeneral, font=("Arial", 12), bg="black", fg="white")
puntajeFinalG.place(x=390, y=700)

root.mainloop()
