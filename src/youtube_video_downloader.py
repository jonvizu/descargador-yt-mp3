import concurrent.futures
import yt_dlp
from pathlib import Path
import re
import logging
import shutil
from urllib.parse import urlparse



# --- Configuración Global / Constantes ---

# Carpeta donde se guardarán todas las descargas de video.

# Se creará automáticamente si no existe.
DOWNLOAD_DIR_VIDEO = "Downloads_Videos"
# Opciones detalladas para yt-dlp para la descarga de video con la mejor calidad.
YDL_OPTS_VIDEO = {
    'format': 'bestvideo+bestaudio/best',
    'outtmpl': f"{Path(DOWNLOAD_DIR_VIDEO) / '%(artist)s - %(title)s.%(ext)s'}",
    'merge_output_format': 'mp4',
    'writedescription': True,
    'nocheckcertificate': True,
    'no_warnings': True,
    'geo_bypass': True,        # Evita restricciones geográficas.
    'quiet': True,
    'progress_hooks': [],
}

# --- Manejo de errores
class DownloadError(Exception):
    """Excepción personalizada para errores de descarga."""
    pass

# --- Funciones Utilitarias ---


def is_valid_youtube_url(url: str) -> bool:
    """
    Verifica si la URL proporcionada es una URL válida de YouTube.

    Args:
        url (str): La URL de YouTube a verificar.

    Returns:
        bool: True si la URL es válida, False en caso contrario.
    """
    youtube_regex = r'^(https?://)?(www\.)?(youtube\.com|youtu\.be)/.+$'
    if not re.match(youtube_regex, url):

        return False

    parsed = urlparse(url)
    return bool(parsed.netloc and parsed.scheme)

def check_ffmpeg_installed() -> bool:
    """
    Verifica si FFmpeg está instalado en el sistema.

    Returns:
        bool: True si FFmpeg está instalado, False en caso contrario.
    """
    return shutil.which('ffmpeg') is not None

def ensure_download_directory_exists(directory_name: str) -> Path:
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
            logging.info(f"Directorio de descarga creado: {download_path}")
        except OSError as e:
            print(f"❌ Error al crear la carpeta '{download_path}': {e}")
            logging.error(f"Error al crear la carpeta '{download_path}': {e}")
            raise
    return download_path

def progress_hook(d):
    """
    Función de enganche para mostrar el progreso de la descarga.

    Args:
        d (dict): Diccionario que contiene información sobre el progreso de la descarga.
    """
    if d['status'] == 'downloading':
        percentage = d['_percent_str']
        speed = d['_speed_str']
        eta = d['_eta_str']
        print(f"   {percentage} descargado a {speed}, ETA: {eta}")
    elif d['status'] == 'finished':
        print("\n✅ Descarga finalizada")

def safe_download(ydl, url):
    """
    Función para descargar de forma segura un video.

    Args:
        ydl (yt_dlp.YoutubeDL): Objeto YoutubeDL.
        url (str): URL del video.
    """
    try:
        ydl.download([url])
    except yt_dlp.utils.DownloadError as e:
        print(f"❌ Error durante la descarga del video: {e}")
        logging.error(f"Error durante la descarga de {url}: {e}")
        raise DownloadError(f"Error al descargar {url}: {e}")
    except yt_dlp.utils.ExtractorError as e:
        print(f"❌ Error al extraer información del video: {e}")
        logging.error(f"Error al extraer información del video {url}: {e}")
        raise DownloadError(f"Error al extraer información del video {url}: {e}")
    except yt_dlp.utils.GeoRestrictedError as e:
        print(f"❌ Video no disponible en tu región: {e}")
        logging.error(f"Video no disponible en tu región {url}: {e}")
        raise DownloadError(f"Video no disponible en tu región {url}: {e}")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        logging.error(f"Error inesperado durante la descarga de {url}: {e}")
        raise DownloadError(f"Error inesperado durante la descarga de {url}: {e}")

def download_youtube_video(youtube_link: str, download_directory: Path):
    """
    Descarga un video de YouTube con la mejor calidad de video y audio disponible,
    y lo guarda en la carpeta especificada. FFmpeg es requerido para la fusión.

    Args:
        youtube_link (str): El enlace (URL) del video de YouTube a descargar.
        download_directory (Path): El objeto Path del directorio donde guardar la descarga.
    """

    if not is_valid_youtube_url(youtube_link):
        print("❌ URL de YouTube no válida. Asegúrate de usar un enlace correcto.")
        logging.warning(f"URL de YouTube no válida: {youtube_link}")
        return
    if not check_ffmpeg_installed():
        print("❌ FFmpeg no está instalado. Por favor, instala FFmpeg para continuar.")
        print("💡 Visita https://ffmpeg.org/download.html para instrucciones de instalación.")
        logging.error("FFmpeg no está instalado.")
        return

    print(f"\n🚀 Iniciando descarga de video de: {youtube_link}")
    logging.info(f"Iniciando descarga de video desde: {youtube_link}")
    try:
        current_ydl_opts = YDL_OPTS_VIDEO.copy()
        current_ydl_opts['outtmpl'] = f"{download_directory / '%(artist)s - %(title)s.%(ext)s'}"
        current_ydl_opts['progress_hooks'].append(progress_hook)  # type: ignore
        with yt_dlp.YoutubeDL(current_ydl_opts) as ydl:
            safe_download(ydl, youtube_link)
        print("✅ Descarga de video completada exitosamente!")
        logging.info(f"Descarga de video completada exitosamente: {youtube_link}")
    except Exception as e:
        print(f"❌ Error general en la descarga: {e}")