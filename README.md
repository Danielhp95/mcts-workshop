
# Introduccion

## Reinforcement learning

![rl loop](https://github.com/Danielhp95/mcts-workshop/blob/master/images/RL-diagram.png "Diagrama Reinforcement Learning")

Reinforcement Learning es una rama de inteligencia artificial basada en el concepto de "prueba y error". Un algoritmo generico de Reinforcement Learning presenta un **agente** que actua en un **entorno** y recibe **recompensa** positiva o negativa a traves de sus **acciones**. 

## Loop de Reinforcement Learning.

Por cada escalon de tiempo *t*:
* El Agente:
  1. Recibe recompensa *r<sub>t</sub>*
  2. Recibe observacion *s<sub>t</sub>*
  3. Ejecuta accion *a<sub>t</sub>*
* El Entorno:
  1. Recibe accion *a<sub>t</sub>*
  2. Emite recompensa *r<sub>t+1</sub>*
  3. Emite observacion *s<sub>t+1</sub>*


### Estados

Set de posibles estados de un entorno (S). Un agente en RL (reinforcement learning) procesa una representacion interna del entorno. Para cada instante *t*, *s<sub>t</sub>* es la representacion del estado del entorno. Escoger una buena representacion del estado *s<sub>t</sub>* puede ser una tarea muy dificil, y una buena representacion puede simplificar mucho la tarea de aprendizaje.

Para este taller, la representacion sera una matriz de 2 dimensiones, que representa el tablero del 4 en ralla. Incluso para un juego tan "sencillo" como el 4 en ralla, hay 4,531,985,219,092 posibles estados. Esto quiere decir que hay 4,531,985,219,092 posibles configuraciones del tablero.

### Acciones

Set de posibles acciones de un agente (A). En el instante *t* el agente "observa" el estado *s<sub>t</sub>*. Tras "observar" el estado *s<sub>t</sub>*, el agente escoge que accion *a<sub>t</sub>* va a llevar a cabo usando una **estrategia** ![policy](https://latex.codecogs.com/gif.latex?a_t%20%5Cpi%28a_t%20%7C%20s_t%29). Una estrategia es un mapeado de estados a acciones. Asumiendo una estrategia (pi) deterministica), dado un estado *s<sub>t</sub>*, (pi(s_t)) asigna una accion *a<sub>t</sub>*. (a_t = pi(s_t)). La accion *a<sub>t</sub>* se lleva a cabo en el entorno. Un vez el entorno se haya modificado, este devolvera un estado *s<sub>t+1</sub>* junto con una recompensa *r<sub>t+1</sub>*.



La estrategia es un mapeado (asignacion) de estados a acciones.
El objetivo de los problemas de RL se basan en encontrar una estrategia optima para el problema en cuestion. Donde optimo se considera que se consige la mayor recompensa posible.

![rl loop 2](https://github.com/Danielhp95/mcts-workshop/blob/master/images/RL-diagram2.png "Diagrama Reinforcement Learning")

### Recompensa

Reinforcement learning se basa en encontrar una policy que devuelva la mayor recompensa acumulada. En el caso del 4 en raya, el objetivo del agente es ganar la partida. Siguiendo un orden logico: un movimiento que gane la partida otorgara al agente una recompensa de +1, un movimiento que no termine la partida otorgara una recompensa de 0, un movimiento que pierda la partida penalizara al agente con una recompensa de -1. Realmente esto importa?

# Monte Carlo Tree Search (MCTS)

MCTS es un metodo de Monte Carlo. Los elementos de Monte Carlo se basan en la siguiente idea: es posible ejecutar muchas simulaciones de algun proceso. Hay algo en este proceso que nos interesa aprender. En IA para videjuegos, esto suele ser la estrategia (*policy* en ingles) optima. Con lo tanto, si hacemos muchas simulaciones (*rollouts* en ingles), y al mismo tiempo guardamos alguna estadistica (como cuantas veces hemos tomado una accion, cuantas victorias hemos acumulado tras hacer una accion a lo largo de todas las simulaciones). Para poner un ejemplo concreto, si un agente se encuentra en

Para ser mas concretos, nos interesa aprender la accion optima que tomar en cada estado del juego. Este concepto se encapsula en la funcion $Q(s,a)$

## Monte Carlo Tree Search - Upper Confidence Bound applied to Trees (MCTS-UCT)

![mcts diagram](https://github.com/Danielhp95/mcts-workshop/blob/master/images/UCT-diagram.png "Diagrama MCTS-UCT")


### Estructura del algoritmo MCTS-UCT
El algoritmo de MCTS-UCT se divide en 4 fases, seleccion, expansion, simulacion y retropropagacion (backpropagation).

Repetir durante *ITERMAX* iteraciones:     
    * **Seleccion**: empezar desde la raíz R y seleccionar nodos hijos sucesivos hasta alcanzar un nodo hoja L. Esto permite que el árbol de juego se expanda hacia movimientos más prometedores, que es la esencia del algoritmo MCTS-UDT.     
    * **Expansion**: a menos que L termine el juego con una victoria/pérdida para cualquiera de los jugadores, ya sea al crear uno o más nodos hijos o elegir entre ellos un nodo C.    
    * **Simulacion**: jugar una partida aleatoria empezando desde el nodo C hasta llegar a un nodo terminal / hoja.    
    * **Retropropagacion**: utilizar el resultado de la simulacion para actualizar la información en los nodos en el camino de C a R.    
**Seleccion de accion** escoger que accion tomar basado en las estadisticas calculadas durante las simulaciones.    
END

#### Seleccion

Formula de UCB1: ![ucb1](https://latex.codecogs.com/gif.latex?%5Cfrac%7Bw_i%7D%7Bn_i%7D%20&plus;%20c%20%5Csqrt%7B%5Cfrac%7B%5Cln%20N_i%7D%7Bn_i%7D%7D)

+ *w<sub>i</sub>* stands for the number of wins for the node considered after the i-th move    
+ *n<sub>i</sub* stands for the number of simulations for the node considered after the i-th move    
+ *N<sub>i</sub>* stands for the total number of simulations after the i-th move    
+ *c* is the exploration parameter—theoretically equal to √2; in practice usually chosen empirically    
  
El nodo que reciba el valor UCB1 mas alto sera seleccionado. Este proceso de seleccion se repetira hasta que se encuentre un nodo que no este completamente expandido (que tenga nodos hijo que nunca hayan sido seleccionados) o al llegar un nodo hoja / terminal.

#### Expansion

El paso mas sencillo, una vez se ha seleccionado un nuevo nodo para anhadirlo en el game tree, este se creara con contadores para varias estadisticas. Para MCTS-UDT nos interesa guardar:

+ *w<sub>i</sub>* stands for the number of wins for the node considered after the i-th move
+ *n<sub>i</sub* stands for the number of simulations for the node considered after the i-th move

#### Simulacion

#### Retropropagacion

En nuestro caso, el 4 en raya, el agente debera colocar un ficha en una de las columnas que no esten llenas. 
  

### Propiedades de metodos Monte Carlo

**Seccion de opcional lectura, pero atender este taller tambien es opcional, con lo que ya que estamos...**


## Terminologia
**Juego de informacion completa:** Toda la informacion del juego (en caso del 4 en raya, la posicion de todas las piezas) y las reglas del juego son conocidas por todos los agentes (jugadores).    
**Juego deterministico:** Cada movimiento tiene un resultado unico. Es decir, cada movimiento solo tiene una posible resultado. Si esto no fuera asi, el juego seria estocastico.    
**Nodo terminal:** Un nodo que no tiene ningun movimiento posible (porque, por ejemplo, uno de los jugadores ha ganado).

## El ejercicio.

Usar MCTS-UCT para calcular para cada turno una accion de entre [1,2,3,4,5,6].

### Instalacion

Necesitaras Python 2.7 para este ejercicio. El script solo tiene una dependencia: `colorama`, un modulo para imprimir texto con colores en la terminal, su uso en este ejercicio es puramente estetico. La implementacion del algoritmo no requiere ninguna herramienta que no venga dentro de la distribucion estandard de Python 2.7. Para instalar `colorama`:

````python
pip install colorama
````


## TODO

### Introduction
* Polish everything
* Add mathematical equations
* Give more workshop specific comments

### MCTS
* Talk about game trees
* Selection policy
    * UCB1
    * Explotation vs Exploration.
* Expansion
* Simulation
* Back propagation

## Ejercicio

Explicar como correr una partida contra otro jugador. Como jugar contra la maquina. como instalar la dependencia
