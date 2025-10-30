

# Prima Classe per il cubo -> inutule per z3



class Cube():
    def __init__(self):
        # rappresentazione del cubo 2x2 mediante 6 liste di 4 elementi
        self.faces = {
            "Upper": ["w1" , "w2", "w4", "w3"],
            "Bottom": ["y1" , "y2", "y4", "y3"],
            "Right": ["b1" , "b2", "b4", "b3"],
            "Left": ["g1" , "g2", "g4", "g3"],
            "Front": ["r1" , "r2", "r4", "r3"],
            "Back": ["o1" , "o2", "o4", "o3"]
        }

        # Rappresentazione dei blocchi di ogni faccia 
        self.blocks = {
            "row_top": [0, 1],
            "row_bottom": [3, 2],
            "col_left": [0, 2],
            "col_right": [1, 3]
        }

        # È la lista che per ogni faccia da muovere collega le altre facce da muovere e in che orientamento 
        self.moves = {
            # Upper face
            "Upper": [
                ("Back", "row_top", "normal"),
                ("Right", "row_top", "normal"),
                ("Front", "row_top", "normal"),
                ("Left", "row_top", "normal")
            ],

            # Bottom face
            "Bottom": [
                ("Front", "row_bottom", "normal"),
                ("Right", "row_bottom", "normal"),
                ("Back", "row_bottom", "normal"),
                ("Left", "row_bottom", "normal")
            ],

            # Front face
            "Front": [
                ("Upper", "row_bottom", "normal"),
                ("Right", "col_left", "reversed"),
                ("Bottom", "row_top", "normal"),
                ("Left", "col_right", "normal")
            ],

            # Back face
            "Back": [
                ("Upper", "row_top", "reversed"),
                ("Left", "col_left", "reversed"),
                ("Bottom", "row_bottom", "normal"),
                ("Right", "col_right", "normal")
            ],

            # Left face
            "Left": [
                ("Upper", "col_left", "normal"),
                ("Front", "col_left", "normal"),
                ("Bottom", "col_left", "reversed"),
                ("Back", "col_right", "normal")
            ],

            # Right face
            "Right": [
                ("Upper", "col_right", "reversed"),
                ("Back", "col_left", "normal"),
                ("Bottom", "col_right", "normal"),
                ("Front", "col_right", "normal")
            ]
        }

    # Definisco il movimento di una faccia
    def movement(self, face, clockwise):
        if clockwise:
           self.rotate_clockwise(face)
        else:
           self.rotate_counterclockwise(face)

    # definisco il moviemnto orario
    def rotate_clockwise(self, face):
        # rotazione oraria della faccia
        f = self.faces[face]
        self.faces[face] = [f[2], f[0], f[3], f[1]]
        moves = self.moves[face]

        # buffer dagli sticker dell’ultima faccia
        prev_face, prev_pos, prev_orient = moves[3]
        prev_buffer = [self.faces[prev_face][i] for i in self.blocks[prev_pos]]
        
        # shift 3 → 2 → 1 → 0
        for i in range(0, 4):

            curr_face, curr_pos, curr_orient = moves[i]
            curr_indices = self.blocks[curr_pos]
            curr_buffer = [self.faces[curr_face][i] for i in self.blocks[curr_pos]]

            if prev_orient == "reversed":
                prev_buffer = list(reversed(prev_buffer))

            for ci, value in zip(curr_indices, prev_buffer):
                self.faces[curr_face][ci] = value

            prev_buffer = curr_buffer 
            prev_face, prev_pos, prev_orient = curr_face, curr_pos, curr_orient

    def rotate_counterclockwise(self, face):
        # rotazione antioraria della faccia
        f = self.faces[face]
        self.faces[face] = [f[1], f[3], f[0], f[2]]  # rotazione faccia 2x2

        moves = self.moves[face]

        # buffer dagli sticker dell’ultima faccia
        prev_face, prev_pos, prev_orient = moves[0]
        prev_buffer = [self.faces[prev_face][i] for i in self.blocks[prev_pos]]
        
        # shift 3 → 2 → 1 → 0
        for i in range(3, -1, -1):

            curr_face, curr_pos, curr_orient = moves[i]
            curr_indices = self.blocks[curr_pos]
            curr_buffer = [self.faces[curr_face][j] for j in self.blocks[curr_pos]]

            if curr_orient == "reversed":
                prev_buffer = list(reversed(prev_buffer))

            for ci, value in zip(curr_indices, prev_buffer):
                self.faces[curr_face][ci] = value

            prev_buffer = curr_buffer 
            prev_face, prev_pos, prev_orient = curr_face, curr_pos, curr_orient


    def print_cube(self):
        f = self.faces  # abbreviazione
        
        # Funzione helper per stampare 2x2 da lista piatta
        def face2x2(face_list):
            return f"{face_list[0]} {face_list[1]}\n{face_list[2]} {face_list[3]}"
        
        # Upper
        print("     " + f"{f['Upper'][0]} {f['Upper'][1]}")
        print("     " + f"{f['Upper'][2]} {f['Upper'][3]}")
        print()
        
        # Middle row: Left Front Right Back
        for i in [0,2]:  # prima riga, poi seconda riga
            print(f"{f['Left'][i]} {f['Left'][i+1]}  {f['Front'][i]} {f['Front'][i+1]}  {f['Right'][i]} {f['Right'][i+1]}  {f['Back'][i]} {f['Back'][i+1]}")
        print()
        
        # Bottom
        print("     " + f"{f['Bottom'][0]} {f['Bottom'][1]}")
        print("     " + f"{f['Bottom'][2]} {f['Bottom'][3]}")
        print()