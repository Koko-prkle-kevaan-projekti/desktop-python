import src.argparse as ap

def main():
    options = ap.parse()
    print(options)
    if options.gui:
        print("JEEJEE")
        import src.gui as gui
        gui.user_interface()
        return

if __name__ == "__main__":
    main()
