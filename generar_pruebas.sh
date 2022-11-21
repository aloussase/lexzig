#!/bin/sh
# Script para generar logs de las pruebas con los algorithmos de ejemplo.

logs=""

if [ -f log.txt ]; then
  logs="$(cat log.txt)"
fi

for prueba in ./examples/*; do
  fecha="Fecha: `date`"
  resultado="Resultado: `python3 LexZig.py $prueba`"
  logs="$(printf "Prueba: %s\n%s\n%s\n\n" "$prueba" "$fecha" "$resultado")\n\n$logs"
done

if [ -f log.txt ]; then
  rm log.txt
fi

echo "$logs" > log.txt
