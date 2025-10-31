from z3 import *

# /-------------------------------------------------------------\

DEPTH = 3
N_STICKER = 24
N_MOV = 12

# /-------------------------------------------------------------\

# ogni perm[j][k] = indice dello sticker in S[i] che va in posizione k dopo la mossa j
perm = { 
    "U":
    [
        2, 0, 3, 1,
        8, 9, 6, 7,
        12, 13, 10, 11, 
        16, 17, 14, 15,
        4, 5, 18, 19,
        20, 21, 22, 23
    ],
    
     "F":
    [
        0, 1, 7, 5,   # U→F: gli sticker inferiori di U vanno su F (ma invertiti)
        4, 20, 6, 21, # L→U e D→L
        10, 8, 11, 9, # F ruota orario
        2, 13, 3, 15,
        16, 17, 18, 19,
        14, 12, 22, 23
    ],
     
    "R":
    [
        0, 9, 2, 11,   # U→B
        4, 5, 6, 7,
        8, 21, 10, 23,   # F→U
        14, 12, 15, 13,   # R ruota orario
        3, 17, 1, 19,   # B→D
        20, 18, 22, 16
    ],
    
    "L":
    [
        19, 1, 17, 3,   # F→U
        6, 4, 7, 5,       # L ruota orario
        0, 9, 2, 11,    # D→F
        12, 13, 14, 15,
        16, 22, 18, 20,     # U→B
        8, 21, 10, 23
    ], 
    
    "B":
    [
        13, 15, 2, 3,
        1, 5, 0, 6,
        8, 9, 10, 11,
        12, 23, 14, 22,
        18, 16, 19, 17,   # B ruota orario
        20, 21, 15, 13      # scambio D e L (parte dietro)
    ], 
    
    "D":
    [
        0, 1, 2, 3,
        4, 5, 18, 19,
        8, 9, 6, 7,
        12, 13, 10, 11,
        16, 17, 14, 15,
        22, 20, 23, 21
    ]
}

# /-------------------------------------------------------------\

def variabili_di_stato():
    # i -> i-esimo stato
    # j -> j-esimo sticker
    return [[Int(f"S_{i}_{j}") for j in range(N_STICKER)] for i in range(DEPTH + 1)]

def variabili_di_transizione():
    # una transizione per ogni passo 
    return [Int(f"T_{i}") for i in range(DEPTH)]


def stato_iniziale(s, S):
    seq = input("Inserire sequenza di mosse:\n\t - ").strip().upper()
    print("Sequenza:", seq)

    # cubo risolto
    stato = list(range(N_STICKER))

    print_cubo(stato)

    # applico le permutazioni
    for ch in seq:
        if ch not in perm:
            print(f"Mossa '{ch}' ignorata (non valida)")
            continue
        stato = [stato[perm[ch][k]] for k in range(N_STICKER)]

        print_cubo(stato)


    # aggiungo i vincoli allo stato iniziale
    for j in range(N_STICKER):
        s.add(S[0][j] == stato[j])

    return s



def print_cubo(stato):
    """
    Stampa un cubo 2x2 dato un vettore di 24 sticker.
    Ogni sticker è rappresentato dal suo indice (0-23) o colore.
    """
    # Utility per stampare una riga con offset
    def riga(offset, vals):
        print(" " * offset + " ".join(f"{v:02}" for v in vals))

    print("\nStato del cubo:\n")

    # U
    riga(6, stato[0:2])
    riga(6, stato[2:4])

    # L, F, R, B
    for r in range(2):
        print(" ".join(
            f"{v:02}" for v in stato[4 + 4*0 + 2*r : 4 + 4*0 + 2*r + 2] +  
            stato[8 + 4*0 + 2*r : 8 + 4*0 + 2*r + 2] +                    
            stato[12 + 4*0 + 2*r : 12 + 4*0 + 2*r + 2] +                  
            stato[16 + 4*0 + 2*r : 16 + 4*0 + 2*r + 2]                    
        ))

    # D
    riga(6, stato[20:22])
    riga(6, stato[22:24])
    print()





if __name__=='__main__':

    print("\t\tManual\n\nDescrizione\n\tRisolutore del cubo di Rubik 2x2\n\nMosse possibili:\n\t - U, upper clockwise\n\t - L, left clockwise\n\t - F, front clockwise\n\t - R, right clockwise\n\t - B, back clockwise\n\t - D, down clockwise\n\n")

    print("Usage\n\t Inserire una sequenza di mosse per modificare il cubo\n\t - example: UBBUDRL\n\n")


    s = Solver()
    S = variabili_di_stato()    
    T = variabili_di_transizione()

    s = stato_iniziale(s, S)

    # STATO FINALE (cubo risolto)
    # Qui ad esempio lo mettiamo uguale allo stato iniziale
    for j in range(N_STICKER):
        s.add(S[DEPTH][j] == j)


    # Vincoli di dominio
    # Per ogni sticker, 0 <= sticker < N_STICKER
    for i in range(DEPTH + 1):
        for j in range(N_STICKER):
            s.add(And(S[i][j] >= 0, S[i][j] < N_STICKER))

    # Per ogni transizione, 0 <= transizione < N_MOV
    for i in range(DEPTH):
        s.add(And(T[i] >= 0, T[i] < N_MOV))

    # Vincoli di unicità (sticker distinti)
    for i in range(DEPTH + 1):
        s.add(Distinct(S[i]))
    #### RICONTROLLARE


    # TRANSIZIONI
    for step in range(DEPTH):
        for k in range(N_STICKER):
            expr = S[step][k]
            # creiamo la cascata di If per collegare transizione -> permutazione
            for mov in range(N_MOV):
                expr = If(T[step] == mov, S[step][perm[mov][k]], expr)
            s.add(S[step+1][k] == expr)


    # ESECUZIONE
    if s.check() == sat:
        m = s.model()
        print("Transizioni scelte:")
        for i in range(DEPTH):
            print(f"Step {i} -> T = {m[T[i]]}")
    else:
        print("Nessuna soluzione trovata.")


