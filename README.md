# Conversor AFND → AFD con visualización y evaluación

Proyecto en Python 3 que permite:

Crear y configurar un AFND (Autómata Finito No Determinista).

Convertirlo automáticamente a AFD (Determinista).

Guardar y cargar autómatas desde archivos .json.

Evaluar cadenas en ambos autómatas (comparando resultados).

Generar diagramas gráficos (.png/.pdf) del AFND y AFD usando Graphviz.

Interactuar fácilmente mediante una interfaz de consola.

## 🧩 Requisitos previos

Python 3.9 o superior

Graphviz instalado en el sistema (para generar los diagramas)

Verifica si Graphviz está instalado:

**dot -V** 

Instalación de Graphviz (según sistema operativo)
Sistema	Comando
**Windows (Chocolatey)**	choco install graphviz -y
**macOS (Homebrew)**	brew install graphviz
**Ubuntu/Debian**	sudo apt update && sudo apt install -y graphviz

⚠️ Si aparece el error ExecutableNotFound: failed to execute 'dot', asegúrate de que el binario de Graphviz esté en el PATH del sistema.

⚙️ Instalación del entorno
# Crear entorno virtual
python -m venv .venv

# Activar entorno
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

▶️ Ejecución

Ejecuta el programa desde la raíz del proyecto:

# Opción 1: directamente
python src/interfaz.py



🧠 Funcionalidades principales
1️⃣ Crear AFND manualmente

Permite definir:

Estados (ej. q0,q1,q2)

Alfabeto (ej. a,b)

Estado inicial

Estados finales

Transiciones (ej. q0,a,q1)

2️⃣ Validar si es AFND

Verifica automáticamente si el autómata es no determinista (más de un destino o transiciones faltantes).

3️⃣ Generar diagrama AFND

Genera automáticamente un archivo .png (y .pdf opcional) con el grafo del autómata.

4️⃣ Convertir AFND → AFD

Convierte el autómata paso a paso, mostrando en consola la construcción de los nuevos estados deterministas.

5️⃣ Generar diagrama AFD

Produce el diagrama determinista a partir de la conversión previa.

6️⃣ Evaluar cadenas

Permite:

Ingresar cadenas manualmente.

Generar cadenas de prueba automáticas.

Cargar desde un archivo .txt.

Evalúa cada cadena e indica si es ACEPTADA o RECHAZADA por el AFND y/o AFD.
Si ambos existen, muestra una tabla comparativa para verificar que los resultados coinciden.

7️⃣ Ver estado actual

Muestra los autómatas actualmente cargados (AFND y AFD).

8️⃣ Guardar AFND

Guarda la configuración actual del AFND en un archivo .json.

9️⃣ Cargar AFND

Permite volver a cargar un autómata guardado previamente desde un archivo .json.

🖼️ Salidas generadas
Tipo	Formato	Ubicación
Diagramas	.png, .pdf	Directorio actual
Configuración AFND	.json	Directorio actual
Evaluaciones	Consola	
💡 Ejemplo rápido
> 1. Crear AFND
Estados: q0,q1
Alfabeto: a,b
Inicial: q0
Finales: q1
Transición: q0,a,q0,q1
Transición: q1,b,q1

> 4. Convertir AFND a AFD
> 6. Evaluar cadenas → Generar automáticas → Longitud máxima: 3


Salida esperada:

'ε'   → ACEPTADA
'a'   → ACEPTADA
'b'   → RECHAZADA
'ab'  → ACEPTADA
...
✓ Ambos autómatas coinciden en todas las cadenas.