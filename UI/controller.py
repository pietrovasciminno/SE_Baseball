import flet as ft
from UI.view import View
from modell.model import Model

class Controller:
    def __init__(self, view: View, model: Model):
        self._view = view
        self._model = model

    def handle_crea_grafo(self, e):
        anno = int(self._view.dd_anno.value)
        return self._model.crea_graph(anno)

    def handle_dettagli(self, e):
        """ Handler per gestire i dettagli """""
        nodo = self._model._dict_squadre[int(self._view.dd_squadra.value)]
        result = self._model.trova_dettagli(nodo)
        self._view.txt_risultato.controls.clear()
        for r in result:
            self._view.txt_risultato.controls.append(ft.Text(f"{r[0].team_code}({r[0].name}) -- peso: {r[1]}"))
        self._view.update()


    def handle_percorso(self, e):
        """ Handler per gestire il problema ricorsivo di ricerca del percorso """""
        nodo = self._model._dict_squadre[int(self._view.dd_squadra.value)]
        path, weight =self._model.trova_percorso(nodo)
        self._view.txt_risultato.controls.clear()
        for i in range(len(path) - 1):
            w = self._model._graph[path[i]][path[i + 1]]["weight"]
            self._view.txt_risultato.controls.append(
                ft.Text(f"{path[i]} -> {path[i + 1]} (peso {w})")
            )
        self._view.txt_risultato.controls.append(
            ft.Text(f"Peso totale: {weight}")
        )
        self._view.update()



    """ Altri possibili metodi per gestire di dd_anno """""
    def get_years(self):
        return self._model.get_years()

    def handler_squadre(self, e):
        anno = int(self._view.dd_anno.value)
        self._model.get_squadre(anno)
        self._view.txt_out_squadre.controls.clear()
        self._view.txt_out_squadre.controls.append(ft.Text(f"Numero squadre: {len(self._model._lista_squadre)}"))
        for y in self._model._lista_squadre:
            self._view.txt_out_squadre.controls.append(ft.Text(f"{y.team_code}({y.name})"))
        self._view.dd_squadra.options = [ft.dropdown.Option(key=str(y.id), text=f"{y.team_code}({y.name})") for y in self._model._lista_squadre]

        self._view.update()



