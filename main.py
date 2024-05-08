import multiprocessing as mp
import flet as ft
from flet import Audio, IconButton, icons
from TikTokLive import TikTokLiveClient
from TikTokLive.events import *
import threading
import gtts.lang
import pyttsx3
from gtts import gTTS
from pygame import mixer
import random
import os, tempfile, gtts, subprocess, gtts
import time
import asyncio
import queue
import sys
import json
import base64
from collections import defaultdict

# session_token = "eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2R0NNIn0..qru4XbaJvJZH_Dn_.rXX5fMZpoOTSumZfNdnWaF27e6mUwL2l3ZuDKQDeF6_sPz5EPk11-dARMYKK-4DAAHV_lqJmsI-lMDmwJ_vaCJLGmxRvkr0DEj8ThO_VwW2gl3IlCHrx--27_Tq34OjysKYszwuWrclcaff8ThKOTClff0W9Fk_ysP9VNCOzCCpV5-06rxwQLjH6S0GOAYUN4lnLQPMSGpgkAgXRRY1-nKL4e1uwyEkD-Wb91bdWS40tb_xr38lDzsRmAgjpVitS_9cq-UMhHkwqmH20UjDrbEYYb7w4vslvVnsPUs2jj65nYWFMmA6KtEfVp8K1N-sbnp-uoeaneJAHhmB7V4pa6vDdc3NJ_TuBAG7MPQryx16l5Zrkn_BYMpMaUNwn82a8KLNz_6932PVQCXfmFTbanu_4k4qJWlTry0zl1Ho_UWCaUnZS90YR-dKOdGSxMc8SI-p03nYeV_OyOf0JFczHABev0x92ixDzjf5tRKFcq0bjzXn8hRgs3ExcJBVvOrZjWOyrAW4ixrDzAY5A-uAJu8_sIWxbfOehmCr36mBkI9WImmByye4AEbs7X-stq6DaXdhZSD59MK3ZximK9u9B9wPNJgVhD6YHb-7I9u2Lgk8G6omlXFbe6paSrWIAb9X844FoEmnNR46NQxKYUMnUiNO5Sok7oPkhELvsCNp3a78yJHoRblLPNmLmVzOuDaySmAn-ro_Pjq2ztkMHzvMjsJ-hTIGIMfAC9OX2Uwmcl3d0NrPgHwKRZ3LEri5mkzLaVtouhVDZdYdjSNRy_8XHNkDDfFqBDz5kvqx8gB1Rp4P8UV4PJLBQ5XUCO5-khIiuRjasH7jvtnOHb8UvC2s1eQQ8rZ9w41Lnh2M94OhZAGf1cyi6TfCkvOcyffdwo_6oImvSnxVyUbUjxSV9dIlb5sExRDm4armmsKifdn_2M5JQ6mR7cQ4Ft7zqmwcbriWxuLEaI0BSR8pNZ3Xy2UIKAk4yUeC2h1uhT-WrOrP6YOzZ4WWkTgZLfDLxC3dOuB3vkxrLUGt9hOjsekbnEmqYmYCG9vs97yxJF5tECi0vkLWIjE4Y9hli4_3t32voxJc2TSw4v_KoENGGem_RN5qOxthycJd5uWEi6xTnygMZozusAywg7HKKWHsrwL45madWlMchlqwpXfp7w-SyAAitNAcAuKXwgBeFW0X_UX2ffXENf8FC6RoOtrFu8INO1hs9AWYAD3m3c0CDkuS-XYFb-94d8aBhZsLGHWBlVCGfVFD5aUSeBzhunHKUb858hnPx4zl9bi_DVp1priQegUMNG_6jou2is0G-zPGlXrJUYbTm1mLZDM_dfGRMaqU_hw50v4AJ5uDYK2z99qqQpf_uWISHv5agZy6rv6x4X8W_n9JCWAsImCVMB38AMivlddCs2CZ0mWWR-B1795ZTRq1FSi9IKAg-36AOr8wQ57-FpK2C3wJ8mFekpr-dgW2PMBf5fM7sjYspwApTL8Qw02nw0Jk5ailUW-AIZnzwDO4oic5iginyYePWL1FwHMhA0fcDcHb6gr1rRJCRCdlNgl3f0W4x43A_blGs28o9vRmin0wPBNuJtBQ_CND9QY7NfoIXf7-K3lfOFYaQBy5rey2JhGlbnUBZQgFac8N-rZsutzgWnR7JE-zrjavQmugWTZgPnLgyv8-FaVkiMN8jvRWJlLHvOWONiD-E0rR_1b1zpTsuoRi5Pbe3ub7Nsp_pN-x-uUMCzo1OsZ3nw0sMkq5ws1eEYzeSth_y6TE_tQDJjl7IyGCZ--PhkgoUX9n3U5VTizom8Uff_B3Axdi8sJRts9TDbanyCb0S2Uao5j_yjgIFfUtzzCSpZKby_OzMa_-anksiVqtazy5bkfKIubYK9kHWm-XgYS8-6Cu--jyYK9ktREASy3-oqmAQGFUet8RPQ_hMTm96IysXujMLmcfj1pdqY-FAv2phxT-11s02TYGek2IIuMiup6gwcvcWneVeKnuLIFePwq6bvvrJkTHQpGRp3jD2iDpHKg9vimMQ6Cq0qPXHYVdCfx6Q8zsl6-GQ9zNk5t42NTn1MjCscqlxkj1D0RtGLtgJM2aa-erRA4KEQt5e691-aSB-KUzefFvNDjrectIsjLQ2mqy5T1KJKdfKmooWHjFosDlcBS82VxCb64Z7zNtcePC3PHH1CISm9LHfCtSEV-el2DVqSUjL5-CtTYOQ4DzmMKHtusI2_MOSfLqcNdbpypvuNCOCaBJYVan_ZNXrPrj94hx_4AXLvPsciDxgmLmxX0vkwcRl4p2FLNzqf50kl8tZNgiwq1wb5Oc3p9oTn1AU5bVlLLJGCpctiZFvHU7fp3x2U96lqWf3VFoFYQza8VbSMw8E2vWzXvVTpGk0BsVzYHO4eM0IpciTxUxP6c78Tz4hspU5sbVd18yqYEbS3TU6jy-SVLQz4hkZRBZYXUwUwkJEipOtRavUI9NAZM-9wU-Buwqov1Eu4QCTzdwV_Ou6AuzkN8HCHyc7K209v8fHc-Df1UreZFgG6d1NN8WLM_1kRjjNHDA8FrysgoQzpCKkd07lJVFR6pVwM-XIIRDIV1oLt2tgTBq_2lz1n2tTfJcr78uh-ZGtUghbbnTBjNe4D5w1kBTLXpKEzmr484B9Gymvj5C7I5fIA7NphfZsNGKapHriMR5KLEUxxN00hWWRShNB2dGldm5Ie2V-BEiKTy-a2gv7LL3WXKzWDzEpxUdXW-sA1-rTs7vB2f1VgGo5uZkE-hIL7RrFIDT0Noc7kZY8p-FNuZ6iS8fYCfrzN5fZ9zDvEIun98GsNw3C31A6cvfDWPAx.tX2qBjTDzNIgYbB1e-s7NQ"
# conversation_id = None # "5937518c-2486-47de-a304-2e39ea774172" 


