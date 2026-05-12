from mfrc522 import SimpleMFRC522
import RPi.GPIO as GPIO
import time
from datetime import datetime
import csv

# ================= GPIO =================
LED_VERDE = 17
LED_VERMELHO = 22
BUZZER = 3

GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_VERDE, GPIO.OUT)
GPIO.setup(LED_VERMELHO, GPIO.OUT)
GPIO.setup(BUZZER, GPIO.OUT)

# ================= RFID =================
reader = SimpleMFRC522()

# ================= USUÁRIOS =================
usuarios = {
    552048006075: {"nome": "Carlos", "autorizado": True},
    288338938175: {"nome": "João", "autorizado": True},
    763370409838: {"nome": "Julia", "autorizado": False},
}

# ================= CONTROLE =================
presenca = {}
tentativas_nao_autorizadas = {}
invasoes = 0

# ================= FUNÇÕES =================
def buzzer_verde():
    GPIO.output(BUZZER, GPIO.HIGH)
    time.sleep(1)
    GPIO.output(BUZZER, GPIO.LOW)

def buzzer_vermelho():
    for _ in range(3):
        GPIO.output(BUZZER, GPIO.HIGH)
        time.sleep(0.2)
        GPIO.output(BUZZER, GPIO.LOW)
        time.sleep(0.2)

def led_verde():
    GPIO.output(LED_VERDE, GPIO.HIGH)
    buzzer_verde()
    time.sleep(5)
    GPIO.output(LED_VERDE, GPIO.LOW)

def led_vermelho():
    GPIO.output(LED_VERMELHO, GPIO.HIGH)
    buzzer_vermelho()
    time.sleep(5)
    GPIO.output(LED_VERMELHO, GPIO.LOW)

def invasao_alerta():
    for _ in range(10):
        GPIO.output(LED_VERMELHO, GPIO.HIGH)
        GPIO.output(BUZZER, GPIO.HIGH)
        time.sleep(0.2)
        GPIO.output(LED_VERMELHO, GPIO.LOW)
        GPIO.output(BUZZER, GPIO.LOW)
        time.sleep(0.2)

# ================= LOOP =================
try:
    print("Sistema iniciado...")

    while True:
        id, text = reader.read()
        agora = datetime.now()

        print("\nTag:", id)

        if id in usuarios:
            user = usuarios[id]
            nome = user["nome"]

            if user["autorizado"]:

                # ENTRADA
                if nome not in presenca or presenca[nome]["saida"] is not None:
                    print(f"Bem-vindo, {nome}")
                    presenca[nome] = {"entrada": agora, "saida": None}

                # SAÍDA
                else:
                    print(f"Saída registrada, {nome}")
                    presenca[nome]["saida"] = agora

                led_verde()

            else:
                print(f"Você não tem acesso a este projeto, {nome}")
                tentativas_nao_autorizadas[nome] = tentativas_nao_autorizadas.get(nome, 0) + 1
                led_vermelho()

        else:
            print("Identificação não encontrada!")
            invasoes += 1
            invasao_alerta()

        time.sleep(2)

# ================= FINAL =================
except KeyboardInterrupt:
    print("\nEncerrando sistema...\n")

    print("===== RELATÓRIO =====\n")

    with open("relatorio.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Nome", "Entrada", "Saída", "Tempo (segundos)"])

        for nome, dados in presenca.items():
            entrada = dados["entrada"]
            saida = dados["saida"]

            entrada_str = entrada.strftime("%H:%M:%S")

            if saida:
                saida_str = saida.strftime("%H:%M:%S")
                tempo = (saida - entrada).total_seconds()
            else:
                saida_str = "Ainda na empresa"
                tempo = 0

            print(f"{nome}: entrou {entrada_str} saiu {saida_str} tempo {tempo:.2f}s")

            writer.writerow([
                nome,
                entrada_str,
                saida_str,
                round(tempo, 2)
            ])

    print("\nTentativas de não autorizados:")
    for nome, qtd in tentativas_nao_autorizadas.items():
        print(f"{nome}: {qtd} tentativas")

    print(f"\nTotal de tentativas de invasão: {invasoes}")

    GPIO.cleanup()