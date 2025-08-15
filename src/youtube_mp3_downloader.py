import yt_dlp
from pathlib import Path
import re
from utils import is_youtube_music_url, ensure_download_directory_exists

# --- Configuración Global / Constantes ---
DOWNLOAD_DIR = "Downloads_Mp3"

# Opciones optimizadas para YouTube Music
YDL_OPTS_MP3 = {
    'format': 'bestaudio[ext=m4a]/bestaudio/best',  # Prioriza formato de audio
    'postprocessors': [
        {
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320',  # Mejor calidad de audio
        }
    ],
    'writethumbnail': True,
    'postprocessors': [
        {
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320',
        }, {
            'key': 'EmbedThumbnail',
        }, {
            'key': 'FFmpegMetadata',
        }
    ],
    'extract_flat': False,  # Para manejar playlists
    'ignore_errors': True,
    'continue_dl': True,
    'no_warnings': True,
    'quiet': False,  # Cambiado a False para ver el progreso
    'verbose': True,
    'cookiefile': 'z:\projects\Descargar_Python\cookies.txt',
    'sleep_interval': 10,
    'sleep_subtitles': 10,
    'extractor_args': {
        'youtubeimusic': {
            'player_client': ['ANDROID_MUSIC'],
        }
    }
}

def download_audio_mp3(youtube_link: str, download_directory: Path, use_browser_cookies: bool):
    """Descarga audio de YouTube Music."""
    print(f"\n🎵 Iniciando descarga de playlist de YouTube Music: {youtube_link}")

    try:
        current_ydl_opts = YDL_OPTS_MP3.copy()

        if use_browser_cookies:
            # Pide al usuario que elija un navegador
            browser = input("¿Qué navegador usar para las cookies? (chrome, firefox, edge, brave, etc.): ").strip().lower()
            if browser:
                current_ydl_opts['cookiesfrombrowser'] = (browser,)
                print(f"🍪 Usando cookies del navegador: {browser}")

        # Formato específico para playlists de YouTube Music
        current_ydl_opts['outtmpl'] = str(download_directory / '%(playlist_index)s - %(title)s.%(ext)s')
        
        with yt_dlp.YoutubeDL(current_ydl_opts) as ydl:
            # Primero extraemos información de la playlist
            info = ydl.extract_info(youtube_link, download=False)
            if info:
                print(f"\n📑 Playlist: {info.get('title', 'Desconocido')}")
                print(f"🎵 Canciones encontradas: {info.get('playlist_count', 'Desconocido')}")
                
                # Descarga real
                ydl.download([youtube_link])
                
        print("\n✅ Descarga de playlist completada exitosamente!")
        
    except yt_dlp.utils.DownloadError as e:
        print(f"\n❌ Error durante la descarga: {e}")
        print("\n💡 Sugerencias:")
        print("1. Verifica que la playlist sea pública o que hayas iniciado sesión")
        print("2. Asegúrate de tener el archivo cookies.txt actualizado")
        print("3. Verifica tu conexión a internet")
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")

def main():
    """Función principal del programa."""
    print("\n=== 🎵 Descargador de Música de YouTube Music ===")
    
    download_folder_path = ensure_download_directory_exists(DOWNLOAD_DIR)
    if not download_folder_path:
        return

    use_cookies_answer = input("¿Quieres intentar usar las cookies de tu navegador para acceder a contenido privado o playlists? (s/n): ").strip().lower()
    use_browser_cookies = use_cookies_answer == 's'

    while True:
        link = input("\n➡️ Ingresa el enlace de la playlist de YouTube Music (o 'q' para salir): ").strip()
        
        if link.lower() == 'q':
            print("\n👋 ¡Hasta pronto!")
            break
        
        if not link:
            print("\n⚠️ Por favor, ingresa un enlace válido")
            continue
            
        if not is_youtube_music_url(link):
            print("\n❌ El enlace debe ser de YouTube Music (music.youtube.com)")
            continue
            
        download_audio_mp3(link, download_folder_path, use_browser_cookies)

if __name__ == "__main__":
    main()