import control
import game_master.fileManager


class Item:
    def __init__(self):
        self.__bgp = []
        self.button_list = [0]
        self.surface_button_list = [0]
        self.box_list = [0]
        self.surface_box_list = [0]
        self.button = control.button.Button()
        self.surfaceButton = control.button.SurfaceButton()
        self.textBox = control.textBox.TextBox()
        self.surfaceTextBox = control.textBox.SurfaceTextBox()
        self.load()

    def load(self):
        item = game_master.fileManager.loading_item()
