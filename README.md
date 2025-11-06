# Rubik's Cube 2x2

### Rappresentazione


Il cubo di Rubik 2x2 è un cubo composto da 6 facce suddivise in 4 parti, quindi $6\cdot4=24$ stickers.

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

Siano:
- $d$, la profondità di calcolo
- $n$, il numero di sticker totali 
- $S \in \mathbb{N}^{d \times 24 }$, il vettore degli stati $s_{j,i}$
- $P \in \mathbb{N}^{d}$, il vettore delle permutazioni $p_{j}$
- $T_j \in \mathbb{N}^d$, il vettore delle transizioni $t_j$
- $I \in \mathbb{N}^{24}$, con $i_j = j, j = 0, \ldots 23$  

uno stato $S_{j}$ del cubo sarà suddiviso quindi così:
- $S_{j,[0,4)}$ è l'Upper face
- $S_{j,[4,8)}$ è il Left face
- $S_{j,[8,12)}$ è il Front face
- $S_{j,[12,16)}$ è il Right face
- $S_{j,[16,20)}$ è il Back face
- $S_{j,[20,24)}$ è il Down face


### Permutazioni
Ogni mossa del cubo è una permutazione degli sticker in una determinata posizione.

Le mosse valide per il cubo saranno in totale 12, 6 in senso orario (clockwise) e 6 in senso antiorario (counter clockwise):
- U e U', sono il movimento della faccia Upper in senso orario e antiorario
- L e L', sono il movimento della faccia Left in senso orario e antiorario
- F e F', sono il movimento della faccia Front in senso orario e antiorario
- R e R', sono il movimento della faccia Right in senso orario e antiorario
- B e B', sono il movimento della faccia Back in senso orario e antiorario
- D e D', sono il movimento della faccia Down in senso orario e antiorario

Ogni permutazione viene definita nel file **permutations.py**, assieme a una codifica che fa corrsispondere un numero alla permutazione: 0 e 1 per U e U', ecc...

### Plot
È possibile verificare visivamente la condizione del cubo utilizzando le funzioni nel file **viewCube**: 
- print_cubo_numeri(State): rappresenta il cubo allo stato State mediante numeri in 2D
- print_cubo(State, True/False): per visualizzare il cubo con corrispondenza colori lettere (w per bianco, r per rosso, b per blu, y per giallo, g per green, o per arancione), oppure a colori



### Solver

Una volta definito il Solver:
##### Varibili:

- `States[i][j]` servono per rappresentare tutti gli stati del cubo su DEPTH livelli, scelto dall'utente. Quindi `States[i]` è lo stato al livello i, mentre `State[i][j]` è lo sticker j-esimo dello stato i-esimo

- `Transaction[j]` servono per rappresentare le transizioni da uno stato all'altro. 

- `Risolto[j]` sono valori booleane per verificare se al livello j-esimo lo stato è finale.


### Condizioni

#### Stato iniziale
Lo stato iniziale $S_{0}$ è definita come la matrice $I$ permutata attraverso i vettori $p_j \in P$

$$
\forall p_i \in P \\

\begin{cases}
I = L_0 \\
L_k = L_{k-1}(p_{k-1})
\end{cases}
$$

$$
S_0 = L_n 
$$



#### Dominio sugli stati
Per ogni stato $S_j$, ogni sticker $s_{j,i}$ deve essere compreso tra 0 e 23
$$
\forall j, \forall i, 0\leq s_{j,i} \lt 24
$$

#### Dominio sulle transizioni
Per ogni transizione $t_j$, il valore delle transizione deve essere compresa tra 0 e 12. In totale sono 13 valori, 12 delle permutazioni effettive + un valore di default per la transizione nulla
$$
\forall j, 0 \leq t_j \leq 12 
$$

#### Unicità degli sticker 
Per ogni stato $s_j$, e per ogni $i,k$, gli sticker $s_{j,i} \neq s_{j,k}$ se $i \neq k$
$$
\forall j, \forall i,k, \text{ se } i \neq k \implies s_{j,i} \neq s_{j, k}
$$

#### Stati finali
Uno stato $S_j$ è stato risolto se:
$$
\forall i, s_{j,i} = i, i = 0, \ldots, 23
$$

se vale questo, allora deve essere che ogni stato successivo $s_{j+l}$, con $l=1,\ldots, d -j$ è uguale a $s_{j}$ e ogni transizione $t_{j+l}$ successiva è uguale a 12, ovvero:
$$
\exists j: \forall i, s_{j,i} = i, i = 0, \ldots, 23 \implies \forall l, l \in [1,d-j], s_{j+l} = s_{j} \land t_{j+l} = 12  
$$

#### Transizioni successive
Sia $T_j$, la transizione al passo j-esimo, allora la transizione $T_{j+1}$ deve essere diversa dall'inversa di $T_{j}$

$$ inv(T_j) = 
\begin{cases}
T_j + 1, \text{se $T_j$ pari} \\
T_j - 1, \text{se $T_j$ dispari}
\end{cases}
$$

Inoltre se $T_j = 12$, definisco $inv(T_j)$ come 
$$
inv(T_j) = T_j
$$

#### Condizione su Risolto[]
Al passo j-esimo:
$$
R_j = 
\begin{cases}
1, \text{ se } \forall i, s_{j,i} = i \\
0, \text{ se } \exists i: s_{j,i} \neq i
\end{cases}
$$
#### Condizione necessaria di terminazione
Almeno uno stato deve essere finale
$$
\exists j: \forall i, s_{j,i} = i
$$

#### Funzione obiettivo
Per far terminare in modo corretto l'algoritmo, cerco di massimizare la somma dei valori di $R_j$

$$
\max \sum R(j)
$$


