#!/usr/bin/env python3
import sys

for line in sys.stdin:
    line = line.strip()
    if not line or line.startswith("id,"):
        continue
    parts = line.split(",")
    if len(parts) != 8:
        continue
    try:
        producto = parts[4]
        cantidad = float(parts[5])
        precio = float(parts[6])
        ingreso = cantidad * precio
        print(f"{producto}\t{ingreso:.2f}")
    except Exception:
        continue
