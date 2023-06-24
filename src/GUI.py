from Interfejs import Interfejs
import PySimpleGUI as sg
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg as FigCanvTk

class MainWindow:
    def __init__(self, interfejs: Interfejs) -> None:
        self.interfejs = interfejs

        options = self.interfejs.podajListePosiadaczy()
        layout = [
            [sg.Text("Wybierz użytkownika")],
            [sg.Combo(options, key='-COMBO-', default_value=options[0] if len(options) != 0 else "", enable_events=True)],
            [sg.Button("Dalej"), sg.Button("Dodaj nowego")],
            [sg.Button("Wyjdź")]
                  ]
        
        # Create the window
        window = sg.Window('Manager wydatków', layout)

        # deaktywowanie przycisku "Dalej" w przypadku, gdy nie ma jeszcze dodanych użytkowników
        window.read(timeout=1)
        if options == []: window['Dalej'].update(disabled=True)
        window.read(timeout=1)        

        # Event loop
        while True:
            event, values = window.read()

            if event == sg.WINDOW_CLOSED or event == "Wyjdź":
                break

            elif event == 'Dalej':
                selected_option = values['-COMBO-']
                sg.popup(f'Selected Option: {selected_option}')

                self.interfejs.przejdzNaPoz(selected_option)

                window.hide()
                self.userWindowLoop()
                window.un_hide()

        # Close the window
        window.close()

    # < - - - - - - - - - - - - - - - - - - - - > Metody okien pobocznych < - - - - - - - - - - - - - - - - - - - - > 
    def userWindowLoop(self):
        tab_options = self.interfejs.podajListeNazwTabWydatkow()
        user_layout = [
            [
                sg.Text("Imie", font=('Arial', 14, 'bold')),
                sg.Text(key="-TEXT1-", font=('Arial', 14)),
                sg.Text("Nazwisko", font=('Arial', 14, 'bold')),
                sg.Text(key="-TEXT2-", font=('Arial', 14))
            ],
            [sg.Combo(tab_options, default_value = "" if len(tab_options) == 0 else tab_options[0], key="-TABS_NAMES_COMBO-", enable_events=True, size=(20,1))],
            [
                sg.Button("Pokaż tabelę"),
                sg.Button("Dodaj tabelę"),
                sg.Button("Wykresy")
            ],
            [sg.Button("Powrót")]
        ]
        user_window = sg.Window("Okno użytkownika", user_layout, size=(400, 200))
        event, values = user_window.read(timeout=1)
        imie, nazw = self.interfejs.podajDanePosiadacza()
        user_window['-TEXT1-'].update(imie)
        user_window['-TEXT2-'].update(nazw)
        event, values = user_window.read(timeout=1)

        while True:
            event, values = user_window.read()
            if event == sg.WINDOW_CLOSED:
                break
            elif event == 'Powrót':
                break
            elif event == 'Dodaj tabelę':
                user_window.disable()
                self.addTabLoop()
                user_window.enable()
                user_window['-TABS_NAMES_COMBO-'].update(values=self.interfejs.podajListeNazwTabWydatkow(), value=self.interfejs.podajListeNazwTabWydatkow()[0])
            elif event == 'Wykresy':
                user_window.disable()
                self.drawGraphs()
                user_window.enable()            
            elif event == 'Pokaż tabelę':
                self.showTable(values['-TABS_NAMES_COMBO-'])

        user_window.close()

    def addTabLoop(self):
        add_tab_layout = [
            [
                sg.Text("Wybierz plik", font=('Arial', 14, 'bold'), key='-FILE_PATH-'),
                sg.FileBrowse(key='-BROWSE-')
            ],
            [sg.Checkbox("Dołącz do tabeli", tooltip="Wczytana tabela zostanie dołączona do tabeli już istniejącej", key="-JOIN_CHECK-", change_submits=True, enable_events=True)],
            [
                sg.Text("Nazwa tabeli", key='-SUBMIT_TEXT-', visible=False),
                sg.Input(key='-INPUT-', visible=False),
                sg.Button("Zatwierdź", key='-SUBMIT-', visible=False)
            ],
            [
                sg.Button("Powrót"),
                sg.Button("Wczytaj")
            ]
        ]
        add_tab_window = sg.Window("Dodawanie tabeli", add_tab_layout)

        while True:
            event, values = add_tab_window.read()
            if event == sg.WINDOW_CLOSED:
                break
            elif event == 'Powrót':
                break
            elif event == '-BROWSE-':
                folder_path = values['-BROWSE-']
                add_tab_window['-FILE_PATH-'].update(folder_path)
                if values['-JOIN_CHECK-']:
                    self.adjustBindedGUIElems(add_tab_window, elems_to_visible=['-SUBMIT_TEXT-', '-INPUT-', '-SUBMIT-'])
            elif event == '-JOIN_CHECK-':
                if values['-JOIN_CHECK-'] and add_tab_window['-FILE_PATH-'].get() != 'Wybierz plik':
                    self.adjustBindedGUIElems(add_tab_window, elems_to_visible=['-SUBMIT_TEXT-', '-INPUT-', '-SUBMIT-'])
                elif not(values['-JOIN_CHECK-']):
                    self.adjustBindedGUIElems(add_tab_window, elems_to_invisible=['-SUBMIT_TEXT-', '-INPUT-', '-SUBMIT-'])
            elif event == 'Wczytaj':
                file_path = add_tab_window['-FILE_PATH-'].get()
                if file_path != 'Wybierz plik' and not values['-JOIN_CHECK-']:
                    self.interfejs.wczytajTabZPliku(file_path, os.path.basename(file_path).split(sep='.')[0], False)
                    break

        add_tab_window.close()

    def showTable(self, nazwa_tab: str):
        df = self.interfejs.podajTabWydatki(nazwa_tab)

        # Convert DataFrame to list of lists
        data_rows = df.values.tolist()

        # Get column headers
        headers = df.columns.tolist()

        show_tab_layout = [
            [sg.Table(values=data_rows, headings=headers, justification='left', num_rows=10, key='-TABLE-')]
        ]
        show_tab_window = sg.Window("Dodawanie tabeli", show_tab_layout)

        while True:
            event, values = show_tab_window.read()
            if event == sg.WINDOW_CLOSED:
                break

        show_tab_window.close()

    def drawGraphs(self):
        graph_types = ["kołowy", "słupkowy"]
        options = self.interfejs.podajListeNazwTabWydatkow()
        # Utworzenie layoutu dla okna
        layout = [
            [
                sg.Text('Wybierz tabele:'), 
                sg.Combo(options, enable_events=True, key='-COMBO-', tooltip="Ponowne wybranie danej opcji usuwa ją z listy wybranych"), 
                sg.Text('Wybierz typ wykresu:'),
                sg.Combo(graph_types, enable_events=True, key='-CB_GRAPH_TYPE-', default_value=graph_types[0])
            ],
            [
                sg.Text('Wybierz kolumny:'), 
                sg.Combo([], enable_events=True, key='-CB_COLS-', auto_size_text=True, size=(20, 10)),
                sg.Text('Wybierz wartości:'),
                sg.Combo([], enable_events=True, key='-CB_COL_VALS-', auto_size_text=True, size=(20, 10), tooltip="Ponowne wybranie danej opcji usuwa ją z listy wybranych")
            ],
            [
                sg.Checkbox("Sumowanie wartości", key="-SUM_CHECK-", enable_events=True, tooltip="Jeśli zaznaczone: sumuje wartości z kolumny wartości.\nW przeciwnym wypadku zlicza wystąpienia"),
                sg.Text('Wybierz kolumnę wartości do sumowania:'), 
                sg.Combo([], enable_events=True, key='-CB_COL_FOR_VALS-', auto_size_text=True, size=(20, 10), disabled=True),
            ],
            [sg.Text('Wybrane opcje:')],
            [
                sg.Output(size=(30, 5), key='-OUTPUT-'),
                sg.Canvas(size=(400, 400), key='-CANVAS-')
            ],
            [
                sg.Button('Rysuj', key='-RYSUJ-', disabled=True),
                sg.Button('Zamknij')
            ]
        ]

        # Utworzenie okna
        graphs_window = sg.Window('Wykresy', layout, finalize=True)
        selected_tabs = []
        selected_col = ''
        selected_col_vals = []

        # Główna pętla metody
        while True:
            event, values = graphs_window.read()
            
            if event == sg.WINDOW_CLOSED or event == 'Zamknij':
                break
            
            # Obsługa zdarzenia wyboru elementu w liście tabel
            if event == '-COMBO-':
                selected_option = values['-COMBO-']
                
                # Aktualizacja wartości pól wyboru na podstawie wybranej opcji
                if selected_option in selected_tabs:
                    selected_tabs.remove(selected_option)
                else:
                    selected_tabs.append(selected_option)
                selected_tabs = sorted(selected_tabs)

                # Aktualizacja listy z nazwami kolumn
                if bool(selected_tabs): self.adjustBindedGUIElems(graphs_window, combos_to_update=['-CB_COLS-'], 
                                                                  combos_new_vals=[self.interfejs.podajUnikatoweNazwyKol(selected_tabs)],
                                                                  combos_to_clear=['-CB_COL_VALS-']
                                                                  )
                else:  
                    self.adjustBindedGUIElems(graphs_window, combos_to_clear=['-CB_COLS-', '-CB_COL_VALS-'])

                selected_col = ''
                selected_col_vals.clear()                    

                # Wyświetlenie aktualnie wybranych opcji                
                graphs_window['-OUTPUT-'].update('')
                print("Wybrane tabele:\n",selected_tabs, '\n')
                print("Wybrana kolumna:\n",selected_col, '\n')
                print("Wybrane wartości kolumn:\n",selected_col_vals, '\n')
            
            # Obsługa zdarzenia wyboru elementu w liście kolumn
            if event == '-CB_COLS-':
                if values['-CB_COLS-'] != selected_col:
                    selected_col = values['-CB_COLS-']
                    selected_col_vals = []
                    self.adjustBindedGUIElems(graphs_window, combos_to_update=['-CB_COL_VALS-'], 
                                            combos_new_vals=[self.interfejs.podajUnikatoweWartZKol(selected_tabs, selected_col)]
                                            )
                    
                    graphs_window['-RYSUJ-'].update(disabled=False)
                    # Wyświetlenie aktualnie wybranych opcji            
                    graphs_window['-OUTPUT-'].update('')
                    print("Wybrane tabele:\n",selected_tabs, '\n')
                    print("Wybrana kolumna:\n",selected_col, '\n')
                    print("Wybrane wartości kolumn:\n",selected_col_vals, '\n')
                
            if event == '-CB_COL_VALS-':
                selected_option = values['-CB_COL_VALS-']
                
                # Aktualizacja wartości pól wyboru na podstawie wybranej opcji
                if selected_option in selected_col_vals:
                    selected_col_vals.remove(selected_option)
                else:
                    selected_col_vals.append(selected_option)
                selected_col_vals = sorted(selected_col_vals)  

                # Wyświetlenie aktualnie wybranych opcji                
                graphs_window['-OUTPUT-'].update('')
                print("Wybrane tabele:\n",selected_tabs, '\n')
                print("Wybrana kolumna:\n",selected_col, '\n')
                print("Wybrane wartości kolumn:\n",selected_col_vals, '\n')

            if event == '-SUM_CHECK-':
                if values['-SUM_CHECK-']: self.adjustBindedGUIElems(graphs_window, elems_to_enable=['-CB_COL_FOR_VALS-'])
                else: self.adjustBindedGUIElems(graphs_window, elems_to_disable=['-CB_COL_FOR_VALS-'])

            if event == '-RYSUJ-':
                #TODO:
                #   trzeba sprawdzić, czy są zaznaczone wszystkie potrzebne opcje 
                etykiety, dane = self.interfejs.podajDaneDoWykresu(selected_tabs, selected_col, etykiety_kol=selected_col_vals)
                canvas = graphs_window['-CANVAS-'].TKCanvas
                canvas.delete('all')
                self.drawGraph(canvas, self.createPieChart(etykiety, dane))

        # Zamknięcie okna
        graphs_window.close()

    # < - - - - - - - - - - - - - - - - - - - - > Metody pomocnicze < - - - - - - - - - - - - - - - - - - - - >
    def adjustBindedGUIElems(
            self, window: sg.Window,
            elems_to_enable = [], elems_to_disable = [], elems_to_visible = [], elems_to_invisible = [], 
            combos_to_update = [], combos_new_vals = [], combos_to_clear = []
            ):
        """ Metoda służąca do odpowiedniego dostosowania powiązanych ze sobą elementów GUI.            

        Parametry
        ----------
        elems_to_enable : list()
        elems_to_disable : list()
        elems_to_visible : list()
        elems_to_invisible : list()

        combos_to_update : list()
            Lista nazw elementów typu PySimpleGUI.Combo do zaktualizowania zawartych opcji

        combos_new_vals : list()
            Zawiera listę z nowymi opcjami dla każdego elementu z combos_to_update. Jeżeli zawiera mniej list wartości niż elementów
            z combos_to_update to ostatnia lista nowych opcji jest przypisywana dla wszystkich pozostałych obiektów PySimpleGUI.Combo

        combos_to_clear : list()
            Lista nazw elementów typu PySimpleGUI.Combo do całkowitego usunięcia zawartych opcji
        """

        for elem in elems_to_enable: window[elem].update(disabled=False)
        for elem in elems_to_disable: window[elem].update(disabled=True)
        for elem in elems_to_visible: window[elem].update(visible=True)
        for elem in elems_to_invisible: window[elem].update(visible=False)
        for combo in combos_to_clear: window[combo].update(values='')

        #TODO: 
        #   Uwzględnić, który element w aktualizowanych Combo listach ma być ustawiony jako domyślny.
        for idx in range(len(combos_to_update)): 
            new_vals = combos_new_vals[idx if len(combos_new_vals) > idx else (len(combos_new_vals) - 1)]
            window[combos_to_update[idx]].update(values=new_vals, value = new_vals[0] if bool(new_vals) else '')

    def drawGraph(self, canvas, figure):
        figure_canvas_agg = FigCanvTk(figure, canvas)
        figure_canvas_agg.draw()
        figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
        return figure_canvas_agg
    
    def createPieChart(self, labels, sizes):
        # Utworzenie wykresu kołowego
        plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
        plt.axis('equal')
        return plt.gcf()