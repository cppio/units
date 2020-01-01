from . import *


def run(source, target):
    try:
        print(convert(Value.parse(source), Unit.parse(target)))
    except ValueError as err:
        print(err)


def main():
    run(input("convert value: ").strip(), input("to unit: ").strip())


if __name__ == "__main__":
    main()
