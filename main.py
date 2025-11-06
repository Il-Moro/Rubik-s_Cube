from z3 import *
from time import sleep
from permutation import permutation
from viewCube import print_cubo, print_cubo_numeri

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
    return [[Int(f"S_{j}_{i}") for i in range(N_STICKER)] for j in range(DEPTH)]

def variabili_di_transizione():
    # una transizione per ogni passo 
    return [Int(f"T_{j}") for j in range(DEPTH)]


def stato_iniziale(s, S):
    seq = input("\tsequenza:\t").strip().upper() # strip() rimuovo spacing

    # stato del cubo a partire da quello risolto
    stato = list(range(N_STICKER))

    rotations = []
    n = len(seq)
    
    # estrapolo i singoli comandi
    for i in range(n):
        if (seq[i] != "'") and i != n-1 and (seq[i+1] == "'"):
            rotations.append(seq[i] + "'")
            i += 1
        elif seq[i] != "'":
            rotations.append(seq[i])
    
    #applico le permutazioni
    for r in rotations:
        if r not in perm:
            print(f"Mossa '{r}' ignorata (non valida)")
            continue
        else:
            stato = [stato[perm[r][k]] for k in range(N_STICKER)]

    # aggiungo i vincoli allo stato iniziale
    for i in range(N_STICKER):
        s.add(S[0][i] == stato[i])

    return s


def stati_finali(States):
    # STATO FINALE (cubo risolto)
    # cubo risolto quando al primo elemento S[F][j] == 0, con j = 0+4k con k = 0,1,2,3,4,5 tutti gli elementi che seguono sono in ordine crescente (ripartendo dall'inizio dell'array quando gli elementi finiscono)
    rotazioni_possibili = []
    for k in range(6): 
        start = 4 * k
        rotazioni_possibili.append(
            And([ States[(start + j) % 24] == j for j in range(24) ])
        )
    return Or(rotazioni_possibili)


'''
def stati_finali(States):
    # STATO FINALE (cubo risolto)
    # cubo risolto quando al primo elemento S[F][j] == 0, con j = 0+4k con k = 0,1,2,3,4,5 tutti gli elementi che seguono sono in ordine crescente (ripartendo dall'inizio dell'array quando gli elementi finiscono)
    cond_finale = And([ States[i] == i for i in range(24) ])
    return Or(cond_finale)
'''
# /-------------------------------------------------------------\





# /-------------------------------------------------------------\

if __name__=='__main__':

    print("Manual\n\nDescrizione\n\tRisolutore del cubo di Rubik 2x2: scelta una profondità, il risolutore calcola se entro tali mosse è possibile risolvere il cubo.\n\nMosse possibili:\n\t - U e U', upper clockwise e counter-clockwise\n\t - L e L', left clockwise e counter-clockwise\n\t - F e F', front clockwise e counter-clockwise\n\t - R e R', right clockwise e counter-clockwise\n\t - B e B', back clockwise e counter-clockwise\n\t - D e D', down clockwise e counter-clockwise\n")
    print("Usage\n\t Inserire la profondità e le sequenza di mosse per modificare il cubo\n\t - example:\n\t\tprofondità:\t4\n\t\tsequenza:\tUB'URDR'L\n\n")
    print(">--------------------------< inizio programma >------------------------<\n\n")
    
    DEPTH = int(input("\tprofondità:\t"))+1
    
    # solver
    solv = Optimize()

    # variaboli stati
    States = variabili_di_stato()

    # variabili transizioni        
    Transaction = variabili_di_transizione()  

    # variabili flag
    Risolto = [Bool(f"R_{i}") for i in range(DEPTH)]



    # stato iniziale
    solv = stato_iniziale(solv, States)


    
    for j in range(DEPTH):
        # Vincoli di dominio
        # Per ogni sticker, 0 <= sticker < N_STICKER    
        for i in range(N_STICKER):
            solv.add(And(States[j][i] >= 0, States[j][i] < N_STICKER))
        
        # Per ogni transizione, 0 <= transizione < N_MOV
        solv.add(And(Transaction[j] >= 0, Transaction[j] <= N_MOV))

         # Vincoli di unicità (sticker distinti)
        solv.add(Distinct(States[j])) 

        # condizione su stati finali
        if j != DEPTH-1:
            solv.add(
                Implies(
                    Risolto[j],
                    And(
                        *[States[j+1][i] == States[j][i] for i in range(N_STICKER)],
                        Transaction[j+1] == N_MOV  # "None"
                    )
                )
            )
        else:
            solv.add(
                Implies(Risolto[j], 
                    And(
                        Transaction[j] == N_MOV
                        )
                    )
                )


        # TRANSIZIONI
        # ogni transazione è una permutazione dello stato precedente
        ###### -> dobbiamo modificare ad ogni stato i, i k-esimi elementi rispetto al i-1, mediante la permutazione in perm
        for i in range(N_STICKER):

            # mi salvo lo sticker corrente
            nuovo_valore = States[j][i]

            # per ogni possibile mossa, costruiamo un If annidato
            for mossa_codice, mossa_nome in enumerate(mosse): # troviamo qual è la permutazione sulla base della T scelta in quel momento dal solver
                # Se la mossa scelta a questo passo è mossa_id,
                # allora lo sticker sticker_id del nuovo stato
                # viene da perm[mossa_nome][i]
                nuovo_valore = If(
                    Transaction[j] == mossa_codice, States[j][perm[mossa_nome][i]], nuovo_valore
                )

            # il nuovo stato a (j+1) deve rispettare questa relazione
            if j != DEPTH-1:
                solv.add(States[j + 1][i] == nuovo_valore)


        # transizioni successive
        if j != 0:
            solv.add(
                Implies(
                    Transaction[j-1] < N_MOV,
                    And(
                        Implies(Transaction[j-1] % 2 == 0, Transaction[j] != Transaction[j-1] + 1),
                        Implies(Transaction[j-1] % 2 == 1, Transaction[j] != Transaction[j-1] - 1),
                    )
                )
            )

        # condizione su risolto 
        solv.add(Risolto[j] == stati_finali(States[j]))


    # almeno uno stato deve essere finale
    solv.add(Or([Risolto[j] for j in range(DEPTH)]))


    # ottimizzare per evitare che il solver usi esattamente DEPTH mosse
    solv.minimize(Sum([If(Risolto[j], j, DEPTH) for j in range(DEPTH)]))



    # ESECUZIONE MODELLO
    if solv.check() == sat:
        m = solv.model()
        # Stampa lo stato iniziale
        print("\n--- Stato 0 (iniziale) ---")
        print_cubo([m.evaluate(States[0][j]).as_long() for j in range(24)], True)

        print("Transizioni scelte:")
        for i in range(DEPTH):
            codicemossa = int(m[Transaction[i]].as_long())
            nome_mossa = mosse[codicemossa]
            if nome_mossa == "None":
                break
            print(f"\nStep {i+1}: {nome_mossa}")

            # Stampa lo stato dopo la mossa
            print_cubo([m.evaluate(States[i+1][j]).as_long() for j in range(24)], True)

            print_cubo_numeri([m.evaluate(States[i+1][j]).as_long() for j in range(24)])
    else:
        print("Nessuna soluzione trovata.")

# /-------------------------------------------------------------\