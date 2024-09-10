from administrador_de_procesos import *

class ProcesamientoPorLotesApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ProcesamientoPorLotes")
        self.root.geometry("600x400")
        self.admin = None
        
        # Atributos para los labels que se van a modificar
        self.label_processes_text = "# Procesos:"
        self.label_reloj_global_text = "Reloj Global"
        self.label_lotes_pendientes_text = "# de Lotes pendientes:"
        
        # Configurar la interfaz
        self.create_widgets()

    def create_widgets(self):
        # Crear marco superior para los controles
        frame_top = tk.Frame(self.root)
        frame_top.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

        # Etiqueta y cuadro de entrada para '# Procesos'
        self.label_processes = tk.Label(frame_top, text=self.label_processes_text)
        self.label_processes.pack(side=tk.LEFT)

        self.entry_processes = tk.Entry(frame_top, width=10)
        self.entry_processes.pack(side=tk.LEFT, padx=5)

        # Botón para 'Generar'
        
        self.button_generate = tk.Button(frame_top, text="Generar", command=lambda:self.iniciar_simulacion(self.entry_processes.get()))
        self.button_generate.pack(side=tk.LEFT, padx=10)

        # Etiqueta para 'Reloj Global'
        self.label_reloj_global = tk.Label(frame_top, text=self.label_reloj_global_text)
        self.label_reloj_global.pack(side=tk.RIGHT)

        # Crear marco principal para las listas
        frame_main = tk.Frame(self.root)
        frame_main.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Lista de 'EN ESPERA'
        label_en_espera = tk.Label(frame_main, text="EN ESPERA")
        label_en_espera.grid(row=0, column=0, padx=20)

        self.listbox_en_espera = tk.Listbox(frame_main, width=20, height=15)
        self.listbox_en_espera.grid(row=1, column=0, padx=20)

        # Lista de 'EJECUCION'
        label_ejecucion = tk.Label(frame_main, text="EJECUCION")
        label_ejecucion.grid(row=0, column=1, padx=20)

        self.listbox_ejecucion = tk.Listbox(frame_main, width=20, height=8)
        self.listbox_ejecucion.grid(row=1, column=1, padx=20, pady=(0,20))

        # Lista de 'TERMINADOS'
        label_terminados = tk.Label(frame_main, text="TERMINADOS")
        label_terminados.grid(row=0, column=2, padx=20)

        self.listbox_terminados = tk.Listbox(frame_main, width=20, height=15)
        self.listbox_terminados.grid(row=1, column=2, padx=0)
        # Scrollbar para las listas
        scrollbar = tk.Scrollbar(frame_main,orient=tk.VERTICAL)
        scrollbar.grid(row=1, column=3,padx=0, sticky="ns")
        self.listbox_terminados.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.listbox_terminados.yview)

        # Crear marco inferior para los controles
        frame_bottom = tk.Frame(self.root)
        frame_bottom.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)

        # Etiqueta para '# de Lotes pendientes:'
        self.label_lotes_pendientes = tk.Label(frame_bottom, text=self.label_lotes_pendientes_text)
        self.label_lotes_pendientes.pack(side=tk.LEFT)

        # Botón para 'OBTENER RESULTADOS'
        self.button_obtener_resultados = tk.Button(frame_bottom, text="OBTENER RESULTADOS",command=lambda:self.admin.generar_txt())
        self.button_obtener_resultados.pack(side=tk.RIGHT)
    def iniciar_simulacion(self,cantidad_procesos):
        administrador = AdministradorDeProcesos(cantidad_procesos,self.label_reloj_global,self.root,self.listbox_en_espera,self.listbox_ejecucion ,self.listbox_terminados,self.label_lotes_pendientes)
        self.admin=administrador
        self.listbox_en_espera.delete(0,tk.END)
        self.listbox_ejecucion.delete(0,tk.END)
        self.listbox_terminados.delete(0,tk.END)
        administrador.iniciar_simulacion()

    # def update_labels(self, processes_text=None, reloj_global_text=None, lotes_pendientes_text=None):
    #     """Método para actualizar los textos de los labels."""
    #     if processes_text:
    #         self.label_processes.config(text=processes_text)
    #     if reloj_global_text:
    #         self.label_reloj_global.config(text=reloj_global_text)
    #     if lotes_pendientes_text:
    #         self.label_lotes_pendientes.config(text=lotes_pendientes_text)
