from z3 import *

DEPTH = 3
N_STICKER = 24
N_MOV = 12


# ogni perm[j][k] = indice dello sticker in S[i] che va in posizione k dopo la mossa j
perm_U = { "U":
    [
        2, 0, 1, 3,
        8, 9, 6, 7,
        12, 13, 10, 11, 
        16, 17, 14, 15,
        4, 5, 18, 19,
        20, 21, 22, 23
    ]
}

perm_F = { "F":
    [
        0, 1, 7, 5,   # U→F: gli sticker inferiori di U vanno su F (ma invertiti)
        4, 20, 6, 21, # L→U e D→L
        10, 8, 9, 11, # F ruota orario
        2, 13, 3, 15,
        16, 17, 18, 19,
        14, 12, 22, 23
    ]
}

perm_R = { "R":
    [
        0, 9, 2, 11,   # U→B
        4, 5, 6, 7,
        8, 21, 10, 23,   # F→U
        14, 12, 13, 15,   # R ruota orario
        3, 17, 1, 19,   # B→D
        20, 18, 22, 16
    ]
}

perm_L = { "L":
    [
        19, 1, 17, 3,   # F→U
        6, 4, 5, 7,       # L ruota orario
        0, 9, 2, 11,    # D→F
        12, 13, 14, 15,
        16, 22, 18, 20,     # U→B
        8, 21, 10, 23
    ]
}

perm_B = { "B":
    [
        13, 15, 2, 3,
        1, 5, 0, 6,
        8, 9, 10, 11,
        12, 23, 14, 22,
        18, 16, 17, 19,   # B ruota orario
        20, 21, 15, 13      # scambio D e L (parte dietro)
    ]
}

perm_D = { "D":
    [
        0, 1, 2, 3,
        4, 5, 18, 19,
        8, 9, 6, 7,
        12, 13, 10, 11,
        16, 17, 14, 15,
        22, 20, 21, 23
    ]
}

perm = {
    perm_U,
    perm_L,
    perm_F,
    perm_R,
    perm_B,
    perm_D    
}


def variabili_di_stato():
    # i -> i-esimo stato
    # j -> j-esimo sticker
    return [[Int(f"S_{i}_{j}") for j in range(N_STICKER)] for i in range(DEPTH + 1)]

def variabili_di_transizione():
    # una transizione per ogni passo 
    return [Int(f"T_{i}") for i in range(DEPTH)]


#### inizio solver

s = Solver()
S = variabili_di_stato()
T = variabili_di_transizione()

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


# STATO INIZIALE
def stato_iniziale():
    for j in range(N_STICKER):
        s.add(S[0][j] == j)
        print("\t\t Manual\n\nDescrizione\n\tRisolutore del cubo di Rubik 2x2:\n\nMosse possibili:\n\t - U = upper clockwise\n\t - L = left clockwise\n\t - F = front clockwise\n\t - B = back clockwise")



# STATO FINALE (cubo risolto)
# Qui ad esempio lo mettiamo uguale allo stato iniziale
for j in range(N_STICKER):
    s.add(S[DEPTH][j] == j)


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
