import argparse
import sys

def main():
    """Main entry point for the pyeverything package."""
    parser = argparse.ArgumentParser(
        description="A command-line interface for Everything."
    )
    subparsers = parser.add_subparsers(dest="command")

    # TUI command
    tui_parser = subparsers.add_parser("tui", help="Run the Textual TUI application.")

    # If no arguments are provided, print the help message
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args()

    if args.command == "tui":
        from pyeverything.tui import EverythingTUI
        app = EverythingTUI()
        app.run()

if __name__ == "__main__":
    main()