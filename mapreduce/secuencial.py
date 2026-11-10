#!/usr/bin/env python3
import sys
import time
from collections import defaultdict

def main():
    if len(sys.argv) < 2:
        print("Uso: python3 secuencial.py <archivo.csv>")
        sys.exit(1)

    csv_path = sys.argv[1]
    start_time = time.time()
    totales = defaultdict(float)

    with open(csv_path, "r", encoding="utf-8") as f:
        f.readline()
        for line in f:
            parts = line.strip().split(",")
            if len(parts) != 8:
                continue
            try:
                producto = parts[4]
                ingreso = float(parts[5]) * float(parts[6])
                totales[producto] += ingreso
            except Exception:
                continue

    top_10 = sorted(totales.items(), key=lambda x: x[1], reverse=True)[:10]
    elapsed = time.time() - start_time
    print(f"Procesado secuencial completado en {elapsed:.4f} segundos.")
    print("Top 10 productos:")
    for prod, total in top_10:
        print(f"{prod}: ${total:,.2f}")

if __name__ == "__main__":
    main()
