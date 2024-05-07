import multiprocessing as mp
import flet as ft
from TikTokLive import TikTokLiveClient
from TikTokLive.events import ConnectEvent, CommentEvent
import threading
import gtts.lang
import pyttsx3
from gtts import gTTS
from pygame import mixer
import random
import os, tempfile, gtts, subprocess, gtts
import time
import asyncio

class TK:
    def __init__(self) -> None:
        self.client: TikTokLiveClient = None

    def on_connect(self, event: ConnectEvent):
        print(f'Conectado como: {event.unique_id}, (Room ID: {self.client.room_id})')

    def on_comment(self, event: CommentEvent):
        print(f"{event.user.nickname} -> {event.comment}")
        tts.hablar(event.comment, cts.voice_dropdown.value)
        cts.chat.controls.append(ft.Text(f"{event.user.nickname} -> {event.comment}"))
        ui.update()

    def connect_tiktok_live(self):
        '''
        Conecta a tiktok live
        '''
        if not self.client:
            self.client = TikTokLiveClient(unique_id=cts.unique_id_input.value)
            ui.save_storage(data={'key':'uniqueId', 'value':cts.unique_id_input.value})
            @self.client.on(ConnectEvent)
            async def on_connect_wrapper(event: ConnectEvent):
                self.on_connect(event)

            self.client.add_listener(CommentEvent, self.on_comment)

            try:
                self.client.run()
                print('Conectado a chat')
            except Exception as e:
                cts.botao_iniciar.visible = True
                cts.unique_id_input.visible = True
                cts.unique_id_input.value = None
                print('Error al conectar')
                ui._page.update()

    def connect_tiktok_live_thread(self):
        threading.Thread(target=self.connect_tiktok_live).start()

    def enviar_mensaje_tunel(mensaje: dict):
        if mensaje["tipo"] == "mensaje":
            # Añadir el mensaje al chat
            cts.chat.controls.append(
                ft.Text(
                    f"{mensaje['usuario']}: {mensaje['texto']}"
                )
            )
        else:
            cts.chat.controls.append(
                ft.Text(
                    f"{mensaje['usuario']} ha entrado al chat",
                    size=12,
                    italic=True,
                    color=ft.colors.ORANGE_500
                )
            )
        ui.update()

class TTS:
    def __init__(self):
        '''
        Clase para tener la utilidades de gTTS.
        '''
        self.data = None

    def get_available_voices(self):
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        engine.stop()

        #print("Available voices:")
        voice_names = []
        for voice in voices:
            voice_names.append(voice.name)

        #print(f" - Name: {voice.name}, ID: {voice.id}, Languages: {voice.languages}")
        return voice_names

    def hablar(self, mensaje, lang1):
        # Usar libreria gTTS
        volume = 1
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

