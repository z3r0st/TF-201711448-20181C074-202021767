![Logo UPC]()
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
1. Resumen Ejecutivo
2. Imagen estática de la ciudad o porción de ciudad elegida.
3. Descripción de los datos consignados por calle.
4. Descripción de la información consignada por intersección.
5. Explicación de cómo se elaboró el grafo, qué representan las aristas y los vértices.

# Resumen Ejecutivo
Para el presente trabajo, se ha procesado la información de las intersecciones de calles de la ciudad de San Francisco, California, Estados Unidos, almacenándolas mediante la creación de un grafo, en formato de listas de adyacencia. Para ello, se tomaron los interceptos como coordenadas con latitud y longitud, las cuales fueron representadas en el grafo como números enteros desde el 0 hasta 9644 (cantidad de interceptos menos 1).

## Imagen estática de la ciudad o porción de ciudad elegida.
![San Francisco]()

# Descripción de los datos consignados por calle
Para la realización o representación de los interceptos por calle se tomó en consideración el nombre de la calle, en conjunto con todas las calles con las que intersectan. Teniendo en un inicio un conjunto del tipo:
***Street_name** : [(latitude_1, longitude_1), (latitude_2, longitude_2), (latitude_3, longitude_4),...]*<br>
El mismo dato que sería almacenado en un diccionario (intercepts) que contenga todos los interceptos por calle (hash/llave).
*intercepts= {‘street_name_1’: [(latitude_1, longitude_1), (latitude_2, longitude_2),...], ‘street_name_2’:
…}*

### Descripción de las variables:
**intercepts**: Nombre del diccionario de interceptos por calle.
**street_name_n** : Nombre de una calle capturado desde el dataset o conjunto de datos.
**latitud_n, longitud_n** : Coordenadas de la calle donde intersecta con otra.
<br>
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
<br>
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
* intercept_1: ( -122.40545417189192, 37.75433723137436)
*Primera calle - primer intercepto:*
* ‘Street_name_1’: ‘UTAH’

* intercept_2: (-122.43974776014164, 37.73236806396732)
*Primera calle - segundo intercepto:*
* ‘Street_name_1’: ‘JOOST’

# Explicación de cómo se elaboró el grafo, qué representan las aristas y los vértices.
Primero, realizamos la lectura del dataset en dónde consideramos la latitud y la longitud de las conexiones entre calles para crear los interceptos. Se utilizan 4 diccionarios en total: 
* **Intercepts**: permite acceder a todos los puntos interceptos que conforman la calle ingresada como llave.
* **Streets**: permite acceder a todas calles a las cuales pertenece un intercepto, por lo general 2 calles.
* **Nodes**: se ingresa como llave la coordenada del intercepto y se obtiene su representación más eficiente (número entero).
* **nodeToIntercept**: se ingresa el nodo (número entero) y se accede al detalle de sus coordenadas.

Luego, tenemos la función donde se crea el grafo (la lista de adyacencia). Dentro creamos una función dónde calculamos la distancia entre el intercepto que se está evaluando y los otros interceptos de cada calle a las cuales pertenece. Este proceso se realiza para cada calle a la que pertenece el intercepto, y se almacena los datos en la lista distance, que almacena listas anidadas, cada una conteniendo el nodo y la distancia respecto al intercepto en evaluación. Luego, se ordena la lista según la distancia y se almacenan los dos más cercanos en la lista neighbours. Luego, se verifica si ambos vecinos son adyacentes por lados opuestos o si son dos nodos que se encuentran en la misma dirección. Dependiendo de esta validación, se añade respectivamente el nodo más cercano o ambos. Finalmente se devuelve el grafo creado.

Finalmente, se genera grafo con la función creada y los datos guardados del dataset.
