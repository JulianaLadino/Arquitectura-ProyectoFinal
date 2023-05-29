import machine
import time

# Definir los pines utilizados para el motor y el sensor
sensor_pin = machine.Pin(3, machine.Pin.IN)
motor_pin = machine.PWM(machine.Pin(8), freq=50)
siche = machine.pin8()
# Función para girar el motor 90 grados
def girar_motor():
    # Gira el motor en una dirección durante un segundo
    motor_pin.duty(45)
    time.sleep(1)

    # Detiene el motor durante medio segundo
    motor_pin.duty(0)
    time.sleep(0.5)

    # Gira el motor en la dirección opuesta durante un segundo
    motor_pin.duty(135)
    time.sleep(1)

    # Detiene el motor durante medio segundo
    motor_pin.duty(0)
    time.sleep(0.5)

    # Vuelve a la posición inicial
    motor_pin.duty(90)
    time.sleep(1)

# Configuración inicial del motor
motor_pin.duty(90)

# Bucle principal del programa
while True:
    # Verificar si el sensor está activo
    if sensor_pin.value() == 1:
        # Llamar a la función para girar el motor 90 grados
        girar_motor()

    # Esperar un breve período antes de verificar el sensor de nuevo
    time.sleep(0.1)

