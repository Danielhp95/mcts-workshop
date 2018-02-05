# Introduccion

## Reinforcement learning

![rl loop](https://github.com/Danielhp95/mcts-workshop/blob/master/images/RL-diagram.png "Diagrama Reinforcement Learning")

Reinforcement Learning es una rama de inteligencia artificial que basa su aprendizaje en el concepto de "prueba y error". Todo algoritmo de Reinforcement Learning presenta a un **agente** que actúa en un **entorno** y recibe una **recompensa** (positiva o negativa) por cada una de sus **acciones**. El objetivo de un **agente** es encontrar una **estrategia** que maximize su **recompensa** a largo plazo.


### Breakout video:
[breakout video](https://www.youtube.com/watch?v=TmPfTpjtdgg)

### Bucle de Reinforcement Learning.

Por cada escalón de tiempo **t**:
* El Agente:
  1. Recibe recompensa **r<sub>t</sub>**
  2. Recibe observación **s<sub>t</sub>**
  3. Emite acción **a<sub>t</sub>**
* El Entorno:
  1. Recibe acción **a<sub>t</sub>** y la ejecuta. La ejecución de la acción **a<sub>t</sub>** modifica el entorno.
  2. Emite recompensa **r<sub>t+1</sub>**
  3. Emite observación **s<sub>t+1</sub>**

<br><br>

## El entorno

### Estados

El entorno para este taller es el juego del 4 en raya. Incluso para un juego tan "sencillo" como el 4 en raya, hay 4,531,985,219,092 posibles estados.

El set de posibles estados de un entorno se denomina **S**. Cada valor ![!s_in_S](https://latex.codecogs.com/gif.latex?s%20%5Cin%20%5Ctextbf%7BS%7D) denota una posible representación del estado de un entorno. **s<sub>t</sub>** es la representación del entorno para cada instante **t**. Normalmente, escoger una buena representación del estado **s<sub>t</sub>** no es fácil, y una buena representacion puede simplificar mucho la tarea de aprendizaje.

Para este taller, la representación será una matriz de 2 dimensiones, que representa el tablero del 4 en raya, nos referiremos al estado como *Board* (*tablero* en ingles). *Board<sub>ij</sub>* denotara el estado de la casilla en la fila *i* y columna *j*. *Board<sub>ij</sub>* = 0: casilla vacia. *Board<sub>ij</sub>* = 1: ficha del jugador 1. *Board<sub>ij</sub>* = 2: ficha del jugador 2.

### Acciones

El set de posibles acciones disponibles en un entorno se denomina **A**. Para este taller, un estado **s<sub>t</sub>** tendrá un máximo de 7 acciones posibles, **A** =  [0, 1, 2, 3, 4, 5, 6]. Cada acción ![possible actions](https://latex.codecogs.com/gif.latex?a%20%5Cin%20%5B0%2C1%2C2%2C3%2C4%2C5%2C6%5D) representa la acción de colocar un ficha en una de las 7 columnas del tablero. En caso de que en un estado **s<sub>t</sub>** la columna número **i** este llena, no se podra colocar una ficha en ella, con lo cual la acción **a<sub>i</sub>** no se podrá ejecutar en el estado **s<sub>t</sub>**. 

Cuando se ejecuta una acción **a<sub>t</sub>** en el entorno, este se modifica. Tras la modificación, el entorno presenta un nuevo estado **s<sub>t+1</sub>** junto con una recompensa **r<sub>t+1</sub>** al agente.

### Recompensa

Cada posible acción, en cada estado, tiene asociada una recompensa. Una recompensa mide, a corto plazo, lo buena o mala que es una acción en un estado concreto.

Para este taller nos interesa ganar la partida. Con lo cual una acción que gane la partida otorgará al agente una recompensa de +1, cualquier otro movimiento otorgara una recompensa de 0.

<br>

## El agente

### Estrategia

Por cada instante **t** el agente "observa" el estado **s<sub>t</sub>**. Tras "observar" el estado **s<sub>t</sub>**, el agente escoge que acción **a<sub>t</sub>** va a ejecutar usando una **estrategia** representada por la letra griega ![policy](https://latex.codecogs.com/gif.latex?%5Cpi). Una estrategia es un mapeado de estados a acciones, y es todo lo necesario para definir el comportamiento de un agente. ![pi state_t](https://latex.codecogs.com/gif.latex?%5Cpi%28s_t%29) representa el mapeado de un estado **s<sub>t</sub>** a una acción **a<sub>t</sub>**. La tarea de "aprendizaje" de un agente en reinforcement learning es la tarea de encontrar una estrategia ![policy](https://latex.codecogs.com/gif.latex?%5Cpi) que maximize su recompensa a largo plazo a partir de recompensas a corto plazo.

<br>

### Representación de un agente y un entorno.
![rl loop 2](https://github.com/Danielhp95/mcts-workshop/blob/master/images/RL-diagram2.png "Diagrama Reinforcement Learning")
<br><br>
<br><br>

# Taller

## Monte Carlo Tree Search (MCTS)

MCTS es un [método de Monte Carlo](https://es.wikipedia.org/wiki/M%C3%A9todo_de_Montecarlo "método de Monte Carlo"). Los métodos de Monte Carlo son métodos de aproximación estadísticos que se basan en la siguiente idea: hay un fenómeno que queremos estudiar. Este fenómeno es generalmente una expresión matemática compleja, con lo que intentamos aproximarlo. Para ello, tenemos acceso a un modelo (un simulador) del entorno donde ocurre este fenómeno. Utilizando el modelo podemos generar muchas simulaciones. Con ellas, podemos calcular estadísticas pertinentes del fenómeno que queremos estudiar. En el campo de inteligencia artificial para videojuegos, el modelo suele ser las reglas del juego. Dado un estado **s<sub>t</sub>** en un entorno, el fenómeno a averiguar es el valor de cada posible acción **a<sub>t</sub>** en un estado **s<sub>t</sub>**. Si tenemos una aproximación del valor real de cada acción posible **a<sub>t</sub>** para cada estado **s<sub>t</sub>**, podemos escoger la acción de mayor valor en cada momento **t** para jugar de forma óptima.


## Monte Carlo Tree Search - Upper Confidence Bound applied to Trees (MCTS-UCT)

![mcts diagram](https://github.com/Danielhp95/mcts-workshop/blob/master/images/UCT-diagram.png "Diagrama MCTS-UCT")

Monte Carlo Tree Search - Upper Confidence Bound applied to Trees (MCTS-UCT) es un algoritmo que se usa para aproximar la estrategia óptima para un agente a cada paso de la partida. MCTS-UCT se usa para responder a la siguiente pregunta. Dado un estado **s<sub>t</sub>** ¿Qué acción **a<sub>t</sub>** nos dará una mayor recompensa a largo plazo? Que es lo mismo que preguntar ¿Qué acción tiene mas probabilidades de ganar la partida? Si un agente utiliza MCTS-UCT en cada uno de sus turnos, está aproximando en todo momento la decisión óptima.

La idea de MCTS-UCT es la próxima. Para averiguar que acción **a<sub>t</sub>** tomar en **s<sub>t</sub>**, simulamos muchisimas partidas, con cada partida aprendemos estadisticas que nos informan sobre lo buena (o mala) que es una acción en el estado **s<sub>t</sub>**. Con estas estadísticas, escogemos que acciones vamos descartando y que acciones prometedoras seguimos investigando.

<br><br>

### Estructura del algoritmo MCTS-UCT
El algoritmo de MCTS-UCT se divide en 4 fases, seleccion, expansion, simulacion y retropropagacion (backpropagation). El único parámetro que MCTS-UCT necesita es la cantidad de iteraciones que se le permite ejecutar antes de decidir que accion tomar. Llamaremos a este parametro **ITERMAX**.

MCTS-UCT(estado inicial = **s<sub>t</sub>**, maximas iteraciones = **ITERMAX**) (hacer mas bonito)    
Inicializar game tree donde el nodo Raiz R representa el estado **s<sub>t</sub>**      
Repetir durante **ITERMAX** iteraciones:     
    * **Seleccion**: empezar desde el nodo raíz R y seleccionar nodos hijos sucesivos (Usando la formula UCB1) hasta alcanzar un nodo hoja L. Esto permite que el game tree se expanda hacia movimientos más prometedores, que es la esencia del algoritmo MCTS-UCT.       
    * **Expansion**: iniciar las estadisicas para el nuevo nodo L.    
    * **Simulacion**: jugar una partida aleatoria (cada movimiento simulado es una accion valida aleatoria) iniciando la simulacion en el estado representado por el nodo L hasta que la partida simulada termine.     
    * **Retropropagacion**: utilizar el resultado de la simulacion para actualizar la información en los nodos en el camino de L a R.     
**Seleccion de accion** escoger que accion tomar basado en las estadisticas calculadas durante las previas iteraciones.     
END     

<br>
#### Selección

Fórmula de UCB1: ![ucb1](https://latex.codecogs.com/gif.latex?%5Cfrac%7Bw_i%7D%7Bn_i%7D%20&plus;%20c%20%5Csqrt%7B%5Cfrac%7B%5Cln%20N_i%7D%7Bn_i%7D%7D)

+ **w<sub>i</sub>**: número de victorias acumuladas en el nodo hijo **i**.
+ **n<sub>i</sub>**: número de simulaciones acumuladas en el nodo hijo **i**.
+ **N<sub>i</sub>**: número de simulaciones acumuladas en el nodo actualmente seleccionado.
+ **c**: parametro de exploracion, es una constante. Nos permite escoger entre los dos términos de la equación de UCB1. Un **c** grande da más importancia a la exploracion. Un **c** pequeño (**c < 1**) da más importancia a la explotación. Ver (ingles) [explotación-vs-exploración](https://medium.com/@dennybritz/exploration-vs-exploitation-f46af4cf62fe "Explotation vs Exploration")

Esta fase empieza seleccinando el nodo raiz R. En caso de que todos los movimientos se hayan seleccionado al menos una vez, aplicamos la fórmula UCB1 a todos los nodos hijo y seleccionamos el que de un valor mayor. Es decir, el nodo hijo **i** que reciba el valor UCB1 mas alto sera seleccionado. Este proceso se repite hasta que se seleccione un nodo que no este completamente expandido (que tenga nodos hijo que nunca hayan sido seleccionados) o al llegar un nodo hoja / terminal. Si seleccionamos un nodo el cual tiene algún movimiento que no se haya expandido, expandimos uno de estos movimientos no seleccionados, terminado la fase de selección.

#### Expansión

El paso mas sencillo. Una vez se ha seleccionado un nuevo hacemos dos cosas. Primero, lo añadimos al game tree que se esta construyendo en la ejecución de MCTS-UCT. Segundo, lo iniciamos con contadores para diferentes estadísticas que serviran para guiar la fase de **selección** en futuras iteraciones. Viendo la equacion de UCB1 las estadísticas que nos interesa guardar son:

+ **w<sub>i</sub>**: número de victorias acumuladas en el nodo hijo **i**.
+ **n<sub>i</sub>**: número de veces que el nodo hijo **i** ha sido seleccionado.

#### Simulación

En términos generales, una simulación es una sucesion de acciones por partes de todos los agentes que cambian el entorno hasta llegar a un estado terminal. En un game tree, una simulacion empieza en el estado **s** correspondiente a un nodo raiz y se toman acciones posibles que llevan a otros nodos. La simulacion termina cuando se llega a un nodo hoja / terminal.

Terminada la expansión del nodo escogido, comenzamos una simulacion del juego (en este taller 4 en raya) desde este nodo. Cada una de las acciones escogidas durante toda la simulacion son aleatorias (los dos agentes juegan movimientos aleatorios). Otros terminos utilizados para hablar de simulaciones en la literaturas son *rollout* o *playout*.

**Nota**: Exceptuando el nodo donde comienza la simulacion todos los otros nodos por los que se pasa en cada simulacion *NO* forman parte del game tree que se esta formando durante MCTS-UCT.

#### Retropropagación

El resultado de la simulación se propaga por todos los nodos del game tree empezando por el nodo creado en la fase de **expansión** y terminando en el nodo raiz del game tree. Para **actualizar** las estadísticas basta con actualizar el número de simulaciones y victorias (en caso de que la simulación haya sido victoriosa) en cada uno de los nodos. Este proceso también se conoce como **backpropagation**.

#### Selección de acción.

El uso de las estadisticas calculadas durante las previas fases es la de seleccionar una accion **a<sub>t</sub>** para tomar en el movimiento numero **t**. Donde **s<sub>t</sub>** es el estado correspondiente al nodo raiz del game tree generado por MCTS-UCT. Inspeccionamos a todos los nodos hijo correspondientes al nodo raiz y tomamos el que tiene un valor mayor de posibilidad de victoria. Tomamos la accion asignada al nodo hijo **c** cuyas estadisticas maximizen la equacion: 

+ **w<sub>c</sub>**: número de victorias acumuladas en el nodo hijo **c**.
+ **n<sub>c</sub>**: número de simulaciones acumuladas en el nodo hijo **c**.

<br><br>
### Animacion de MCTS

![mcts animation](https://github.com/Danielhp95/taller-mcts-coruna/blob/master/images/gif/gif.gif)


## El Reto
¡Implementa el algoritmo MCTS-UCT en python para jugar al 4 en raya contra una inteligencia artificial! 

### Instalación

Necesitarás Python 2.7 para este ejercicio. La implementación del algoritmo no requiere ninguna herramienta que no venga dentro de la distribucion estandard de Python 2.7. El script solo tiene una dependencia: `colorama`, un módulo para imprimir texto con colores en la terminal, su uso en este ejercicio es puramente estético ¿Pero quién no quiero tener texto de colores en la terminal? Para instalar `colorama`:

```python
pip install colorama
```

## El script

El script `MCTS.py` contiene todo el código necesario para los dos talleres. También es el único archivo que deberá ser modificado durante los talleres. Su contenido está escrito en inglés para facilitar busquedas relacionadas en internet. Los comentarios están en español. Utiliza los comentarios dentro del codigo como documentación del mismo.

Para jugar una partida entre 2 humanos ejecuta: `python MCTS.py`
