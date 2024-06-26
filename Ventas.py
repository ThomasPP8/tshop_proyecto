from tkinter import *
from tkinter import ttk, messagebox
import ttkbootstrap as tb #Acceder estilos de bootstrap

import sqlite3

class Ventana(tb.Window): #Aqui cambia el "TK" por "tb.Window"
    def __init__(self):
        super().__init__()
        self.ventana_login()

    #VENTANA Log in
    def ventana_login(self):
        self.frame_login=Frame(self)
        self.frame_login.pack()

        self.lblframe__login=LabelFrame(self.frame_login, text='Acceso') #Panel e input Acceso
        self.lblframe__login.pack(padx=10,pady=10)

        lbltitulo=Label(self.lblframe__login,text='inicio de sesion', font=('Arial',18)) #Etiqueta titulo
        lbltitulo.pack(padx=10,pady=35)

        txt_usuario=ttk.Entry(self.lblframe__login, width=40, justify=CENTER) #Entry para campo de texto
        txt_usuario.pack(padx=10,pady=10)
        txt_clave=ttk.Entry(self.lblframe__login,width=40, justify=CENTER)
        txt_clave.pack(padx=10,pady=10)
        txt_clave.configure(show='*') #Censurar clave
        btn_acceso=ttk.Button(self.lblframe__login,text='Log in',command=self.logueo)
        btn_acceso.pack(padx=10,pady=10)
    #VENTANA Menu
    def ventana_menu(self):
        self.frame_left=Frame(self,width=200)
        self.frame_left.grid(row=0,column=0,sticky=NSEW)
        self.frame_center=Frame(self)
        self.frame_center.grid(row=0,column=1,sticky=NSEW)
        self.frame_right=Frame(self,width=400)
        self.frame_right.grid(row=0,column=2,sticky=NSEW)

        btn_productos=ttk.Button(self.frame_left,text='Productos',width=15)
        btn_productos.grid(row=0,column=0,padx=10,pady=10)
        btn_ventas=ttk.Button(self.frame_left,text='Ventas',width=15)
        btn_ventas.grid(row=1,column=0,padx=10,pady=10)
        btn_clientes=ttk.Button(self.frame_left,text='Clientes',width=15)
        btn_clientes.grid(row=2,column=0,padx=10,pady=10)
        btn_compras=ttk.Button(self.frame_left,text='Compras',width=15)
        btn_compras.grid(row=3,column=0,padx=10,pady=10)
        btn_usuarios=ttk.Button(self.frame_left,text='Usuarios',width=15,command=self.ventana_lista_usuarios)
        btn_usuarios.grid(row=4,column=0,padx=10,pady=10)
        btn_reportes=ttk.Button(self.frame_left,text='Reportes',width=15)
        btn_reportes.grid(row=5,column=0,padx=10,pady=10)
        btn_backup=ttk.Button(self.frame_left,text='Backup',width=15)
        btn_backup.grid(row=6,column=0,padx=10,pady=10)
        btn_restaurabd=ttk.Button(self.frame_left,text='Restaurar BD',width=15)
        btn_restaurabd.grid(row=7,column=0,padx=10,pady=10)


        lbl2=Label(self.frame_center,text='Aqui Pondremos las ventanas que creemos')
        lbl2.grid(row=0,column=0,padx=10,pady=10)

        lbl3=Label(self.frame_right,text='Aqui Pondremos las busquedas para la ventana')
        lbl3.grid(row=0,column=0,padx=10,pady=10)

    def logueo(self):
        self.frame_login.pack_forget()#Ocultar la ventana de Login
        self.ventana_menu()#abrir ventana de menu

    def ventana_lista_usuarios(self):
        self.frame_lista_usuarios=Frame(self.frame_center)
        self.frame_lista_usuarios.grid(row=0,column=0,columnspan=2,sticky=NSEW)

        self.lblframe_botones_listusu=LabelFrame(self.frame_lista_usuarios)
        self.lblframe_botones_listusu.grid(row=0,column=0,padx=10,pady=10,sticky=NSEW)

        btn_nuevo_usuario=tb.Button(self.lblframe_botones_listusu,text='Nuevo',width=15,bootstyle="success")
        btn_nuevo_usuario.grid(row=0,column=0,padx=5,pady=5)
        btn_modificar_usuario=tb.Button(self.lblframe_botones_listusu,text='Modificar',width=15,bootstyle="warning")
        btn_modificar_usuario.grid(row=0,column=1,padx=5,pady=5)
        btn_eliminar_usuario=tb.Button(self.lblframe_botones_listusu,text='Eliminar',width=15,bootstyle="danger")
        btn_eliminar_usuario.grid(row=0,column=2,padx=5,pady=5)

        self.lblframe_busqueda_listusu=LabelFrame(self.frame_lista_usuarios)
        self.lblframe_busqueda_listusu.grid(row=1,column=0,padx=10,pady=10,sticky=NSEW)

        txt_busqueda_usuarios=ttk.Entry(self.lblframe_busqueda_listusu,width=90)
        txt_busqueda_usuarios.grid(row=0,column=0,padx=5,pady=5)

        #====================Treeview=====================================

        self.lblframe_tree_listusu=LabelFrame(self.frame_lista_usuarios)
        self.lblframe_tree_listusu.grid(row=2,column=0,padx=10,pady=10,sticky=NSEW)
        
        columnas=("codigo","nombre","clave","rol")

        self.tree_lista_usuarios=tb.Treeview(self.lblframe_tree_listusu,columns=columnas,
                                        height=17,show='headings',bootstyle='dark')
        self.tree_lista_usuarios.grid(row=0,column=0)

        self.tree_lista_usuarios.heading("codigo",text="Codigo",anchor=W)
        self.tree_lista_usuarios.heading("nombre",text="Nombre",anchor=W)
        self.tree_lista_usuarios.heading("clave",text="Clave",anchor=W)
        self.tree_lista_usuarios.heading("rol",text="Rol",anchor=W)
        self.tree_lista_usuarios['displaycolumns']=("codigo","nombre","rol") #Ocultar columna clave

        #Crear Scrolbar
        tree_scroll_listausu=tb.Scrollbar(self.frame_lista_usuarios,bootstyle='round-success')
        tree_scroll_listausu.grid(row=2,column=1)
        #configurar scrolbar
        tree_scroll_listausu.config(command=self.tree_lista_usuarios.yview)

        #Llamamos a nuestra funcion mostrar usuarios
        self.mostrar_usuarios()

    def mostrar_usuarios(self):
        #Capturador errores
        try:
            #Establecer la conexion
            miConexion=sqlite3.connect('Ventas.db')
            #Crear Cursor
            miCursor=miConexion.cursor()
            #Limpiamos nuetro treeview
            registros=self.tree_lista_usuarios.get_children()
            #Recorremos cada registro
            for elementos in registros:
                self.tree_lista_usuarios.delete(elementos)
            #Consultar nuetra base de datos
            miCursor.execute("SELECT * FROM Usuarios")
            #con esto traemos todos los registros y lo guardamos en "datos"
            datos=miCursor.fetchall()
            #Recorremos cada fila encontrada
            for row in datos:
                self.tree_lista_usuarios.insert("",0,text=row[0],values=(row[0],row[1],row[2],row[3]))
            #Aplicamos Cambios
            miConexion.commit()
            #Cerramos la conexion
            miConexion.close()

        except:
            #Mensaje error
            messagebox.showerror("Lista de Usuario","Ocurrio un error al mostrar las listas de usuario")




def main():
    app=Ventana()
    app.title('Sistema de ventas') #Titulo de la ventana
    app.state('zoomed') #zoomed inicia la ventana maximizada
    tb.Style('superhero') #Themes: solar, superhero, darkly, cyborg, vapor - https://ttkbootstrap.readthedocs.io/en/latest/themes/dark/
    app.mainloop()

if __name__=='__main__':
        main()