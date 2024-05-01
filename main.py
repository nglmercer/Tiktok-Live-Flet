import multiprocessing as mp
import flet as ft
from TikTokLive import TikTokLiveClient
from TikTokLive.events import ConnectEvent, CommentEvent
import threading
import pyttsx3
from gtts import gTTS
from pygame import mixer
import random
import os, tempfile, gtts, subprocess, gtts
import time
# Create the TikTokLive client instance
client: TikTokLiveClient = None

def get_available_voices():
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.stop()

    #print("Available voices:")
    voice_names = []
    for voice in voices:
        voice_names.append(voice.name)
        
    #print(f" - Name: {voice.name}, ID: {voice.id}, Languages: {voice.languages}")
    return voice_names

def hablar(mensaje,lang1):
    # Usar libreria gTTS
    volume = 0.7
    tts = gTTS(mensaje, lang="es" if lang1 is None else lang1, slow=False)
    ran = random.randint(0,9999)
    filename = 'Temp' + format(ran) + '.mp3'
    tts.save(filename)
    mixer.init()
    mixer.music.load(filename)
    mixer.music.set_volume(volume)
    mixer.music.play()

    while mixer.music.get_busy():
        time.sleep(0.3)

    mixer.quit()
    os.remove(filename)

# Imprimir los idiomas soportados
print("Idiomas soportados por gTTS:")
LANGUAGES = [language for language in gtts.lang.tts_langs()]
print(LANGUAGES)
def main(page):
    title = ft.Text("Available Text-to-Speech Voices")
    uniqueId = page.client_storage.get("uniqueId")
    # Fetch voice data from the function
    voice_names = get_available_voices()
    def dropdown_changed(e):
        texto.value = f"Dropdown changed to {voice_dropdown.value}"
        hablar(voice_dropdown.value,voice_dropdown.value)
        page.update()
    
    # Create dropdown options from the voice names
    voice_dropdown = ft.Dropdown(on_change=dropdown_changed,width=300)  # Initialize dropdown
    ft.dropdown.Option(key=uniqueId,text=uniqueId)
    for lang in LANGUAGES:
        option = ft.dropdown.Option(key=lang, text=lang)
        voice_dropdown.options.append(option)  # Add option to dropdown
    # Create the dropdown control
    
    # Add elements to the page
    page.add(title)
    page.add(voice_dropdown)
    texto = ft.Text("TiktokLive")
    chat = ft.Column(scroll="auto", height=400)  # Se agrega scroll al chat
    unique_id_input = ft.TextField(label="Escribe UniqueId" ,value=uniqueId)

    def on_connect(event: ConnectEvent):
        print(f"Connected to @{event.unique_id} (Room ID: {client.room_id})")
    
    async def on_comment(event: CommentEvent):
        print(f"{event.user.nickname} -> {event.comment}")
        hablar(event.comment,voice_dropdown.value)
        chat.controls.append(ft.Text(f"{event.user.nickname} -> {event.comment}"))
        page.update()
    def connect_tiktok_live():
        global client
        if not client:
            client = TikTokLiveClient(unique_id=unique_id_input.value)
            page.client_storage.set("uniqueId", unique_id_input.value)
            @client.on(ConnectEvent)
            async def on_connect_wrapper(event: ConnectEvent):
                on_connect(event)

            client.add_listener(CommentEvent, on_comment)

            client.run()

    def connect_tiktok_live_thread():
        threading.Thread(target=connect_tiktok_live).start()
    def enviar_mensaje_tunel(mensaje):
        tipo = mensaje["tipo"]
        if tipo == "mensaje":
            texto_mensaje = mensaje["texto"]
            usuario_mensaje = mensaje["usuario"]
            # Añadir el mensaje al chat
            chat.controls.append(ft.Text(f"{usuario_mensaje}: {texto_mensaje}"))
        else:
            usuario_mensaje = mensaje["usuario"]
            chat.controls.append(ft.Text(f"{usuario_mensaje} ha entrado al chat", 
                                          size=12, italic=True, color=ft.colors.ORANGE_500))
        page.update()

    page.pubsub.subscribe(enviar_mensaje_tunel)
    
    def enviar_mensaje(evento):
        page.pubsub.send_all({"texto": campo_mensaje.value, "usuario": unique_id_input.value,
                                "tipo": "mensaje"})
        # Limpiar el campo de mensaje
        campo_mensaje.value = ""
        page.update()

    campo_mensaje = ft.TextField(label="Escribe un mensaje", on_submit=enviar_mensaje)
    botao_enviar_mensaje = ft.ElevatedButton("Enviar", on_click=enviar_mensaje)

    def entrar_popup(evento):
        page.pubsub.send_all({"usuario": unique_id_input.value, "tipo": "entrada"})
        # Añadir el chat
        page.add(chat)
        # Cerrar el popup
        popup.open = False
        # Quitar el botón de iniciar chat
        page.remove(botao_iniciar)
        page.remove(texto)
        # Crear el campo de mensaje del usuario
        # Crear el botón de enviar mensaje del usuario
        page.add(ft.Row(
            [campo_mensaje, botao_enviar_mensaje]
        ))
        page.update()

    popup = ft.AlertDialog(
        open=False, 
        modal=True,
        title=ft.Text("Escribe UniqueId para conectar"),
        content=unique_id_input,
        actions=[ft.ElevatedButton("Entrar", on_click=entrar_popup)],
    )

    def entrar_chat(evento):
        connect_tiktok_live_thread()
        page.add(chat)
        page.remove(botao_iniciar)
        page.remove(texto)
        page.add(ft.Row([campo_mensaje, botao_enviar_mensaje]))
        page.update()

    botao_iniciar = ft.ElevatedButton("Iniciar chat", on_click=entrar_chat)

    page.add(texto)
    page.add(botao_iniciar)
    page.add(unique_id_input)

if __name__ == '__main__':
    mp.set_start_method('spawn')
    app_process = mp.Process(target=ft.app, kwargs={'target': main, 'view': ft.WEB_BROWSER, 'port': 8000})
    app_process.start()
    app_process.join()