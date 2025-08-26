import os
from datetime import datetime
from pathlib import Path
from random import sample

from processors import Evaluator
from textual import events
from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical, ScrollableContainer
from textual.widgets import Header, Footer, Button, Static

class WordDisplay(Static):
    """ Widget to display word"""

class ResultsDisplay(Static):
    """ Widget to display results"""
    def __init__(self) -> None:
        super().__init__()
        self.rendered_result = WordDisplay("PLACEHOLDER")

    def compose(self) -> None:
        yield self.rendered_result
    
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
        with Horizontal():
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
        self.results_box = ResultsDisplay()
        yield self.results_box

    def action_toggle_dark(self) -> None:
        """Action to toggle dark mode """
        self.dark = not self.dark

    def on_button_pressed(self, event: Button.Pressed) -> None:        
        self._next_noun()

    def _next_noun(self) -> None:
        set_idx = sample(range(0,2000), self.SET_SIZE)
        selected_word = self.words_dict[set_idx[0]]

        self.current_id = set_idx[0]
        self.artikel_choice.word_display.update(selected_word['de'])
        self.artikel_choice.word_data = selected_word
        self.artikel_choice.word_translation_display.update(selected_word['en'])

    def on_key(self, event: events.Key) -> None:
        if self.artikel_choice.word_data is None:
            self._next_noun()

        if event.key in self.KEY_MAP:
            if self.KEY_MAP[event.key] == self.artikel_choice.word_data['de artikel']:
                with open(self.daily_record_path, 'a', encoding='utf8') as f:
                    f.write(f"{self.current_id}\t1\n")
                self._next_noun()
            else:
                with open(self.daily_record_path, 'a', encoding='utf8') as f:
                    f.write(f"{self.current_id}\t0\n")

        if event.key == "w":
            self.artikel_choice.word_translation_display.visible = not self.artikel_choice.word_translation_display.visible  
        elif event.key == "e":
            #if not self.results_box.visible:
            evaluation = Evaluator.evaluate(self.data_file.stem)
            evaluation_list_out = evaluation[0:5] if len(evaluation)>=5 else evaluation
            evaluation_text = '\n'.join([f"{i[0]}\t{i[1]}" for i in evaluation_list_out])

            self.results_box.rendered_result.update(evaluation_text)
            #self.results_box.visible = not self.results_box.visible

if __name__ == "__main__":
    app = ArtikelApp()
    app.run()
