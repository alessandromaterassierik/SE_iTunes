import networkx as nx
from database.dao import DAO

class Model:
    def __init__(self):
        self.albums = []
        self.durata = ''
        self.tuple_albums = []
        self.tuple_def = []
        self.G = nx.Graph()
        self.album_info = ''
        self.id_nodo = ''

    def get_albums(self, durata):       #{'id': 249, 'title': 'The Office, Season 1'}
        self.albums = DAO.load_albums(durata)
        return self.albums

    def get_tuple_albums(self, durata):     #{'a1': 347, 'a2': 335}
        self.tuple_albums = DAO.load_tuple_albums(durata)
        return self.tuple_albums


    def create_graph(self, durata):
        self.durata= durata
        self.get_tuple_albums(durata)
        for e in self.tuple_albums:
            #print(e['a1'], e['a2'])
            self.G.add_edge(e['a1'], e['a2'])

    def get_info(self):
        return len(self.G.nodes), len(self.G.edges)

    def get_album_infos(self):
        self.album_info = self.get_albums(self.durata)
        for g in self.G.nodes:
            for t in self.album_info:
                if g == t['id']:
                    self.G.nodes[g]['title'] = t['title']
                    self.G.nodes[g]['durata'] = float(t['durata'])

    def analisi_album(self, nodo):
        #print(f' questo è il nodo di input {nodo}')
        for t in self.album_info:
            #print(f' ogni elemento di album info{t}')
            if nodo == t['title']:
                self.id_nodo = t['id']
                break
        list_nodes = nx.node_connected_component(self.G, self.id_nodo)
        t_tot=0
        for n in list_nodes:
            #print(f'durata tot per nodo {self.G.nodes[n]["durata"]}')
            t_tot += self.G.nodes[n]['durata']
        return len(list_nodes), t_tot

    def ricerca_cammino(self, d_input):
        a1 = self.id_nodo
        nodes_con_a1 = list(nx.node_connected_component(self.G, self.id_nodo)-{self.id_nodo})
        d_a1 = float(self.G.nodes[a1]['durata'])

        sol_part=[a1]
        self.sol_ott = sol_part
        self.d_ott= d_a1
        self.ricorsione(start_index=0, sol_part=[a1], d_cur=d_a1, nodes_con_a1= nodes_con_a1, max_d= float(d_input))

        return self.sol_ott, self.d_ott

    def ricorsione(self, start_index, sol_part, d_cur, nodes_con_a1, max_d):

        if len(sol_part) > len(self.sol_ott) and d_cur < max_d:
            self.sol_ott = sol_part.copy()
            self.d_ott = d_cur

        #end
        if start_index == len(nodes_con_a1) or d_cur ==max_d:
            return

        #ciclo
        for i in range(start_index, len(nodes_con_a1)):
            n = nodes_con_a1[i]
            if self.vincoli(n, d_cur, max_d, sol_part) is not None:
                d_n = float(self.G.nodes[n]['durata'])
                sol_part.append(n)
                self.ricorsione(start_index +1, sol_part, d_cur +d_n , nodes_con_a1, max_d)
                sol_part.pop()

    def vincoli(self, n, d_cur,max_d, sol_part):
        if d_cur + float(self.G.nodes[n]['durata']) > float(max_d):
            return False
        else:
            return True




