import tkinter as tk
from tkinter import ttk
from procesos import *
class AdministradorDeProcesos:
  def __init__(self,cantidad_procesos):
    self.proceso_actual = 0
    self.tiempo_global = 0
    self.lista_procesos = []
    self.procesos_por_lote = 7
    cant=int(cantidad_procesos)
    self.generar_lista_procesos(cant)
    self.text=""

  def generar_lista_procesos(self, cantidad):
    Procesos.restart()
    for _ in range(cantidad):
      proceso = Procesos()
      self.lista_procesos.append(proceso)
    #return self.lista_procesos
  def ejecutar_procesos(self,root,reloj_global,lista_espera,lista_ejecucion,lista_terminados,lotes_pendientes):  
    self.tiempo_global += 1
    reloj_global.config(text="Reloj Global:"+str(self.tiempo_global))
    lista_espera.delete(0,tk.END)
    lista_ejecucion.delete(0,tk.END)
    
    if(self.proceso_actual<len(self.lista_procesos) and self.lista_procesos[self.proceso_actual].duracion>0):
      lotes_pendientes.config(text=f"# de Lotes pendientes: {int(((len(self.lista_procesos)-1)/self.procesos_por_lote)-int(self.proceso_actual/self.procesos_por_lote))}")
      # self.text+=f"# de Lotes pendientes: {int(((len(self.lista_procesos)-1)/self.procesos_por_lote)-int(self.proceso_actual/self.procesos_por_lote))}"
      self.extraer_datos(self.lista_procesos[self.proceso_actual],lista_ejecucion)
      if(self.proceso_actual+1<len(self.lista_procesos)):
        self.extraer_datos(self.lista_procesos[self.proceso_actual+1],lista_espera)
        sobras=len(self.lista_procesos)-(int(len(self.lista_procesos)/self.procesos_por_lote)*self.procesos_por_lote)
        # print(sobras)
        if(self.proceso_actual>len(self.lista_procesos)-sobras-1):
          lista_espera.insert(tk.END,f"Procesos pendientes: {sobras-(self.proceso_actual%self.procesos_por_lote)-1}")
          # self.text+=f"Procesos pendientes: {sobras-(self.proceso_actual%self.procesos_por_lote)-1}"
          # print(sobras)
        else:  
          lista_espera.insert(tk.END,f"Procesos pendientes: {self.procesos_por_lote-(self.proceso_actual%self.procesos_por_lote)-1}")
          # self.text+=f"Procesos pendientes: {self.procesos_por_lote-(self.proceso_actual%self.procesos_por_lote)-1}"
      self.lista_procesos[self.proceso_actual].duracion-=1
      root.after(1000, self.ejecutar_procesos, root,reloj_global, lista_espera, lista_ejecucion, lista_terminados,lotes_pendientes)
    elif(self.proceso_actual<len(self.lista_procesos)):
      if((self.proceso_actual)%self.procesos_por_lote==0):
        lista_terminados.insert(tk.END,f"Lote {int(self.proceso_actual/self.procesos_por_lote)+1}")
        self.text+=f"Lote {int(self.proceso_actual/self.procesos_por_lote)+1}\n"
      lista_terminados.insert(tk.END,f"{self.lista_procesos[self.proceso_actual].id} - {self.lista_procesos[self.proceso_actual].nombre_de_proceso}")
      lista_terminados.insert(tk.END,self.lista_procesos[self.proceso_actual].resultado)
      self.text+=f"{self.lista_procesos[self.proceso_actual].id} - {self.lista_procesos[self.proceso_actual].nombre_de_proceso}\n{self.lista_procesos[self.proceso_actual].resultado}\n"
      self.proceso_actual += 1
      self.ejecutar_procesos(root,reloj_global,lista_espera,lista_ejecucion,lista_terminados,lotes_pendientes)
    
    
  def extraer_datos(self,proceso,label_list):
    label_list.insert(tk.END,f"{proceso.id} - {proceso.nombre_de_proceso}")
    label_list.insert(tk.END,proceso.resultado)
    label_list.insert(tk.END,f"TME:{proceso.duracion}")

  def generar_txt(self):
    with open('textoDelPrograma.txt','w') as archivo:
      archivo.write(self.text+"\n")
