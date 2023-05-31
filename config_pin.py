# Importar librerías
import machine
import time
try:
  import urequests as requests
except:
  import requests 
import network
import esp
esp.osdebug(None)
import gc
gc.collect()

# Configuración de pines GPIO
pin_sensor = machine.Pin(27, machine.Pin.IN)
pin_pulsador = machine.Pin(26, machine.Pin.IN)
pin_servo = machine.Pin(12)
servo = machine.PWM(pin_servo)

# Configuración de los límites del pulso del servo
servo.freq(50)
servo.duty_ns(500000)  # 0 grados

# Variables para almacenar el estado anterior del sensor y el pulsador
estado_anterior_sensor = 0
estado_anterior_pulsador = 0

# Funciones para leer el estado del sensor infrarrojo y el pulsador
def leer_sensor():
    return pin_sensor.value()

def leer_pulsador():
    return pin_pulsador.value()

# Variables para almacenar las credenciales de la red WIFI
ssid = 'Dla Net'
password = 'qjja6352'

# Variables empleadas por la api de Whatsapp
numero_cel = '573234912231'
api_key = '9719222'
api_url = 'https://api.callmebot.com/whatsapp.php?phone='

# Función para conectarse a una red wifi
def conectar_wifi(ssid, password):
  station = network.WLAN(network.STA_IF)
  station.active(True)
  station.connect(ssid, password)
  while station.isconnected() == False:
    pass
  print('Conexión exitosa')
  print(station.ifconfig())

# Función para el envío de mensajes al chat de whatsapp
def enviar_mensaje(numero_cel, api_key, api_url, mensaje):
  # Configurar url para el envío de mensajes 
  url = api_url+numero_cel+'&text='+mensaje+'&apikey='+api_key

  # Realizar petición GET
  respuesta = requests.get(url)

  #Validar el estado de la petición GET
  if respuesta.status_code == 200:
    print('Mensaje enviado!')
  else:
    print('Error')
    print(respuesta.text)

# Conexión a la red WiFi
conectar_wifi(ssid, password)

# Bucle principal
while True:
    estado_sensor = leer_sensor()
    estado_pulsador = leer_pulsador()

    if estado_sensor != estado_anterior_sensor:
        print("Cambio en el estado del sensor:", estado_sensor)
        mensaje = 'Se%20ha%20detectado%20un%20movimimento%0ALa%20puerta%20se%20abrir%C3%A1%20'
        enviar_mensaje(numero_cel, api_key, api_url, mensaje)
        estado_anterior_sensor = estado_sensor

    if estado_pulsador != estado_anterior_pulsador:
        print("Cambio en el estado del pulsador:", estado_pulsador)
        mensaje = '%C2%A1Alguien%20ha%20oprimido%20el%20pulsador%21%0ALa%20puerta%20se%20abrir%C3%A1%20'
        enviar_mensaje(numero_cel, api_key, api_url, mensaje)
        estado_anterior_pulsador = estado_pulsador

    if estado_sensor == 0 or estado_pulsador == 1:
        # El sensor infrarrojo o el pulsador están activos, mueve el servo a 90 grados
        servo.duty_ns(1500000)  # 90 grados
        time.sleep(3)
    else:
        # El sensor infrarrojo y el pulsador están inactivos, mueve el servo a 0 grados
        servo.duty_ns(500000)  # 0 grados

    # Pequeña pausa para evitar lecturas rápidas del sensor y el pulsador
    time.sleep(0.1)
