from pathlib import Path
from .utils import ensure_download_directory_exists, is_valid_youtube_url
from .downloader import download

# --- Configuración Específica para Audio ---

DOWNLOAD_DIR = "Downloads_Mp3"

YDL_OPTS_AUDIO = {
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
    'quiet': False,
    'verbose': True,
    'cookiefile': r'z:\projects\Descargar_Python\cookies.txt',
    'sleep_interval': 10,
    'sleep_subtitles': 10,
    'outtmpl': {
        'default': '%(playlist_index)s - %(artist,uploader)s - %(title)s.%(ext)s',
    },
}

# --- Función Principal ---

def main():
    """
    Función principal para la descarga de audio.
    """
    print("\n--- 🎧 Descargador de Audio MP3 de YouTube ---")
    
    download_folder_path = ensure_download_directory_exists(DOWNLOAD_DIR)
    if not download_folder_path:
        return

    use_cookies_answer = input("¿Usar cookies del navegador para contenido privado? (s/n): ").strip().lower()
    use_browser_cookies = use_cookies_answer == 's'

    while True:
        link = input("\n➡️ Ingresa el enlace del video/playlist de YouTube (o 'q' para salir): ").strip()
        
        if link.lower() == 'q':
            print("\n👋 ¡Hasta pronto!")
            break
        
        if not is_valid_youtube_url(link):
            print("❌ URL de YouTube no válida.")
            continue
            
        download(link, YDL_OPTS_AUDIO, download_folder_path, use_browser_cookies)

if __name__ == "__main__":
    main()