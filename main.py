from z3 import *
from time import sleep
from permutation import permutation

# /-------------------------------------------------------------\





# /-------------------------------------------------------------\

DEPTH = 5
N_STICKER = 24
N_MOV = 12
mosse, perm = permutation() 

# /-------------------------------------------------------------\





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

    # applico le permutazioni
    for ch in seq:
        if ch not in perm:
            print(f"Mossa '{ch}' ignorata (non valida)")
            continue
        stato = [stato[perm[ch][k]] for k in range(N_STICKER)]

    # aggiungo i vincoli allo stato iniziale
    for j in range(N_STICKER):
        s.add(S[0][j] == stato[j])

    return s

# /-------------------------------------------------------------\





# /-------------------------------------------------------------\

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
    ###### -> dobbiamo modificare ad ogni stato i, i k-esimi elementi rispetto al i-1, mediante la permutazione in perm
    for passo in range(DEPTH):
        for sticker_id in range(N_STICKER):

            # valore predefinito: lo sticker rimane dove sta
            nuovo_valore = S[passo][sticker_id]

            # per ogni possibile mossa, costruiamo un If annidato
            for mossa_id, mossa_nome in enumerate(mosse):
                # Se la mossa scelta a questo passo è mossa_id,
                # allora lo sticker sticker_id del nuovo stato
                # viene da perm[mossa_nome][sticker_idx]
                nuovo_valore = If(
                    T[passo] == mossa_id,
                    S[passo][perm[mossa_nome][sticker_id]],
                    nuovo_valore
                )

            # il nuovo stato a (passo+1) deve rispettare questa relazione
            s.add(S[passo + 1][sticker_id] == nuovo_valore)



    # ESECUZIONE
    if s.check() == sat:
        m = s.model()
        print("Transizioni scelte:")
        for i in range(DEPTH):
            sleep(0.5)
            codicemossa = int(m[T[i]].as_long())  # converte il valore Z3 in int
            nome_mossa = mosse[codicemossa-1]
            print(f"Step {i}: {nome_mossa}")
    else:
        print("Nessuna soluzione trovata.")

# /-------------------------------------------------------------\