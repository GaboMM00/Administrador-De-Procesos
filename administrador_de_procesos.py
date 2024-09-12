import tkinter as tk
from tkinter import ttk
from procesos import *
class AdministradorDeProcesos:
  def __init__(self,cantidad_procesos,reloj_global,root,lista_espera,lista_ejecucion,lista_terminados,lotes_pendientes):
    # Tiempos
    self.tiempo_global = 0
    self.reloj_global = reloj_global
    #Listas Graficas
    self.root = root
    self.lista_espera = lista_espera
    self.lista_ejecucion = lista_ejecucion
    self.lista_terminados = lista_terminados
    self.lotes_pendientes = lotes_pendientes
    #Lotes 
    self.lote_actual = 0
    self.procesos_por_lote = 7
    self.matriz_procesos = []
    cant = int(cantidad_procesos)
    self.generar_matriz_procesos(cant)
    self.generar_datos_del_programa()
    self.text = ""

  def generar_matriz_procesos(self, cantidad):
    Procesos.restart()
    cantidad_lotes = int(cantidad/self.procesos_por_lote)+(1 if cantidad%self.procesos_por_lote!=0 else 0)
    self.total_time=0
    for i in range(cantidad_lotes):
      j = 0
      self.matriz_procesos.append([])
      while(j<self.procesos_por_lote and cantidad!=0):
        cantidad -= 1
        proceso = Procesos()
        self.total_time += proceso.duracion
        self.matriz_procesos[i].append(proceso)
        j += 1


  def iniciar_simulacion(self):
      self.lote_actual = 0  
      self.procesar_lote()  

  def procesar_lote(self):
    if self.lote_actual < len(self.matriz_procesos):  # Si aún hay lotes por procesar
        self.lotes_pendientes.config(text=f"# de Lotes pendientes: {len(self.matriz_procesos)-(self.lote_actual+1)}")
        self.ejecutar_procesos(self.matriz_procesos[self.lote_actual], 0, self.lote_actual+1)  # Procesar el lote actual
    else:
        print("Todos los lotes han sido procesados")
        print(f"Tiempo total: {self.total_time}")

  def ejecutar_procesos(self, lista_procesos, proceso_actual, lote):
    # Limpiar las listas de la UI
    self.lista_espera.delete(0, tk.END)
    self.lista_ejecucion.delete(0, tk.END)

    if proceso_actual < len(lista_procesos) and lista_procesos[proceso_actual].duracion > 0:
        self.extraer_datos(lista_procesos[proceso_actual], self.lista_ejecucion)

        if proceso_actual + 1 < len(lista_procesos):
            self.extraer_datos(lista_procesos[proceso_actual + 1], self.lista_espera)
            self.lista_espera.insert(tk.END, f"Procesos pendientes: {len(lista_procesos) - (proceso_actual +2)}")

        lista_procesos[proceso_actual].duracion -= 1
        self.actualizar_reloj_global(1)
        
        # Volver a ejecutar el mismo proceso después de 1 segundo
        self.root.after(1000, self.ejecutar_procesos, lista_procesos, proceso_actual, lote)

    elif proceso_actual < len(lista_procesos):
        if proceso_actual == 0:
            self.lista_terminados.insert(tk.END, f"Lote {lote}\n")
            self.text += f"Lote {lote}\n"

        self.lista_terminados.insert(tk.END, f"{lista_procesos[proceso_actual].id} - {lista_procesos[proceso_actual].nombre_de_proceso}")
        self.lista_terminados.insert(tk.END, lista_procesos[proceso_actual].resultado)
        self.text += f"{lista_procesos[proceso_actual].id} - {lista_procesos[proceso_actual].nombre_de_proceso}\n{lista_procesos[proceso_actual].resultado}\n"
        
        proceso_actual += 1
        
        # Ejecutar el siguiente proceso en el mismo lote
        self.ejecutar_procesos(lista_procesos, proceso_actual, lote)

    # Si todos los procesos del lote actual han sido ejecutados, pasa al siguiente lote
    elif proceso_actual == len(lista_procesos):
        self.lote_actual += 1
        self.procesar_lote()
    
  def actualizar_reloj_global(self,suma):
    self.tiempo_global += suma
    self.reloj_global.config(text="Reloj Global:"+str(self.tiempo_global))

  def extraer_datos(self,proceso,label_list):
    label_list.insert(tk.END,f"{proceso.id} - {proceso.nombre_de_proceso}")
    label_list.insert(tk.END,proceso.resultado)
    label_list.insert(tk.END,f"TME:{proceso.duracion}")

  def generar_txt(self):
    with open('textoDelPrograma.txt','w') as archivo:
      archivo.write(self.text+"\n")
  def generar_datos_del_programa(self):
    i=1
    txt=""
    with open('datosDelPrograma.txt','w')as archivo:
      for lote in self.matriz_procesos:
        txt+=f"Lote {i}\n"
        i+=1
        for proceso in lote:
          txt+=f"{proceso.id} - {proceso.nombre_de_proceso}\nTME:{proceso.duracion}\n{proceso.operacion}\n"
      archivo.write(txt+"\n")