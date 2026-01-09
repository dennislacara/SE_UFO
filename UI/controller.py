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

        self._model.crea_grafo(int(self._view.dd_year.value), str(self._view.dd_shape.value))

        # implementazione View
        self._view.lista_visualizzazione_1.clean()
        if not self._model.intorni:
            print('Intorni non calcolati')
            return
        if self._model.vertici_pesati == []:
            print('Non esiste alcun intorno, per ogni nodo')
            self._view.show_alert('Non esiste alcun intorno')
            return

        self._view.lista_visualizzazione_1.controls.append(ft.Text(f'Numero di vertici: {self._model.G.number_of_nodes()} - Numero di archi: {self._model.G.number_of_edges()}'))
        for tupla in self._model.intorni:
            self._view.lista_visualizzazione_1.controls.append(ft.Text(f'Nodo: {tupla[0]} - Somma pesi su archi = {tupla[1]}'))
        self._view.update()
        # TODO

    def handle_path(self, e):
        """ Handler per gestire il problema ricorsivo di ricerca del cammino """
        percorsoMigliore, pesoMigliore, pesiArchi, pesiGeo = self._model.algoritmo()

        #gestione View
        self._view.lista_visualizzazione_2.controls.clear()
        if percorsoMigliore == []:
            self._view.show_alert('Non esiste alcun percorso')
            return
        self._view.lista_visualizzazione_2.controls.append(ft.Text(f'Peso cammino massimo: {pesoMigliore}'))
        for i in range(len(percorsoMigliore)-1):
            self._view.lista_visualizzazione_2.controls.append(ft.Text(f'{percorsoMigliore[i]} --> {percorsoMigliore[i+1]} -- Peso arco: {pesiArchi[i]} -- Distanza: {pesiGeo[i]}'))

        self._view.update()

