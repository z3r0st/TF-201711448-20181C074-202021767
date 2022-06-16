![Logo UPC](https://github.com/z3r0st/TF-201711448-20181C074-202021767/blob/main/img/upc_logo.jpeg)
## Universidad Peruana de Ciencias Aplicadas
## Ciencias de la Computación - 4to Ciclo
## Profesor: Canaval Sanchez, Luis Martin
## Grupo 5
## Integrantes
* Basauri Quispe, Roberto Carlos > 20181C074 
* Bravo Navarro, Rebeca Liliana > 201711448 > relibrana
* González Vidalón, Ian Steve > 202021767 > z3r0st
## Junio, 2022

# Tabla de Contenidos
1. [Resumen Ejecutivo](#resumen-ejecutivo)
2. [Imagen estática de la ciudad o porción de ciudad elegida](#imagen-estática-de-la-ciudad-o-porción-de-ciudad-elegida)
3. [Descripción de los datos consignados por calle](#descripción-de-los-datos-consignados-por-calle)
4. [Descripción de la información consignada por intersección](#descripción-de-la-información-consignada-por-intersección)
5. [Explicación de cómo se elaboró el grafo, qué representan las aristas y los vértices](#explicación-de-cómo-se-elaboró-el-grafo-qué-representan-las-aristas-y-los-vértices)
6. [Explicación del cálculo de la distancia entre puntos](#explicación-del-cálculo-de-la-distancia-entre-puntos)
7. [Explicación de la implementación del factor tiempo del tráfico](#explicación-de-la-implementación-del-factor-tiempo-del-tráfico)
8. [Explicación de la implementación de la variabilidad del tráfico por zonas](#explicación-de-la-implementación-de-la-variabilidad-del-tráfico-por-zonas)
9. [Explicación de los algoritmos de obtención de rutas más cortas](#explicación-de-los-algoritmos-de-obtención-de-rutas-más-cortas)

# Resumen Ejecutivo
Para el presente trabajo, se ha procesado la información de las intersecciones de calles de la ciudad de San Francisco, California, Estados Unidos, almacenándolas mediante la creación de un grafo, en formato de listas de adyacencia. Para ello, se tomaron los interceptos como coordenadas con latitud y longitud, las cuales fueron representadas en el grafo como números enteros desde el 0 hasta 9644 (cantidad de interceptos menos 1).

## Imagen estática de la ciudad o porción de ciudad elegida.
<p align="center">
<img src="https://github.com/z3r0st/TF-201711448-20181C074-202021767/blob/main/img/san_francisco.png" width="600"/>
</p>


# Descripción de los datos consignados por calle
Para la realización o representación de los interceptos por calle se tomó en consideración el nombre de la calle, en conjunto con todas las calles con las que intersectan. Teniendo en un inicio un conjunto del tipo:<br>
***Street_name** : [(latitude_1, longitude_1), (latitude_2, longitude_2), (latitude_3, longitude_4),...]*

El mismo dato que sería almacenado en un diccionario (intercepts) que contenga todos los interceptos por calle (hash/llave).<br>
*intercepts= {‘street_name_1’: [(latitude_1, longitude_1), (latitude_2, longitude_2),...], ‘street_name_2’:…}*

### Descripción de las variables:
* **intercepts**: Nombre del diccionario de interceptos por calle.
* **street_name_n** : Nombre de una calle capturado desde el dataset o conjunto de datos.
* **latitud_n, longitud_n** : Coordenadas de la calle donde intersecta con otra.

Por ejemplo, tomando como referencia las dos primeras líneas del dataset, se tendría la siguiente estructura capturada:

| CNN | ST_NAME | the_geom | ST_TYPE | CNNTEXT |
|:----|:-------:|:--------:|:-------:|-------:|
| 23730000 | UTAH | POINT (-122.40545417189192 37.75433723137436) | ST | 23730000 |
| 22141000 | JOOST | POINT (-122.43974776014164 37.73236806396732) | AVE | 22141000 |

### Descripción de los datos:
Entonces, la información que nos consigna guardar sería:

1. ‘Street_name_1’: ‘UTAH’
	+ Primer intercepto - primera calle:
	+ latitude_1: -122.40545417189192
	+ longitude_1: 37.75433723137436
	
2. ‘Street_name_2’: ‘JOOST’
	+ Primer intercepto - segunda calle:
	+ latitude_1: -122.43974776014164
	+ longitude_1: 37.73236806396732

**Nota: Tanto latitud y longitud son contenidos en una tupla (intercepto) para una mejor organización de la lista contenida por llave/hash (street_name_n).**

# Descripción de la información consignada por intersección.

Para la realización o representación de los interceptos o intersección se tomó en consideración el punto de intersección, en conjunto con todas las calles que incurren en él. Teniendo en un inicio un conjunto del tipo:

	*Intercept: [‘street_name_1’, ‘street_name2’]*
	
El mismo dato que sería almacenado en un diccionario (streets) que contenga todos las calles por intercepto(hash/llave).

*streets= {intercept_1: [‘street_name_1’, ‘street_name_2’], intercept_2: …}*
+ **streets**: Nombre del diccionario de calles por intercepto.
+ **intecerpt_n**: Punto de intersección de un conjunto de calles (**del dataset extraído generalmente 2**).
+ **street_name_1, street_name_2**: Nombre de la calle que cruce por el intersecto que lo contiene.

| CNN | ST_NAME | the_geom | ST_TYPE | CNNTEXT |
|:----|:-------:|:--------:|:-------:|-------:|
| 23730000 | UTAH | POINT (-122.40545417189192 37.75433723137436) | ST | 23730000 |
| 22141000 | JOOST | POINT (-122.43974776014164 37.73236806396732) | AVE | 22141000 |

Entonces, la información que nos consigna guardar sería:
* intercept_1: ( -122.40545417189192, 37.75433723137436)<br>
*Primera calle - primer intercepto:*<br>
* ‘Street_name_1’: ‘UTAH’

* intercept_2: (-122.43974776014164, 37.73236806396732)<br>
*Primera calle - segundo intercepto:*<br>
* ‘Street_name_1’: ‘JOOST’

# Explicación de cómo se elaboró el grafo, qué representan las aristas y los vértices.

Primero, realizamos la lectura del dataset en dónde consideramos la latitud y la longitud de las conexiones entre calles para crear los interceptos. Se utilizan 4 diccionarios en total: 
* **Intercepts**: permite acceder a todos los puntos interceptos que conforman la calle ingresada como llave.
* **Streets**: permite acceder a todas calles a las cuales pertenece un intercepto, por lo general 2 calles.
* **Nodes**: se ingresa como llave la coordenada del intercepto y se obtiene su representación más eficiente (número entero).
* **nodeToIntercept**: se ingresa el nodo (número entero) y se accede al detalle de sus coordenadas.

Luego, tenemos la función donde se crea el grafo (la lista de adyacencia). Dentro creamos una función dónde calculamos la distancia entre el intercepto que se está evaluando y los otros interceptos de cada calle a las cuales pertenece. Este proceso se realiza para cada calle a la que pertenece el intercepto, y se almacena los datos en la lista distance, que almacena listas anidadas, cada una conteniendo el nodo y la distancia respecto al intercepto en evaluación. Luego, se ordena la lista según la distancia y se almacenan los dos más cercanos en la lista neighbours. Luego, se verifica si ambos vecinos son adyacentes por lados opuestos o si son dos nodos que se encuentran en la misma dirección. Dependiendo de esta validación, se añade respectivamente el nodo más cercano o ambos. Finalmente se devuelve el grafo creado.

Finalmente, se genera grafo con la función creada y los datos guardados del dataset.

# Explicación del cálculo de la distancia entre puntos
Para el cálculo de la distancia entre puntos se omitió la idea de realizarlo por un método euclidiano debido a que este proceso omitía la curvatura de la Tierra. En cambio, se optó por usar la fórmula de Haversine.
La fórmula de Haversine es muy usada para el cálculo de distancias entre dos puntos de un globo sabiendo su longitud y su latitud.
Esta forma parte de la ley de los semiversenos, la cual se expresa de la siguiente manera:

semiversin(d/R) = semiversin(latitud1 - latitud2) + cos(latitud1)cos(latitud2)semiversin(longitud1-longitud2)

Donde:
* *semiversin:* Función semiverseno equivalente a sin2(angulo/2), donde el ángulo está en radianes, y sin2 equivale a la función seno elevado al cuadrado
* *d:* Distancia entre dos puntos en una esfera.
* *R:* Radio de la esfera.
* *Latitud1:* Latitud del punto 1
* *Latitu2:* Latitud del punto 2
* *Longitud1:* Longitud del punto 1
* *Longitud2:* Longitud del punto 2

Cabe resaltar que ambas diferencias (diferencias entre longitudes y latitudes) deben estar expresadas en radianes, ya que el valor entrante se encuentra en grados/minutos/segundos.

Para el cálculo de la distancia, fue necesario primero, una función de conversión a radianes, lo cual resultó en un simple proceso de conversión:

angulo_en_radianes = angulo_en_grados*pi/180

Segundo, fue necesario convertir la ley de los semiversenos a funciones conocidas por el entorno, para ello fue necesario la equivalencia:


sen2(d/(R*2)) = sen2((latitud1 - latitud2)/2) + cos(latitud1)cos(latitud2)sen2((longitud1-longitud2)/2)

Como todo el resultado del lado derecho es un cálculo con puras constantes, almacenaremos el valor en una variable cualquiera,

c = sen2((latitud1 - latitud2)/2) + cos(latitud1)cos(latitud2)sen2((longitud1-longitud2)/2)

Entonces tenemos que:

sen2(d/(R*2)) = c

sen(d/(R*2)) = sqrt(c)

Para el cálculo "d", se procedió a realizar la siguiente expresión:

d/(R*2) = arctan(sqrt(c)/sqrt(1-c))

Por último tenemos que:

d = 2*R*arctan(sqrt(c)/sqrt(1-c))

Almacenando los procesos de conversión de grados a radianes, calculando con los valores de ingreso la constante "c", y por último asumiendo un radio fijo para la Tierra (la Tierra no es netamente un globo) pero aproximado (usando el radio equivolumen), es que logramos capturar obtener el valor de la distancia de un punto a otro.

# Explicación de la implementación del factor tiempo del tráfico

Para la creación de un tráfico más preciso y realista se ha implementado un factor tiempo teniendo en cuenta las horas pico durante el día. Se implementó la función **timeFactor** la cual recibe una hora y retorna un subarray del array **timeToTraffic**, creado manualmente, el cual contiene un factor mínimo y máximo. Estos dos valores se usan en la siguiente función llamada **addTraffic** para la implementación total de los pesos en el grafo.

# Explicación de la implementación de la variabilidad del tráfico por zonas

Para concebir el tráfico, se formuló un modelo de dos capas, donde la primera capa es el tiempo y la segunda la zona (de la ciudad). Según el tiempo, como se explicó, se asigna un factor mínimo y máximo, que son descriptivos de la magnitud del tráfico vehicular en un intervalo de una hora. El mínimo es un multiplicador fijo, al cual se le añade, **dependiendo de la zona**, un valor entre 0 y la diferencia entre el factor máximo y mínimo:

w = d * (fMIn + (fMax - fMin) * r)

Donde: 
* **w** = peso
* **d** = distancia (entre los dos interceptos)
* **fMin** = factor mínimo, de acuerdo al intervalo horario
* **fMax** = factor máximo, de acuerdo al intervalo horario
* **r** = factor seudo-aleatorio, determinado por la ubicación

Ya que el tráfico no sigue patrones completamente aleatorios, donde una calle tendría un atasco y la siguiente estaría fluida, se optó por utilizar un generador de números seudo-aleatorios, que produce resultados más naturales, al suavizar la aleatoreidad. A continuación se presentan dos imágenes para ilustrar el contraste:

### Función aleatoria a lo largo del tiempo
![Random function](https://github.com/z3r0st/TF-201711448-20181C074-202021767/blob/main/img/random.png)

### Función suedo-aleatoria a lo largo del tiempo
![Pseudo-random function](https://github.com/z3r0st/TF-201711448-20181C074-202021767/blob/main/img/pseudo-random.png)

[Fuente: Artículo de Khan Academy](https://www.khanacademy.org/computing/computer-programming/programming-natural-simulations/programming-noise/a/perlin-noise)


Específicamente, se utilizó la función de ruido Perlin-Noise, que recibe uno o más valores de entrada y retorna un número entre -1 y 1, como regla general. La particularidad es que cuanto más cercanos sean los valores de entrada, habrá una cercanía entre los valores de salida.

Para cada arista, se calculó unas coordenadas promedio (tomando las coordenadas de los dos interceptos que la limitan) y se ingresó el valor de latitud y longitud como argumentos a la función de ruido. Es necesario precisar que el rango de Perlin Noise depende de la cantidad de dimensiones (determinada por la cantidad de parámetros de entrada):

rango = [−√N/4,√N/4]

Por lo tanto, al ingresar dos valores de entrada, se trabaja con dos dimensiones y el rango de salida es [-0.707, 0.707]. Por ello, se sumó 0.707 al resultado y se aplicó un reescalamiento lineal para pasar del rango [-0.707, 0.707] a [0, 1.414] y finalmente a [0, fMax - fMin].

# Explicación de los algoritmos de obtención de rutas más cortas

Para obtener las tres rutas más cortas, se tomó el *algoritmo de **Dijkstra*** como pilar de la solución. En primer lugar, se modificó el algoritmo para que se pueda ingresar un punto de destino y un arreglo de padres. Este último sirve para poder determinar qué nodos del grafo pueden ser incluidos en el camino más corto, es decir, es una forma de que **Dijkstra** trabaje sobre un subconjunto del grafo que recibe. Además, el arreglo de padres se modificó para que almacene tanto el nodo padre como el costo de la arista que lo conecta con el hijo. Esto permite retornar tanto el arreglo del camino (la secuencia de nodos), como el costo particular para llegar del nodo i al nodo i+1.

El camino más corto se obtiene directamente como resultado de la ejecución del *algoritmo de **Dijkstra***. Sin embargo, para obtener los otros caminos alternativos, se requiere un trabajo más expansivo, para lo cual se implementó el *algoritmo de **Yen***. Este obtiene el enésimo camino más corto y lo toma como referencia para obtener el siguiente camino. Específicamente, a partir del último camino validado, se toman todos los posibles subconjuntos (tamaño de 0 a n-1), que se denomina camino raíz. Luego, se anula la arista que conecta el último nodo del conjunto raíz con el resto del camino y se marcan como visitados los nodos pertenecientes al conjunto raíz (asignándoles un valor en el arreglo de padres). Una vez realizado esta preparación, se llama a **Dijkstra** y se revierten los cambios mencionados. De este manera, se asegura que **Dijkstra** tome una porción del último camino más corto encontrado y luego lo complemente con un nuevo camino. Una vez que se tienen todos los posibles caminos más cortos, se toma el que tiene el menor costo total y se agrega como enésimo camino más corto. Se repite todo el proceso hasta que se llega al número de caminos que se busca obtener.

## Pseudocódigo del algoritmo de Yen
```
function YenKSP(Graph, source, sink, K):
    // Determine the shortest path from the source to the sink.
    A[0] = Dijkstra(Graph, source, sink);
    // Initialize the set to store the potential kth shortest path.
    B = [];
    
    for k from 1 to K:
        // The spur node ranges from the first node to the next to last node in the previous k-shortest path.
        for i from 0 to size(A[k − 1]) − 2:
            
            // Spur node is retrieved from the previous k-shortest path, k − 1.
            spurNode = A[k-1].node(i);
            // The sequence of nodes from the source to the spur node of the previous k-shortest path.
            rootPath = A[k-1].nodes(0, i);
            
            for each path p in A:
                if rootPath == p.nodes(0, i):
                    // Remove the links that are part of the previous shortest paths which share the same root path.
                    remove p.edge(i,i + 1) from Graph;
            
            for each node rootPathNode in rootPath except spurNode:
                remove rootPathNode from Graph;
            
            // Calculate the spur path from the spur node to the sink.
            // Consider also checking if any spurPath found
            spurPath = Dijkstra(Graph, spurNode, sink);
            
            // Entire path is made up of the root path and spur path.
            totalPath = rootPath + spurPath;
            // Add the potential k-shortest path to the heap.
            if (totalPath not in B):
                B.append(totalPath);
            
            // Add back the edges and nodes that were removed from the graph.
            restore edges to Graph;
            restore nodes in rootPath to Graph;
                    
        if B is empty:
            // This handles the case of there being no spur paths, or no spur paths left.
            // This could happen if the spur paths have already been exhausted (added to A), 
            // or there are no spur paths at all - such as when both the source and sink vertices 
            // lie along a "dead end".
            break;
        // Sort the potential k-shortest paths by cost.
        B.sort();
        // Add the lowest cost path becomes the k-shortest path.
        A[k] = B[0];
        // In fact we should rather use shift since we are removing the first element
        B.pop();
    
    return A;
```
## Animación del Algoritmo de Yen
![Alt Text](https://github.com/z3r0st/TF-201711448-20181C074-202021767/blob/main/img/Yen's_K-Shortest_Path_Algorithm%2C_K%3D3%2C_A_to_F.gif)
