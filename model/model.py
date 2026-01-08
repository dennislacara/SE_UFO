import networkx as nx
from database.dao import DAO

class Model:
    def init(self):
        self.anni = None
        self.forme = None
        self.vertici = None
        self.archi = None

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
            self.G.add_edge(arco[0], arco[1], somma_eventi=0)

        self.vertici_pesati = DAO.read_vertici_validi(anno, forma)
        for vertice in self.vertici_pesati:
            self.G.nodes[vertice[0]]['Neventi'] = vertice[1]
            print(self.G.nodes[vertice[0]])

        #adesso che i nodi sono pesati; calcolo peso dell'intorno di ogni nodo
        self.calcola_intorni()


    def get_anni(self):
        self.anni = DAO.read_anni()
        return self.anni

    def get_forme(self):
        self.forme = DAO.read_forme()
        return self.forme

    def get_vertici(self):
        self.vertici = DAO.read_vertici()

    def get_archi(self):
        self.archi = DAO.read_archi()

    def calcola_intorni(self):
        for nodo in self.G.nodes():
            vicini = nx.neighbors(self.G, nodo)
            somma_eventi = sum([self.G.nodes[n]['Neventi']+ self.G.nodes[nodo]['Neventi'] for n in vicini])
            if somma_eventi > 0:
                print(nodo, somma_eventi)