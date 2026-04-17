import sys
import random


def solve():
    data = sys.stdin.read().strip().split()
    if not data:
        return
    a = list(map(int, data))
    n = len(a)
    # Problem statement says N=40; be tolerant to extra spaces/newlines.
    if n != 40:
        # If input contains more numbers, only first 40 are relevant by statement.
        a = a[:40]
        n = len(a)

    # Fast path: duplicate single element -> answer of size 1 and 1.
    seen_val = {}
    for i, v in enumerate(a):
        j = seen_val.get(v)
        if j is not None:
            _print_answer([j + 1], [i + 1])
            return
        seen_val[v] = i

    # General path: randomized search for two different subsets with equal sum.
    # If S1 and S2 have same sum, then A=S1\\S2 and B=S2\\S1 are disjoint and have equal sums.
    rng = random.Random(0)
    max_batches = 40
    steps_per_batch = 250_000
    max_table = 350_000  # cap memory per batch

    for batch in range(max_batches):
        base = rng.randrange(1 << n)
        mask = base
        s = 0
        for i in range(n):
            if (mask >> i) & 1:
                s += a[i]

        table = {s: mask}

        for _ in range(steps_per_batch):
            i = rng.randrange(n)
            bit = 1 << i
            if mask & bit:
                mask ^= bit
                s -= a[i]
            else:
                mask ^= bit
                s += a[i]

            prev = table.get(s)
            if prev is not None and prev != mask:
                a_mask = prev & ~mask
                b_mask = mask & ~prev
                if a_mask and b_mask:
                    subset1 = [idx + 1 for idx in range(n) if (a_mask >> idx) & 1]
                    subset2 = [idx + 1 for idx in range(n) if (b_mask >> idx) & 1]
                    _print_answer(subset1, subset2)
                    return
            elif len(table) < max_table:
                table[s] = mask

        # change seed trajectory between batches
        rng.seed(batch + 1)

    # If we get here, something is inconsistent with "solution exists"
    # Still exit cleanly with no output rather than raising.
    return


def _print_answer(subset1, subset2):
    sys.stdout.write(str(len(subset1)) + "\n")
    sys.stdout.write(" ".join(map(str, subset1)) + "\n")
    sys.stdout.write(str(len(subset2)) + "\n")
    sys.stdout.write(" ".join(map(str, subset2)) + "\n")


if __name__ == "__main__":
    solve()

