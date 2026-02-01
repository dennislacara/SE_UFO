import networkx as nx
from database.dao import DAO
from geopy import distance

class Model:
    def __init__(self):
        self.sightings = []
        self.load_sightings()
        self.states = []
        self.map_states = {}
        self.load_states()

        self.G = nx.Graph()
        self.edges = []
        self.distanze = {}

    def crea_grafo(self, anno, forma):
        self.G.clear()
        #nodi
        for state in self.states:
            self.G.add_node(state.id)
            print(state)
        #archi
        self.load_edges(anno, forma)
        for n in self.edges:
            self.G.add_edge(n.state1, n.state2, peso = n.total_sightings)
        print(self.G)


    def load_sightings(self):
        self.sightings = DAO.read_sightings()
        print('Avvistamenti caricati')

    def load_states(self):
        self.states = DAO.read_states()
        #creo un dizionario dedicato
        self.map_states.clear()
        for state in self.states:
            self.map_states[state.id] = state

    def load_edges(self, anno, forma):
        self.edges = DAO.read_archi(anno, forma)

    def pesoArchixnodo(self):
        l = {}
        for state in self.G:
            l[state] = 0
            for i,j,data in self.G.edges(state, data=True):

                l[state] += data['peso']
        return sorted(l.items(), key=lambda x: x[0])

    def calcola_percorso(self):
        self.best_percorso =[]
        self.best_valore = 0
        self.info = []

        for state in self.G:
            lp = [state]
            vp = 0
            info = []
            self.ricorsione(self.G, lp, vp, info)
        return self.info, self.best_valore

    def ricorsione(self, grafo, lp, vp, info):


        if vp > self.best_valore:
            self.best_valore = vp
            self.best_percorso = lp.copy()
            self.info = info.copy()

        for vicino in nx.neighbors(grafo, lp[-1]):
            if grafo[lp[-1]][vicino]['peso'] == 0:
                continue

            if len(lp) >=2:
                #se il penultimo arco è meno pesante del successivo, lo scarto
                if grafo[lp[-2]][lp[-1]]['peso'] >= grafo[lp[-1]][vicino]['peso']:
                    continue

            peso_arco = grafo[lp[-1]][vicino]['peso']
            distanza = self.calcola_distanza(lp[-1], vicino)
            info.append((lp[-1],vicino, peso_arco, distanza))
            lp.append(vicino)
            self.ricorsione(grafo, lp, vp + distanza, info)
            lp.pop(-1)
            info.pop(-1)


    def calcola_distanza(self, nodo, vicino):
        if (nodo, vicino) in self.distanze:
            #leggi nel dizionario
            distanza = self.distanze[(nodo, vicino)]
        elif (vicino, nodo) in self.distanze:
            #leggi nel dizionario
            distanza = self.distanze[(vicino, nodo)]
        else:
            #calcolo distanza
            state1 = self.map_states[nodo]
            state2 = self.map_states[vicino]
            coordState1 = (state1.lat, state1.lng)
            coordState2 = (state2.lat, state2.lng)
            distanza = distance.geodesic(coordState1, coordState2).km
            #salvo nel dizionario
            self.distanze[(nodo, vicino)] = distanza

        return distanza
