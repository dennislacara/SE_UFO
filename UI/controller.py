import flet as ft

class Controller:
    def __init__(self, view, model):
        self._view = view
        self._model = model

    def populate_dd(self):
        """ Metodo per popolare i dropdown """
        anni = self._model.get_anni()
        forme = self._model.get_forme()

        self._view.dd_year.options.clear()
        self._view.dd_shape.options.clear()
        self._view.dd_year.options = [ft.dropdown.Option(anno) for anno in anni]
        self._view.dd_shape.options = [ft.dropdown.Option(forma) for forma in forme]
        self._view.update()
        # TODO

    def handle_graph(self, e):
        """ Handler per gestire creazione del grafo """
        if not self._view.dd_year.value or not self._view.dd_shape.value:
            self._view.show_alert('Inserire valori validi')
            return

        print(self._view.dd_year.value, self._view.dd_shape.value)
        self._model.crea_grafo(int(self._view.dd_year.value), str(self._view.dd_shape.value))


        # TODO

    def handle_path(self, e):
        """ Handler per gestire il problema ricorsivo di ricerca del cammino """
        # TODO
