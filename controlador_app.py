from tkinter import Tk
import vista_app
from modelo_app import InteraccionBd
import observador

# Importo el modulo tkinter para utilizar el root.
# Importo el modulo vista_app, la cual contiene la botonera y la parte visual de la aplicacion.
# IMporto del modelo_app observador.


class Controller:

    def __init__(self, root) -> None:
        self.root_tk = root
        self.app = vista_app.VistaTotal(self.root_tk)
        self.el_observador = observador.ConcreteObserverA(self.app.objeto)
        # objeto que instancia la clase que se encuentra en el modelo.


if __name__ == "__main__":
    root_tk = Tk()
    vista = vista_app.VistaTotal(root_tk)
    vista.ventana()
    root_tk.mainloop()
