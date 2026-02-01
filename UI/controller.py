import flet as ft

class Controller:
    def __init__(self, view, model):
        self._view = view
        self._model = model

    def populate_dd(self):
        """ Metodo per popolare i dropdown """
        anni = []
        for s in self._model.sightings:
            if s.s_datetime.year not in anni:
                anni.append(s.s_datetime.year)
        #gestione view
        for a in sorted(anni):
            self._view.dd_year.options.append(ft.dropdown.Option(key=a, text=a))
        self._view.update()


    def handle_graph(self, e):
        """ Handler per gestire creazione del grafo """
        anno, forma = self.controlla_dd_values(self._view.dd_year.value, self._view.dd_shape.value)
        if anno and forma:
            self._model.crea_grafo(anno, forma)
        else:
            self._view.show_alert('Inserire valori')
            return
        # somma dei pesi degli archi per ogni stato
        diz = self._model.pesoArchixnodo()
        self._view.lista_visualizzazione_1.controls.clear()
        for state in diz:
            self._view.lista_visualizzazione_1.controls.append(ft.Text(f'{state[0]} : {state[1]}'))
        self._view.update()

    def handle_path(self, e):
        """ Handler per gestire il problema ricorsivo di ricerca del cammino """

        info, valore = self._model.calcola_percorso()
        self._view.lista_visualizzazione_2.controls.clear()
        self._view.lista_visualizzazione_2.controls.append(ft.Text(f'Distanza massima: {valore}'))
        for t in info:
            #print(i, j, peso, distanza)
            self._view.lista_visualizzazione_2.controls.append(ft.Text(f'{t[0]} -> {t[1]} - peso: {t[2]} - distanza: {t[3]}'))
        self._view.update()

    def populate_dd_shape(self, e):
        self._view.dd_shape.options.clear()
        lista = []
        for s in self._model.sightings:
            if s.s_datetime.year == int(self._view.dd_year.value):
                if s.shape not in lista:
                    lista.append(s.shape)
        for f in sorted(lista):
            self._view.dd_shape.options.append(ft.dropdown.Option(key=f, text=f))
        self._view.update()

    def controlla_dd_values(self, anno, forma):
        if not anno:
            anno = None
        else:
            anno = int(anno)

        if not forma:
            forma = None
        print(forma)

        return anno, forma


