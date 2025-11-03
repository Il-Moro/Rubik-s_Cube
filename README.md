# Rubik's Cube 2x2

### Rappresentazione

Il cubo di Rubik 2x2 è un cubo composto da 6 facce suddivse in 4 parti, quindi $6\cdot4=24$ stickers.

La rappresentazione del cubo sarà effettuata tramite una lista di 24 numeri da 0 a 23, divisi 4 a 4, ognuno rappresenta una faccia.

La rappresentazione del cubo in 2D sarà nel modo seguente:

```
        00 01
        02 03

04 05   08 09   12 13   16 17
06 07   10 11   14 15   18 19

        20 21
        22 23
```
quindi, uno stato $S \in \mathbb{N}^{24}, 0\leq s_i \lt 24, \forall i =0,\ldots,23$ del cubo sarà:
- $s_i, \forall i=0, \ldots, 3$ è l'Upper face
- $s_i, \forall i=4, \ldots, 7$ è il Left face
- $s_i, \forall i=8, \ldots, 11$ è il Front face
- $s_i, \forall i=12, \ldots, 15$ è il Right face
- $s_i, \forall i=16, \ldots, 19$ è il Back face
- $s_i, \forall i=20, \ldots, 23$ è il Down face


### Permutazioni
Ogni mossa del cubo è una permutazione deli sticker in una determinata posizione.

Le mosse valide per il cubo saranno in totale 12, 6 in senso orario (clockwise) e 6 in senso antiorario (counter clockwise):
- U e U', sono il movimento della faccia Upper in senso orario e antiorario
- L e L', sono il movimento della faccia Left in senso orario e antiorario
- F e F', sono il movimento della faccia Front in senso orario e antiorario
- R e R', sono il movimento della faccia Right in senso orario e antiorario
- B e B', sono il movimento della faccia Back in senso orario e antiorario
- D e D', sono il movimento della faccia Down in senso orario e antiorario

Ogni permutazione viene definita nel file **permutations.py**, assieme a una codifica che fa corrsispondere un numero alla permutazione: 0 e 1 per U e U', ecc...

### Plot
È possibile verificare visivamente la condizione del cubo mediante il file **viewCube** che contiene due funzioni: 
- print_cubo_numeri(State): rappresenta il cubo allo stato State mediante numeri in 2D
- print_cubo(State, True/False): per visualizzare il cubo con corrispondenza colori lettere (w per bianco, r per rosso, b per blu, y per giallo, g per green, o per arancione), oppure a colori



### Solver

Una volta definito il Solver, si utilizza `States[i][j]` per rappresentare tutti gli stati del cubo su DEPTH livelli, scelto dall'utente.

