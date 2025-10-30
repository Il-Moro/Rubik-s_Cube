# Rubik-s_Cube

1) Idea principale (in due righe, perché so che odii le storie)

Il 2x2 ha solo 8 corner. Uno stato è: una permutazione delle 8 cubie e la loro orientazione (0,1,2).
Modello Z3: per ogni passo t (sequenza di mosse di lunghezza fissata D) rappresenti lo stato con 8 variabili permutazione + 8 orientazioni; ogni passo è ottenuto dal passo precedente applicando una delle mosse (U, R, F, D, L, B o anche solo generatori R,U,F basta). Z3 trova i valori delle scelte di mosse che portano dallo stato iniziale allo stato risolto.

Fonti coi tavoli delle mosse (se vuoi i dati già pronti): Joyner / cube20 (ho usato le convenzioni usate dai solver classici). 
fuw.edu.pl
+1

2) Rappresentazione concreta (serve per implementare)

Scegliamo un ordinamento standard dei corner (molto usato):