# with SyncChatGPT(session_token=session_token) as chatgpt:
#     prompt = input("Enter your prompt: ")

#     if conversation_id:
#         conversation = chatgpt.get_conversation(conversation_id)
#     else:
#         conversation = chatgpt.create_new_conversation()

#     for message in conversation.chat(prompt):
#         print(message["content"], flush=True, end="")

# async def main():
ImageTest = "https://seranking.com/es/blog/wp-content/uploads/sites/13/2021/09/que-es-una-url.png"
#     async with AsyncChatGPT(session_token=session_token) as chatgpt:
#         prompt = input("Enter your prompt: ")

#         if conversation_id:
#             conversation = chatgpt.get_conversation(conversation_id)
#         else:
#             conversation = chatgpt.create_new_conversation()

#         async for message in conversation.chat(prompt):
#             print(message["content"], flush=True, end="")
class TK:
    def __init__(self) -> None:
        self.client: TikTokLiveClient = None
        self.user_points = {}  # Diccionario para almacenar los puntos de cada usuario

    def on_connect(self, event: ConnectEvent):
        print(f'Conectado como: {event.unique_id}, (Room ID: {self.client.room_id}) {self.client.web.fetch_gift_list}')

    def on_comment(self, event: CommentEvent):
        user_id = event.user.unique_id 
        # Verificar la longitud del comentario y actualizar puntos
        comment_length = len(event.comment)
        if comment_length < 3 or comment_length > 40:
            self.decrement_user_points(user_id)
        elif self.user_points.get(user_id, 0) > 0: #comment_length >= 3 and comment_length <= 20 and self.user_points.get(user_id, 0) > 0:
            # Si el usuario tiene menos de 0 puntos, imprimir un mensaje
            tts.hablar(event.comment, cts.voice_dropdown.value)
        elif comment_length >= 3 and comment_length <= 40:
            self.increment_user_points(user_id) 
        else:
            if self.user_points.get(user_id, 0) < 0:
                print(f"@{user_id} no tiene puntos")

        print(f"{event.user.nickname} -> {event.comment}")
        # if (event.comment_quality_scores):
        #     print(event.comment_quality_scores)
        data = event.user.avatar_thumb.url_list
        json_str = json.dumps(data)
        cts.chat.controls.append(
            ft.Row(
                controls=[
                    (ft.Image(src=f"{event.user.avatar_thumb.url_list[0]}",height=50,width=50)),
                    ft.Text(f"{event.user.nickname} -> {event.comment}"),
                    # (ft.Image(src=f"{event.user.avatar_thumb.url_list[0]}",height=50,width=50)),
                ]
            )
        )
        # cts.chat.controls.append(ft.Image(f'{event.user.avatar_thumb}'),ft.Text(f"{event.user.nickname} -> {event.comment}"))
        ui.update()

    def on_gift(self, event: GiftEvent):
        try: 
            user_id = event.user.unique_id
            self.increment_user_points(user_id)
        # If it's type 1 and the streak is over
            if event.gift.streakable and not event.streaking:
                print(f"{event.user.unique_id} envio {event.repeat_count}x \"{event.gift.name}\"")
                cts.chat.controls.append(
                    ft.Row(
                        controls=[
                            (ft.Image(src=f"{event.user.avatar_thumb.url_list[0]}",height=50,width=50)),
                            ft.Text(f"{event.user.unique_id} envio {event.repeat_count}x \"{event.gift.name}\""),
                            (ft.Image(src=f"{event.gift.icon.url_list[0]}",height=50,width=50)),
                            # (ft.Image(src=f"{event.gift.image.url_list[0]}",height=50,width=50)),
                        ]
                    )
                )       
            elif not event.gift.streakable: 
                print(f"{event.user.unique_id} envio \"{event.gift.name}\"")
                cts.chat.controls.append(
                    ft.Row(
                        controls=[
                            (ft.Image(src=f"{event.user.avatar_thumb.url_list[0]}",height=50,width=50)),
                            ft.Text(f"{event.user.unique_id} envio \"{event.gift.name}\""),
                            (ft.Image(src=f"{event.gift.icon.url_list[0]}",height=50,width=50)),
                            # (ft.Image(src=f"{event.gift.image.url_list[0]}",height=50,width=50)),
                        ]
                    )
                )
                print(f'gift ICON------------- {event.gift.icon.url_list[0]}')
        except Exception as e:
            print("fallo al obtener datos GIFT",e)
            
    def on_like(self, event: LikeEvent):
        user_id = event.user.unique_id
        self.increment_user_points(user_id)
        cts.chat.controls.append(
            ft.Row(
                controls=[
                    (ft.Image(src=f"{event.user.avatar_thumb.url_list[0]}",height=50,width=50)),
                    ft.Text(f"{event.user.unique_id} -> le dió like al live ❤️"),
                    # (ft.Image(src=f"{event.user.avatar_thumb.url_list[0]}",height=50,width=50)),
                ]
            )
        )
        # json_like = json.dumps(event.to_json)
        # print(f'{event.to_json}')
        print(f'❤️  @{event.user.unique_id} le dió like al live (Cantidad total de like al live)')

    def on_share(self, event: ShareEvent):
        user_id = event.user.unique_id
        self.increment_user_points(user_id)
        cts.chat.controls.append(
            ft.Row(
                controls=[
                    (ft.Image(src=f"{event.user.avatar_thumb.url_list[0]}",height=50,width=50)),
                    ft.Text(f"📣  @{event.user.unique_id} compartió el live"),
                    # (ft.Image(src=f"{event.user.avatar_thumb.url_list[0]}",height=50,width=50)),
                ]
            )
        )
        print(f"📣  @{event.user.unique_id} compartió el live")
    def on_follow(self, event: FollowEvent):
        user_id = event.user.unique_id
        self.increment_user_points(user_id)
        try:
            # Incrementar puntos del usuario
            cts.chat.controls.append(
                ft.Row(
                    controls=[
                        (ft.Image(src=f"{event.user.avatar_thumb.url_list[0]}",height=50,width=50)),
                        ft.Text(f"🥑  @{event.user.unique_id} acaba de dar follow"),
                        # (ft.Image(src=f"{event.user.avatar_thumb.url_list[0]}",height=50,width=50)),
                    ]
                )
            )
            print(f"🥑  @{event.user.unique_id} acaba de dar follow")
        except Exception as e:
            print("fallo al obtener datos FOLLOW",e)
    def increment_user_points(self, user_id):
        if user_id in self.user_points:
            self.user_points[user_id] += 1
            print("Puntos del usuario: ",user_id, self.user_points[user_id])
        else:
            self.user_points[user_id] = 1
            print("Puntos del usuario: ",user_id, self.user_points[user_id])
    def decrement_user_points(self, user_id):
        if user_id in self.user_points:
            self.user_points[user_id] -= 1
        else:
            # Si el usuario no está en el diccionario, iniciar con -1 punto
            self.user_points[user_id] = -1

    def get_top_users(self, n=10):
        sorted_users = sorted(self.user_points.items(), key=lambda x: x[1], reverse=True)[:n]
        return sorted_users           
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
            self.client.add_listener(GiftEvent, self.on_gift)
            self.client.add_listener(LikeEvent, self.on_like)
            self.client.add_listener(ShareEvent, self.on_share)
            self.client.add_listener(FollowEvent, self.on_follow)

            try:
                self.client.run()
                print('Conectado a chat')
            except Exception as e:
                cts.botao_iniciar.visible = True
                cts.unique_id_input.visible = True
                cts.unique_id_input.value = None
                print('Error al conectar',e)
                ui._page.update()

    def connect_tiktok_live_thread(self):
        threading.Thread(target=self.connect_tiktok_live).start()
    def aiCredentials():
        session_token = "__Secure-next-auth.session-token here"
        conversation_id = None # conversation ID here
        return session_token
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

