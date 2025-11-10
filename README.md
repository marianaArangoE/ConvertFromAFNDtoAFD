# Conversor AFND → AFD con visualización

Proyecto en Python para convertir un **AFND** a **AFD**, **minimizarlo**, generar **diagramas (PNG/PDF)** y evaluar cadenas, con una **interfaz interactiva por consola**.

## Requisitos
- Python 3.9+
- Graphviz instalado en el sistema (binarios). Verifica con `dot -V`.
- Dependencias Python: `pip install -r requirements.txt`

### Instalar Graphviz (binarios del sistema)
- **Windows (Chocolatey):** `choco install graphviz -y`
- **macOS (Homebrew):** `brew install graphviz`
- **Ubuntu/Debian:** `sudo apt-get update && sudo apt-get install -y graphviz`

> Si obtienes `ExecutableNotFound: failed to execute 'dot'`, añade Graphviz al PATH del sistema.

## Instalación
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
```

## Ejecutar
```bash
# Opción 1: directamente
python src/interfaz.py

# Opción 2: como módulo
python -m src.interfaz
```

## Salidas
- Diagramas `*.png` y `*.pdf`
- Configuraciones `*.json`

## Estructura
```
automatas-conversor/
├─ README.md
├─ requirements.txt
├─ .gitignore
└─ src/
   ├─ __init__.py
   ├─ afnd_to_afd_converter.py
   └─ interfaz.py
```
