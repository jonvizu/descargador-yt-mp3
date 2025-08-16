from pathlib import Path
from .utils import ensure_download_directory_exists, is_youtube_music_url
from .downloader import download

# --- Configuración Específica para YouTube Music ---

DOWNLOAD_DIR = "Downloads_Mp3"

YDL_OPTS_MP3 = {
    'format': 'bestaudio[ext=m4a]/bestaudio/best',
    'writethumbnail': True,
    'postprocessors': [
        {
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320',
        }, 
        {
            'key': 'EmbedThumbnail',
        },
        {
            'key': 'FFmpegMetadata',
        }
    ],
    'extract_flat': False,
    'ignore_errors': True,
    'continue_dl': True,
    'no_warnings': True,
    'quiet': False,
    'verbose': True,
    'cookiefile': r'z:\projects\Descargar_Python\cookies.txt',
    'sleep_interval': 10,
    'sleep_subtitles': 10,
    'extractor_args': {
        'youtubeimusic': {
            'player_client': ['ANDROID_MUSIC'],
        }
    },
    'outtmpl': {
        'default': '%(playlist_index)s - %(title)s.%(ext)s',
    },
}

# --- Función Principal ---

def main():
    """
    Función principal para la descarga de música de YouTube Music.
    """
    print("\n--- 🎵 Descargador de Música de YouTube Music ---")
    
    download_folder_path = ensure_download_directory_exists(DOWNLOAD_DIR)
    if not download_folder_path:
        return

    use_cookies_answer = input("¿Usar cookies del navegador para contenido privado? (s/n): ").strip().lower()
    use_browser_cookies = use_cookies_answer == 's'

    while True:
        link = input("\n➡️ Ingresa el enlace de la playlist de YouTube Music (o 'q' para salir): ").strip()
        
        if link.lower() == 'q':
            print("\n👋 ¡Hasta pronto!")
            break
        
        if not is_youtube_music_url(link):
            print("❌ El enlace debe ser de YouTube Music (music.youtube.com)")
            continue
            
        download(link, YDL_OPTS_MP3, download_folder_path, use_browser_cookies)

if __name__ == "__main__":
    main()