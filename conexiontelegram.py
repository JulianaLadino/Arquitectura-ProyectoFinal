import machine
import time
import network
import urequests

# Configuración de pines GPIO
pin_sensor = machine.Pin(27, machine.Pin.IN)
pin_pulsador = machine.Pin(25, machine.Pin.IN)
pin_servo = machine.Pin(12)
servo = machine.PWM(pin_servo)

# Configuración de los límites del pulso del servo (ajusta según tu servo)
servo.freq(50)
servo.duty_ns(2500000)  # -90 grados

# Variables para almacenar el estado anterior del sensor y el pulsador
estado_anterior_sensor = 1
estado_anterior_pulsador = 0

# Configuración de la conexión WiFi
ssid = "ZETA_ZETA"
password = "1214739710m"

def conectar_wifi():
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        sta_if.active(True)
        sta_if.connect(ssid, password)
        while not sta_if.isconnected():
            pass
    print("Conexión WiFi establecida:", sta_if.ifconfig())

# Funciones para leer el estado del sensor infrarrojo y el pulsador
def leer_sensor():
    return pin_sensor.value()

def leer_pulsador():
    return pin_pulsador.value()

def enviar_mensaje_telegram(texto):
    # Aquí debes proporcionar el token de acceso y el chat ID para enviar el mensaje a través de la API de Telegram
    token = "6167490093:AAFB1FYnKx2wZvewTb3r4uqcMSPyfmpb3w4"
    chat_id = "888243944"
    url = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={texto}"
    response = urequests.get(url)
    print("Mensaje enviado a Telegram:", response.text)
    response.close()

# Conexión WiFi
conectar_wifi()

# Bucle principal
while True:
    estado_sensor = leer_sensor()
    estado_pulsador = leer_pulsador()

    if estado_sensor != estado_anterior_sensor:
        print("Cambio en el estado del sensor:", estado_sensor)
        estado_anterior_sensor = estado_sensor
        mensaje = f"Nuevo estado del sensor: {estado_sensor}"
        enviar_mensaje_telegram(mensaje)

    if estado_pulsador != estado_anterior_pulsador:
        print("Cambio en el estado del pulsador:", estado_pulsador)
        estado_anterior_pulsador = estado_pulsador
        mensaje = f"Nuevo estado del pulsador: {estado_pulsador}"
        enviar_mensaje_telegram(mensaje)

    if estado_sensor == 0 or estado_pulsador == 1:
        # El sensor infrarrojo o el pulsador están activos, mueve el servo a -90 grados
        servo.duty_ns(1500000)  # 0 grados
        time.sleep(3)
    else:
        # El sensor infrarrojo y el pulsador están inactivos, mueve el servo a 0 grados
        servo.duty_ns(2500000)  # -90 grados

    # Pequeña pausa para evitar lecturas rápidas del sensor y el pulsador
    time.sleep(0.1)


































# Escribe tu código aquí :-)
