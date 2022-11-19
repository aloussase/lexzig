#!/bin/sh
# Script para generar logs de las pruebas con los algorithmos de ejemplo.

for prueba in ./examples/*; do
  fecha="Fecha: `date`"
  resultado="Resultado: `python3 LexZig.py $prueba`"
  printf "Prueba: %s\n%s\n%s\n\n" "$prueba" "$fecha" "$resultado" >> log.txt
done
