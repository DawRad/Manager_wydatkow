from Interfejs import Interfejs
import PySimpleGUI as sg
import os
import datetime as dtm
import calendar as cld
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg as FigCanvTk

class MainWindow:
    def __init__(self, interfejs: Interfejs) -> None:
        self.interfejs = interfejs
        options = self.interfejs.podajListePosiadaczy()

        layout = [
            [
                sg.Text("Wybierz użytkownika:"),
                sg.Combo(options, key='-COMBO-', default_value=options[0] if len(options) != 0 else "", enable_events=True, readonly=True)
            ],
            [sg.Button("Dalej"), sg.Button("Dodaj nowego")],
            [sg.Button("Wyjdź")]
        ]

        # Create the window
        window = sg.Window('Manager wydatków', layout, element_justification='center')

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
        
        # Składowe kontenery layout'u
        frame = [
            [
                sg.Text("Imie", font=('Arial', 14, 'bold')),
                sg.Text(key="-TEXT1-", font=('Arial', 14))
            ],
            [
                sg.Text("Nazwisko", font=('Arial', 14, 'bold')),
                sg.Text(key="-TEXT2-", font=('Arial', 14))
            ]
        ]
        
        # Główny layout
        user_layout = [
            [sg.Frame('Dane użytkownika', frame)],
            [
                sg.Text("Wybrana tabela:"),
                sg.Combo(tab_options, default_value = "" if len(tab_options) == 0 else tab_options[0], key="-TABS_NAMES_COMBO-", enable_events=True, size=(20,1), readonly=True),
                sg.Button("Pokaż tabelę")
            ],
            [                
                sg.Button("Dodaj tabelę"),
                sg.Button("Wykresy"),
                sg.Button("Finanse")
            ],
            [sg.Text(''), sg.Button("Powrót")]
        ]

        # Tworzenie okna
        user_window = sg.Window("Okno użytkownika", user_layout, size=(400, 200))

        # Ustawianie początkowych stanów i wartości
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
            elif event == 'Finanse':
                self.analyzeFinances()            

        user_window.close()

    def addTabLoop(self):
        add_tab_layout = [
            [
                sg.Text("Wybierz plik", font=('Arial', 14, 'bold'), key='-FILE_PATH-'),
                sg.FileBrowse(key='-BROWSE-')
            ],
            [sg.Checkbox("Dołącz do tabeli", tooltip="Wczytana tabela zostanie dołączona do tabeli już istniejącej", key="-JOIN_CHECK-", enable_events=True)],
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
        # Lokalne zmienne
        graph_types = ["kołowy", "słupkowy - zestawienie serii", "słupkowy - bilans finansów"]        
        options = self.interfejs.podajListeNazwTabWydatkow()

        start_date = None
        end_date = None
        selected_tabs = []
        selected_col = ''
        selected_col_vals = []
        canvas_fig = None

        # Kolumny layout'u
        lay_col_1 = [
            [sg.Text('Wybierz typ wykresu:')],
            [sg.Combo(graph_types, enable_events=True, key='-CB_GRAPH_TYPE-', default_value=graph_types[0], readonly=True)],
            [sg.Text('Wybierz tabele:')],
            [sg.Listbox(options, enable_events=True, select_mode='multiple', key='-LISTBOX-', size=(20, 3))],
            [sg.Text('Wybierz kolumny:')],
            [sg.Combo([], enable_events=True, key='-CB_COLS-', auto_size_text=True, size=(20, 10), readonly=True)],
            [sg.Text('Wybierz wartości:')],
            [sg.Listbox([], enable_events=True, select_mode='multiple', key='-LB_COL_VALS-', size=(20, 3))]
        ]

        lay_col_2 = [
            [sg.Checkbox("Sumowanie wartości", key="-SUM_CHECK-", enable_events=True, tooltip="Jeśli zaznaczone: sumuje wartości z kolumny wartości.\nW przeciwnym wypadku zlicza wystąpienia")],
            [sg.Text('Wybierz kolumnę wartości do sumowania:')],
            [sg.Combo([], enable_events=True, key='-CB_COL_FOR_VALS-', auto_size_text=True, size=(20, 10), disabled=True, readonly=True)],
            [sg.Text('Wybrane opcje:')],
            [sg.Output(size=(30, 10), key='-OUTPUT-')],
            [
                sg.Button('Rysuj', key='-RYSUJ-', disabled=True),
                sg.Button('Wyczyść', key='-CLEAR-'),
                sg.Button('Zamknij')
            ]
        ]

        lay_row_12 = []
        self.addDateChoiceStruct(lay_row_12)

        lay_col_3 = [[sg.Canvas(size=(400, 400), key='-CANVAS-')]] 

        # Utworzenie głównego layout'u dla okna
        layout = [
            [
                sg.Column(lay_col_1),
                sg.Column(lay_col_2),
                lay_row_12,
                sg.Column(lay_col_3)
            ]
        ]

        # Utworzenie okna
        graphs_window = sg.Window('Wykresy', layout, finalize=True)               

        # Główna pętla metody
        while True:
            event, values = graphs_window.read()
            
            if event == sg.WINDOW_CLOSED or event == 'Zamknij':
                break
            
            # Obsługa zdarzenia wyboru elementu w liście tabel
            if event == '-LISTBOX-':
                selected_tabs = values['-LISTBOX-']

                # Aktualizacja listy z nazwami kolumn
                if bool(selected_tabs): self.adjustBindedGUIElems(graphs_window, combos_to_update=['-CB_COLS-'], 
                                                                  combos_new_vals=[self.interfejs.podajUnikatoweNazwyKol(selected_tabs)],
                                                                  combos_to_clear=['-LB_COL_VALS-']
                                                                  )
                else:  
                    self.adjustBindedGUIElems(graphs_window, combos_to_clear=['-CB_COLS-', '-LB_COL_VALS-'])

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
                    self.adjustBindedGUIElems(graphs_window, combos_to_update=['-LB_COL_VALS-'], 
                                            combos_new_vals=[self.interfejs.podajUnikatoweWartZKol(selected_tabs, selected_col)]
                                            )
                    
                    graphs_window['-RYSUJ-'].update(disabled=False)
                    # Wyświetlenie aktualnie wybranych opcji            
                    graphs_window['-OUTPUT-'].update('')
                    print("Wybrane tabele:\n",selected_tabs, '\n')
                    print("Wybrana kolumna:\n",selected_col, '\n')
                    print("Wybrane wartości kolumn:\n",selected_col_vals, '\n')
                
            if event == '-LB_COL_VALS-':
                selected_col_vals = values['-LB_COL_VALS-'] 

                # Wyświetlenie aktualnie wybranych opcji                
                graphs_window['-OUTPUT-'].update('')
                print("Wybrane tabele:\n",selected_tabs, '\n')
                print("Wybrana kolumna:\n",selected_col, '\n')
                print("Wybrane wartości kolumn:\n",selected_col_vals, '\n')

            if event == '-SUM_CHECK-':
                if not values['-SUM_CHECK-'] and bool(selected_tabs) and selected_col != '' and bool(selected_col_vals) and canvas_fig is not None:
                    # Jeśli wcześniej był narysowany wykres zsumowanych wartości, to po odznaczeniu opcji sumowania od razu rysowany jest wykres zliczeń
                    self.adjustBindedGUIElems(graphs_window, elems_to_disable=['-CB_COL_FOR_VALS-'], combos_to_clear=['-CB_COL_FOR_VALS-'])
                    canvas = graphs_window['-CANVAS-'].TKCanvas
                    etykiety, dane = self.interfejs.podajDaneDoWykresu(selected_tabs, selected_col, values['-CB_COL_FOR_VALS-'], etykiety_kol=selected_col_vals)
                    canvas_fig.get_tk_widget().destroy()
                    canvas_fig = None
                    plt.close('all')
                    canvas_fig = self.drawGraph(canvas, self.createPieChart(etykiety, dane))

                elif values['-SUM_CHECK-'] and bool(selected_tabs):
                    self.adjustBindedGUIElems(graphs_window, elems_to_enable=['-CB_COL_FOR_VALS-'], combos_to_update=['-CB_COL_FOR_VALS-'], combos_new_vals=[self.interfejs.podajUnikatNazwyKolNumer(selected_tabs)])

                else:
                    self.adjustBindedGUIElems(graphs_window, elems_to_disable=['-CB_COL_FOR_VALS-'], combos_to_clear=['-CB_COL_FOR_VALS-'])

            if event == '-RYSUJ-':                
                #TODO:
                #   trzeba sprawdzić, czy są zaznaczone wszystkie potrzebne opcje
                if (values['-START_DATE-'] and not str(values['-INPUT_START_YEAR-']).isdecimal()) or (values['-END_DATE-'] and not str(values['-INPUT_END_YEAR-']).isdecimal()):
                    sg.popup('Podany rok musi być liczbą całkowitą!')
                    continue

                if values['-START_DATE-']:
                    year = int(values['-INPUT_START_YEAR-'])
                    month = values['-CB_START_MONTH-'] if values['-CB_START_MONTH-'] != '-' else 1
                    start_date = dtm.datetime(
                        year,
                        month,
                        values['-CB_START_DAY-'] if values['-CB_START_DAY-'] != '-' else 1,
                        values['-CB_START_HOUR-'] if values['-CB_START_HOUR-'] != '-' else 0,
                        values['-CB_START_MIN-'] if values['-CB_START_MIN-'] != '-' else 0,
                        values['-CB_START_SEC-'] if values['-CB_START_SEC-'] != '-' else 0
                    )

                if values['-END_DATE-']:
                    year = int(values['-INPUT_END_YEAR-'])
                    month = values['-CB_END_MONTH-'] if values['-CB_END_MONTH-'] != '-' else 12
                    _, day = cld.monthrange(year, month)
                    day = values['-CB_END_DAY-'] if values['-CB_END_DAY-'] != '-' else day
                    end_date = dtm.datetime(
                        year,
                        month,
                        day,
                        values['-CB_END_HOUR-'] if values['-CB_END_HOUR-'] != '-' else 23,
                        values['-CB_END_MIN-'] if values['-CB_END_MIN-'] != '-' else 59,
                        values['-CB_END_SEC-'] if values['-CB_END_SEC-'] != '-' else 59
                    )

                if start_date is not None and end_date is not None and start_date > end_date:
                    sg.popup('Początkowa data musi być wcześniejsza!')
                    continue

                if values['-CB_GRAPH_TYPE-'] == 'kołowy':
                    [etykiety, dane] = self.interfejs.podajDaneDoWykresu(selected_tabs, selected_col, etykiety_kol=selected_col_vals, start_date=start_date, end_date=end_date) if not values['-SUM_CHECK-'] else self.interfejs.podajDaneDoWykresu(selected_tabs, selected_col, values['-CB_COL_FOR_VALS-'], etykiety_kol=selected_col_vals, sumuj=True, start_date=start_date, end_date=end_date)
                    canvas = graphs_window['-CANVAS-'].TKCanvas
                    if canvas_fig is not None: 
                        canvas_fig.get_tk_widget().destroy()
                        canvas_fig = None
                        plt.close('all')
                    canvas_fig = self.drawGraph(canvas, self.createPieChart(etykiety, dane))

                if values['-CB_GRAPH_TYPE-'] == 'słupkowy':
                    pass

            if event == '-CLEAR-':
                if canvas_fig is not None: 
                    canvas_fig.get_tk_widget().destroy()
                    canvas_fig = None
                    plt.close('all')

            if event == '-START_DATE-':
                if values['-START_DATE-']: 
                    self.adjustBindedGUIElems(graphs_window, ['-CB_START_DAY-', '-CB_START_MONTH-', '-INPUT_START_YEAR-', '-CB_START_HOUR-', '-CB_START_MIN-', '-CB_START_SEC-'])
                    start_date = dtm.datetime(
                        int(values['-INPUT_START_YEAR-']),
                        values['-CB_START_MONTH-'] if values['-CB_START_MONTH-'] != '-' else 1,
                        values['-CB_START_DAY-'] if values['-CB_START_DAY-'] != '-' else 1,
                        values['-CB_START_HOUR-'] if values['-CB_START_HOUR-'] != '-' else 0,
                        values['-CB_START_MIN-'] if values['-CB_START_MIN-'] != '-' else 0,
                        values['-CB_START_SEC-'] if values['-CB_START_SEC-'] != '-' else 0
                    )                    
                else: 
                    self.adjustBindedGUIElems(graphs_window, elems_to_disable=['-CB_START_DAY-', '-CB_START_MONTH-', '-INPUT_START_YEAR-', '-CB_START_HOUR-', '-CB_START_MIN-', '-CB_START_SEC-'])
                    start_date = None

            if event == '-END_DATE-':
                if values['-END_DATE-']: 
                    self.adjustBindedGUIElems(graphs_window, ['-CB_END_DAY-', '-CB_END_MONTH-', '-INPUT_END_YEAR-', '-CB_END_HOUR-', '-CB_END_MIN-', '-CB_END_SEC-'])
                    year = int(values['-INPUT_END_YEAR-'])
                    month = values['-CB_END_MONTH-'] if values['-CB_END_MONTH-'] != '-' else 12
                    _, day = cld.monthrange(year, month)
                    day = values['-CB_END_DAY-'] if values['-CB_END_DAY-'] != '-' else day
                    end_date = dtm.datetime(
                        year,
                        month,
                        day,
                        values['-CB_END_HOUR-'] if values['-CB_END_HOUR-'] != '-' else 23,
                        values['-CB_END_MIN-'] if values['-CB_END_MIN-'] != '-' else 59,
                        values['-CB_END_SEC-'] if values['-CB_END_SEC-'] != '-' else 59
                    )
                else: 
                    self.adjustBindedGUIElems(graphs_window, elems_to_disable=['-CB_END_DAY-', '-CB_END_MONTH-', '-INPUT_END_YEAR-', '-CB_END_HOUR-', '-CB_END_MIN-', '-CB_END_SEC-'])
                    end_date = None
            
            if event == '-CB_START_MONTH-':
                # Sprawdzenie poprawności podanego roku
                if str(values['-INPUT_START_YEAR-']).isdecimal(): year = int(values['-INPUT_START_YEAR-'])
                else:
                    sg.popup("Rok musi być liczbą całkowitą!")
                    continue

                if values['-CB_START_MONTH-'] == '-': graphs_window['-CB_START_DAY-'].update(disabled=True)
                else:
                    _, max_day = cld.monthrange(year, values['-CB_START_MONTH-'])
                    new_vals = [i for i in range(1, max_day + 1)]
                    new_vals.append('-')
                    graphs_window['-CB_START_DAY-'].update(values=new_vals, value=new_vals[0], disabled=False)

            if event == '-CB_END_MONTH-':
                # Sprawdzenie poprawności podanego roku
                if str(values['-INPUT_END_YEAR-']).isdecimal(): year = int(values['-INPUT_END_YEAR-'])
                else:
                    sg.popup("Rok musi być liczbą całkowitą!")
                    continue

                if values['-CB_END_MONTH-'] == '-': graphs_window['-CB_END_DAY-'].update(disabled=True)
                else:
                    _, max_day = cld.monthrange(year, values['-CB_END_MONTH-'])
                    new_vals = [i for i in range(1, max_day + 1)]
                    new_vals.append('-')
                    graphs_window['-CB_END_DAY-'].update(values=new_vals, value=new_vals[0], disabled=False)

        # Zamknięcie okna
        graphs_window.close()

    def analyzeFinances(self):
        updating_flag = True # flaga wskazująca, czy wątek uaktualniania konta ma się wykonywać
        options = self.interfejs.podajListeNazwTabWydatkow()
        output = {}

        # Pobieranie tabeli do wydrukowania
        df = self.interfejs.podajTabWydatki(options[0])
        data_rows = df.values.tolist()
        headers = df.columns.tolist()
        
        # kolumny layout'u
        lay_col_1 = [
            [
                sg.Radio('Dodaj przychód', 'rodzaj', key='-PRZYCHOD-', enable_events=True), 
                sg.Radio('Dodaj wydatek', 'rodzaj', key='-WYDATEK-', default=True, enable_events=True)
            ],
            [sg.Combo(options, options[0], enable_events=True, key='-COMBO-', tooltip="", readonly=True)],
            [
                sg.Button('Wczytaj dane', key='-WCZYTAJ-'),
                sg.Button('Dodaj pozycje', key='-DODAJ-')
            ],
            [sg.Button('Zamknij')]
        ]

        options.append('Przychody')
        lay_col_2 = [
            [sg.Text("Stan konta: "), sg.Text(str(self.interfejs.uaktualnianieKonta(dtm.datetime.now())))],
            [sg.Combo(options, options[0], enable_events=True, key='-COMBO_DISP-', tooltip="", readonly=True)],
            [sg.Table(values=data_rows, headings=headers, justification='left', num_rows=10, key='-TABLE-')]
        ]

        # główny layout
        layout = [
            [sg.Column(lay_col_1), sg.Column(lay_col_2)]
        ]

        # Utworzenie okna
        finances_window = sg.Window('Finanse', layout, finalize=False)
        finances_window.finalize()

        while True:
            event, values = finances_window.read()
            
            if event == sg.WINDOW_CLOSED or event == 'Zamknij':
                break

            if event == '-WCZYTAJ-':
                fields = self.interfejs.podajNazwyKolTabWydatkow(values['-COMBO-'])
                self.customInputDataWindow(output, fields)

            if event == '-PRZYCHOD-': finances_window['-COMBO-'].update(disabled=True)

            if event == '-WYDATEK-': finances_window['-COMBO-'].update(disabled=False)

            if event == '-COMBO_DISP-':
                # Pobieranie tabeli do wydrukowania
                df = self.interfejs.podajTabWydatki(values['-COMBO_DISP-'])
                data_rows = df.values.tolist()
                headers = df.columns.tolist()
                data_rows = [[headers[i] for i in range(len(headers))]] + data_rows
                finances_window['-TABLE-'].Update(values=data_rows)

        # Zamknięcie okna
        finances_window.close()

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
            Lista nazw elementów typu PySimpleGUI.Combo lub PySimpleGUI.Listbox do zaktualizowania zawartych opcji

        combos_new_vals : list()
            Zawiera listę z nowymi opcjami dla każdego elementu z combos_to_update. Jeżeli zawiera mniej list wartości niż elementów
            z combos_to_update to ostatnia lista nowych opcji jest przypisywana dla wszystkich pozostałych obiektów PySimpleGUI.Combo

        combos_to_clear : list()
            Lista nazw elementów typu PySimpleGUI.Combo do całkowitego usunięcia zawartych opcji
        """

        for elem in elems_to_enable: window[elem].update(disabled=False)        
        for elem in elems_to_visible: window[elem].update(visible=True)
        for elem in elems_to_invisible: window[elem].update(visible=False)
        for combo in combos_to_clear: window[combo].update(values='')
        for elem in elems_to_disable: window[elem].update(disabled=True)     

        #TODO: 
        #   Uwzględnić, który element w aktualizowanych Combo listach ma być ustawiony jako domyślny.
        for idx in range(len(combos_to_update)): 
            new_vals = combos_new_vals[idx if len(combos_new_vals) > idx else (len(combos_new_vals) - 1)]
            if isinstance(window[combos_to_update[idx]], sg.Combo): window[combos_to_update[idx]].update(values=new_vals, value = new_vals[0] if bool(new_vals) else '')
            else: window[combos_to_update[idx]].update(values=new_vals)

    def customInputDataWindow(self, output = {}, fields = []):
        """ Metoda pomocnicza, która umożliwia podanie przez użytkownika danych wtedy, gdy liczba pól
        wejścia nie jest stała.
        """

        end_flag = False
        layout = []        
        for field in fields:
            layout.append([sg.Text(f'{field}:'), sg.Input(key=field)])

        layout.append([sg.Button('Wczytaj dane'), sg.Button('Wstecz')])

        # Utworzenie okna
        window = sg.Window('Finanse', layout, finalize=True)

        while True:
            event, values = window.read()
            
            if event == sg.WINDOW_CLOSED or event == 'Wstecz' or end_flag:
                output = {}
                break
            if event == 'Wczytaj dane':
                output = {}
                end_flag = True
                for field in fields:
                    tmp = values[field]
                    if tmp == '':
                        end_flag = False
                        sg.popup(f'Nie podano wartości dla pola: {field}')
                        break
                    output[field] = tmp                

        # Zamknięcie okna
        window.close()                

    def drawGraph(self, canvas, figure):
        figure_canvas_agg = FigCanvTk(figure, canvas)
        figure_canvas_agg.draw()
        figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
        return figure_canvas_agg
    
    def createPieChart(self, labels, sizes, autopct='%1.2f%%'):
        # Utworzenie wykresu kołowego
        plt.pie(sizes, labels=labels, autopct=autopct, startangle=90)
        plt.axis('equal')
        return plt.gcf()
    
    def addDateChoiceStruct(self, layout: list()):
        days = [i for i in range(1, 32)]
        days.append('-')
        months = [i for i in range(1, 13)]
        months.append('-')
        hours = [i for i in range(0, 24)]
        hours.append('-')
        mins_secs = [i for i in range(0, 60)]
        mins_secs.append('-')

        layout.append([sg.Checkbox("Podaj początkową datę (dd-mm-yyyy  hh-mm-ss)", key="-START_DATE-", enable_events=True)])
        layout.append(
            [
                sg.Combo(days, days[0], enable_events=True, key='-CB_START_DAY-', auto_size_text=True, size=(4, 10), disabled=True, readonly=True),
                sg.Text(' - '),
                sg.Combo(months, months[0], enable_events=True, key='-CB_START_MONTH-', auto_size_text=True, size=(10, 10), disabled=True, readonly=True),
                sg.Text(' - '),
                sg.Input(str(dtm.date.today().year), key='-INPUT_START_YEAR-', size=(15, 1), disabled=True, enable_events=True),
                sg.Text('   '),
                sg.Combo(hours, hours[0], enable_events=True, key='-CB_START_HOUR-', auto_size_text=True, size=(4, 10), disabled=True, readonly=True),
                sg.Text(' : '),
                sg.Combo(mins_secs, mins_secs[0], enable_events=True, key='-CB_START_MIN-', auto_size_text=True, size=(4, 10), disabled=True, readonly=True),
                sg.Text(' : '),
                sg.Combo(mins_secs, mins_secs[0], enable_events=True, key='-CB_START_SEC-', auto_size_text=True, size=(4, 10), disabled=True, readonly=True)
            ]
        )

        layout.append([sg.Checkbox("Podaj końcową datę (dd-mm-yyyy  hh-mm-ss)", key="-END_DATE-", enable_events=True)])
        layout.append(
            [
                sg.Combo(days, days[0], enable_events=True, key='-CB_END_DAY-', auto_size_text=True, size=(4, 10), disabled=True, readonly=True),
                sg.Text(' - '),
                sg.Combo(months, months[0], enable_events=True, key='-CB_END_MONTH-', auto_size_text=True, size=(10, 10), disabled=True, readonly=True),
                sg.Text(' - '),
                sg.Input(str(dtm.date.today().year), key='-INPUT_END_YEAR-', size=(15, 1), disabled=True, enable_events=True),
                sg.Text('   '),
                sg.Combo(hours, hours[0], enable_events=True, key='-CB_END_HOUR-', auto_size_text=True, size=(4, 10), disabled=True, readonly=True),
                sg.Text(' : '),
                sg.Combo(mins_secs, mins_secs[0], enable_events=True, key='-CB_END_MIN-', auto_size_text=True, size=(4, 10), disabled=True, readonly=True),
                sg.Text(' : '),
                sg.Combo(mins_secs, mins_secs[0], enable_events=True, key='-CB_END_SEC-', auto_size_text=True, size=(4, 10), disabled=True, readonly=True)
            ]
        )