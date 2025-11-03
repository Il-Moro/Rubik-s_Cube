# /-------------------------------------------------------------\

stickers = {}

def print_cubo(stato, usa_colori=False):
    if len(stato) != 24:
        raise ValueError("Lo stato del cubo deve avere esattamente 24 elementi.")

    # mapping base: intervallo -> colore
    colori = {
        range(0, 4): "W",   # Up - White
        range(4, 8): "B",   # Left - Blue
        range(8, 12): "R",  # Front - Red
        range(12, 16): "G", # Right - Green
        range(16, 20): "O", # Back - Orange
        range(20, 24): "Y"  # Down - Yellow
    }

    def colore(idx):
        for rng, c in colori.items():
            if idx in rng:
                return c
        return "?"

    if usa_colori:
        ansi = {
            "W": "\033[38;2;255;255;255m■\033[0m",   # bianco
            "B": "\033[38;2;0;102;255m■\033[0m",     # blu saturo
            "R": "\033[38;2;255;30;30m■\033[0m",     # rosso vivo
            "G": "\033[38;2;0;200;0m■\033[0m",       # verde brillante
            "O": "\033[38;2;255;128;0m■\033[0m",     # arancione pieno
            "Y": "\033[38;2;255;230;0m■\033[0m"      # giallo acceso
        }
        def get_char(idx): return ansi[colore(stato[idx])]
    else:
        def get_char(idx): return colore(stato[idx])

    # estrai facce
    U = [get_char(i) for i in range(0, 4)]
    L = [get_char(i) for i in range(4, 8)]
    F = [get_char(i) for i in range(8, 12)]
    R = [get_char(i) for i in range(12, 16)]
    B = [get_char(i) for i in range(16, 20)]
    D = [get_char(i) for i in range(20, 24)]

    print("\nCUBO 2x2\n")
    print(" " * 7 + f"{U[0]} {U[1]}")
    print(" " * 7 + f"{U[2]} {U[3]}")
    print(f" {L[0]} {L[1]}   {F[0]} {F[1]}   {R[0]} {R[1]}   {B[0]} {B[1]}")
    print(f" {L[2]} {L[3]}   {F[2]} {F[3]}   {R[2]} {R[3]}   {B[2]} {B[3]}")
    print(" " * 7 + f"{D[0]} {D[1]}")
    print(" " * 7 + f"{D[2]} {D[3]}")
    print()

# /-------------------------------------------------------------\