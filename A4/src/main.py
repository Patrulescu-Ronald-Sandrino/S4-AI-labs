import os.path

from src.domain.map import *


def main():
    map_filename: str = os.path.join('data', 'map.txt')
    map_instance: Map = MapFactory.from_text_file(map_filename)
    print(map_instance)
    # MapWriter.to_text_file(map_instance, os.path.join('data', 'map.txt'))


if __name__ == '__main__':
    main()


