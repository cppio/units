from . import *


def run(source, target):
    print(convert(Value.parse(source), Unit.parse(target)))


def main():
    run(input("convert value: ").strip(), input("to unit: ").strip())


if __name__ == "__main__":
    main()
