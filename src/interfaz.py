from logica_automata import (
    AFND, AFD, ConversorAFNDaAFD, crear_afnd_desde_dict,
    guardar_afnd_en_json, cargar_afnd_desde_json
)
import os
from typing import List


class InterfazInteractiva:
    def __init__(self):
        self.afnd = None
        self.afd = None
    def mostrar_menu_principal(self):
        print("\n" + "="*60)
        print(" TAREA: CONVERSOR AFND → AFD")
        print("="*60)
        print("\n1. Crear AFND manualmente")
        print("2. Validar si es AFND (no determinista)")
        print("3. Generar diagrama AFND")
        print("4. Convertir AFND a AFD")
        print("5. Generar diagrama AFD")
        print("6. Evaluar cadenas")
        print("7. Ver estado actual")
        print("8. Guardar AFND en JSON")
        print("9. Cargar AFND desde JSON")
        print("0. Salir")
        print("-"*60)

    # ============================================================
    # 1. CREAR AFND
    # ============================================================
    def crear_afnd_manual(self):
        print("\n--- 1. CREAR AFND MANUALMENTE ---")
        self.afnd = None
        self.afd = None

        try:
            estados_str = input("Estados (ej: q0,q1,q2): ").strip()
            estados = [e.strip() for e in estados_str.split(',') if e.strip()]
            if not estados:
                print("✗ Debe ingresar al menos un estado.")
                return

            alfabeto_str = input("Alfabeto (ej: a,b): ").strip()
            alfabeto = [s.strip() for s in alfabeto_str.split(',') if s.strip()]
            if not alfabeto:
                print("✗ Debe ingresar al menos un símbolo en el alfabeto.")
                return

            estado_inicial = input("Estado inicial: ").strip()
            if estado_inicial not in estados:
                print(f"✗ El estado inicial '{estado_inicial}' no está en {estados}")
                return

            estados_finales_str = input("Estados finales (ej: q1,q2): ").strip()
            estados_finales = [e.strip() for e in estados_finales_str.split(',') if e.strip()]
            if not estados_finales:
                print("✗ Debe indicar al menos un estado final.")
                return

            print("\n--- TRANSICIONES ---")
            print("Formato: origen,simbolo,destino1,destino2,... (Enter vacío para terminar)\n")

            transiciones_dict = {}

            while True:
                trans_str = input("Transición: ").strip()
                if not trans_str:
                    break

                partes = [p.strip() for p in trans_str.split(',')]
                if len(partes) < 3:
                    print("  ✗ Formato inválido. Ej: q0,a,q1,q2")
                    continue

                origen, simbolo = partes[0], partes[1]
                destinos = [d for d in partes[2:] if d]

                if origen not in estados or simbolo not in alfabeto:
                    print(f"  ✗ Error en origen o símbolo no válido.")
                    continue

                for d in destinos:
                    if d not in estados:
                        print(f"  ✗ Destino '{d}' no está en {estados}")
                        break
                else:
                    transiciones_dict.setdefault((origen, simbolo), set()).update(destinos)
                    print(f"  ✓ Agregada: δ({origen}, {simbolo}) = {sorted(list(transiciones_dict[(origen, simbolo)]))}")

            transiciones_config = [
                {'origen': k[0], 'simbolo': k[1], 'destinos': list(v)}
                for k, v in transiciones_dict.items()
            ]

            config = {
                'estados': estados,
                'alfabeto': alfabeto,
                'estado_inicial': estado_inicial,
                'estados_finales': estados_finales,
                'transiciones': transiciones_config
            }

            self.afnd = crear_afnd_desde_dict(config)
            print("\n✓ AFND creado exitosamente.")
            self.validar_afnd()

        except Exception as e:
            print(f"\n✗ Error: {e}")
            self.afnd = None

    # ============================================================
    # 2. VALIDAR AFND
    # ============================================================
    def validar_afnd(self):
        print("\n--- 2. VALIDACIÓN DE NO DETERMINISMO ---")
        if not self.afnd:
            print("✗ Primero debe crear o cargar un AFND (Opción 1 o 9)")
            return
        es_nd, razon = self.afnd.validar_no_determinismo()
        if es_nd:
            print(f"✓ VALIDADO: El autómata es un AFND.")
            print(f"  Razón: {razon}")
        else:
            print(f"✗ El autómata ingresado es determinístico.")
            print(f"  Razón: {razon}")

    # ============================================================
    # 3. DIAGRAMA AFND
    # ============================================================
    def generar_diagrama_afnd(self):
        if not self.afnd:
            print("✗ Primero debe crear o cargar un AFND (Opción 1 o 9)")
            return
        nombre = input("Nombre del archivo AFND (sin extensión): ").strip() or "afnd"
        self.afnd.diagramar(nombre)

    # ============================================================
    # 4. CONVERSIÓN AFND → AFD
    # ============================================================
    def convertir_a_afd(self):
        if not self.afnd:
            print("✗ Primero debe crear o cargar un AFND (Opción 1 o 9)")
            return
        self.afd = ConversorAFNDaAFD.convertir(self.afnd)
        print("\n✓ Conversión a AFD completada.")

    # ============================================================
    # 5. DIAGRAMA AFD
    # ============================================================
    def generar_diagrama_afd(self):
        if not self.afd:
            print("✗ Primero debe convertir el AFND a AFD (Opción 4)")
            return
        nombre = input("Nombre del archivo AFD (sin extensión): ").strip() or "afd"
        self.afd.diagramar(nombre)

    # ============================================================
    # 6. EVALUAR CADENAS
    # ============================================================
    def evaluar_cadenas(self):
        if not self.afnd and not self.afd:
            print("\n✗ No hay autómatas disponibles.")
            return

        print("\n--- 6. EVALUAR CADENAS ---")
        print("1. Ingresar cadenas manualmente")
        print("2. Generar cadenas de prueba automáticamente")
        print("3. Cargar cadenas desde archivo (.txt)")
        opcion = input("\nSeleccione opción: ").strip()

        cadenas = []
        if opcion == '1':
            print("\nIngrese las cadenas (Enter vacío para terminar):")
            while True:
                s = input("Cadena: ")
                if s == "":
                    break
                cadenas.append(s)
        elif opcion == '2':
            alfabeto = list(self.afnd.alfabeto if self.afnd else self.afd.alfabeto)
            alfabeto = [x for x in alfabeto if x not in ('ε', '')]
            try:
                longitud_max = int(input("Longitud máxima (default 3): ").strip() or "3")
            except ValueError:
                longitud_max = 3
            cadenas = self.generar_cadenas_prueba(alfabeto, longitud_max)
            print(f"\nGeneradas {len(cadenas)} cadenas de prueba")
        elif opcion == '3':
            archivo = input("Archivo (.txt): ").strip()
            try:
                with open(archivo, 'r', encoding='utf-8') as f:
                    cadenas = [line.strip() for line in f if line.strip()]
                print(f"\nCargadas {len(cadenas)} cadenas desde {archivo}")
            except Exception as e:
                print(f"✗ Error al leer archivo: {e}")
                return
        else:
            print("\n✗ Opción inválida")
            return

        if not cadenas:
            print("\n(No hay cadenas para evaluar)")
            return

        def _eval(automata, nombre):
            print(f"\nEvaluando en {nombre}...")
            print("-"*40)
            for cadena in cadenas:
                ok = automata.evaluar_cadena(cadena)
                print(f"  '{cadena if cadena != '' else 'ε'}' → {'ACEPTADA' if ok else 'RECHAZADA'}")

        if self.afnd and self.afd:
            print("\nComparando AFND vs AFD...")
            print("{:<15} {:<12} {:<12} {:<8}".format("Cadena", "AFND", "AFD", "Coincide"))
            print("-"*52)
            todo_ok = True
            for c in cadenas:
                r1 = self.afnd.evaluar_cadena(c)
                r2 = self.afd.evaluar_cadena(c)
                coincide = (r1 == r2)
                if not coincide:
                    todo_ok = False
                print("{:<15} {:<12} {:<12} {:<8}".format(
                    f"'{c if c != '' else 'ε'}'",
                    "ACEPTA" if r1 else "RECHAZA",
                    "ACEPTA" if r2 else "RECHAZA",
                    "✓" if coincide else "✗"
                ))
            if todo_ok:
                print("\n✓ Ambos autómatas coinciden en todas las cadenas.")
            else:
                print("\n✗ Diferencias detectadas entre AFND y AFD.")
        elif self.afnd:
            _eval(self.afnd, "AFND")
        elif self.afd:
            _eval(self.afd, "AFD")

    # ============================================================
    # Generador de cadenas
    # ============================================================
    def generar_cadenas_prueba(self, alfabeto: List[str], longitud_max: int) -> List[str]:
        from itertools import product
        cadenas = ['']  # incluye la cadena vacía
        for L in range(1, longitud_max + 1):
            for comb in product(alfabeto, repeat=L):
                cadenas.append(''.join(comb))
        return cadenas

    # ============================================================
    # 7. ESTADO ACTUAL
    # ============================================================
    def mostrar_estado_actual(self):
        print("\n--- 7. ESTADO ACTUAL ---")
        if self.afnd:
            print("\nAFND:")
            print(f"  Estados: {self.afnd.estados}")
            print(f"  Alfabeto: {self.afnd.alfabeto}")
            print(f"  Inicial: {self.afnd.estado_inicial}")
            print(f"  Finales: {self.afnd.estados_finales}")
        else:
            print("\nAFND: No cargado")

        if self.afd:
            print("\nAFD:")
            print(f"  Estados: {len(self.afd.estados)}")
            print(f"  Finales: {len(self.afd.estados_finales)}")
        else:
            print("\nAFD: No generado")

    # ============================================================
    # 8. GUARDAR AFND EN JSON
    # ============================================================
    def guardar_afnd_json(self):
        if not self.afnd:
            print("✗ Primero debe crear o cargar un AFND (Opción 1 o 9)")
            return
        nombre = input("Nombre de archivo (sin extensión, ej: mi_afnd): ").strip() or "mi_afnd"
        guardar_afnd_en_json(self.afnd, nombre)

    # ============================================================
    # 9. CARGAR AFND DESDE JSON
    # ============================================================
    def cargar_afnd_json(self):
        nombre = input("Nombre del archivo (sin extensión, ej: mi_afnd): ").strip()
        if not nombre:
            print("✗ Debe indicar un nombre.")
            return
        self.afnd = cargar_afnd_desde_json(nombre)
        self.afd = None
        print("✓ AFND cargado correctamente.")

    # ============================================================
    # EJECUCIÓN PRINCIPAL
    # ============================================================
    def ejecutar(self):
        print("\n" + "="*60)
        print(" BIENVENIDO A LA TAREA DE AUTÓMATAS")
        print("="*60)
        while True:
            self.mostrar_menu_principal()
            opcion = input("Seleccione opción: ").strip()

            if opcion == '0':
                print("\n¡Hasta luego!")
                break
            elif opcion == '1':
                self.crear_afnd_manual()
            elif opcion == '2':
                self.validar_afnd()
            elif opcion == '3':
                self.generar_diagrama_afnd()
            elif opcion == '4':
                self.convertir_a_afd()
            elif opcion == '5':
                self.generar_diagrama_afd()
            elif opcion == '6':
                self.evaluar_cadenas()
            elif opcion == '7':
                self.mostrar_estado_actual()
            elif opcion == '8':
                self.guardar_afnd_json()
            elif opcion == '9':
                self.cargar_afnd_json()
            else:
                print("\n✗ Opción inválida")


def main():
    interfaz = InterfazInteractiva()
    interfaz.ejecutar()


if __name__ == "__main__":
    main()
