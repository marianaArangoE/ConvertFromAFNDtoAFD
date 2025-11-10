import graphviz
import json
import os
from typing import Set, Dict, List, Tuple, Optional, Union
from collections import deque


# ============================================================
# CLASE AFND (Autómata Finito No Determinista)
# ============================================================

class AFND:
    def __init__(self, 
                 estados: Set[str], 
                 alfabeto: Set[str], 
                 transiciones: Dict[Tuple[str, str], Set[str]], 
                 estado_inicial: str, 
                 estados_finales: Set[str]):
        self.estados = estados
        self.alfabeto = alfabeto
        self.transiciones = transiciones
        self.estado_inicial = estado_inicial
        self.estados_finales = estados_finales
        
    # Revisa los conjuntos de transiciones
    def obtener_transicion(self, estado: str, simbolo: str) -> Set[str]:
        return self.transiciones.get((estado, simbolo), set())
    
    # Si tengo varios estados, los une
    def mover(self, estados: Set[str], simbolo: str) -> Set[str]:
        resultado = set()
        for estado in estados:
            resultado.update(self.obtener_transicion(estado, simbolo))
        return resultado

    # Chequea si la cadena es aceptada
    def evaluar_cadena(self, cadena: str) -> bool:
        # Empieza en el estado inicial
        estados_actuales = {self.estado_inicial}
        # Recorre cada símbolo de la cadena
        for simbolo in cadena:
            if simbolo not in self.alfabeto:
                return False
            estados_actuales = self.mover(estados_actuales, simbolo)
            if not estados_actuales:
                return False
        # Si alguno de los estados actuales es final, acepta
        return len(estados_actuales & self.estados_finales) > 0

    # Verifica si el autómata es no determinista
    def validar_no_determinismo(self) -> Tuple[bool, str]:
        for (estado, simbolo), destinos in self.transiciones.items():
            if len(destinos) > 1:
                return (True, f"Tiene múltiples destinos (δ({estado}, {simbolo}) = {destinos})")
        for estado in self.estados:
            for simbolo in self.alfabeto:
                if (estado, simbolo) not in self.transiciones:
                    return (True, f"Transición faltante: δ({estado}, {simbolo}) no está definida")
        return (False, "El autómata ingresado es determinista")

    # Dibuja el diagrama del AFND
    def diagramar(self, nombre_archivo: str = "afnd"):
        dot = graphviz.Digraph(comment='AFND')
        dot.attr(rankdir='LR')
        dot.attr('node', shape='circle')
        
        for estado in self.estados:
            if estado in self.estados_finales:
                dot.node(estado, shape='doublecircle')
            else:
                dot.node(estado)
        
        dot.node('', shape='none')
        dot.edge('', self.estado_inicial)
        
        transiciones_agrupadas = {}
        for (origen, simbolo), destinos in self.transiciones.items():
            for destino in destinos:
                key = (origen, destino)
                transiciones_agrupadas.setdefault(key, []).append(simbolo)
        
        for (origen, destino), simbolos in transiciones_agrupadas.items():
            dot.edge(origen, destino, label=','.join(sorted(set(simbolos))))
        
        dot.render(nombre_archivo, format='png', cleanup=True)
        print(f"\n✓ Diagrama AFND generado: {nombre_archivo}.png")
        return dot


# ============================================================
# CLASE AFD (Autómata Finito Determinista)
# ============================================================

class AFD:
    def __init__(self, estados: Set[str], alfabeto: Set[str],
                 transiciones: Dict[Tuple[str, str], str],
                 estado_inicial: str, estados_finales: Set[str]):
        self.estados = estados
        self.alfabeto = alfabeto
        self.transiciones = transiciones
        self.estado_inicial = estado_inicial
        self.estados_finales = estados_finales
    
    def obtener_transicion(self, estado: str, simbolo: str) -> Optional[str]:
        return self.transiciones.get((estado, simbolo))
    
    # Como solo hay un camino posible
    def evaluar_cadena(self, cadena: str) -> bool:
        estado_actual = self.estado_inicial
        for simbolo in cadena:
            if simbolo not in self.alfabeto:
                return False
            estado_actual = self.obtener_transicion(estado_actual, simbolo)
            if estado_actual is None:
                return False
        return estado_actual in self.estados_finales

    def diagramar(self, nombre_archivo: str = "afd"):
        dot = graphviz.Digraph(comment='AFD')
        dot.attr(rankdir='LR')
        dot.attr('node', shape='circle')
        
        for estado in self.estados:
            if estado in self.estados_finales:
                dot.node(estado, shape='doublecircle')
            else:
                dot.node(estado)
        
        dot.node('', shape='none')
        dot.edge('', self.estado_inicial)
        
        for (origen, simbolo), destino in self.transiciones.items():
            dot.edge(origen, destino, label=simbolo)
        
        dot.render(nombre_archivo, format='png', cleanup=True)
        print(f"\n✓ Diagrama AFD generado: {nombre_archivo}.png")
        return dot


