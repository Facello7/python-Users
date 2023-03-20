from tkinter import *
import sqlite3
from tkinter import messagebox
from tkinter import filedialog
import pickle
raiz= Tk()
raiz.title("Manejo de info usuarios")



#------------------------------DEFINICIONES-----ZZZ---------
varId=StringVar()
varNombre=StringVar()
varApellido=StringVar()
varDireccion=StringVar()
varContraseña=StringVar()
compId=0
#--------------------------------FUNCIONES------------------

def crearTabla():
	miConexion=sqlite3.connect("Usuarios")
	miCursor=miConexion.cursor()

	try:
		miCursor.execute("CREATE TABLE DATOSUSUARIOS(ID INTEGER PRIMARY KEY AUTOINCREMENT, NOMBRE_USUARIO VARCHAR(50), APELLIDO VARCHAR(50), PASSWORD VARCHAR(50), DIRECCION VARCHAR(50), COMENTARIOS VARCHAR(500))")
		messagebox.showinfo("BBDD", "BBDD creada con exito")
	except:
		messagebox.showerror("BBDD", "La base de datos ya existe")
def salir():
	valor=messagebox.askokcancel("Salir", "Desea salir de la aplicacion?")

	if valor==True:
		raiz.destroy()

def borrarTodo():
	varId.set("")
	varNombre.set("")
	varApellido.set("")
	varDireccion.set("")
	varContraseña.set("")
	cuadroComentario.delete(1.0, END)


def añadir():
	miConexion=sqlite3.connect("Usuarios")
	miCursor=miConexion.cursor()
	datos=varNombre.get(),varApellido.get(),varDireccion.get(),varContraseña.get(),cuadroComentario.get(1.0, END)
	try:
		miCursor.execute("INSERT INTO DATOSUSUARIOS VALUES(NULL,?,?,?,?,?)",(datos))
		miConexion.commit()
		messagebox.showinfo("BBDD", "Registro guardado con exito")
	except:
		messagebox.showerror("BBDD", "La base de datos no existe")

def buscar():
	miConexion=sqlite3.connect("Usuarios")
	miCursor=miConexion.cursor()
	miCursor.execute("SELECT * FROM DATOSUSUARIOS WHERE ID=" + varId.get())
	usuario=miCursor.fetchall()
	for dato in usuario:
		varNombre.set(dato[1]), varApellido.set(dato[2]), varDireccion.set(dato[3]), varContraseña.set(dato[4]), cuadroComentario.insert(1.0,dato[5])
	miConexion.commit()

def actualizar():
	nuevoApellido=varApellido.get()
	miConexion=sqlite3.connect("Usuarios")
	miCursor=miConexion.cursor()
	
	datos=varNombre.get(),varApellido.get(),varDireccion.get(),varContraseña.get(),cuadroComentario.get(1.0, END)
	miCursor.execute("UPDATE DATOSUSUARIOS SET NOMBRE_USUARIO=?, APELLIDO=?, DIRECCION=?, PASSWORD=?,COMENTARIOS=?"+
		"WHERE ID="+ varId.get(),(datos))

	miConexion.commit()
	messagebox.showinfo("BBDD", "Registro actualizado con exito")

def delete():
	miConexion=sqlite3.connect("Usuarios")
	miCursor=miConexion.cursor()
	miCursor.execute("DELETE FROM DATOSUSUARIOS WHERE ID="+ varId.get())
	miConexion.commit()
	messagebox.showinfo("BBDD", "Usuario borrado con exito")

#--------------------------MENU DE LA INTERFAZ--------------
barraMenu=Menu(raiz)

bbdd=Menu(barraMenu, tearoff=0)
bbdd.add_command(label="Conectar", command=crearTabla)
bbdd.add_command(label="Salir", command=salir)

borrar=Menu(barraMenu, tearoff=0)
borrar.add_command(label="Borrar", command=borrarTodo)

crud=Menu(barraMenu, tearoff=0)
crud.add_command(label="Crear", command=añadir)
crud.add_command(label="Leer", command=buscar)
crud.add_command(label="Actualizar", command=actualizar)
crud.add_command(label="Eliminar", command=delete)

ayuda=Menu(barraMenu, tearoff=0)
ayuda.add_command(label="Licencia")
ayuda.add_command(label="Acerca de...")

raiz.config(menu=barraMenu, width=300, height=300)
barraMenu.add_cascade(label="BBDD", menu=bbdd)
barraMenu.add_cascade(label="Borrar", menu=borrar)
barraMenu.add_cascade(label="CRUD", menu=crud)
barraMenu.add_cascade(label="Ayuda", menu=ayuda)
#-----------------------------------------------------------

#-------------------------CAMPOS DE DATOS-------------------
frameDatos=Frame(raiz, width=300, height=500)
frameDatos.pack()

textoId=Label(frameDatos, text="ID:")
textoId.grid(row=0, column=0, padx=10, pady=10)

cuadroId=Entry(frameDatos, textvariable=varId)
cuadroId.grid(row=0, column=1, padx=10, pady=10)

textoNombre=Label(frameDatos, text="Nombre:")
textoNombre.grid(row=1, column=0, padx=10, pady=10)

cuadroNombre=Entry(frameDatos, textvariable=varNombre)
cuadroNombre.grid(row=1, column=1, padx=10, pady=10)

textoApellido=Label(frameDatos, text="Apellido:")
textoApellido.grid(row=2, column=0, padx=10, pady=10)

cuadroApellido=Entry(frameDatos, textvariable=varApellido)
cuadroApellido.grid(row=2, column=1, padx=10, pady=10)

textoDireccion=Label(frameDatos, text="Direccion:")
textoDireccion.grid(row=3, column=0, padx=10, pady=10)

cuadroDireccion=Entry(frameDatos, textvariable=varDireccion)
cuadroDireccion.grid(row=3, column=1, padx=10, pady=10)

textoContraseña=Label(frameDatos, text="Contraseña:")
textoContraseña.grid(row=4, column=0, padx=10, pady=10)

cuadroContraseña=Entry(frameDatos, textvariable=varContraseña)
cuadroContraseña.grid(row=4, column=1, padx=10, pady=10)
cuadroContraseña.config(show="*")

textoComentario=Label(frameDatos, text="Comentarios:")
textoComentario.grid(row=5, column=0, padx=10, pady=10)

cuadroComentario=Text(frameDatos, width=16, height=5)
cuadroComentario.grid(row=5, column=1, padx=10, pady=10)


scrollVert=Scrollbar(frameDatos, command=cuadroComentario.yview)
scrollVert.grid(row=5, column=2, sticky="nsew")

cuadroComentario.config(yscrollcommand=scrollVert.set)
#-----------------------------------------------------------

#-------------------------BOTONES DE CRUD-------------------
frameBotones=Frame(raiz, width=300, height=100)
frameBotones.pack()

botonCreate=Button(frameBotones, text="Create", command=añadir)
botonRead=Button(frameBotones, text="Read", command=buscar)
botonUpdate=Button(frameBotones, text="Update", command=actualizar)
botonDelete=Button(frameBotones, text="Delete", command=delete)
botonCreate.grid(row=0, column=0, padx=10, pady=10)
botonRead.grid(row=0, column=1, padx=10, pady=10)
botonUpdate.grid(row=0, column=2, padx=10, pady=10)
botonDelete.grid(row=0, column=3, padx=10, pady=10)
#-----------------------------------------------------------

raiz.mainloop()