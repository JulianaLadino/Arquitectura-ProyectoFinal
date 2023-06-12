import machine
import time
import network
import urequests
import ujson
#import arequests
# port uasyncio

# Configuración de pines GPIO
pin_sensor = machine.Pin(27, machine.Pin.IN)
pin_pulsador = machine.Pin(25, machine.Pin.IN)
pin_servo = machine.Pin(12)
servo = machine.PWM(pin_servo)

# Configuración de los límites del pulso del servo (ajusta según tu servo)
servo.freq(50)
servo.duty_ns(2500000)  # -90 grados

# Variables para almacenar el estado del servo_motor
estado_servo=0

# Configuración de la conexión WiFi
ssid = "Dla Net"
password = ""

# Aquí debes proporcionar el token de acceso y el chat ID para enviar el mensaje a través de la API de Telegram
token = "6122260212:AAG5nHeI8pXvSmcVBIpmr70QzIUPNBeej10"
chat_id = "6082831038"
url = f"https://api.telegram.org/bot{token}"

# Opciones de respuestas
opc1 = {'keyboard': [[ {"text": "Si"}, {"text": "No"} ]]}
opc2 = {'keyboard': [[ {"text": "Abrir"}, {"text": "Cerrar"} ]]}

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

def enviar_mensaje_telegram(texto, respuestas):
    data = {'chat_id': chat_id, 'text': texto, 'reply_markup': respuestas}
    response = urequests.post(url + '/sendMessage', json=data)
#    print("Mensaje enviado a Telegram:", response.text)
    response.close()

def enviar_confirmacion_telegram(texto):
    response = urequests.get(url + '/sendMessage?chat_id=' + chat_id + '&text=' + texto +'&')
   # print("Mensaje enviado a Telegram:", response.text)
    response.close()

def obtener_respuesta_telegram():
    url = f"https://api.telegram.org/bot{token}/getUpdates?offset=-1"
    response = urequests.get(url)
    data = ujson.loads(response.text)
    messages = data["result"][0]["message"]["text"]
    return messages

def control_servo(mensaje,mov):
    enviar_confirmacion_telegram(mensaje)
    servo.duty_ns(mov)  # 0 grados

# Conexión WiFi
conectar_wifi()

ban=0
salir="No"

while True:
    if ban == 0 :

        mensaje = f"Activación remota de la puerta, ¿Desea continuar?"
        enviar_mensaje_telegram(mensaje, opc1)
        time.sleep(1)
        respuesta = obtener_respuesta_telegram()

        if respuesta == "Si":
            salir ="No"
            while salir =="No":

                mensaje = f"Seleccione la acción a realizar:"
                enviar_mensaje_telegram(mensaje, opc2)
                time.sleep(2)
                resp = obtener_respuesta_telegram()

                if resp == "Abrir" and estado_servo != 1500000:
                    mensaje = f"Puerta abierta remotamente"
                    estado_servo=1500000
                    control_servo(mensaje,estado_servo)
                    time.sleep(1)
                elif estado_servo == 1500000 and resp == "Abrir":
                    mensaje = f"La puerta se encuentra abierta"
                    enviar_confirmacion_telegram(mensaje)

                if resp == "Cerrar" and estado_servo != 2500000:
                    mensaje = f"¡Puerta cerrada remotamente!"
                    estado_servo=2500000
                    control_servo(mensaje,estado_servo)
                    time.sleep(1)
                elif estado_servo == 2500000 and resp == "Cerrar":
                    mensaje = f"La puerta se encuentra cerrada"
                    enviar_confirmacion_telegram(mensaje)

                time.sleep(2)
                salir2 = obtener_respuesta_telegram()

                if salir2 == "salir" or salir2 == "Salir":
                    salir="Si"

        if respuesta == "No" or salir == "Si":
            mensaje = f"Control remoto desactivado"
            enviar_confirmacion_telegram(mensaje)
            ban = 1

            # Bucle principal
            while ban ==1:

                print("leyendo Sensores")
                estado_sensor = leer_sensor()
                estado_pulsador = leer_pulsador()
                time.sleep(1)

               #abrir puerta
                if estado_sensor == 0 and estado_servo != 1500000:
                    mensaje = f"Puerta abierta, por detección de movimiento"
                    estado_servo=1500000
                    control_servo(mensaje,estado_servo)

                if estado_pulsador == 1 and estado_servo!=1500000:
                    mensaje = f"Puerta abierta, activación manual"
                    estado_servo=1500000
                    control_servo(mensaje,estado_servo)

                # Validar puerta abierta
                #if estado_servo == 1500000 and estado_sensor == 0 :
                 #   mensaje = f"La puerta ya ha sido abierta"
                  #  enviar_mensaje_telegram(mensaje)

                #if estado_servo == 1500000 and estado_pulsador == 1 :
                 #   mensaje = f"La puerta ya ha sido abierta"
                  #  enviar_mensaje_telegram(mensaje)

                if estado_servo == 1500000:
                    mensaje = f"¿Deseas cerrar la puerta?"
                    enviar_mensaje_telegram(mensaje,opc1)
                    time.sleep(2)
                    resp = obtener_respuesta_telegram()

                    if resp == "Si":
                        estado_servo=2500000
                        control_servo("¡Puerta cerrada!",estado_servo)

                time.sleep(1)
                salir = obtener_respuesta_telegram()

                if salir == "salir" or salir == "Salir":
                    ban=0
