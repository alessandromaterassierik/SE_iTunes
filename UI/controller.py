import flet as ft
from UI.view import View
from model.model import Model
from UI.alert import AlertManager

class Controller:
    def __init__(self, view: View, model: Model, alert: AlertManager):
        self._view = view
        self._model = model
        self._alert = alert

    def handle_crea_grafo(self, e):
        """ Handler per gestire creazione del grafo """""
        self._view.lista_visualizzazione_1.controls.clear()
        input = self._view.txt_durata.value
        if input.isdigit() and int(input) > 0:
            self._model.create_graph(input)
            num_nodes, num_edges = self._model.get_info()
            self._view.lista_visualizzazione_1.controls.append(ft.Text(f'Grafo creato: {num_nodes} album, {num_edges} archi'))
            self._view.update()
            self.popola_dd()
        else:
            self._alert.show_alert(message='Put a fucking positive number: NOT STRINGS, NOT NEGATIVE NUMBERS')


    def popola_dd(self):
        self._view.dd_album.options.clear()
        self._model.get_album_infos()
        for g in self._model.G.nodes:
            title = self._model.G.nodes[g]['title']
            self._view.dd_album.options.append(ft.dropdown.Option(key = title, text= title))
        self._view.update()

    def get_selected_album(self, e):
        """ Handler per gestire la selezione dell'album dal dropdown """""
        self.input_album = e.control.value

    def handle_analisi_comp(self, e):
        """ Handler per gestire l'analisi della componente connessa """""
        self.input_album = self._view.dd_album.value
        num, dur_tot = self._model.analisi_album(self.input_album)

        self._view.lista_visualizzazione_2.controls.clear()
        self._view.lista_visualizzazione_2.controls.append(ft.Text(f'Dimensione componente: {num}'))
        self._view.lista_visualizzazione_2.controls.append(ft.Text(f'Durata totale: {dur_tot : .2f} minuti'))
        self._view.update()

    def handle_get_set_album(self, e):
        """ Handler per gestire il problema ricorsivo di ricerca del set di album """""
        self._view.lista_visualizzazione_3.controls.clear()
        d_input = self._view.txt_durata_totale.value
        if d_input.isdigit() and int(d_input) > 0:
            sol_ott, d_ott = self._model.ricerca_cammino(d_input)

            print(sol_ott, d_ott)
            self._view.lista_visualizzazione_3.controls.append(
                ft.Text(f'Set trovato({len(sol_ott)} album, durata {d_ott :.2f} minuti):'))
            for i in range(len(sol_ott)):
                self._view.lista_visualizzazione_3.controls.append(
                    ft.Text(f'{self._model.G.nodes[sol_ott[i]]['title']} - ({self._model.G.nodes[sol_ott[i]]['durata'] :.2f}min) '))
            self._view.update()
        else:
            self._alert.show_alert(message='Put a fucking positive number: NOT STRINGS, NOT NEGATIVE NUMBERS')
