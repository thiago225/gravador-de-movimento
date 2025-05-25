from pynput.mouse import Controller as MouseController, Button
from pynput.keyboard import Controller as KeyboardController, Key, Listener as KeyboardListener
import time
import json
import threading

# Variável de controle
reproduzindo = True

# Controladores
mouse = MouseController()
teclado = KeyboardController()

# Carrega os eventos
with open("macro.json", "r") as f:
    eventos = json.load(f)

# Função para escutar ESC
def escutador_esc():
    def on_press(tecla):
        global reproduzindo
        if tecla == Key.esc:
            print("ESC pressionado. Parando reprodução...")
            reproduzindo = False
            return False  # Para o listener
    with KeyboardListener(on_press=on_press) as listener:
        listener.join()

# Inicia o listener do ESC em outra thread
threading.Thread(target=escutador_esc, daemon=True).start()

# Loop de reprodução
print("Reproduzindo... Pressione ESC para parar.")
while reproduzindo:
    tempo_inicial = eventos[0]['tempo']
    inicio_reproducao = time.time()
    
    for evento in eventos:
        if not reproduzindo:
            break

        tempo_espera = evento['tempo'] - tempo_inicial
        agora = time.time()
        atraso = tempo_espera - (agora - inicio_reproducao)
        if atraso > 0:
            time.sleep(atraso)
            
        if evento['tipo'] == 'mouse':
            mouse.position = (evento['x'], evento['y'])
            if evento['pressionado']:
                mouse.press(Button.left)
            else:
                mouse.release(Button.left)

        elif evento['tipo'] == 'teclado':
            tecla = evento['tecla'].replace("'", "")
            try:
                if len(tecla) == 1:
                    teclado.press(tecla)
                    teclado.release(tecla)
                else:
                    tecla_obj = getattr(Key, tecla.replace('Key.', ''), None)
                    if tecla_obj:
                        teclado.press(tecla_obj)
                        teclado.release(tecla_obj)
            except Exception as e:
                print(f"Erro ao pressionar tecla {tecla}: {e}")

print("Reprodução finalizada.")
