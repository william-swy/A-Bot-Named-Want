import sys
from model import utils

# sets bot command prefix
if __name__ == "__main__":

    while True:
        prefix = input("Input one letter prefix to invoke bot command:")
        if len(prefix) == 1:
            break
        print("Inputted prefix was not one letter long, try again")

    with open(utils.DATA_DIR + "\\prefix.txt", 'w') as file:
        file.write(str(prefix))
        print("Prefix " + prefix + " successfully set")

