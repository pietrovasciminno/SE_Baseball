from operator import itemgetter

import networkx as nx

from database.dao import DAO


class Model:
    def __init__(self):
        self._lista_squadre = []
        self._dict_squadre = {}
        self._graph = nx.Graph()
        self._lista_connessioni = []
        self.K = 3
        self._salary_map = {}
        self.best_path = []
        self.best_weight = 0

    def crea_graph(self, anno):
        self._lista_connessioni.clear()
        self._graph.clear()
        pesi = self.get_peso(anno)
        for z in self._lista_squadre:
            self._graph.add_node(z)
        for y in self._lista_squadre:
            for x in self._lista_squadre:
                salario = pesi[x.id] + pesi[y.id]
                if (x,y,salario) not in self._lista_connessioni and x != y:
                    self._lista_connessioni.append((x,y,salario))
        for z in self._lista_connessioni:
            self._graph.add_edge(z[0], z[1], weight=z[2])
        return self._graph



    def get_years(self):
        return DAO.get_years_from_1980()

    def get_squadre(self, year):
        self._lista_squadre = DAO.read_teams_for_year(year)
        for squadra in self._lista_squadre:
            self._dict_squadre[squadra.id] = squadra

        return self._lista_squadre, self._dict_squadre

    def get_peso(self, anno):
        self._salary_map = DAO.read_peso(anno)
        return self._salary_map

    def trova_dettagli(self, nodo):
        vicini = []
        for n in self._graph.neighbors(nodo):
            w = self._graph[nodo][n]["weight"]
            vicini.append((n, w))
        return sorted(vicini, key=lambda x: x[1], reverse=True)

    def trova_percorso(self, nodo):
        self.best_path = []
        self.best_weight = 0
        self.ricorsione([nodo], 0, float("inf"))
        return self.best_path, self.best_weight

    def ricorsione(self, path, weight, last_edge_weight):
        n_last = path[-1]

        if weight > self.best_weight:
            self.best_weight = weight
            self.best_path = path.copy()

        vicini = self.trova_dettagli(n_last)
        neigh = []
        counter = 0
        for node, edge_w in vicini:
            if node in path:
                continue
            if edge_w <= last_edge_weight:
                neigh.append((node, edge_w))
                counter += 1
                if counter == self.K:
                    break

        for node, edge_w in neigh:
            path.append(node)
            self.ricorsione(path, weight + edge_w, edge_w)
            path.pop()