class COMPONETS:
    def __init__(self):
        '''
        Clase para tener los componentes UI.
        '''
        self.userTemp = ''
        self.title = ft.Text("Available Text-to-Speech Voices")
        self.texto = ft.Text("TiktokLive")
        self.chat = ft.Column(
            scroll="auto",
            height=400,
            visible=False
        )
        self.option = [
            ft.dropdown.Option(
                key=lang,
                text=lang
            ) for lang in gtts.lang.tts_langs()
        ]
        self.voice_dropdown = ft.Dropdown(
            on_change=self.dropdown_changed,
            width=300,
            options=self.option
        )
        self.unique_id_input = ft.TextField(
            label="Escribe UniqueId" ,
            hint_text='coloca usuario',
            value=None
        )
        self.campo_mensaje = ft.TextField(
            label="Escribe un mensaje",
            on_submit=self.enviar_mensaje,
            visible=False
        )
        self.botao_enviar_mensaje = ft.ElevatedButton(
            "Enviar",
            on_click=self.enviar_mensaje,
            visible=False
        )
        self.popup = ft.AlertDialog(
            open=False,
            modal=True,
            title=ft.Text("Escribe UniqueId para conectar"),
            content=self.unique_id_input,
            actions=[ft.ElevatedButton("Entrar", on_click=self.entrar_popup)],
        )
        self.botao_iniciar = ft.ElevatedButton("Iniciar chat", on_click=self.entrar_chat)
        self.list_elements = [
            self.title,
            self.voice_dropdown,
            self.texto,
            self.botao_iniciar,
            self.unique_id_input,
            self.chat,
            self.campo_mensaje,
            self.botao_enviar_mensaje
        ]
        self.content = ft.Column(
            self.list_elements
        )
        self.window = ft.Container(
            content=self.content
        )

    def entrar_chat(self, evento):
        tk.connect_tiktok_live_thread()
        ui._page.add(self.chat)
        # ui._page.remove(self.botao_iniciar)
        self.botao_iniciar.visible = False
        # ui._page.remove(self.texto)
        self.texto.visible = False
        self.unique_id_input.visible = False
        ui._page.title = f'TTS - Tiktok - {self.unique_id_input.value}'
        self.userTemp = self.unique_id_input.value
        self.campo_mensaje.visible = True
        self.botao_enviar_mensaje.visible = True
        self.chat.visible = True
        ui._page.update()

    def entrar_popup(self, evento):
        ui._page.pubsub.send_all({"usuario": self.unique_id_input.value, "tipo": "entrada"})
        # Añadir el chat
        ui._page.add(self.chat)
        # Cerrar el popup
        self.popup.open = False
        # Quitar el botón de iniciar chat
        ui._page.remove(self.botao_iniciar)
        ui._page.remove(self.texto)
        # Crear el campo de mensaje del usuario
        # Crear el botón de enviar mensaje del usuario
        ui._page.add(ft.Row(
            [self.campo_mensaje, self.botao_enviar_mensaje]
        ))
        ui._page.update()

    def enviar_mensaje(self, evento):
        ui._page.pubsub.send_all(
            {"texto": self.userTemp,
            "usuario": self.unique_id_input.value,
            "tipo": "mensaje"}
        )
        # Limpiar el campo de mensaje
        self.chat.controls.append(ft.Text(f"{self.userTemp}: {self.campo_mensaje.value}"))
        self.campo_mensaje.value = ""
        ui._page.update()

    def dropdown_changed(self, e):
        self.texto.value = f"Dropdown cambiado a {self.voice_dropdown.value}"
        tts.hablar(self.voice_dropdown.value, self.voice_dropdown.value)
        e.page.update()

class UI:
    def __init__(self):
        '''
        Clase la cual se encarga de iniciar flet y organizar la ventana.
        '''
        self._page = None

    def __call__(self, flet_page: ft.Page):
        self._page = flet_page
        self._page.title = 'TTS - Tiktok'
        self._page.theme_mode = ft.ThemeMode.DARK
        self.initial()
        self._page.add(
            cts.window
        )

    def get_uniqueId_storage(self) -> str:
        '''
        Devuelve el uniqueId del almacenamiento del cliente.
        '''
        try:
            uniqueId = self._page.client_storage.get('uniqueId') or None
            return uniqueId
        except TimeoutError:
            uniqueId = None
            print("Error al acceder al almacenamiento del cliente")
            return uniqueId

    def save_storage(self, data: dict):
        '''
        Guarda datos en la session del cliente, recibe un diccionaro:
        ```
        data = {
            'key': 'Mi Clave',
            'value': 'Valor de la Clase'
        }
        ```
        '''
        self._page.client_storage.set(key=data['key'], value=data['value'])

    def initial(self):
        cts.unique_id_input.value = self.get_uniqueId_storage()

    def update(self):
        self._page.update()

if __name__ == '__main__':
    tk = TK()
    tts = TTS()
    cts = COMPONETS()
    ui = UI()
    ft.app(target=ui, assets_dir="static")