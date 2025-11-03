from z3 import *
from time import sleep
from permutation import permutation
from viewCube import print_cubo

# /-------------------------------------------------------------\





# /-------------------------------------------------------------\

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
    seq = input("\tsequenza:\t").strip().upper()

    # cubo risolto: identità
    stato = list(range(N_STICKER))

    rotations = []
    # applico le permutazioni
    n = len(seq)
    for i in range(n):
        if (seq[i] != "'") and i != n-1 and (seq[i+1] == "'"):
            rotations.append(seq[i] + "'")
            i += 1
        elif seq[i] != "'":
            rotations.append(seq[i])

    for r in rotations:
        if r not in perm:
            print(f"Mossa '{r}' ignorata (non valida)")
            continue
        
        stato = [stato[perm[r][k]] for k in range(N_STICKER)]
    
    print_cubo(stato, True)

    # aggiungo i vincoli allo stato iniziale
    for j in range(N_STICKER):
        s.add(S[0][j] == stato[j])

    return s


def stati_finali(States):
    # STATO FINALE (cubo risolto)
    # cubo risolto quando al primo elemento S[F][j] == 0, con j = 0+4k con k = 0,1,2,3,4,5 tutti gli elementi che seguono sono in ordine crescente (ripartendo dall'inizio dell'array quando gli elementi finiscono)
    rotazioni_possibili = []
    for k in range(6): 
        start = 4 * k
        rotazioni_possibili.append(
            And([
                States[(start + j) % 24] == j
                for j in range(24)
            ])
        )
    return Or(rotazioni_possibili)

# /-------------------------------------------------------------\





# /-------------------------------------------------------------\

if __name__=='__main__':

    print("Manual\n\nDescrizione\n\tRisolutore del cubo di Rubik 2x2: scelta una profondità, il risolutore calcola se entro tali mosse è possibile risolvere il cubo.\n\nMosse possibili:\n\t - U e U', upper clockwise e counter-clockwise\n\t - L e L', left clockwise e counter-clockwise\n\t - F e F', front clockwise e counter-clockwise\n\t - R e R', right clockwise e counter-clockwise\n\t - B e B', back clockwise e counter-clockwise\n\t - D e D', down clockwise e counter-clockwise\n")
    print("Usage\n\t Inserire la profondità e le sequenza di mosse per modificare il cubo\n\t - example:\n\t\tprofondità:\t4\n\t\tsequenza:\tUB'URDR'L\n\n")
    print(">--------------------------< inizio programma >------------------------<\n\n")
    
    
    DEPTH = int(input("\tprofondità:\t"))
    solv = Solver()
    States = variabili_di_stato()        
    Transaction = variabili_di_transizione()  

    # stato iniziale
    solv = stato_iniziale(solv, States)        
    
    # stati finali
    solv.add(stati_finali(States[DEPTH][:]))



    # Vincoli di dominio
    # Per ogni sticker, 0 <= sticker < N_STICKER
    for i in range(DEPTH + 1):
        for j in range(N_STICKER):
            solv.add(And(States[i][j] >= 0, States[i][j] < N_STICKER))

    # Per ogni transizione, 0 <= transizione < N_MOV
    for i in range(DEPTH):
        solv.add(And(Transaction[i] >= 0, Transaction[i] < N_MOV))

    # Vincoli di unicità (sticker distinti)
    for i in range(DEPTH + 1):
        solv.add(Distinct(States[i]))


    # TRANSIZIONI
    # ogni transazione è una permutazione dello stato precedente
    ###### -> dobbiamo modificare ad ogni stato i, i k-esimi elementi rispetto al i-1, mediante la permutazione in perm
    for passo in range(DEPTH):
        for sticker_id in range(N_STICKER):

            nuovo_valore = States[passo][sticker_id]

            # per ogni possibile mossa, costruiamo un If annidato
            for mossa_id, mossa_nome in enumerate(mosse):
                # Se la mossa scelta a questo passo è mossa_id,
                # allora lo sticker sticker_id del nuovo stato
                # viene da perm[mossa_nome][sticker_idx]
                nuovo_valore = If(
                    Transaction[passo] == mossa_id, States[passo][perm[mossa_nome][sticker_id]], nuovo_valore
                )

            # il nuovo stato a (passo+1) deve rispettare questa relazione
            solv.add(States[passo + 1][sticker_id] == nuovo_valore)
    
    # TRANSAZIONE SUCCESSIVA != T PRECEDENTE INVERSA
    for i in range(1, DEPTH):
        solv.add(Implies(Transaction[i] % 2 == 0, Transaction[i] != Transaction[i-1]+1))
        solv.add(Implies(Transaction[i] % 2 != 0, Transaction[i] != Transaction[i-1]-1))

    

    # per ogni passo i, se il cubo è già risolto, allora lo stato successivo resta uguale
    for i in range(DEPTH - 1):  # attenzione: T[i+1] esiste solo fino a DEPTH-1
        solv.add(
            Implies(
                stati_finali(States[i]),  # vincolo “stato i è finale”
                And(
                    [States[i+1][j] == States[i][j] for j in range(N_STICKER)] +  # stato successivo uguale
                    [Transaction[i+1] == -1]  # transizione neutra
                )
            )
        )


    # ESECUZIONE MODELLO
    if solv.check() == sat:
        m = solv.model()
        print("Transizioni scelte:")

        # Stampa lo stato iniziale
        print("\n--- Stato 0 (iniziale) ---")
        print_cubo([m.evaluate(States[0][j]).as_long() for j in range(24)], True)

        for i in range(DEPTH):
            codicemossa = int(m[Transaction[i]].as_long())
            nome_mossa = mosse[codicemossa]
            print(f"\nStep {i+1}: {nome_mossa}")

            # Stampa lo stato dopo la mossa
            print_cubo([m.evaluate(States[i+1][j]).as_long() for j in range(24)], True)
    else:
        print("Nessuna soluzione trovata.")


# /-------------------------------------------------------------\