from pynput import mouse, keyboard
import time
import json

eventos = []
gravando = True
tempo_inicio = time.time()

def gravar_mouse(x, y, button, pressed):
    if gravando:
        eventos.append({
            'tipo': 'mouse',
            'acao': 'click',
            'x': x,
            'y': y,
            'botao': str(button),
            'pressionado': pressed,
            'tempo': time.time()
        })

def gravar_scroll(x, y, dx, dy):
    if gravando:
        eventos.append({
            'tipo': 'mouse',
            'acao': 'scroll',
            'x': x,
            'y': y,
            'dx': dx,
            'dy': dy,
            'tempo': time.time()
        })

def gravar_teclado(tecla):
    global gravando
    tempo = time.time()
    if tecla == keyboard.Key.esc:
        print("Parando a gravação...")
        gravando = False
        # Parar o listener do teclado
        return False
    else:
        eventos.append({
            'tipo': 'teclado',
            'tecla': str(tecla),
            'tempo': tempo
        })

print("Gravando... Pressione ESC para parar.")

# Criar os listeners
mouse_listener = mouse.Listener(on_click=gravar_mouse, on_scroll=gravar_scroll)
teclado_listener = keyboard.Listener(on_press=gravar_teclado)

# Iniciar os listeners
mouse_listener.start()
teclado_listener.start()

# Espera até pressionar ESC
teclado_listener.join()
mouse_listener.stop()

# Salvar os eventos
with open("macro.json", "w") as f:
    json.dump(eventos, f, indent=4)

print("Gravação salva em macro.json")
