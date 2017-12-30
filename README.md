
# Introduccion

## Reinforcement learning

![alt text](https://github.com/Danielhp95/mcts-workshop/blob/master/images/RL-diagram.png "Diagrama Reinforcement Learning")

El 4 en raya es episodico. Merece mencion?

## Loop de Reinforcement Learning.

Por cada momento *t*:
* El Agente:
  1. Recibe recompensa *r<sub>t</sub>*
  2. Recibe observacion *s<sub>t</sub>*
  3. Ejecuta accion *a<sub>t</sub>*
* El Entorno:
  1. Recibe accion *a<sub>t</sub>*
  2. Emite recompensa *r<sub>t+1</sub>*
  3. Emite observacion *s<sub>t+1</sub>*


### Estados

Un agente en RL (reinforcement learning) procesa una representacion interna del entorno. Para cada instante *t*, *s<sub>t</sub>* es la representacion del estado del entorno. Escoger una buena representacion del estado *s<sub>t</sub>* puede ser una tarea muy dificil, y una buena representacion puede simplificar mucho la tarea de aprendizaje. Para este taller, la representacion sera una matriz de 2 dimensiones, que representa el tablero del 4 en ralla. Incluso para un juego tan "sencillo" como el 4 en ralla, hay 4,531,985,219,092 posibles estados. Esto quiere decir que hay 4,531,985,219,092 posibles configuraciones del tablero.

### Acciones

En el instante *t* el agente "observa" el estado *s<sub>t</sub>*. Tras "observar" el estado *s<sub>t</sub>*, el agente debe tomar una accion

El agente recibe un estado, utiliza una estrategia (policy) para escoger una decision.
Su accion modifica el entorno, que devuelve un nuevo estado y una recompensa.
La estrategia es un mapeado (asignacion) de estados a acciones.
El objetivo de los problemas de RL se basan en encontrar una estrategia optima para el problema en cuestion. Donde optimo se considera que se consige la mayor recompensa posible.

![alt text](https://github.com/Danielhp95/mcts-workshop/blob/master/images/RL-diagram.png "Diagrama Reinforcement Learning")

### Recompensa

Reinforcement learning se basa en encontrar una policy que devuelva la mayor recompensa acumulada. En el caso del 4 en raya, el objetivo del agente es ganar la partida. Siguiendo un orden logico: un movimiento que gane la partida otorgara al agente una recompensa de +1, un movimiento que no termine la partida otorgara una recompensa de 0, un movimiento que pierda la partida penalizara al agente con una recompensa de -1. Realmente esto importa?

## Monte Carlo Tree Search (MCTS)

MCTS es un metodo de Monte Carlo. Los elementos de Monte Carlo se basan en la siguiente idea: es posible ejecutar muchas simulaciones de algun proceso. Hay algo en este proceso que nos interesa aprender. En IA para videjuegos, esto suele ser la estrategia (*policy* en ingles) optima. Con lo tanto, si hacemos muchas simulaciones (*rollouts* en ingles), y al mismo tiempo guardamos alguna estadistica (como cuantas veces hemos tomado una accion, cuantas victorias hemos acumulado tras hacer una accion a lo largo de todas las simulaciones). Para poner un ejemplo concreto, si un agente se encuentra en

Para ser mas concretos, nos interesa aprender la accion optima que tomar en cada estado del juego. Este concepto se encapsula en la funcion $Q(s,a)$

![alt text](https://github.com/Danielhp95/mcts-workshop/blob/master/images/UCT-diagram.png "Diagrama MCTS-UCT")
  

### Propiedades de metodos Monte Carlo

**Seccion de opcional lectura, pero atender este taller tambien es opcional, con lo que ya que estamos...**


## Terminologia
**Juego de informacion completa:** Toda la informacion del juego (en caso del 4 en raya, la posicion de todas las piezas) y las reglas del juego son conocidas por todos los agentes (jugadores).    
**Juego deterministico:** Cada movimiento tiene un resultado unico. Es decir, cada movimiento solo tiene una posible resultado. Si esto no fuera asi, el juego seria estocastico.    
**Nodo terminal:** Un nodo que no tiene ningun movimiento posible (porque, por ejemplo, uno de los jugadores ha ganado).

## El reto

Usar MCTS-UCT para calcular para cada turno una accion de entre [1,2,3,4,5,6].