# def handle_chat(data, msg):
#     global preguntas

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
        volume = 0
        tts = gTTS(mensaje, lang="es" if lang1 is None else lang1, slow=False)
        ran = random.randint(0,9999)
        filename = 'Temp' + format(ran) + '.mp3'
        tts.save(filename)
        mixer.init()
        mixer.music.load(filename)
        mixer.music.set_volume(volume)
        cts.audio_player.src = f"{filename}"  # Replace with actual path
        mixer.music.play()
        while mixer.music.get_busy():
            time.sleep(0.3)
        cts.audio_player.play()
        ui._page.update()
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
        self.audio_player = ft.Audio(src = "", autoplay= True,
        volume=0.1,        
        balance=0,
        # on_loaded=lambda _: print("Loaded"),
        # on_duration_changed=lambda e: print("Duration changed:", e.data),
        # on_position_changed=lambda e: print("Position changed:", e.data),
        # on_state_changed=lambda e: print("State changed:", e.data),
        # on_seek_complete=lambda _: print("Seek complete"),
        ) 
        self.play_button = IconButton(icon=icons.PLAY_ARROW, on_click=self.play_audio)
        self.pause_button = IconButton(icon=icons.PAUSE, on_click=self.pause_audio)
        
        # Add audio controls to the list of elements
        self.list_elements.extend([
            self.audio_player,
            ft.Row([self.play_button, self.pause_button])
        ])
    def play_audio(self, e):
 # Replace with actual path
        self.audio_player.play()
        ui._page.update()

    def pause_audio(self, e):
        self.audio_player.pause()
        ui._page.update()
    def entrar_chat(self, event):
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

    def entrar_popup(self, event):
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

    def enviar_mensaje(self, event):
        ui._page.pubsub.send_all(
            {"texto": self.userTemp,
            "usuario": self.unique_id_input.value,
            "tipo": "mensaje"}
        )
        # Limpiar el campo de mensaje
        self.chat.controls.append(
            ft.Row(
                controls=[
                    ft.Text(f"{self.userTemp}: {self.campo_mensaje.value}"),
                    #  (ft.Image(src=f"{event.user.avatar_thumb.url_list[0]}",height=50,width=50)),
                ]
            )
        )
        self.campo_mensaje.value = ""
        # print('{src=ImageTest}')
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
    
