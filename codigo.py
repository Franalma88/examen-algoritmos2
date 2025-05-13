import heapq
import json
import os
from datetime import datetime

ARCHIVO = "tareas.json"

class Tarea:
    def __init__(self, nombre, prioridad, fecha_vencimiento, dependencias=None):
        self.nombre = nombre
        self.prioridad = int(prioridad)
        self.fecha_vencimiento = datetime.strptime(fecha_vencimiento, "%Y-%m-%d")
        self.dependencias = dependencias or []

    def to_dict(self):
        return {
            "nombre": self.nombre,
            "prioridad": self.prioridad,
            "fecha_vencimiento": self.fecha_vencimiento.strftime("%Y-%m-%d"),
            "dependencias": self.dependencias
        }

    @staticmethod
    def from_dict(d):
        return Tarea(
            d["nombre"],
            d["prioridad"],
            d["fecha_vencimiento"],
            d["dependencias"]
        )

    def __lt__(self, other):
        if self.prioridad == other.prioridad:
            return self.fecha_vencimiento < other.fecha_vencimiento
        return self.prioridad < other.prioridad

class GestorTareas:
    def __init__(self):
        self.tareas = []
        self.tareas_dict = {}  # Para evitar duplicados y manejar dependencias
        self.cargar()

    def guardar(self):
        with open(ARCHIVO, "w") as f:
            json.dump([t.to_dict() for t in self.tareas], f)

    def cargar(self):
        if os.path.exists(ARCHIVO):
            with open(ARCHIVO, "r") as f:
                datos = json.load(f)
                for d in datos:
                    tarea = Tarea.from_dict(d)
                    heapq.heappush(self.tareas, tarea)
                    self.tareas_dict[tarea.nombre] = tarea

    def añadir_tarea(self, nombre, prioridad, fecha_vencimiento, dependencias=None):
        if not nombre.strip():
            print(" El nombre no puede estar vacío.")
            return
        if nombre in self.tareas_dict:
            print(" Ya existe una tarea con ese nombre.")
            return
        try:
            prioridad = int(prioridad)
        except ValueError:
            print(" La prioridad debe ser un número entero.")
            return

        tarea = Tarea(nombre, prioridad, fecha_vencimiento, dependencias)
        
        heapq.heappush(self.tareas, tarea)
        self.tareas_dict[nombre] = tarea
        self.guardar()
        print("Tarea añadida correctamente.")

    def mostrar_tareas(self, ordenar_por_fecha=False):
        tareas_ordenadas = sorted(self.tareas, key=lambda t: (t.fecha_vencimiento if ordenar_por_fecha else t))
        print("\n Tareas pendientes:")
        for tarea in tareas_ordenadas:
            print(f"- {tarea.nombre} | Prioridad: {tarea.prioridad} | Vence: {tarea.fecha_vencimiento.date()} | Dep: {', '.join(tarea.dependencias)}")

    def completar_tarea(self, nombre):
        if nombre not in self.tareas_dict:
            print(" Tarea no encontrada.")
            return

        # Validar que no haya otras tareas dependiendo de esta
        for t in self.tareas:
            if nombre in t.dependencias:
                print(f" No puedes completar '{nombre}' porque depende de ella la tarea '{t.nombre}'.")
                return

        self.tareas = [t for t in self.tareas if t.nombre != nombre]
        heapq.heapify(self.tareas)
        del self.tareas_dict[nombre]
        self.guardar()
        print(" Tarea completada y eliminada.")

    def obtener_siguiente(self):
        if not self.tareas:
            print(" No hay tareas pendientes.")
            return
        siguiente = self.tareas[0]
        print(f"\n Siguiente tarea: {siguiente.nombre} | Prioridad: {siguiente.prioridad} | Vence: {siguiente.fecha_vencimiento.date()}")

# -------------------------------
# Menú de uso
# -------------------------------

def menu():
    gestor = GestorTareas()

    while True:
        print("\n🐾 Menú - Gestor de tareas para tienda de animales")
        print("1. Añadir tarea")
        print("2. Mostrar tareas por prioridad")
        print("3. Mostrar tareas por fecha de vencimiento")
        print("4. Marcar tarea como completada")
        print("5. Obtener siguiente tarea")
        print("6. Salir")
        op = input("Elige una opción: ")

        if op == "1":
            nombre = input("Nombre de la tarea: ").strip()
            prioridad = input("Prioridad (entero, menor es más urgente): ")
            fecha = input("Fecha de vencimiento (YYYY-MM-DD): ")
            deps = input("Dependencias (nombres separados por coma, o nada): ").strip()
            dependencias = [d.strip() for d in deps.split(",")] if deps else []
            gestor.añadir_tarea(nombre, prioridad, fecha, dependencias)

        elif op == "2":
            gestor.mostrar_tareas(ordenar_por_fecha=False)
        elif op == "3":
            gestor.mostrar_tareas(ordenar_por_fecha=True)
        elif op == "4":
            nombre = input("Nombre de la tarea a completar: ").strip()
            gestor.completar_tarea(nombre)
        elif op == "5":
            gestor.obtener_siguiente()
        elif op == "6":
            print(" ¡Hasta luego!")
            break
        else:
            print(" Opción no válida.")

if __name__ == "__main__":
    menu()
