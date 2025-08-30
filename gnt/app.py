import os
from typing import List
from datetime import datetime
from pathlib import Path
from random import sample
from dataclasses import dataclass

from textual import events
from textual.screen import Screen
from textual.containers import Horizontal, Vertical
from textual.reactive import reactive
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Button, Static, Label

from processors import Evaluator

GREEN_LIGHT = "🟢"
RED_LIGHT = "🔴"

class WordDisplay(Static):
    """ Widget to display word"""

class ResultsDisplay(Static):
    """ Widget to display results"""
    def __init__(self) -> None:
        super().__init__()
        self.rendered_result = Static("")

    def compose(self) -> None:
        yield self.rendered_result

class HistoryDisplay(Static):
    history = reactive(list, recompose=True)

    def __init__(self) -> None:
        super().__init__()
        self.history = []

    def add_to_history(self, new, classes):
        if len(self.history)>=10:
            self.history.pop(9)
        self.history = [(new, classes)] + self.history

    def compose(self) -> None:
        for i in self.history:
            yield Label(i[0], classes=i[1]) 

class ArtikelChoice(Static):
    """ Widget to display article options"""
    def __init__(self):
        super().__init__()
        self.word_display = WordDisplay("My Word")
        self.word_data = None
        self.word_translation_display = WordDisplay("My Translation")
        self.word_translation_display.visible = False

    def compose(self) -> ComposeResult:
        """Create article choice buttons"""
        yield self.word_display
        with Horizontal(classes="btn_row"):
            with Vertical(classes="btn_col"):
                yield Button("der", id="btn_der")
            with Vertical(classes="btn_col"):
                yield Button("die", id="btn_die")
            with Vertical(classes="btn_col"):
                yield Button("das", id="btn_das")
        yield self.word_translation_display

class ArtikelApp(App):
    """An app for quick practice of german articles"""

    DATA_FILE_NAME = "most_common_nouns.csv"
    SET_SIZE = 10
    CSS_PATH = "app.tcss"
    BINDINGS = [("d", "toggle_dark", "Toggle dark mode")]
    KEY_MAP = {
            "i": "der",
            "o": "die",
            "p": "das",
            }
    GENUS_COLOR_MAP = {
            "der": "der_label",
            "die": "die_label",
            "das": "das_label"
            }

    def __init__(self):
        super().__init__()
        self.daily_record_path = None
        self.words_dict = None
        self.artikel_choice = None
        self.results_box = None
        self.filter_mode = "n"

        

    def on_mount(self) -> None:
        """ Run on creation of app """
        self.data_file = Path(__file__).parent / "data" / self.DATA_FILE_NAME
        records_folder = Path(__file__).parent / "records"

        today = datetime.now().strftime("%Y-%m-%d.log")
        self.daily_record_path = records_folder / self.data_file.stem / today

        for d in [records_folder, records_folder / self.data_file.stem]:
            if not os.path.exists(d):
                os.mkdir(d)

        with open(self.data_file, 'r', encoding='utf8') as f:
            word_data = f.readlines()

        self.words_dict = {index: item.strip().split('\t') for index, item in enumerate(word_data)}

        for k, v in self.words_dict.items():
            self.words_dict[k] = {
                    'en': v[0].split(' ')[1],
                    'de artikel': v[1].split(' ')[0].lower() if ' ' in v[1] else v[1],
                    'de': v[1].split(' ')[1] if ' ' in v[1] else '',
                    }

    def compose(self) -> ComposeResult:
        """Create child widgets for the app"""
        yield Header()
        yield Footer()
        self.artikel_choice = ArtikelChoice()
        yield self.artikel_choice
        with Horizontal(classes="insight_row"):
            self.results_box = ResultsDisplay()
            yield self.results_box
            self.history_box = HistoryDisplay()
            yield self.history_box

    def action_toggle_dark(self) -> None:
        """Action to toggle dark mode """
        self.dark = not self.dark

    def on_button_pressed(self, event: Button.Pressed) -> None:        
        self._next_noun()

    def _next_noun(self) -> None:
        set_idx = sample(range(0,2000), self.SET_SIZE)
        selected_word = self.words_dict[set_idx[0]]

        self.history_box.add_to_history(
                new = self.artikel_choice.word_data['de artikel'] + \
                " " + \
                self.artikel_choice.word_data['de'] + \
                " - " + \
                self.artikel_choice.word_data['en']
                , 
                classes = self.GENUS_COLOR_MAP[
                    self.artikel_choice.word_data['de artikel']
                    ]) if self.artikel_choice.word_data else None

        self.current_id = set_idx[0]
        self.artikel_choice.word_display.update(selected_word['de'])
        self.artikel_choice.word_data = selected_word
        self.artikel_choice.word_translation_display.update(selected_word['en'])

    def on_key(self, event: events.Key) -> None:
        if self.artikel_choice.word_data is None:
            self._next_noun()

        if event.key in self.KEY_MAP:
            correct_choice = (self.KEY_MAP[event.key] == self.artikel_choice.word_data['de artikel'])
            with open(self.daily_record_path, 'a', encoding='utf8') as f:
                f.write(f"{self.current_id}\t{int(correct_choice)}\n")
            self._next_noun() if correct_choice else None

        if event.key == "w":
            self.artikel_choice.word_translation_display.visible = not self.artikel_choice.word_translation_display.visible  
        elif event.key == "e":
            #if not self.results_box.visible:
            evaluation = Evaluator.evaluate(self.data_file.stem)
            evaluation_list_out = evaluation[0:5] if len(evaluation)>=5 else evaluation
            evaluation_text = '\n'.join([f"{i[0]}\t{i[1]}" for i in evaluation_list_out])

            self.results_box.rendered_result.update(evaluation_text)
            #self.results_box.visible = not self.results_box.visible

class InputScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Input(placeholder="test input")


if __name__ == "__main__":
    app = ArtikelApp()
    app.run()
