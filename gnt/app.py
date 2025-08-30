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
from models.article import DeArtikels
from models.worddict import WordDict

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
        self.selected_word = None

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
    CSS_PATH = "app.tcss"
    BINDINGS = [("d", "toggle_dark", "Toggle dark mode")]

    def __init__(self):
        super().__init__()
        self.daily_record_path = None
        self.words_dict = None
        self.artikel_choice = None
        self.results_box = None
        self.filter_mode = "n"

    def on_mount(self) -> None:
        """ Run on creation of app """
        data_folder = Path(__file__).parent / "data"
        records_folder = Path(__file__).parent / "records"

        today = datetime.now().strftime("%Y-%m-%d.log")
        self.daily_record_path = records_folder / 'default' / today

        for d in [records_folder, records_folder / 'default']:
            if not os.path.exists(d):
                os.mkdir(d)

        self.words_dict = WordDict.from_default_csv()

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
        previous_selected = self.artikel_choice.selected_word if self.artikel_choice else None
        selected_index, selected_word = self.words_dict.select_word()

        self.history_box.add_to_history(
                new = previous_selected.history_repr(), 
                classes = previous_selected.word_de_artikel.classes_key) if previous_selected else None

        self.current_id = selected_index
        self.artikel_choice.word_display.update(selected_word.word_de)
        self.artikel_choice.selected_word = selected_word
        self.artikel_choice.word_translation_display.update(selected_word.word_en)

    def on_key(self, event: events.Key) -> None:
        if self.artikel_choice.selected_word is None:
            self._next_noun()
            return 1

        if event.key in DeArtikels.keys():
            verify_result = self.words_dict.verify_index(self.current_id, DeArtikels.from_key(event.key))
            with open(self.daily_record_path, 'a', encoding='utf8') as f:
                f.write(f"{self.current_id}\t{int(verify_result)}\n")
            if verify_result:
                self._next_noun()
            return 1

        if event.key == "w":
            self.artikel_choice.word_translation_display.visible = not self.artikel_choice.word_translation_display.visible  
        elif event.key == "e":
            #if not self.results_box.visible:
            evaluation = Evaluator.evaluate('default')
            evaluation_list_out = evaluation[0:5] if len(evaluation)>=5 else evaluation
            evaluation_text = '\n'.join([f"{i[0]}\t{i[1]}" for i in evaluation_list_out])

            self.results_box.rendered_result.update(evaluation_text)
            #self.results_box.visible = not self.results_box.visible
        return 0

class InputScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Input(placeholder="test input")


if __name__ == "__main__":
    app = ArtikelApp()
    app.run()
