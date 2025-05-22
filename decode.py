import sys
from decodeFunctions import decode

def main():
    filename = sys.argv[1]
    decode(filename)

if __name__ == "__main__":
    print("decoding...")
    main()

