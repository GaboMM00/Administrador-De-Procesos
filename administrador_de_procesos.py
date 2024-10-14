import tkinter as tk
from procesos import *

class AdministradorDeProcesos:
  def __init__(self, cantidad_procesos, boton, reloj_global, root, lista_espera, lista_ejecucion,inter_bloqueados,lista_terminados,label_procesos_pendientes):
    # Boton
    self.button_generate = boton
    # Tiempos
    self.tiempo_global = 0
    self.reloj_global = reloj_global
    #Listas Graficas
    self.root = root
    self.lista_espera = lista_espera
    self.lista_ejecucion = lista_ejecucion
    self.lista_terminados = lista_terminados
    self.bloqueados=inter_bloqueados
    # Lista de procesos nuevos
    self.lista_nuevos = []
    cant = int(cantidad_procesos) if cantidad_procesos != "" else 0
    self.generar_lista_procesos(cant)
    self.generar_datos_del_programa()
    self.text = ""
    # Procesos en listos
    self.cantidad_procesos_listos = 7
    self.lista_listos = []

    self.proceso_actual=None
    # Proceos pendientes
    self.procesos_pendientes = label_procesos_pendientes

    self.cantidad_procesos_interrupcion = 0
    self.bandera_interrupcion = False
    self.tiempo_a_interrumpir=5
    self.lista_bloqueados=[]
    # Lista de resultados
    self.lista_resultados = []
    # Bandera que se activa cuando hay procesos en ejecucion
    self.estatus = False
    # Algoritmo de planificación
    self.algoritmo_de_planificacion = self.planificacion_fifo
