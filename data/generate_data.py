#!/usr/bin/env python3
"""
generate_data.py
Sinh bộ dữ liệu kiểm thử thực nghiệm (Sedgewick, Algorithms 4e, 1.3 Algorithm Analysis).
Hỗ trợ cờ --smoke-test (chế độ CI) và chế độ full.
"""

import argparse
import math
from pathlib import Path
import random

DATA_TYPES = ["random", "sorted", "reversed", "nearly_sorted", "many_duplicates"]

FULL_SIZES = [100, 500, 1_000, 5_000, 10_000, 50_000, 100_000]
SMOKE_SIZES = [100, 500, 1_000, 5_000]


def gen_random(n: int) -> list[int]:
    return [random.randint(0, n * 10) for _ in range(n)]


def gen_sorted(n: int) -> list[int]:
    return list(range(n))


def gen_reversed(n: int) -> list[int]:
    return list(range(n, 0, -1))


def gen_nearly_sorted(n: int) -> list[int]:
    a = list(range(n))
    swaps = max(1, n // 20)
    for _ in range(swaps):
        i = random.randint(0, n - 1)
        j = random.randint(0, n - 1)
        a[i], a[j] = a[j], a[i]
    return a


def gen_many_duplicates(n: int) -> list[int]:
    rng = int(math.sqrt(n)) + 1
    return [random.randint(0, rng) for _ in range(n)]


GENERATORS = {
    "random": gen_random,
    "sorted": gen_sorted,
    "reversed": gen_reversed,
    "nearly_sorted": gen_nearly_sorted,
    "many_duplicates": gen_many_duplicates,
}


def main():
    parser = argparse.ArgumentParser(description="Sinh bộ dữ liệu thực nghiệm cho MergeSort CUTOFF")
    parser.add_argument("--smoke-test", action="store_true", help="Chạy chế độ nhẹ cho CI (N <= 5000)")
    parser.add_argument("--seed", type=int, default=2024, help="Random seed tái hiện kết quả")
    parser.add_argument("--out-dir", type=str, default="data", help="Thư mục xuất dữ liệu")
    args = parser.parse_args()

    random.seed(args.seed)
    sizes = SMOKE_SIZES if args.smoke_test else FULL_SIZES
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    count = 0
    for dtype in DATA_TYPES:
        for n in sizes:
            filename = out_dir / f"{dtype}_n{n}.txt"
            data = GENERATORS[dtype](n)
            with open(filename, "w", encoding="utf-8") as f:
                f.write(f"# Dataset: {dtype}, N: {n}\n")
                f.write("\n".join(str(x) for x in data) + "\n")
            count += 1
            print(f"Generated {filename} ({n} elements)")

    print(f"\nDone! Successfully generated {count} dataset files in '{out_dir}'.")


if __name__ == "__main__":
    main()
