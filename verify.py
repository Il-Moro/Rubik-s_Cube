from permutation import permutation
from viewCube import print_cubo


# /-------------------- verify permutations --------------------\

if __name__ == "__main__":
    mosse, perm = permutation()

    Stato = [i for i in range(24)]
    print_cubo(Stato)

    while(True):
        move = input("Inserire mossa: ")

        if(move == "s"):
            break;

        Stato = [Stato[i] for i in perm[move]]
        print_cubo(Stato, True)
        print_cubo(Stato)

# /-------------------------------------------------------------\
    