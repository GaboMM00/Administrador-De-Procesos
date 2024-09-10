import tkinter as tk
import random
import time
import threading

class Proceso:
    id_autoincrement = 1

    def __init__(self):
        self.programador = random.choice(['José', 'Carlos', 'Carolina', 'Juan'])
        self.operacion, self.resultado = self.generar_operacion()
        self.tme = random.randint(6, 12)
        self.numero_programa = Proceso.id_autoincrement
        Proceso.id_autoincrement += 1

    def generar_operacion(self):
        operador = random.choice(['+', '-', '*', '/'])
        num1 = random.randint(1, 10)
        num2 = random.randint(1, 10)
        if operador == '/' and num2 == 0:
            num2 = 1  # Evitar división por cero
        return f"{num1} {operador} {num2}", eval(f"{num1}{operador}{num2}")

    def ejecutar(self):
        while self.tme > 0:
            time.sleep(1)
            self.tme -= 1
        return f"{self.numero_programa}. {self.programador} - {self.operacion} = {self.resultado}"

class Lote:
    def __init__(self, id):
        self.id = id
        self.procesos = []

    def agregar_proceso(self, proceso):
        self.procesos.append(proceso)

    def procesar(self):
        resultados = []
        for proceso in self.procesos:
            resultado = proceso.ejecutar()
            if resultado is not None:
                resultados.append(resultado)
        return resultados

class Simulador:
    def __init__(self, procesos):
        self.lotes = self.crear_lotes(procesos)
        self.resultados = []

    def crear_lotes(self, procesos):
        lotes = []
        for i in range(0, len(procesos), 7):
            lote = Lote(len(lotes) + 1)
            for j in range(i, min(i + 7, len(procesos))):
                lote.agregar_proceso(procesos[j])
            lotes.append(lote)
        return lotes

    def iniciar(self, interfaz):
        for lote in self.lotes:
            resultados = lote.procesar()
            self.resultados.append(resultados)
            interfaz.actualizar_procesos(lote)
        self.guardar_resultados()

    def guardar_resultados(self):
        with open("Resultados.txt", "w") as file:
            for i, lote in enumerate(self.resultados):
                file.write(f"Lote {i + 1}\n")
                for resultado in lote:
                    file.write(f"{resultado}\n")
                file.write("\n")

class ProcesamientoPorLotesApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Procesamiento Por Lotes")
        self.root.geometry("600x400")
        
        self.label_processes_text = "# Procesos:"
        self.label_reloj_global_text = "Reloj Global"
        self.label_lotes_pendientes_text = "# de Lotes pendientes:"
        
        self.create_widgets()
        self.procesos = []
        self.simulador = None
        self.reloj_corriendo = False

    def create_widgets(self):
        frame_top = tk.Frame(self.root)
        frame_top.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

        self.label_processes = tk.Label(frame_top, text=self.label_processes_text)
        self.label_processes.pack(side=tk.LEFT)

        self.entry_processes = tk.Entry(frame_top, width=10)
        self.entry_processes.pack(side=tk.LEFT, padx=5)

        self.button_generate = tk.Button(frame_top, text="Generar", command=self.iniciar_simulacion)
        self.button_generate.pack(side=tk.LEFT, padx=10)

        self.label_reloj_global = tk.Label(frame_top, text=self.label_reloj_global_text)
        self.label_reloj_global.pack(side=tk.RIGHT)

        frame_main = tk.Frame(self.root)
        frame_main.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        label_en_espera = tk.Label(frame_main, text="EN ESPERA")
        label_en_espera.grid(row=0, column=0, padx=20)

        self.listbox_en_espera = tk.Listbox(frame_main, width=20, height=15)
        self.listbox_en_espera.grid(row=1, column=0, padx=20)

        label_ejecucion = tk.Label(frame_main, text="EJECUCION")
        label_ejecucion.grid(row=0, column=1, padx=20)

        self.listbox_ejecucion = tk.Listbox(frame_main, width=20, height=8)
        self.listbox_ejecucion.grid(row=1, column=1, padx=20, pady=(0,20))

        label_terminados = tk.Label(frame_main, text="TERMINADOS")
        label_terminados.grid(row=0, column=2, padx=20)

        self.listbox_terminados = tk.Listbox(frame_main, width=20, height=15)
        self.listbox_terminados.grid(row=1, column=2, padx=20)

        frame_bottom = tk.Frame(self.root)
        frame_bottom.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)

        self.label_lotes_pendientes = tk.Label(frame_bottom, text=self.label_lotes_pendientes_text)
        self.label_lotes_pendientes.pack(side=tk.LEFT)

        self.button_obtener_resultados = tk.Button(frame_bottom, text="OBTENER RESULTADOS", command=self.obtener_resultados)
        self.button_obtener_resultados.pack(side=tk.RIGHT)

    def iniciar_simulacion(self):
        num_procesos = int(self.entry_processes.get()) if self.entry_processes.get().isdigit() else 15
        self.procesos = [Proceso() for _ in range(num_procesos)]
        self.simulador = Simulador(self.procesos)
        self.reloj_corriendo = True
        
        # Ejecutar la simulación y la actualización del reloj en hilos separados
        threading.Thread(target=self.actualizar_reloj).start()
        threading.Thread(target=self.simulador.iniciar, args=(self,)).start()

    def actualizar_reloj(self):
        reloj = 0
        while self.reloj_corriendo:
            self.label_reloj_global.config(text=f"Reloj Global: {reloj}")
            time.sleep(1)
            reloj += 1

    def obtener_resultados(self):
        if self.simulador:
            self.reloj_corriendo = False
            self.simulador.guardar_resultados()
            tk.messagebox.showinfo("Resultados", "Los resultados se han guardado en Resultados.txt")

    def actualizar_procesos(self, lote):
        if lote.procesos:
            self.listbox_en_espera.delete(0, tk.END)
            for proceso in lote.procesos[1:]:
                self.listbox_en_espera.insert(tk.END, f"{proceso.numero_programa} - {proceso.programador}")

            proceso_actual = lote.procesos[0]
            self.listbox_ejecucion.delete(0, tk.END)
            self.listbox_ejecucion.insert(tk.END, f"{proceso_actual.numero_programa} - {proceso_actual.programador}")
            self.listbox_ejecucion.insert(tk.END, f"{proceso_actual.operacion}")

            self.listbox_terminados.insert(tk.END, f"{proceso_actual.numero_programa} - {proceso_actual.operacion} = {proceso_actual.resultado}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ProcesamientoPorLotesApp(root)
    root.mainloop()
