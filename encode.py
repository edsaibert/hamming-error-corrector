import sys
from encodeFunctions import *

def main():
    filename = sys.argv[1]
    encode(filename)

if __name__ == "__main__":
    print("encoding...")
    main()