# Algoritmo de planificación FiFo (First In, First Out)
  def planificacion_fifo(self):
    if len(self.lista_listos) > 0:
      proceso = self.lista_listos[0]  # Siempre selecciona el primer proceso en la lista
      return proceso, proceso.duracion  # Ejecuta el proceso completo
    else:
      return None, 0  # No hay procesos para ejecutar
      
  # Generar lista de procesos 
  def generar_lista_procesos(self, cantidad):
    Procesos.restart()
    self.total_time = 0
    for _ in range(cantidad):
      proceso = Procesos()
      self.total_time += proceso.duracion
      self.lista_nuevos.append(proceso)

  # Iniciar simulación (eliminar manejo de lotes)
  def iniciar_simulacion(self):
    self.llenar_lista_de_listos()
    self.mostrar_listos()
    self.procesos_pendientes.config(text=f"# de Procesos pendientes: {len(self.lista_nuevos)}")
    self.estatus = True
    self.button_generate.config(state=tk.DISABLED)
    self.procesar_siguiente_proceso()  # Iniciar con el primer proceso según el algoritmo

  # Procesar el siguiente proceso basado en el algoritmo de planificación
  def procesar_siguiente_proceso(self):
    if len(self.lista_listos) > 0 or len(self.lista_bloqueados):  # Si aún hay procesos por ejecutar
      proceso, tiempo_ejecucion = self.algoritmo_de_planificacion()
      self.proceso_actual = proceso
      if proceso:  # Si se seleccionó un proceso válido      
        self.ejecutar_tiempo_de_proceso(proceso, tiempo_ejecucion)
      else:
        print("No hay procesos listos para ejecutar")#Buscar una solucion para cuando todos los procesos sean interrumpidos
    else:
      print("Todos los procesos han sido procesados")
      self.button_generate.config(state=tk.NORMAL)
      self.estatus = False

  def retener_proceso(self,time,proceso):
    if(self.bandera_interrupcion==True):
      self.bandera_interrupcion=False
      self.lista_bloqueados.append(self.proceso_actual)
      self.lista_listos.remove(self.proceso_actual)
      self.procesar_siguiente_proceso()
    elif(time>0 and proceso.duracion>0):
      self.actualizar_reloj_global(1)
      self.actualizar_lista_de_interrupcion()
      proceso.duracion -= 1
      # self.lista_espera.delete(0, tk.END)
      self.lista_ejecucion.delete(0, tk.END)
      self.extraer_datos2(proceso, self.lista_ejecucion)
      self.root.after(1000, self.retener_proceso, time-1, proceso)
    else:
      # self.bandera_interrupcion=False
      self.procesar_siguiente_proceso()  
  # Ejecutar una cantidad de tiempo de un proceso
  def ejecutar_tiempo_de_proceso(self, proceso, tiempo):
    if proceso.duracion > 0:
      # Actualizar el tiempo del proceso
      tiempo_a_ejecutar = min(tiempo, proceso.duracion)
      self.retener_proceso(tiempo_a_ejecutar,proceso)
      self.mostrar_listos(proceso)
      # 
      # 
      # Revisar si tienes que volver a meter el proceso en la lista de listos
      # 
      # 
    if proceso.duracion == 0:
      # Marcar el proceso como terminado
      self.lista_terminados.insert(tk.END, f"{proceso.id} - {proceso.nombre_de_proceso}")
      self.lista_terminados.insert(tk.END, proceso.resultado)
      self.text += f"{proceso.id} - {proceso.nombre_de_proceso}\n{proceso.resultado}\n"
      # 
      self.lista_resultados.append(proceso)
      self.lista_listos.remove(proceso)
      self.llenar_lista_de_listos()
      self.procesos_pendientes.config(text=f"# de Procesos pendientes: {len(self.lista_nuevos)}")
      self.procesar_siguiente_proceso()
  def mostrar_listos(self, event=None):
    self.lista_espera.delete(0, tk.END)
    # print("mostar listos")
    for proceso in self.lista_listos:
      # print("for")
      if event!=proceso:
        self.lista_espera.insert(tk.END, f"{proceso.id} - {proceso.nombre_de_proceso}")
        self.lista_espera.insert(tk.END, f"TME:{proceso.duracion}")
        if proceso.duracion != proceso.tiempo_maximo:
          self.lista_espera.insert(tk.END, f"TME Resgtante:{proceso.duracion}")

  def llenar_lista_de_listos(self):
    if(len(self.lista_listos) < self.cantidad_procesos_listos-self.cantidad_procesos_interrupcion):
      if(len(self.lista_nuevos) > 0):
        self.lista_listos.append(self.lista_nuevos.pop(0))
        self.llenar_lista_de_listos()

  def actualizar_reloj_global(self, suma):
    self.tiempo_global += suma
    self.reloj_global.config(text="Reloj Global:" + str(self.tiempo_global))

  def extraer_datos(self, proceso, label_list):
    label_list.insert(tk.END, f"{proceso.id} - {proceso.nombre_de_proceso}")
    label_list.insert(tk.END, proceso.resultado)
    label_list.insert(tk.END, f"TME Max:{proceso.tiempo_maximo}")
    if proceso.duracion != proceso.tiempo_maximo:
      label_list.insert(tk.END, f"TME Restante:{proceso.duracion}")

  def extraer_datos2(self, proceso, label_list):
    label_list.insert(tk.END, f"{proceso.id} - {proceso.nombre_de_proceso}")
    label_list.insert(tk.END, proceso.resultado)
    label_list.insert(tk.END, f"TME Ejecutado: {proceso.tiempo_maximo - proceso.duracion-1}")
    label_list.insert(tk.END, f"TME Restante: {proceso.duracion}")

  def generar_txt(self):
    with open('resultados.txt', 'w') as archivo:
      archivo.write(self.text + "\n")
    self.generar_tabla_de_resultados()

  def generar_datos_del_programa(self):
    txt = ""
    with open('datos.txt', 'w') as archivo:
      for proceso in self.lista_nuevos:
        txt += f"{proceso.id} - {proceso.nombre_de_proceso}\nTME:{proceso.duracion}\n{proceso.operacion}\n"
      archivo.write(txt + "\n")
      
  def interrumpir_proceso_actual(self):
    # Preguntarle a la maestra como hacerle :(
    print("Interrumpir proceso")
    self.cantidad_procesos_interrupcion += 1
    self.bandera_interrupcion = True
    self.proceso_actual.set_tiempo_a_interrumpir(self.tiempo_a_interrumpir)
    # self.procesar_siguiente_proceso()
  def actualizar_lista_de_interrupcion(self):
    self.bloqueados.delete(0, tk.END)
    for proceso in self.lista_bloqueados:
      if(proceso.tiempo_interrumpido>0):
        proceso.tiempo_interrumpido-=1
        self.bloqueados.insert("end",f"{proceso.id} - {proceso.nombre_de_proceso}")
        self.bloqueados.insert("end",f"TME:{self.tiempo_a_interrumpir-proceso.tiempo_interrumpido-1}")
      elif proceso.tiempo_interrumpido <= 0:
        self.lista_listos.append(proceso)
        self.lista_bloqueados.remove(proceso)
    
  def terminar_proceso_actual_con_error(self):
    self.proceso_actual.terminar_proceso_error()
  def generar_tabla_de_resultados(self):
    with open("resultados.txt", "a") as file:
      # Obtener el encabezado (los nombres de los atributos del primer objeto)
      headers=["ID","Tiempo de llegada","Tiempo de Finalizacion","Tiempo de retorno","Tiempo de respuesta","Tiempo de espera","Tiempo de servicio"]
      # headers = vars(self.lista_resultados[0]).keys()
      file.write("\t".join(headers) + "\n")
      
      # Escribir las filas (los valores de los atributos de cada objeto)
      for proceso in self.lista_resultados:
          # valores = [str(valor) for valor in vars(proceso).values()]
          v = [str(proceso.id),str(proceso.tiempo_de_llegada),str(proceso.tiempo_de_finalizacion),str(proceso.tiempo_de_retorno),str(proceso.tiempo_de_respuesta),str(proceso.tiempo_de_espera),str(proceso.tiempo_de_servicio)]
          file.write(v[0]+"\t\t\t\t\t"+v[1]+"\t\t\t\t\t\t\t\t\t\t\t"+v[2]+"\t\t\t\t\t\t\t\t\t\t\t"+v[3]+"\t\t\t\t\t\t\t\t\t"+v[4]+"\t\t\t\t\t\t\t\t\t\t"+v[5]+"\t\t\t\t\t\t\t\t\t\t"+v[6]+"\n")