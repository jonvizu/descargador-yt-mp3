
import yt_dlp
from pathlib import Path
import logging

# --- Configuración de Logging ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- Excepción Personalizada ---
class DownloadError(Exception):
    """Excepción personalizada para errores de descarga."""
    pass

# --- Funciones de Hook ---
def progress_hook(d):
    """Muestra el progreso de la descarga."""
    if d['status'] == 'downloading':
        percentage = d['_percent_str']
        speed = d['_speed_str']
        eta = d['_eta_str']
        print(f"   \r{percentage} descargado a {speed}, ETA: {eta}", end='')
    elif d['status'] == 'finished':
        print("\n✅ Descarga finalizada")

# --- Lógica de Descarga Principal ---
def download(url: str, ydl_opts: dict, download_directory: Path, use_browser_cookies: bool = False):
    """
    Función genérica para descargar contenido de YouTube usando yt-dlp.
    """
    if not url:
        print("⚠️ No se proporcionó una URL.")
        return

    print(f"\n🚀 Iniciando descarga desde: {url}")
    logging.info(f"Iniciando descarga desde: {url}")

    current_ydl_opts = ydl_opts.copy()
    current_ydl_opts['outtmpl'] = str(download_directory / current_ydl_opts['outtmpl']['default'])
    current_ydl_opts['progress_hooks'] = [progress_hook]

    if use_browser_cookies:
        print("\nIMPORTANTE: Para que la extracción de cookies funcione, \nasegúrate de que el navegador que elijas esté completamente cerrado.")
        while True:
            browser = input("¿Qué navegador usar para las cookies? (chrome, firefox, edge, brave, etc.) o presiona Enter para omitir: ").strip().lower()
            if not browser:
                print("⏩ Omitiendo el uso de cookies del navegador.")
                break
            try:
                print(f"🍪 Intentando usar cookies del navegador: {browser}...")
                current_ydl_opts['cookiesfrombrowser'] = (browser,)
                # Prueba rápida para forzar la carga de cookies
                with yt_dlp.YoutubeDL(current_ydl_opts) as ydl:
                    ydl.extract_info(url, download=False, process=False)
                print("✅ Cookies cargadas exitosamente.")
                break
            except Exception as e:
                if 'Permission denied' in str(e) or 'Could not copy' in str(e):
                    print(f"❌ Error de permisos al acceder a las cookies de {browser}.")
                    print("💡 Por favor, CIERRA COMPLETAMENTE el navegador y vuelve a intentarlo.")
                else:
                    print(f"❌ No se pudieron cargar las cookies de {browser}. Error: {e}")
                
                retry = input("¿Quieres intentar con otro navegador o volver a intentarlo? (s/n): ").strip().lower()
                if retry != 's':
                    print("⏩ Continuando sin cookies del navegador.")
                    current_ydl_opts.pop('cookiesfrombrowser', None)
                    break
    
    try:
        with yt_dlp.YoutubeDL(current_ydl_opts) as ydl:
            ydl.download([url])
        print("\n✅ ¡Descarga completada exitosamente!")
        logging.info(f"Descarga completada exitosamente: {url}")
    except yt_dlp.utils.DownloadError as e:
        print(f"\n❌ Error durante la descarga: {e}")
        logging.error(f"Error durante la descarga de {url}: {e}")
    except Exception as e:
        print(f"\n❌ Ocurrió un error inesperado: {e}")
        logging.error(f"Error inesperado durante la descarga de {url}: {e}")
