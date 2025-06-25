# Redes_y_sistemas

MyPrompt : 
```bash
PS1='\[\e[33m\](\A)\[\e[32m\][\u@\h]\[\e[34m\]\[\e[35m\]{jobs:\j}\[\e[34m\] \W\[\e[0m\] : '

(hs:min)[user@host]{jobs:} working_directory : 
```
---

## Lab00 - Ejercicios de introduccion.
#### Dependencias
- Python 3.*
#### Ejecucion
```Python
python hget.py http://_some_url 
```
---
## Lab01 - API with Flask - Python
#### Dependencias
- Python 3.*
- Python virtual environment
- pytest
- pip
#### Ejecucion
```Python
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py
```
#### Para testestear
```Python
python test.py
pytest test_pytest_main.py
```

---
## Lab02 - Aplicacion/servidor - Python
#### Dependencias
- Python 3.*
- python virtual environment
#### Ejecucion
En diferentes terminales, sobre la misma pc

- Server
```Python
python -m venv .venv
source .venv/bin/activate
python server.py
```
- Cliente
```Python
python server-test.py
```
---
## Lab03 - Capa de transporte - C++/OMNeT++
#### Dependencias
- [OMNeT++](https://omnetpp.org/download/)
- C++ compiler

ps: trabajamos en una maquina virtual con todo ya previamente instalado por si falta alguna dependencia
#### Ejecucion
- Desde OMNeT++
---
## Lab04 - Capa de red - C++/omnet++
#### Dependencias
- [OMNeT++](https://omnetpp.org/download/)
- C++ compiler

ps: trabajamos en una maquina virtual con todo ya previamente instalado por si falta alguna dependencia
#### Ejecucion
- Desde OMNeT++
---