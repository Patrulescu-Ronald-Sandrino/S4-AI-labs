from UI import UI
# from domain.Map import Map
#  fixes: dummy = pickle.load(f) AttributeError: Can't get attribute; source: https://stackoverflow.com/a/68279928
from domain.Map import Map


def main() -> None:
    ui = UI()
    ui.run()


if __name__ == "__main__":
    main()
