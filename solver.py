from z3 import *

DEPTH = 3
N_STICKER = 24
N_MOV = 12


# ogni perm[j][k] = indice dello sticker in S[i] che va in posizione k dopo la mossa j
perm_U = [
    2, 0, 3, 1,
    8, 9, 6, 7,
    12, 13, 10, 11, 
    16, 17, 14, 15,
    4, 5, 18, 19,
    20, 21, 22, 23
]

perm_F = [
    0, 1, 6, 7,   # U→F: gli sticker inferiori di U vanno su F (ma invertiti)
    4, 5, 20, 21, # L→U e D→L
    22, 23, 10, 8, # F ruota orario
    12, 13, 14, 15,
    16, 17, 18, 19
]

perm_R = [
    0, 1, 2, 19,   # U→B
    4, 5, 6, 7,
    8, 9, 10, 3,   # F→U
    14, 12, 15, 13,   # R ruota orario
    16, 17, 11, 18,   # B→D
    20, 21, 22, 23
]

perm_L = [
    8, 1, 10, 3,   # F→U
    6, 4, 7, 5,       # L ruota orario
    20, 9, 22, 11,    # D→F
    12, 13, 14, 15,
    0, 17, 2, 19,     # U→B
    16, 18, 21, 23
]

perm_B = [
    0, 1, 2, 3,
    4, 5, 6, 7,
    8, 9, 10, 11,
    12, 13, 14, 15,
    18, 16, 19, 17,   # B ruota orario
    5, 4, 21, 20      # scambio D e L (parte dietro)
]

perm_D = [
    0, 1, 2, 3,
    4, 5, 6, 7,
    10, 11, 8, 9,
    14, 15, 12, 13,
    18, 19, 16, 17,
    22, 20, 23, 21
]

perm = [
    perm_U,
    perm_L,
    perm_F,
    perm_R,
    perm_B,
    perm_D    
]


def variabili_di_stato():
    # i -> i-esimo stato
    # j -> j-esimo sticker
    return [[Int(f"S_{i}_{j}") for j in range(N_STICKER)] for i in range(DEPTH + 1)]

def variabili_di_transizione():
    # una transizione per ogni passo (non per ogni mossa)
    return [Int(f"T_{i}") for i in range(DEPTH)]


#### inizio solver

s = Solver()
S = variabili_di_stato()
T = variabili_di_transizione()

# Vincoli di dominio
for i in range(DEPTH + 1):
    for j in range(N_STICKER):
        s.add(And(S[i][j] >= 0, S[i][j] < N_STICKER))

for i in range(DEPTH):
    s.add(And(T[i] >= 0, T[i] < N_MOV))

# Vincoli di unicità (sticker distinti)
for i in range(DEPTH + 1):
    s.add(Distinct(S[i]))

# STATO INIZIALE
for j in range(N_STICKER):
    s.add(S[0][j] == j)

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
