from mfrc522 import SimpleMFRC522
import RPi.GPIO as GPIO
import requests
import time

FLASK_URL = 'http://localhost:5000/rfid'  # ← IP DO SEU PC

LED_VERDE    = 17
LED_VERMELHO = 22
BUZZER       = 3

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()
GPIO.setup(LED_VERDE,    GPIO.OUT)
GPIO.setup(LED_VERMELHO, GPIO.OUT)
GPIO.setup(BUZZER,       GPIO.OUT)

reader = SimpleMFRC522()

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

def sinal_verde():
    GPIO.output(LED_VERDE, GPIO.HIGH)
    buzzer_verde()
    time.sleep(2)
    GPIO.output(LED_VERDE, GPIO.LOW)

def sinal_vermelho():
    GPIO.output(LED_VERMELHO, GPIO.HIGH)
    buzzer_vermelho()
    time.sleep(2)
    GPIO.output(LED_VERMELHO, GPIO.LOW)

def sinal_invasao():
    for _ in range(10):
        GPIO.output(LED_VERMELHO, GPIO.HIGH)
        GPIO.output(BUZZER,       GPIO.HIGH)
        time.sleep(0.15)
        GPIO.output(LED_VERMELHO, GPIO.LOW)
        GPIO.output(BUZZER,       GPIO.LOW)
        time.sleep(0.15)

def enviar_tag(tag_id):
    try:
        response = requests.post(
            FLASK_URL,
            json={'rfid_tag': str(tag_id)},
            timeout=5
        )
        return response.json(), response.status_code
    except requests.exceptions.ConnectionError:
        print('[ERRO] Nao conseguiu conectar no Flask. Verifique o IP.')
        return None, None
    except requests.exceptions.Timeout:
        print('[ERRO] Timeout — servidor demorou demais.')
        return None, None
    except Exception as e:
        print(f'[ERRO] Falha inesperada: {e}')
        return None, None

try:
    print('Sistema iniciado. Aproxime a tag...')
    while True:
        tag_id, _ = reader.read()
        print(f'\nTag lida: {tag_id}')

        dados, status = enviar_tag(tag_id)

        if dados is None:
            sinal_vermelho()
            time.sleep(2)
            continue

        status_retorno = dados.get('status', '')
        mensagem       = dados.get('mensagem', '')
        print(f'Resposta: {status_retorno} — {mensagem}')

        if status_retorno in ('permitido', 'saida'):
            sinal_verde()
        elif status_retorno == 'negado':
            sinal_vermelho()
        elif status_retorno == 'invasao':
            sinal_invasao()
        else:
            sinal_vermelho()

        time.sleep(2)

except KeyboardInterrupt:
    print('\nSistema encerrado.')
finally:
    GPIO.cleanup()