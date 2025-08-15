import yt_dlp
from pathlib import Path
import argparse
from utils import ensure_download_directory_exists

# --- Configuración Global / Constantes ---

DOWNLOAD_DIR = "Downloads_Mp3"

# Opciones base para yt-dlp para la descarga de audio MP3.
YDL_OPTS_BASE = {
    'format': 'bestaudio/best',
    'writethumbnail': True,
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '0', # 192 is default, 0 is best
    }, {
        'key': 'EmbedThumbnail',
    }, {
        'key': 'FFmpegMetadata',
    }],
    'nocheckcertificate': True,
    'geo_bypass': True,
    'no_warnings': True,
    'ignoreerrors': True,
    'continue_dl': True,
    'quiet': False,
    'progress_hooks': [],
    'verbose': True,
    'cookiefile': 'z:\\projects\\Descargar_Python\\cookies.txt',
    'sleep_interval': 10,
    'sleep_subtitles': 10,
}

# --- Funciones del Programa ---

def download_audio(youtube_link: str, download_directory: Path, use_browser_cookies: bool):
    """
    Descarga el audio de un video o playlist de YouTube en formato MP3.
    """
    print(f"\n🚀 Iniciando descarga y procesamiento de audio de: {youtube_link}")

    try:
        current_ydl_opts = YDL_OPTS_BASE.copy()

        if use_browser_cookies:
            # Pide al usuario que elija un navegador
            browser = input("¿Qué navegador usar para las cookies? (chrome, firefox, edge, brave, etc.): ").strip().lower()
            if browser:
                current_ydl_opts['cookiesfrombrowser'] = (browser,)
                print(f"🍪 Usando cookies del navegador: {browser}")

        if "playlist" in youtube_link.lower():
            output_template = str(download_directory / '%(playlist_index)s - %(artist)s - %(title)s.%(ext)s')
        else:
            output_template = str(download_directory / '%(artist)s - %(title)s.%(ext)s')

        current_ydl_opts['outtmpl'] = output_template

        with yt_dlp.YoutubeDL(current_ydl_opts) as ydl:
            ydl.download([youtube_link])
        print("✅ Descarga de audio con metadatos y carátula completada exitosamente!")
    except yt_dlp.utils.DownloadError as e:
        print(f"❌ Error general durante la descarga: {e}")
        print("💡 Verifica que el enlace sea válido y que FFmpeg esté instalado. También verifica la autenticación si el contenido está restringido.")
    except Exception as e:
        print(f"❌ Ocurrió un error inesperado durante la descarga: {e}")
        print("💡 Asegúrate de que FFmpeg esté correctamente instalado y en tu PATH.")

def main():
    """
    Función principal del script que maneja la interacción con el usuario.
    """
    print("\n--- 🎧 Descargador Unificado de Audio MP3 de YouTube 🚀 ---")
    print("Este script te ayudará a obtener el audio de tus videos o playlists favoritos.")

    download_folder_path = ensure_download_directory_exists(DOWNLOAD_DIR)
    if download_folder_path is None:
        print("🚫 No se pudo inicializar el programa debido a un error en la carpeta de descargas.")
        return

    use_cookies_answer = input("¿Quieres intentar usar las cookies de tu navegador para acceder a contenido privado o playlists? (s/n): ").strip().lower()
    use_browser_cookies = use_cookies_answer == 's'

    while True:
        link = input(" \n➡️ Ingresa el enlace del video o playlist de YouTube (o 'q' para salir): ").strip()

        if link.lower() == 'q':
            print("👋 Saliendo del programa. ¡Hasta pronto!")
            break
        elif link:
            download_audio(link, download_folder_path, use_browser_cookies)
        else:
            print("⚠️ No se ingresó ningún enlace válido. Por favor, intenta de nuevo.")

if __name__ == "__main__":
    main()
