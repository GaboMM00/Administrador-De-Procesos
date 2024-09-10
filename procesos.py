import random
class Procesos:
  numero_de_proceso=1
  nombres_de_procesos=["Jose","Juan","Carolina","Carlos"]
  _operaciones=["+","-","*","/"]
  def __init__(self):
    self.nombre_de_proceso=""
    self.duracion=0
    self.operacion=""
    self.resultado=""
    #Genera un id autoincremental Global
    self.id=Procesos.numero_de_proceso
    Procesos.numero_de_proceso+=1
    #Inicializa los metodos con un valor aleatorio
    self.duracion=random.randint(6,12)
    self.operacion=self._operaciones[random.randint(0,3)]
    self.resultado=self.generar_operacion()
    self.nombre_de_proceso=self.nombres_de_procesos[random.randint(0,3)]
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
    return f"{num1} {self.operacion} {num2} = {resultado}"
  @staticmethod
  def restart():
    Procesos.numero_de_proceso=1

# proceso =Procesos()
# print(proceso.operacion)
# print(proceso.duracion)