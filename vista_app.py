##########################################
####### Integrantes del Grupo:     #######
####### *  Motroni Bruno           #######
####### *  Agustino Juan Sebastian #######
##########################################


from tkinter import Label, StringVar, Entry, ttk, Button, messagebox
from modelo_app import Auxiliares
from modelo_app import InteraccionBd

# Se realiza la importacion desde tkinter solo de lo que voy a utilizar del mismo.
# Importo de modelo_app la clase Auxiliares y InteraccionBd con el fin de utilizar sus metodos.


class VistaTotal:
    def __init__(self, root, tree=None):
        self.root = root
        self.tree = tree
        self.objeto = InteraccionBd(root)
        self.objeto2 = Auxiliares(tree)

    # Ventana es un metodo el cual contiene la configuracion visual de la app, campos de entrada, botonera, etc.
    def ventana(self):
        self.root.title("Compostura de calzado")

        titulo = Label(
            self.root,
            text="Ingresar datos:",
            bg="white",
            fg="black",
            height=1,
            width=60,
        )
        titulo.grid(row=0, column=0, columnspan=4, padx=1, pady=1, sticky="w")

        cliente = Label(self.root, text="Cliente")
        cliente.grid(row=1, column=0, sticky="w")
        trabajo = Label(self.root, text="Trabajo realizado")
        trabajo.grid(row=2, column=0, sticky="w")
        precio = Label(self.root, text="Precio $$$")
        precio.grid(row=3, column=0, sticky="w")
        busqueda = Label(self.root, text="Buscar Cliente")
        busqueda.grid(row=7, column=0, sticky="w")
        # Aqui declaramos las variables que se utilizaran y el tipo de dato que contienen.
        self.var1, self.var2, self.var3, self.var4 = (
            StringVar(),
            StringVar(),
            StringVar(),
            StringVar(),
        )
        # En esta seccion declaramos los entry de datos y la posicion de los mismos en pantalla.
        w_ancho = 20
        clienteE = Entry(self.root, textvariable=self.var1, width=w_ancho)
        clienteE.grid(row=1, column=1)
        trabajoE = Entry(self.root, textvariable=self.var2, width=w_ancho)
        trabajoE.grid(row=2, column=1)
        precioE = Entry(self.root, textvariable=self.var3, width=w_ancho)
        precioE.grid(row=3, column=1)
        busquedaE = Entry(self.root, textvariable=self.var4, width=w_ancho)
        busquedaE.grid(row=7, column=1)

        # TREEVIEW
        # En esta seccion declaramos la cantidad de columnas y su tamaño y posicion dentro del Treeview, como tambien su posicion visual.
        if self.tree is None:
            self.tree = ttk.Treeview(self.root)
            self.tree["columns"] = ("col1", "col2", "col3")
            self.tree.column("#0", width=50, minwidth=50, anchor="w")
            self.tree.column("col1", width=130, minwidth=50)
            self.tree.column("col2", width=130, minwidth=50)
            self.tree.column("col3", width=80, minwidth=50)
            self.tree.heading("#0", text="ID")
            self.tree.heading("col1", text="Cliente")
            self.tree.heading("col2", text="Trabajo")
            self.tree.heading("col3", text="Precio")
            self.tree.grid(row=10, column=0, columnspan=4)

        self.objeto = InteraccionBd(self.tree)
        # En esta seccion encontramos la botonera de la app.
        boton_guardar = Button(
            self.root,
            text="Guardar cliente",
            command=self.alta,
        )
        boton_modificar = Button(
            self.root,
            text="Modificar cliente",
            command=self.modificar,
        )
        boton_borrar = Button(
            self.root,
            text="Borrar cliente",
            command=self.borrar,
        )
        boton_consulta = Button(
            self.root,
            text="Consultar",
            command=self.consulta,
        )
        boton_actualizar = Button(
            self.root, text="Actualizar vista", command=self.actualizar
        )
        # Esta seccion es donde indicamos la posicion de los botones en pantalla.
        boton_guardar.grid(row=6, column=0, columnspan=1, padx=(0, 2))
        boton_modificar.grid(row=6, column=1, padx=2, columnspan=1)
        boton_borrar.grid(row=6, column=2, padx=(0, 5), columnspan=1)
        boton_consulta.grid(row=7, column=2)
        boton_actualizar.grid(row=8, column=1)

        self.objeto2.actualizar_treeview(self.tree, self.var1, self.var2, self.var3)

    # En esta seccion encontramos los metodos que son llamados en la botonera, se utiliza de esta manera para capturar un retorno, como por ejemplo los mensajes.
    def alta(self):
        retorno = self.objeto.guardar_cliente(
            self.var1, self.var2, self.var3, self.tree
        )
        messagebox.showinfo("Retorno", retorno)

    def borrar(self):
        retorno = self.objeto.borrar_cliente(self.tree, self.var1, self.var2, self.var3)
        messagebox.showinfo("Retorno", retorno)

    def modificar(self):
        retorno = self.objeto.modificar_cliente(
            self.tree, self.var1, self.var2, self.var3
        )
        messagebox.showinfo("Retorno", retorno)

    def consulta(self):
        retorno = self.objeto.consultar_y_mostrar_clientes(
            self.tree, self.var1, self.var2, self.var3, self.var4
        )
        messagebox.showinfo("Retorno", retorno)

    def actualizar(self):
        retorno = self.objeto2.actualizar_treeview(
            self.tree, self.var1, self.var2, self.var3
        )
        messagebox.showinfo("Retorno", retorno)
