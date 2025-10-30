from typing import List, Tuple, Dict
from z3 import Bool, Solver, And, Or, Implies, is_true, sat, PbEq


# 2x2 cube stickers (24): order U, L, F, R, B, D; each face indices [0,1,2,3] as
# 0 1
# 2 3


def _canonical_sticker_positions() -> List[Tuple[float, float, float]]:
    positions: List[Tuple[float, float, float]] = []
    # grid offsets for 2x2 on a face (using +/- 0.5 for aesthetic)
    offs = [(-0.5, 0.5), (0.5, 0.5), (-0.5, -0.5), (0.5, -0.5)]
    # U (y=+1)
    for (x, z) in offs:
        positions.append((x, 1.0, z))
    # L (x=-1)
    for (z, y) in offs:
        positions.append((-1.0, y, z))
    # F (z=+1)
    for (x, y) in offs:
        positions.append((x, y, 1.0))
    # R (x=+1)
    for (z, y) in offs:
        positions.append((1.0, y, z))
    # B (z=-1)
    for (x, y) in offs:
        positions.append((x, y, -1.0))
    # D (y=-1)
    for (x, z) in offs:
        positions.append((x, -1.0, z))
    return positions


CANON = _canonical_sticker_positions()


def _rot90(v: Tuple[float, float, float], axis: str, k: int) -> Tuple[float, float, float]:
    # Rotate vector v by k quarter turns (+90 deg) about axis in right-hand rule
    x, y, z = v
    k = k % 4
    if k == 0:
        return v
    if axis == 'x':
        for _ in range(k):
            y, z = -z, y
        return (x, y, z)
    if axis == 'y':
        for _ in range(k):
            x, z = z, -x
        return (x, y, z)
    if axis == 'z':
        for _ in range(k):
            x, y = -y, x
        return (x, y, z)
    raise ValueError("axis must be x,y,z")


def _face_axis(face: str) -> Tuple[str, float]:
    if face == 'U':
        return ('y', 1.0)
    if face == 'D':
        return ('y', -1.0)
    if face == 'F':
        return ('z', 1.0)
    if face == 'B':
        return ('z', -1.0)
    if face == 'R':
        return ('x', 1.0)
    if face == 'L':
        return ('x', -1.0)
    raise ValueError("invalid face")


def _build_move_permutation(face: str, quarter_turns: int) -> List[int]:
    axis, sign = _face_axis(face)
    # Determine which stickers belong to this face by matching the face coordinate with sign
    idxs = []
    for i, (x, y, z) in enumerate(CANON):
        coord = {'x': x, 'y': y, 'z': z}[axis]
        if abs(coord - sign) < 1e-6:
            idxs.append(i)
    # Map all 24 stickers: those on the rotating face get rotated, others unchanged.
    rotated_positions = list(CANON)
    for i in idxs:
        rotated_positions[i] = _rot90(CANON[i], axis, quarter_turns)
    # Build mapping by nearest canonical position match
    perm = [None] * 24
    for src in range(24):
        pos = rotated_positions[src]
        # find index j in CANON equal to pos (float compare tolerant)
        dst = None
        for j, p in enumerate(CANON):
            if all(abs(a - b) < 1e-6 for a, b in zip(pos, p)):
                dst = j
                break
        if dst is None:
            raise RuntimeError("Failed to match rotated position to canonical grid")
        perm[src] = dst
    return perm


def build_all_move_permutations() -> Dict[str, List[int]]:
    names = ['U', 'D', 'L', 'R', 'F', 'B']
    perms: Dict[str, List[int]] = {}
    for n in names:
        perms[n] = _build_move_permutation(n, 1)
        perms[n + "'"] = _build_move_permutation(n, 3)
        perms[n + '2'] = _build_move_permutation(n, 2)
    return perms


def apply_perm(state: List[int], perm: List[int]) -> List[int]:
    new_state = state[:]
    for i in range(24):
        new_state[perm[i]] = state[i]
    return new_state


def initial_state_from_scramble(perms: Dict[str, List[int]], scramble: List[str]) -> List[int]:
    # solved state: face colors 0..5
    state: List[int] = []
    for color in range(6):
        state.extend([color] * 4)
    for mv in scramble:
        state = apply_perm(state, perms[mv])
    return state


def solve_2x2(max_depth: int = 8, scramble: List[str] | None = None) -> Tuple[bool, List[str]]:
    perms = build_all_move_permutations()
    if not scramble:
        scramble = ["R", "U", "R'", "U'"]
    init = initial_state_from_scramble(perms, scramble)

    state = [[Int(f's_{t}_{i}') for i in range(24)] for t in range(max_depth + 1)]
    s = Solver()

    for t in range(max_depth + 1):
        for i in range(24):
            s.add(And(state[t][i] >= 0, state[t][i] <= 5))

    for i in range(24):
        s.add(state[0][i] == init[i])

    def face_solved(v: List[object]):
        cs = []
        for f in range(6):
            a = v[4 * f]
            cs.append(And(v[4 * f + 1] == a, v[4 * f + 2] == a, v[4 * f + 3] == a))
        return And(*cs)

    move_names = [
        'U', "U'", 'U2', 'D', "D'", 'D2',
        'L', "L'", 'L2', 'R', "R'", 'R2',
        'F', "F'", 'F2', 'B', "B'", 'B2',
    ]
    mv = [[Bool(f'm_{t}_{name}') for name in move_names] for t in range(max_depth)]
    for t in range(max_depth):
        s.add(PbEq([(v, 1) for v in mv[t]], 1))

    for t in range(max_depth):
        for mi, name in enumerate(move_names):
            perm = perms[name]
            for i in range(24):
                s.add(Implies(mv[t][mi], state[t + 1][perm[i]] == state[t][i]))

    solved_flags = [Bool(f'solved_{t}') for t in range(max_depth + 1)]
    for t in range(max_depth + 1):
        s.add(solved_flags[t] == face_solved(state[t]))
    s.add(Or(*solved_flags))

    if s.check() != sat:
        return False, []

    m = s.model()
    t_star = 0
    for t in range(max_depth + 1):
        if is_true(m[solved_flags[t]]):
            t_star = t
            break

    seq: List[str] = []
    for t in range(t_star):
        for mi, name in enumerate(move_names):
            if is_true(m[mv[t][mi]]):
                seq.append(name)
                break
    return True, seq


