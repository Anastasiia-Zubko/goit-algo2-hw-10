from __future__ import annotations
import random
import sys
import time
from typing import Iterable, List
import matplotlib.pyplot as plt
import pandas as pd

sys.setrecursionlimit(1_000_000)


def randomized_quick_sort(arr: List[int]) -> List[int]:
    if len(arr) <= 1:
        return arr
    pivot = random.choice(arr)
    less = [x for x in arr if x < pivot]
    equal = [x for x in arr if x == pivot]
    greater = [x for x in arr if x > pivot]
    return randomized_quick_sort(less) + equal + randomized_quick_sort(greater)


def deterministic_quick_sort(arr: List[int], pivot_rule: str = "middle") -> List[int]:
    if len(arr) <= 1:
        return arr

    if pivot_rule == "first":
        pivot = arr[0]
    elif pivot_rule == "last":
        pivot = arr[-1]
    else:
        pivot = arr[len(arr) // 2]

    less = [x for x in arr if x < pivot]
    equal = [x for x in arr if x == pivot]
    greater = [x for x in arr if x > pivot]
    return (
        deterministic_quick_sort(less, pivot_rule)
        + equal
        + deterministic_quick_sort(greater, pivot_rule)
    )


def benchmark(
    sizes: Iterable[int] | None = None,
    repeats: int = 5,
    pivot_rule: str = "middle",
) -> pd.DataFrame:

    if sizes is None:
        sizes = (10_000, 50_000, 100_000, 500_000)

    rows: list[dict[str, float]] = []
    for n in sizes:
        base: list[int] = [random.randint(0, 1_000_000) for _ in range(n)]
        rand_times, det_times = [], []

        for _ in range(repeats):
            start = time.perf_counter()
            randomized_quick_sort(base.copy())
            rand_times.append(time.perf_counter() - start)

            start = time.perf_counter()
            deterministic_quick_sort(base.copy(), pivot_rule)
            det_times.append(time.perf_counter() - start)

        rows.append(
            {
                "Array size": n,
                "Randomized QuickSort (s)": sum(rand_times) / repeats,
                "Deterministic QuickSort (s)": sum(det_times) / repeats,
            }
        )

    return pd.DataFrame(rows)


def print_results(df: pd.DataFrame) -> None:
    for _, row in df.iterrows():
        size = int(row["Array size"])
        rand = row["Randomized QuickSort (s)"]
        det = row["Deterministic QuickSort (s)"]
        print(f"Розмір масиву: {size}")
        print(f"\tРандомізований QuickSort: {rand:.4f} секунд")
        print(f"\tДетермінований QuickSort: {det:.4f} секунд\n")



def main() -> None:
    df = benchmark()
    print_results(df)

    plt.figure()
    plt.plot(df["Array size"], df["Randomized QuickSort (s)"], marker="o", label="Randomized QuickSort")
    plt.plot(df["Array size"], df["Deterministic QuickSort (s)"], marker="o", label="Deterministic QuickSort")
    plt.xlabel("Array size")
    plt.ylabel("Average time (seconds)")
    plt.title("Deterministic vs Randomized QuickSort Performance")
    plt.legend()
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
