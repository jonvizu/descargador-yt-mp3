import yt_dlp
from pathlib import Path

# --- Configuración Global / Constantes ---

DOWNLOAD_DIR = "Downloads_Mp3"

# Opciones detalladas para yt-dlp para la descarga de audio MP3.
YDL_OPTS_MP3 = {
    'format': 'bestaudio/best',
    'writethumbnail': True,
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '0',
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
    'quiet': True,
    'progress_hooks': [],
    # --- NUEVAS OPCIONES DE AUTENTICACIÓN ---
    # Asegúrate de haber iniciado sesión en YouTube en este navegador.
    # Elige el navegador que uses comúnmente. Algunos ejemplos:
    # 'cookiesfrombrowser': 'chrome'
    # 'cookiesfrombrowser': 'firefox'
    # 'cookiesfrombrowser': 'edge'
    # 'cookiesfrombrowser': 'brave'
    # 'cookiesfrombrowser': ('chrome', None, '/path/to/cookies.txt') # Si necesitas especificar la ruta del perfil
    'cookiesfrombrowser': ('chrome',), #'cookiesfrombrowser': 'chrome', # Por ejemplo, si usas Google Chrome
    # 'username': 'tu_usuario_youtube', # Menos recomendado por seguridad
    # 'password': 'tu_contraseña_youtube', # Menos recomendado por seguridad
    'verbose': True,
    'cookiefile': 'cookies.txt',
}

# --- Funciones del Programa (el resto del código es el mismo que el anterior) ---

def ensure_download_directory_exists(directory_name: str) -> Path | None:
    download_path = Path(directory_name)
    if not download_path.exists():
        try:
            download_path.mkdir(parents=True, exist_ok=True)
            print(f"📁 Carpeta de descargas creada: '{download_path}'")
        except OSError as e:
            print(f"❌ Error al crear la carpeta '{download_path}': {e}")
            return None
    return download_path

def download_audio_mp3(youtube_link: str, download_directory: Path):
    print(f"\n🚀 Iniciando descarga y procesamiento de audio de: {youtube_link}")

    try:
        current_ydl_opts = YDL_OPTS_MP3.copy()

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
    print("\n--- 🎧 Descargador Profesional de Audio MP3 de YouTube 🚀 ---")
    print("Este script te ayudará a obtener el audio de tus videos o playlists favoritos.")

    download_folder_path = ensure_download_directory_exists(DOWNLOAD_DIR)
    if download_folder_path is None:
        print("🚫 No se pudo inicializar el programa debido a un error en la carpeta de descargas.")
        return

    while True:
        link = input(" \n➡️ Ingresa el enlace del video o playlist de YouTube (o 'q' para salir): ").strip()

        if link.lower() == 'q':
            print("👋 Saliendo del programa. ¡Hasta pronto!")
            break
        elif link:
            download_audio_mp3(link, download_folder_path)
        else:
            print("⚠️ No se ingresó ningún enlace válido. Por favor, intenta de nuevo.")

if __name__ == "__main__":
    main()