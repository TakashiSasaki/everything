from textual.app import App, ComposeResult
from textual.containers import Container
from textual.widgets import Header, Footer, Input, Button, RadioSet, RadioButton, DataTable

from pyeverything.everything import Everything

class EverythingTUI(App):
    """A Textual user interface for pyeverything."""

    CSS_PATH = "tui.css"

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        with Container(id="app-grid"):
            yield Input(placeholder="Search query")
            with RadioSet(id="method-selector"):
                yield RadioButton("DLL", id="dll", value=True)
                yield RadioButton("ES", id="es")
                yield RadioButton("HTTP", id="http")
            yield Button("Search", id="search")
            yield DataTable(id="results-table")
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Event handler called when a button is pressed."""
        if event.button.id == "search":
            self.run_search()

    def run_search(self) -> None:
        """Perform the search and update the results table."""
        query = self.query_one(Input).value
        method_selector = self.query_one(RadioSet)
        method = ""
        if method_selector.pressed_button.id == "dll":
            method = "dll"
        elif method_selector.pressed_button.id == "es":
            method = "es"
        elif method_selector.pressed_button.id == "http":
            method = "http"

        if query:
            # In a real app, you would handle the case where Everything is not running
            # or the method is not available.
            ev = Everything(method=method)
            results = ev.search(query)
            table = self.query_one(DataTable)
            table.clear(columns=True)
            if results:
                # Assuming all results have the same keys
                table.add_columns(*results[0].keys())
                for row in results:
                    # Ensure all values are strings for display
                    table.add_row(*[str(v) for v in row.values()])

if __name__ == "__main__":
    app = EverythingTUI()
    app.run()