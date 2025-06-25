# Lab 02 - Aplicación Servidor

## Grupo 37

### <u>Integrantes:</u>

- Vazquez Joaquin
- Peralta Mariano Daniel
- Scavuzo Marco Andres
- Quevedo Tomas Luciano

### <u>Preguntas:</u>

- ¿Qué estrategias existen para poder implementar este mismo servidor pero con capacidad de atender multiples clientes simultaneamente?

Una de las estrategias es mediante threads, cada conexion crea un hilo que procesa los comandos de manera aislada para cada cliente.

- ¿Que diferencia hay si se corre el servidor desde la ip "localhost", "127.0.0.1" o "0.0.0.0"? Teniendo en cuenta que el server y el cliente se corren en diferentes maquinas

En nuestro caso, no nos percatamos de testear a tiempo esta propuesta, por lo que un compañero realizo tests en dos maquinas sobre una misma conexion, y niguna de las tres ips funciono, solo funciono con la direccion ip de su maquina.

[Video defensa g37](https://www.youtube.com/watch?v=-F3_uDARVfc)
