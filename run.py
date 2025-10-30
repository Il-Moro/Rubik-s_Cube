from z3_2x2_solver import solve_2x2


def main():
    ok, seq = solve_2x2(max_depth=8, scramble=None)
    if ok:
        print('✅ Soluzione trovata:', ' '.join(seq))
    else:
        print('❌ Nessuna soluzione entro la profondità richiesta.')


if __name__ == '__main__':
    main()


