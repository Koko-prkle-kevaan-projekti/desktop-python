import tassu_tutka.argparse as ap

def main():
    options = ap.parse()
    print(options)
    if options.gui:
        print("JEEJEE")
        import tassu_tutka.gui as gui
        gui.user_interface()
        return

if __name__ == "__main__":
    main()
