import random
class Procesos:
  # Atributos estaticos de la clase
  numero_de_proceso=1
  nombres_de_procesos=["Jose","Juan","Carolina","Carlos"]
  _operaciones=["+","-","*","/"]

  def __init__(self):
    # Datos Iniciales del Proceso
    self.nombre_de_proceso=""
    self.duracion=0
    self.operacion=""
    self.resultado=""
    #Genera un id autoincremental Global
    self.id=Procesos.numero_de_proceso
    Procesos.numero_de_proceso+=1
    #Inicializa los atributos iniciales con un valor aleatorio
    self.duracion=random.randint(6,12)
    self.tiempo_maximo=self.duracion
    self.operacion=self._operaciones[random.randint(0,3)]
    self.resultado=self.generar_operacion()
    self.nombre_de_proceso=self.nombres_de_procesos[random.randint(0,3)]
    # Datos posteriores del proceso
    self.tiempo_de_llegada=0
    self.tiempo_de_finalizacion=0
    self.tiempo_de_retorno=0
    # Tiempo transcurrido desde que llega hasta que es atendido por primera vez.
    self.tiempo_de_respuesta=0
    self.tiempo_de_espera=0
    # Tiempo de servicio = tiempo maximo estimado
    self.tiempo_de_servicio=0

    # Tiempo  interrumpido
    self.tiempo_interrumpido=0

  def generar_operacion(self):
    num1=random.randint(0,100)
    num2=random.randint(1,100)
    if(self.operacion=="+"):
      resultado=num1+num2
    elif(self.operacion=="-"):
      resultado=num1-num2
    elif(self.operacion=="*"):
      resultado=num1*num2
    elif(self.operacion=="/"):
      resultado=num1/num2
    self.operacion=f"{num1} {self.operacion} {num2}"
    return f"{self.operacion} = {resultado}"
  def set_tiempo_a_interrumpir(self,tiempo_a_interrumpir):
    self.tiempo_interrumpido=tiempo_a_interrumpir
  # Hora en la que el proceso llega al sistema
  def asignar_tiempo_de_llegada(self,tiempo_de_llegada):
    self.tiempo_de_llegada=tiempo_de_llegada
  # Hora en la que el proceso termino su ejecucion
  def asignar_tiempo_de_finalizacion(self,tiempo_de_finalizacion):  
    self.tiempo_de_finalizacion=tiempo_de_finalizacion    
  # Tiempo que transcurre desde que llega hasta que termina su ejecucion
  def calcular_tiempo_de_retorno(self): 
    self.tiempo_de_retorno=self.tiempo_de_finalizacion-self.tiempo_de_llegada
  # Tiempo transcurrido desde que llega hasta que es atendido por primera vez
  def asignar_tiempo_de_respuesta(self,tiempo):
    self.tiempo_de_respuesta=tiempo-self.tiempo_de_llegada
  # tiempo que el proceso estuvo en esperando para usar el procesador
  def sumar_tiempo_de_espera(self,tiempo_de_espera):
    self.tiempo_de_espera+=tiempo_de_espera

  def asignar_tiempo_de_servicio(self):
    # Anadir condiciones adicionales en caso de termino por error
    self.tiempo_de_servicio=self.tiempo_maximo

  def terminar_proceso_error(self):
    self.duracion=0
    self.resultado=f"{self.operacion} = Error"

  @staticmethod
  def restart():
    Procesos.numero_de_proceso=1