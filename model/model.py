from collections import defaultdict

import networkx as nx
from database.dao import DAO
from geopy.distance import geodesic


class Model:
    def init(self):
        self.anni = None
        self.forme = None
        self.vertici = None
        self.map_coordinate = None
        self.archi = None
        self.intorni = None

    def crea_grafo(self, anno, forma):
        self.G = nx.Graph()
        self.get_vertici()
        self.get_archi()

        if self.anni is None or self.forme is None:
            print('Lista vertici/archi non valida/e, non si può iterare')
            return

        for vertice in self.vertici:
            self.G.add_node(vertice, Neventi=0)
        for arco in self.archi:
            self.G.add_edge(arco[0], arco[1], SommaEventi = 0)

        self.vertici_pesati = DAO.read_vertici_validi(anno, forma)
        for vertice in self.vertici_pesati:
            self.G.nodes[vertice[0]]['Neventi'] = vertice[1]

        #adesso che i nodi sono pesati; calcolo peso dell'intorno di ogni nodo
        self.intorni = self.calcola_intorni()

    def get_anni(self):
        self.anni = DAO.read_anni()
        return self.anni

    def get_forme(self):
        self.forme = DAO.read_forme()
        return self.forme

    def get_vertici(self):
        self.vertici, self.map_coordinate = DAO.read_vertici()

    def get_archi(self):
        self.archi = DAO.read_archi()

    def calcola_intorni(self):
        result = []
        for nodo in self.G.nodes():
            vicini = list(nx.neighbors(self.G, nodo))
            somma_eventi = sum([self.G.nodes[n]['Neventi']+ self.G.nodes[nodo]['Neventi'] for n in vicini])

            result.append((nodo, somma_eventi))
            #incremento gli archi del grafo
            self.incremento_archi(nodo, vicini)
        return result

    def incremento_archi(self, nodo, vicini):
        for vicino in vicini:
            arco = self.G[nodo][vicino]
            peso =arco['SommaEventi']
            if peso == 0:
                peso = self.G.nodes[nodo]['Neventi'] + self.G.nodes[vicino]['Neventi']
                arco['SommaEventi'] = peso

    def algoritmo(self):
        self.percorso_migliore = []
        self.pesi_archi = []
        self.pesi_geo = []

        self.peso_migliore = float('-inf')

        for nodo in self.vertici:
            self.ricorsione(
                g=self.G,
                nodo_corrente=nodo,
                percorso=[nodo],
                peso_corrente=0,
                pa=[],
                pg=[]
            )

        return self.percorso_migliore, self.peso_migliore, self.pesi_archi, self.pesi_geo

    def ricorsione(self, g, nodo_corrente, percorso, peso_corrente, pa, pg):

        # replica ESATTA della tua condizione
        if len(percorso) >= 3:
            if peso_corrente > self.peso_migliore:
                self.percorso_migliore = percorso.copy()
                self.pesi_archi = pa.copy()
                self.pesi_geo = pg.copy()
                self.peso_migliore = peso_corrente

        for vicino in g.neighbors(nodo_corrente):

            peso_arco = g[nodo_corrente][vicino]['SommaEventi']
            #verificare che l'arco non sia nullo
            if peso_arco == 0:
                continue

            #verificare che il percorso sia crescente in peso
            if len(percorso) >= 2:
                arco_prec = g[percorso[-2]][percorso[-1]]['SommaEventi']
                if peso_arco <= arco_prec:
                    continue

            # evitare cicli infiniti
            MAX_VISITE = 2
            contatore_vicini = defaultdict(int)
            if contatore_vicini[vicino] >= MAX_VISITE:
                continue

            coord1 = self.map_coordinate[nodo_corrente]
            coord2 = self.map_coordinate[vicino]
            delta = geodesic(coord1, coord2).km

            percorso.append(vicino)
            pa.append(peso_arco)
            pg.append(delta)
            self.ricorsione(
                g,
                vicino,
                percorso,
                peso_corrente + delta,
                pa,
                pg
            )
            percorso.pop()
            pa.pop()
            pg.pop()

