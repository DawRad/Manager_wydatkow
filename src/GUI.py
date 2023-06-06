from Interfejs import Interfejs
import PySimpleGUI as sg

class MainWindow:
    def __init__(self, interfejs: Interfejs) -> None:
        self.interfejs = interfejs

        options = self.interfejs.podajListePosiadaczy()
        layout = [
            [sg.Text("Wybierz użytkownika")],
            [sg.Combo(options, key='-COMBO-', default_value=options[0] if len(options) != 0 else "", enable_events=True)],
            [sg.Button("Dalej"), sg.Button("Dodaj nowego")]
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

            if event == sg.WINDOW_CLOSED:
                break

            elif event == 'Dalej':
                selected_option, selected_option_idx = values['-COMBO-'], interfejs.podajListePosiadaczy().index(values['-COMBO-'])
                sg.popup(f'Selected Option: {selected_option}, Selected idx: {selected_option_idx}')

                self.interfejs.przejdzNaPoz(selected_option_idx)
                
                window.hide()
                self.userWindowLoop()                
                window.un_hide()

        # Close the window
        window.close()

    def userWindowLoop(self):
        tab_options = self.interfejs.podajListeNazwTabWydatkow()
        user_layout = [
            [
                sg.Text("Imie", font=('Arial', 14, 'bold')), 
                sg.Text(key="-TEXT1-", font=('Arial', 14)), 
                sg.Text("Nazwisko", font=('Arial', 14, 'bold')), 
                sg.Text(key="-TEXT2-", font=('Arial', 14))
            ],
            [sg.Combo(self.interfejs.podajListeNazwTabWydatkow(), key="-TABS_NAMES_COMBO-", enable_events=True)],
            [
                sg.Button("Pokaż tabelę"),
                sg.Button("Dodaj tabelę")
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
            elif event == 'Pokaż tabelę':
                pass

        user_window.close()

    def addTabLoop(self):
        add_tab_layout = [
            [
                sg.Text("Wybrany plik", font=('Arial', 14, 'bold'), key='-FILE_PATH-'),
                sg.FileBrowse(key='-BROWSE-')
            ],
            [sg.Checkbox("Dołącz do tabeli", metadata="Wczytana tabela zostanie dołączona do tabeli już istniejącej", key="-JOIN_CHECK-")],
            [
                sg.Text("Nazwa tabeli", key='-SUBMIT_TEXT-', visible=False),
                sg.Input(key='-INPUT-', visible=False),
                sg.Button("Zatwierdź", key='-SUBMIT-', visible=False)
            ]
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
                    add_tab_window['-SUBMIT_TEXT-'].update(visible=True)
                    add_tab_window['-INPUT-'].update(visible=True)
                    add_tab_window['-SUBMIT-'].update(visible=True)

        add_tab_window.close()