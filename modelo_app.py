from auxx import Auxiliares
from basededatos import conexion_db
import os
from datetime import datetime
from observador import Sujeto


# Decorador para el metodo alta
def decorador_alta_cliente(funcion):
    def envoltura(*args, **kwargs):
        data = funcion(*args, **kwargs)
        if isinstance(data, str):
            print("Se ejecuto alta")
            funcion_log(funcion.__name__, data)
        else:
            return data

    return envoltura


# Decorador para el metodo baja
def decorador_baja_cliente(funcion):
    def envoltura(*args, **kwargs):
        data = funcion(*args, **kwargs)
        print("Se ejecuto la baja")
        funcion_log(funcion.__name__, data)

    return envoltura


# Decorador para el metodo modificar
def decorador_modificar_cliente(funcion):
    def envoltura(*args, **kwargs):
        data = funcion(*args, **kwargs)
        print("Se ejecuto la modificacion")
        funcion_log(funcion.__name__, data)

    return envoltura


def funcion_log(parameter, data):
    BASE_DIR = os.path.dirname((os.path.abspath(__file__)))
    ruta = os.path.join(BASE_DIR, "function_log.txt")
    log_function = open(ruta, "a")
    print(
        datetime.now().strftime("%H:%M:%S--%d/%m/%y"),
        "- Se utilizo el metodo",
        parameter,
        "\nDatos:",
        data,
        "\n",
        file=log_function,
    )


# Importamos del modulo auxx, la clase Auxiliares, la cual contiene metodos que seran utilizados dentro de la misma.
# Esta seccion contiene los metodos mas importantes de la aplicacion.
class InteraccionBd(Sujeto):
    def __init__(self, tree) -> None:
        self.tree = tree
        self.aux = Auxiliares(self.tree)

    # El siguiente metodo sera utilizado para guardar los datos ingresados en pantalla, y se enviaran tanto a la parte visual, como a una base de datos.
    @decorador_alta_cliente
    def guardar_cliente(self, var1, var2, var3, tree):
        valor_var1 = var1.get()
        valor_var2 = var2.get()
        valor_var3 = var3.get()
        validacion, mensaje = self.aux.validar_los_campos(
            valor_var1, valor_var2, valor_var3
        )

        if not validacion:
            return mensaje

        con = conexion_db()
        cursor = con.cursor()
        data = (valor_var1, valor_var2, valor_var3)
        sql = "INSERT INTO clientes(cliente, trabajo, precio) VALUES(?, ?, ?)"
        cursor.execute(sql, data)
        con.commit()
        print("Estoy en guardar_cliente")
        self.notificar(var1.get(), var2.get, var3.get)
        self.aux.actualizar_treeview(self.tree, var1, var2, var3)
        self.aux.limpiar_campos_get(var1, var2, var3)

        return "Cliente guardado con éxito"

    # Desde aqui al seleccionar un cliente desde la parte visual, podremos cargar sus datos nuevamente y modificarlos.
    @decorador_modificar_cliente
    def modificar_cliente(self, tree, var1, var2, var3):
        con = conexion_db()
        cursor = con.cursor()
        item = tree.focus()

        if item:
            id_cliente = tree.item(item, "text")

            valor_var1 = var1.get()
            valor_var2 = var2.get()
            valor_var3 = var3.get()

            validacion, mensaje = self.aux.validar_los_campos(
                valor_var1, valor_var2, valor_var3
            )
            if not validacion:
                return mensaje

            cursor.execute(
                """
                UPDATE clientes
                SET cliente=?, trabajo=?, precio=?
                WHERE id=?
                """,
                (
                    valor_var1,
                    valor_var2,
                    valor_var3,
                    id_cliente,
                ),
            )
            con.commit()
            self.aux.limpiar_campos_get(var1, var2, var3)
            self.aux.actualizar_treeview(self.tree, var1, var2, var3)
            return "Cliente modificado con éxito"
        else:
            return "Error al modificar cliente"

    # Esta seccion nos permtie eliminar un cliente desde la vista, el cual tambien sera eliminado de la base de datos.
    @decorador_baja_cliente
    def borrar_cliente(self, tree, var1, var2, var3):
        valor = tree.selection()
        item = tree.item(valor)
        mi_id = item["text"]

        con = conexion_db()
        cursor = con.cursor()
        data = (mi_id,)
        sql = "DELETE FROM clientes WHERE id = ?;"
        cursor.execute(sql, data)
        con.commit()
        tree.delete(valor)
        self.aux.limpiar_campos_get(var1, var2, var3)
        return "Cliente borrado con éxito" if valor else "Error al borrar cliente"

    # Desde aqui podremos consultar o buscar un cliente en nuestra base de datos, desde la parte visual.
    def consultar_y_mostrar_clientes(self, tree, var1, var2, var3, var4):
        con = conexion_db()
        cursor = con.cursor()
        self.aux.limpiar_campos_get(var1, var2, var3)
        nombre_a_buscar = var4.get()
        cursor.execute(
            "SELECT * FROM clientes WHERE cliente LIKE ? OR trabajo LIKE ?",
            ("%" + nombre_a_buscar + "%", "%" + nombre_a_buscar + "%"),
        )
        resultados = cursor.fetchall()
        if resultados:
            tree.delete(*tree.get_children())
            for resultado in resultados:
                tree.insert(
                    "",
                    "end",
                    text=str(resultado[0]),
                    values=(resultado[1], resultado[2], resultado[3]),
                )
            var4.set("")
            return "Cliente consultado con éxito"
        else:
            var4.set("")
            return "Error al consultar cliente"
