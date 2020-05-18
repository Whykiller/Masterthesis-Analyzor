import PySimpleGUI as sg
import alsort

"""Project created for my Man ZZ; Copyright: don't know much about legal studies..., don't know much about
anything..."""


class Gui:
    """Defines a simple gui to input your paths and such"""
    def __init__(self):
        self.al_sort = alsort.AlphabeticSort
        self.create_gui()

    def create_gui(self):

        # Define Theme
        sg.theme("DarkAmber")

        # Define Layout
        layout = [
            [sg.Text("Choose your file:")],
            [sg.Input(), sg.FileBrowse()],
            [sg.Text("Choose output location:")],
            [sg.Input(), sg.FolderBrowse()],
            [sg.Text("Plot cutoff"), sg.InputText("10")],
            [sg.Text("Zipf cutoff"), sg.InputText("100")],
            [sg.Submit(), sg.Cancel()]
        ]

        # Define Window
        window = sg.Window("Masterthesis Analyzor", layout)

        # Gets the data if submit is pressed or closes the window if exit or cancel
        while True:
            event, values = window.read()
            if event in (None, "Cancel"):
                break
            if event == "Submit":
                self.al_sort(path=values[0], path_save=values[1], plot_cutoff=values[2], z_cutoff=values[3])
                break

        window.close()


if __name__ == "__main__":
    main = Gui
    main()
