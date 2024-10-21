import re
from basededatos import conexion_db

# En este modulo importamos el modulo re, el cual nos permtie generar un patron.
# El patron de validar campos es utilizado para restringir el ingreso de informacion segun se requiera.


class Auxiliares:
    def __init__(self, tree) -> None:
        self.tree = tree

    # Este metodo deja la parte visual limpia luego de utilizar un boton.
    def limpiar_campos_get(self, var1, var2, var3):
        var1.set("")
        var2.set("")
        var3.set("")

    # Este metodo nos permite que al modificar la base de datos, nos de la informacion actualizada en la parte visual.
    def actualizar_treeview(self, treview_vista, var1, var2, var3):
        try:
            records = treview_vista.get_children()
            for element in records:
                treview_vista.delete(element)

            con = conexion_db()
            cursor = con.cursor()
            sql = "SELECT * FROM clientes ORDER BY id ASC"
            datos = cursor.execute(sql)

            resultado = datos.fetchall()
            for fila in resultado:
                print(fila)
                treview_vista.insert(
                    "", 0, text=fila[0], values=(fila[1], fila[2], fila[3])
                )
            Auxiliares.limpiar_campos_get(self, var1, var2, var3)
            return "Actualizado con exito"
        except Exception as e:
            # Captura cualquier excepción y muestra un mensaje genérico
            print(f"Error o falla al actualizar treeview: {e}")
        return "Error al actualizar treeview"

    # Este metodo nos permtie restringir caracteres dentro de cada campo a ingresar, evitando por ejemplo un numero en un nombre o una letra en un precio.
    def validar_los_campos(self, var1, var2, var3):
        try:
            patron_textos = re.compile(r"^[a-zA-Z\u00f1\u00d1 ]+$")
            patron_numeros = re.compile(r"^\d+$")
            # ^ Inicio de la cadena, azAZ todas las mayus y minus. + puede haber 1 o mas letras
            # $ final de cadena(r"^[a-zA-Z ]+$") el espacio al final del corchete
            # es importante permite agregar 2 o mas nombres, permite el espacio.
            # /d numeros del 1 al 9 + aparece 1 o mas veces
            if not patron_textos.match(var1):
                return False, "El cliente solo puede contener letras"
            if not patron_textos.match(var2):
                return False, "El trabajo solo puede contener letras"
            if not patron_numeros.match(var3):
                return False, "El precio solo puede contener numeros enteros"
            return True, "Campos validados"
        except Exception as e:
            # Captura cualquier excepción y muestra un mensaje genérico
            print(f"Error o falla en validar campos: {e}")
        return "Error al validar campos"
