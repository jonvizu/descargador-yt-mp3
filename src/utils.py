from pathlib import Path
import shutil
import re

def ensure_download_directory_exists(directory_name: str) -> Path | None:
    """
    Asegura que el directorio de descargas exista. Si no existe, lo crea.
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

def is_valid_youtube_url(url: str) -> bool:
    """
    Verifica si la URL proporcionada es una URL válida de YouTube.
    """
    youtube_regex = r'^(https?://)?(www\.)?(youtube\.com|youtu\.be)/.+$'
    return bool(re.match(youtube_regex, url))

def is_youtube_music_url(url: str) -> bool:
    """Verifica si la URL es de YouTube Music."""
    patterns = [
        r'^(https?://)?(music\.youtube\.com/.*)',
        r'^(https?://)?(www\.music\.youtube\.com/.*)'
    ]
    return any(re.match(pattern, url) for pattern in patterns)

def check_ffmpeg_installed() -> bool:
    """
    Verifica si FFmpeg está instalado en el sistema.
    """
    return shutil.which('ffmpeg') is not None
