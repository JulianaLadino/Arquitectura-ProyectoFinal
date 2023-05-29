import machine
import time

# Configuración de pines GPIO
pin_sensor = machine.Pin(22, machine.Pin.IN)
pin_switch = machine.Pin(23, machine.Pin.IN)
pin_servo = machine.Pin(14)
servo = machine.PWM(pin_servo)

# Configuración de los límites del pulso del servo (ajusta según tu servo)
servo.freq(50)
servo.duty_ns(500000)  # 0 grados

# Funciones para leer el estado del sensor infrarrojo y el switch
def leer_sensor():
    return pin_sensor.value()

def leer_switch():
    return pin_switch.value()

# Bucle principal
while True:
    if leer_sensor() == 1 or leer_switch() == 1:
        # El sensor infrarrojo o el switch están activos, mueve el servo a 90 grados
        servo.duty_ns(1500000)  # 90 grados
        time.sleep(3)
    else:
        # El sensor infrarrojo y el switch están inactivos, mueve el servo a 0 grados
        servo.duty_ns(500000)  # 0 grados

    # Pequeña pausa para evitar lecturas rápidas del sensor y el switch
    time.sleep(0.1)

