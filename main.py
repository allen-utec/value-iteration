import time
import numpy as np
from utils import *

# Leer el archivo
archivo = './PruebasGrid/FixedGoalInitialState/navigation_1.net'

# Extraemos los estados y tamaño de la grilla
states, grid_shape = obtener_states(archivo)

# Extraemos el estado inicial y objetivo
initial_state = obtener_initial_state(archivo)
goal_state = obtener_goal_state(archivo)

# Extraemos las acciones por cada movimiento en un diccionario
# con la siguiente estructura
# {
#   'robot-at-x1y1': {
#     'move-south': {
#       'accion': {
#         'estado_sucesor': 'robot-at-x1y1',
#         'probabilidad_de_accion': 1.0,
#         'descartar': 1.0
#       },
#       'costo': 1.0
#     }
#   }
# }
state_actions = {}
obtener_actions(archivo, 'move-south', state_actions)
obtener_actions(archivo, 'move-north', state_actions)
obtener_actions(archivo, 'move-west', state_actions)
obtener_actions(archivo, 'move-east', state_actions)
obtener_cost(archivo, state_actions)


def value_iteration(epsilon=0.1, max_iterations=1000):
    start_time = round(time.time() * 1000)

    # Número de estados a procesar
    num_states = len(states)

    # Inicialización de los valores iniciales para cada estado
    V = np.zeros(num_states)

    # Contador del número de iteraciones
    iteration = 0

    # Inicializamos un arreglo con los posibles movimientos de acción
    moves = ['move-south', 'move-north', 'move-west', 'move-east']

    # Iteramos hasta que el algoritmo converja
    while True:
        # Inicialización del delta
        delta = 0.0

        # Iteramos sobre cada estado
        for state_idx in range(num_states):
            # No iteramos sobre el estado objetivo
            if states[state_idx] == goal_state:
                continue

            # Guardamos el valor actual del estado actual
            v_initial = V[state_idx]

            # Validamos que el diccionario state_actions
            # contenga una entrada para el estado actual
            state_dicc = state_actions.get(states[state_idx])
            if state_dicc == None:
                continue

            # Inicializamos el arreglo de los valores de cada movimiento
            action_values = []

            # Iteramos sobre los 4 posibles movimientos
            for move in moves:
                # Inicializamos el valor esperado para el movimiento
                expected_value = 0.0

                # Validamos que el diccionario state_dicc
                # contenga una entrada para el movimiento actual
                move_dicc = state_dicc.get(move)
                if move_dicc != None:
                    for action in move_dicc['acciones']:
                        estado_sucesor_idx = states.index(
                            action['estado_sucesor'])
                        probabilidad_de_accion = action['probabilidad_de_accion']
                        costo = move_dicc['costo']

                        # Calculamos el valor esperado de la acción
                        expected_value += probabilidad_de_accion * \
                            (costo + V[estado_sucesor_idx])

                # Agregamos el valor esperado
                action_values.append(expected_value)

            # Seleccionamos el mejor valor esperado para el estado actual
            best_value = min(action_values)

            # Actualizamos el valor del estado actual
            V[state_idx] = best_value

            # Actualizamos el delta
            delta = max(delta, abs(v_initial - V[state_idx]))

        # Contamos la iteración hecha
        iteration += 1

        # Verificamos la condición de convergencia
        if delta < epsilon:
            break

        # Verificamos la condición de iteraciones
        if iteration == max_iterations:
            break

    # Política Óptima
    # Inicializamos de los valores de la política óptima: [(estado, movimiento),...]
    policy = [(None, None)] * num_states

    # Repetimos el proceso para llenar nuestro politica óptima
    for state_idx in range(num_states):
        if states[state_idx] == goal_state:
            policy[state_idx] = (states[state_idx], None)
            continue

        state_dicc = state_actions.get(states[state_idx])
        if state_dicc == None:
            continue

        action_values = []

        for move in moves:
            move_dicc = state_dicc.get(move)
            if move_dicc == None:
                continue

            expected_value = 0.0
            for action in move_dicc['acciones']:
                estado_sucesor_idx = states.index(action['estado_sucesor'])
                probabilidad_de_accion = action['probabilidad_de_accion']
                costo = move_dicc['costo']

                expected_value += probabilidad_de_accion * \
                    (costo + V[estado_sucesor_idx])

            action_values.append(expected_value)

        best_value = np.argmin(action_values)
        policy[state_idx] = (states[state_idx], moves[best_value])

    end_time = round(time.time() * 1000)

    # Retornamos el arreglo de valor encontrado, la politica óptima
    # y el tiempo de ejecución del algoritmo.
    return V, policy, iteration, end_time - start_time


# Ejecución del algoritmo
V, policy, iteration, execution_time = value_iteration()

# Reporte de resultados
filename = savePolicy(initial_state, goal_state, policy,
                      iteration, execution_time, grid_shape, archivo)
print(open(filename, 'r').read())
