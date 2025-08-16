from pathlib import Path
from .utils import ensure_download_directory_exists, is_valid_youtube_url, check_ffmpeg_installed
from .downloader import download

# --- Configuración Específica para Video ---

DOWNLOAD_DIR_VIDEO = "Downloads_Videos"

YDL_OPTS_VIDEO = {
    'format': 'bestvideo+bestaudio/best',
    'merge_output_format': 'mp4',
    'writedescription': True,
    'nocheckcertificate': True,
    'no_warnings': True,
    'geo_bypass': True,
    'quiet': False,
    'verbose': True,
    'cookiefile': r'z:\projects\Descargar_Python\cookies.txt',
    'sleep_interval': 10,
    'sleep_subtitles': 10,
    'outtmpl': {
        'default': '%(artist)s - %(title)s.%(ext)s',
    },
}

# --- Función Principal ---

def main():
    """
    Función principal para la descarga de videos.
    """
    print("\n--- 🎬 Descargador de Videos de YouTube ---")
    
    if not check_ffmpeg_installed():
        print("❌ FFmpeg no está instalado. Por favor, instala FFmpeg para continuar.")
        print("💡 Visita https://ffmpeg.org/download.html para instrucciones de instalación.")
        return

    download_folder_path = ensure_download_directory_exists(DOWNLOAD_DIR_VIDEO)
    if not download_folder_path:
        return

    use_cookies_answer = input("¿Usar cookies del navegador para contenido privado? (s/n): ").strip().lower()
    use_browser_cookies = use_cookies_answer == 's'

    while True:
        link = input("\n➡️ Ingresa el enlace del video de YouTube (o 'q' para salir): ").strip()
        
        if link.lower() == 'q':
            print("\n👋 ¡Hasta pronto!")
            break
        
        if not is_valid_youtube_url(link):
            print("❌ URL de YouTube no válida.")
            continue
            
        download(link, YDL_OPTS_VIDEO, download_folder_path, use_browser_cookies)

if __name__ == "__main__":
    main()