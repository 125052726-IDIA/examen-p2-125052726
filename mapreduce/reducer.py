#!/usr/bin/env python3
import sys

current_producto = None
current_total = 0.0
totales = {}

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    try:
        producto, val = line.split("\t", 1)
        val = float(val)
    except ValueError:
        continue

    if current_producto == producto:
        current_total += val
    else:
        if current_producto:
            totales[current_producto] = current_total
        current_producto = producto
        current_total = val

if current_producto:
    totales[current_producto] = current_total

top_10 = sorted(totales.items(), key=lambda x: x[1], reverse=True)[:10]
for prod, total in top_10:
    print(f"{prod}\t{total:.2f}")
