# /-------------------------------------------------------------\

def print_cubo(stato):
    
    # helper per stampare una faccia 2x2
    def faccia(face):
        return f"{face[0]:2} {face[1]:2}\n{face[2]:2} {face[3]:2}"

    # estrai facce
    U = stato[0:4]
    L = stato[4:8]
    F = stato[8:12]
    R = stato[12:16]
    B = stato[16:20]
    D = stato[20:24]

    # stampa con layout sviluppato
    print("\nCUBO 2x2\n")
    print(" " * 7 + f"{U[0]:2} {U[1]:2}")
    print(" " * 7 + f"{U[2]:2} {U[3]:2}")
    print(f"{L[0]:2} {L[1]:2}   {F[0]:2} {F[1]:2}   {R[0]:2} {R[1]:2}   {B[0]:2} {B[1]:2}")
    print(f"{L[2]:2} {L[3]:2}   {F[2]:2} {F[3]:2}   {R[2]:2} {R[3]:2}   {B[2]:2} {B[3]:2}")
    print(" " * 7 + f"{D[0]:2} {D[1]:2}")
    print(" " * 7 + f"{D[2]:2} {D[3]:2}")
    print()

# /-------------------------------------------------------------\