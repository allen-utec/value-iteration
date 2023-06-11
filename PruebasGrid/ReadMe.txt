El archivo tiene:

1. Los estados separados por comas. 

2. Las transiciones para cada accion definidas de la seguinte forma:

action nombre_de_accion
	estado_actual estado_sucesor probabilidad_de_accion descartar
end_action

3. El costo de cada par estado accion.

4. El estado inicial.

5. El estado objetivo.

6. Un grid que es solo para visualizacion. En el grid:

1 - Pared
2 - Estado Inicial
3 - Estado Final
4 - Marca que indica que hay una pared al lado