# ============================================================
# CONVERSOR AFND → AFD
# ============================================================

class ConversorAFNDaAFD:
    @staticmethod
    def convertir(afnd: AFND) -> AFD:
        print("\n" + "="*60)
        print("INICIANDO CONVERSIÓN DE AFND A AFD")
        print("="*60)
        
        alfabeto_afd = afnd.alfabeto
        estados_afd = set()
        transiciones_afd = {}
        estados_finales_afd = set()
        
        conjunto_inicial = frozenset({afnd.estado_inicial})
        estado_inicial_afd = ConversorAFNDaAFD._nombre_estado(conjunto_inicial)
        
        cola = deque([conjunto_inicial])
        estados_procesados = {conjunto_inicial}
        estados_afd.add(estado_inicial_afd)
        
        print(f"\nEstado inicial AFD: {estado_inicial_afd}")
        
        if conjunto_inicial & afnd.estados_finales:
            estados_finales_afd.add(estado_inicial_afd)
            print(f"  → Es estado final")
        
        print("\nProcesando transiciones:")
        print("-" * 40)
        
        while cola:
            conjunto_actual = cola.popleft()
            nombre_actual = ConversorAFNDaAFD._nombre_estado(conjunto_actual)
            
            for simbolo in alfabeto_afd:
                conjunto_mover = afnd.mover(conjunto_actual, simbolo)
                conjunto_destino = frozenset(conjunto_mover)
                nombre_destino = ConversorAFNDaAFD._nombre_estado(conjunto_destino)
                
                print(f"  δ({nombre_actual}, {simbolo}) = {nombre_destino}")
                transiciones_afd[(nombre_actual, simbolo)] = nombre_destino
                
                if conjunto_destino not in estados_procesados:
                    estados_procesados.add(conjunto_destino)
                    estados_afd.add(nombre_destino)
                    cola.append(conjunto_destino)
                    
                    if conjunto_destino & afnd.estados_finales:
                        estados_finales_afd.add(nombre_destino)
                        print(f"    → {nombre_destino} es estado final")

        print("\n" + "="*60)
        print("CONVERSIÓN COMPLETADA")
        print("="*60)
        
        return AFD(estados_afd, alfabeto_afd, transiciones_afd,
                   estado_inicial_afd, estados_finales_afd)
    
    @staticmethod
    def _nombre_estado(conjunto: frozenset) -> str:
        """Devuelve el nombre legible de un conjunto de estados"""
        if not conjunto:
            return "∅"
        return "{" + ",".join(sorted(conjunto)) + "}"


# ============================================================
# FUNCIONES PARA CREAR, GUARDAR Y CARGAR AFND
# ============================================================

def crear_afnd_desde_dict(config: dict) -> AFND:
    estados = set(config['estados'])
    alfabeto = set(config['alfabeto'])
    estado_inicial = config['estado_inicial']
    estados_finales = set(config['estados_finales'])
    
    transiciones = {}
    for t in config['transiciones']:
        origen = t['origen']
        simbolo = t['simbolo']
        destinos = set(t['destinos'])
        transiciones[(origen, simbolo)] = destinos
    
    return AFND(estados, alfabeto, transiciones, estado_inicial, estados_finales)


def guardar_afnd_en_json(afnd: AFND, nombre_archivo: str):
    data = {
        "estados": list(afnd.estados),
        "alfabeto": list(afnd.alfabeto),
        "estado_inicial": afnd.estado_inicial,
        "estados_finales": list(afnd.estados_finales),
        "transiciones": [
            {"origen": origen, "simbolo": simbolo, "destinos": list(destinos)}
            for (origen, simbolo), destinos in afnd.transiciones.items()
        ]
    }
    ruta = f"{nombre_archivo}.json"
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print(f"\n✅ AFND guardado exitosamente en '{ruta}'")


def cargar_afnd_desde_json(nombre_archivo: str) -> AFND:
    ruta = f"{nombre_archivo}.json"
    if not os.path.exists(ruta):
        raise FileNotFoundError(f"El archivo '{ruta}' no existe.")
    with open(ruta, "r", encoding="utf-8") as f:
        data = json.load(f)
    print(f"\n📂 AFND cargado desde '{ruta}' correctamente")
    return crear_afnd_desde_dict(data)
