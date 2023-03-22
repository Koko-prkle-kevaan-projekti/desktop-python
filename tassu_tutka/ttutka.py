import tassu_tutka.argparse as ap

def main():
    options = ap.parse()
    print(options)
    if hasattr(options, "gui") and options.gui:
        import tassu_tutka.gui as gui
        gui.user_interface()
        return
    elif hasattr(options, "start") and options.start == "start":
        import tassu_tutka.server as sr
        sr.serve()

if __name__ == "__main__":
    main()
