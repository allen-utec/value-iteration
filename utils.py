import numpy as np
import re


def obtener_states(archivo):
    with open(archivo, 'r') as f:
        contenido = f.read()

    inicio_bloque = 'states'
    fin_bloque = 'endstates'

    inicio = contenido.find(inicio_bloque)
    fin = contenido.find(fin_bloque)

    if inicio == -1 or fin == -1:
        return []  # Si no se encuentra uno de los bloques, retorna un arreglo vacío

    inicio += len(inicio_bloque)
    contenido_bloque = contenido[inicio:fin].strip()
    arreglo_contenido = contenido_bloque.split(',')

    states = [s.strip() for s in arreglo_contenido]

    grid_bloque = 'Grid:'
    grid_inicio = contenido.find(grid_bloque)
    grid_inicio += len(grid_bloque)
    grid_fin = contenido.find('\n', grid_inicio + 1)
    first_row_grid = contenido[grid_inicio:grid_fin].strip().split()
    size = len(first_row_grid)

    return states, (size, size)


def obtener_initial_state(archivo):
    with open(archivo, 'r') as f:
        contenido = f.read()

    inicio_bloque = 'initialstate'
    fin_bloque = 'endinitialstate'

    inicio = contenido.find(inicio_bloque)
    fin = contenido.find(fin_bloque)

    if inicio == -1 or fin == -1:
        return []  # Si no se encuentra uno de los bloques, retorna un arreglo vacío

    inicio += len(inicio_bloque)
    contenido_bloque = contenido[inicio:fin].strip()
    arreglo_contenido = contenido_bloque.split(',')

    return [s.strip() for s in arreglo_contenido][0]


def obtener_goal_state(archivo):
    with open(archivo, 'r') as f:
        contenido = f.read()

    inicio_bloque = 'goalstate'
    fin_bloque = 'endgoalstate'

    inicio = contenido.find(inicio_bloque)
    fin = contenido.find(fin_bloque)

    if inicio == -1 or fin == -1:
        return []  # Si no se encuentra uno de los bloques, retorna un arreglo vacío

    inicio += len(inicio_bloque)
    contenido_bloque = contenido[inicio:fin].strip()
    arreglo_contenido = contenido_bloque.split(',')

    return [s.strip() for s in arreglo_contenido][0]


def obtener_actions(archivo, move, actions_moves):
    with open(archivo, 'r') as f:
        contenido = f.read()

    inicio_bloque = 'action ' + move
    fin_bloque = 'endaction'

    inicio = contenido.find(inicio_bloque)
    fin = contenido.find(fin_bloque, inicio)

    if inicio == -1 or fin == -1:
        return []  # Si no se encuentra uno de los bloques, retorna un arreglo vacío

    inicio += len(inicio_bloque)
    contenido_bloque = contenido[inicio:fin].strip()
    lineas = contenido_bloque.split('\n')

    for linea in lineas:
        elementos = linea.split()
        state_dicc = actions_moves.get(elementos[0])
        if state_dicc == None:
            actions_moves[elementos[0]] = {}

        move_dicc = actions_moves[elementos[0]].get(move)
        if move_dicc == None:
            actions_moves[elementos[0]][move] = {
                'acciones': []
            }

        action = {
            'estado_sucesor': elementos[1],
            'probabilidad_de_accion': float(elementos[2]),
            'descartar': float(elementos[3])
        }
        actions_moves[elementos[0]][move]['acciones'].append(action)

    return actions_moves


def obtener_cost(archivo, actions_moves):
    with open(archivo, 'r') as f:
        contenido = f.read()

    inicio_bloque = 'cost'
    fin_bloque = 'endcost'

    inicio = contenido.find(inicio_bloque)
    fin = contenido.find(fin_bloque)

    if inicio == -1 or fin == -1:
        return []  # Si no se encuentra uno de los bloques, retorna un arreglo vacío

    inicio += len(inicio_bloque)
    contenido_bloque = contenido[inicio:fin].strip()
    lineas = contenido_bloque.split('\n')

    for linea in lineas:
        elementos = linea.split()
        state_dicc = actions_moves.get(elementos[0])
        if state_dicc == None:
            actions_moves[elementos[0]] = {}

        move_dicc = actions_moves[elementos[0]].get(elementos[1])
        if move_dicc == None:
            actions_moves[elementos[0]][elementos[1]] = {}

        actions_moves[elementos[0]][elementos[1]
                                    ]['costo'] = float(elementos[2])

    return actions_moves


def filtrar_por_state(matrix, state):
    filas_coincidentes = []

    for fila in matrix:
        if fila[0] == state:
            filas_coincidentes.append(fila)

    return filas_coincidentes


def savePolicy(initial_state, goal_state, policy, iteration, execution_time, grid_shape, archivo):
    archivo_split = archivo.split('/')[-2:]
    x, y = grid_shape

    initial_state_x_y = re.findall(r'\d+', initial_state)
    goal_state_x_y = re.findall(r'\d+', goal_state)

    array = np.empty(x * y, dtype=object)

    counter = 0
    for i in range(x):
        for j in range(y):
            array[counter] = '■'
            counter += 1

    matriz = array.reshape(x, y)

    for (state, move) in policy:
        if state == goal_state:
            matriz[int(goal_state_x_y[0]) - 1,
                   int(goal_state_x_y[1]) - 1] = '\U0001F7E2'
            continue

        if state == initial_state:
            if move == 'move-north':
                matriz[int(initial_state_x_y[0]) - 1,
                       int(initial_state_x_y[1]) - 1] = '\U0001F446'
            if move == 'move-south':
                matriz[int(initial_state_x_y[0]) - 1,
                       int(initial_state_x_y[1]) - 1] = '\U0001F447'
            if move == 'move-west':
                matriz[int(initial_state_x_y[0]) - 1,
                       int(initial_state_x_y[1]) - 1] = '\U0001F448'
            if move == 'move-east':
                matriz[int(initial_state_x_y[0]) - 1,
                       int(initial_state_x_y[1]) - 1] = '\U0001F449'
            continue

        if state == None:
            continue

        x_y = re.findall(r'\d+', state)

        if move == 'move-north':
            matriz[int(x_y[0])-1, int(x_y[1])-1] = '↑'
            continue

        if move == 'move-south':
            matriz[int(x_y[0])-1, int(x_y[1])-1] = '↓'
            continue

        if move == 'move-west':
            matriz[int(x_y[0])-1, int(x_y[1])-1] = '←'
            continue

        if move == 'move-east':
            matriz[int(x_y[0])-1, int(x_y[1])-1] = '→'

    filename = 'Experimentos/' + archivo_split[0] + '_' + \
        archivo_split[1].replace('.net', '.policy')

    policy_str = matriz.transpose()[::-1]

    with open(filename, 'w') as fout:
        fout.writelines([
            'Número de iteraciones hasta la convergencia: ' + str(iteration),
            '\nEl tiempo en milisegundos utilizado por el algoritmo: ' +
            str(execution_time),
            '\nPolicy:\n'
        ])
        np.savetxt(fout, policy_str, fmt='%s')
        fout.close()

    return filename
