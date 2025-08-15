import yt_dlp
from pathlib import Path

# --- Configuración Global / Constantes ---

# Nombre de la carpeta donde se guardarán todas las descargas MP3.
# Se creará automáticamente si no existe.
DOWNLOAD_DIR = "Downloads_Mp3"

# Opciones detalladas para yt-dlp para la descarga de audio MP3.
# NOTA: 'outtmpl' se definirá dinámicamente en la función download_audio_mp3
# para asegurar que la ruta de la carpeta se maneje correctamente.
YDL_OPTS_MP3 = {
    'format': 'bestaudio/best',
    # 'outtmpl' se establecerá en la función de descarga
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
    'progress_hooks': [], # Se puede añadir el hook personalizado aquí si es necesario
}

# --- Funciones del Programa ---

def ensure_download_directory_exists(directory_name: str) -> Path | None:
    """
    Asegura que el directorio de descargas exista. Si no existe, lo crea.

    Args:
        directory_name (str): El nombre de la carpeta a verificar/crear.

    Returns:
        Path | None: El objeto Path del directorio si se creó o ya existía,
                     o None si hubo un error al crearlo.
    """
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
    """
    Descarga el audio de un video o playlist de YouTube en formato MP3 con la mejor calidad,
    e incrusta metadatos y la carátula.

    Requiere que la herramienta FFmpeg esté instalada en el sistema.

    Args:
        youtube_link (str): El enlace (URL) del video o playlist de YouTube a descargar.
        download_directory (Path): El objeto Path del directorio donde guardar la descarga.
    """
    print(f"\n🚀 Iniciando descarga y procesamiento de audio de: {youtube_link}")

    try:
        current_ydl_opts = YDL_OPTS_MP3.copy()
        
        # --- CORRECCIÓN CLAVE AQUÍ ---
        # Construimos la plantilla de salida para yt-dlp.
        # Aseguramos que la ruta base del directorio esté al principio,
        # seguida por la plantilla de nombre de archivo que yt-dlp procesará.
        # Es crucial que yt-dlp reciba una cadena con los placeholders,
        # no un objeto Path que ya ha resuelto la ruta.
        if "playlist" in youtube_link.lower(): # He añadido .lower() por si la URL de playlist está en mayúsculas
            # Para playlists, incluimos el índice de la playlist.
            output_template = str(download_directory / '%(playlist_index)s - %(artist)s - %(title)s.%(ext)s')
        else:
            # Para videos individuales, sin el índice de la playlist.
            output_template = str(download_directory / '%(artist)s - %(title)s.%(ext)s')
        
        current_ydl_opts['outtmpl'] = output_template

        # Opcional: Si quieres un progress hook personalizado, asegúrate de que esté configurado.
        # Por ejemplo, puedes definir 'my_hook' aquí o importarlo si está en otro archivo.
        # from your_module import my_hook
        # current_ydl_opts['progress_hooks'] = [my_hook]


        with yt_dlp.YoutubeDL(current_ydl_opts) as ydl:
            ydl.download([youtube_link])
        print("✅ Descarga de audio con metadatos y carátula completada exitosamente!")
    except yt_dlp.utils.DownloadError as e:
        print(f"❌ Error general durante la descarga: {e}")
        print("💡 Verifica que el enlace sea válido y que FFmpeg esté instalado.")
    except Exception as e:
        print(f"❌ Ocurrió un error inesperado durante la descarga: {e}")
        print("💡 Asegúrate de que FFmpeg esté correctamente instalado y en tu PATH.")

def main():
    """
    Función principal del script que maneja la interacción con el usuario
    y el flujo de descarga.
    """
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