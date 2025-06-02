import yt_dlp
import os # Necesario para manejar rutas de archivos y crear directorios

# --- Configuración Global / Constantes ---
# Nombre de la carpeta donde se guardarán todas las descargas MP3.
# Se creará automáticamente si no existe.
DOWNLOAD_DIR = "Downloads_Mp3"

# Opciones detalladas para yt-dlp para la descarga de audio MP3.
# Estas opciones configuran el formato, la calidad, los metadatos y la carátula.
YDL_OPTS_MP3 = {
    'format': 'bestaudio/best',  # Descarga solo la mejor pista de audio disponible.
    # Define el formato del nombre del archivo de salida.
    # %(artist)s se refiere al uploader o al nombre del canal,
    # %(title)s es el título del video, y %(ext)s será la extensión final (mp3).
    # os.path.join asegura compatibilidad de rutas entre sistemas operativos.
    'outtmpl': os.path.join(DOWNLOAD_DIR, '%(artist)s - %(title)s.%(ext)s'),
    'writethumbnail': True,      # Habilita la descarga de la miniatura del video.
    'postprocessors': [{
        'key': 'FFmpegExtractAudio', # Postprocesador clave para extraer el audio.
        'preferredcodec': 'mp3',    # Especifica el códec de audio preferido como MP3.
        'preferredquality': '0',    # '0' indica la mejor calidad posible para el MP3 (bitrate).
    }, {
        'key': 'EmbedThumbnail',     # Postprocesador para incrustar la miniatura descargada como carátula del álbum en el archivo MP3.
    }, {
        'key': 'FFmpegMetadata',     # Postprocesador para incrustar metadatos (título, artista, etc.) del video en las etiquetas ID3 del archivo MP3.
    }],
    # Nota: No se requiere 'merge_output_format' ya que solo se descarga audio.
}

# --- Funciones del Programa ---

def download_audio_mp3(youtube_link: str):
    """
    Descarga el audio de un video de YouTube en formato MP3 con la mejor calidad,
    e incrusta metadatos (título, artista/uploader) y la carátula del video.

    Requiere que la herramienta FFmpeg esté instalada en el sistema
    y sea accesible a través de la variable de entorno PATH para que
    los postprocesadores funcionen correctamente.

    Args:
        youtube_link (str): El enlace (URL) del video de YouTube a descargar.
    """
    print(f"\n🚀 Iniciando descarga y procesamiento de audio de: {youtube_link}")

    # Crea la carpeta de descargas si no existe.
    # 'exist_ok=True' evita un error si la carpeta ya existe.
    if not os.path.exists(DOWNLOAD_DIR):
        try:
            os.makedirs(DOWNLOAD_DIR, exist_ok=True)
            print(f"📁 Carpeta de descargas creada: '{DOWNLOAD_DIR}'")
        except OSError as e:
            print(f"❌ Error al crear la carpeta '{DOWNLOAD_DIR}': {e}")
            return # Terminar la función si no se puede crear la carpeta

    try:
        # Crea una instancia de YoutubeDL con las opciones definidas.
        with yt_dlp.YoutubeDL(YDL_OPTS_MP3) as ydl:
            ydl.download([youtube_link]) # Inicia la descarga del enlace.
        print("✅ Descarga de audio con metadatos y carátula completada exitosamente!")
    except Exception as e:
        # Captura cualquier excepción que ocurra durante el proceso.
        # En un proyecto más grande, se usaría un sistema de logging.
        print(f"❌ Ocurrió un error inesperado durante la descarga: {e}")
        print("💡 Asegúrate de que FFmpeg esté correctamente instalado y en tu PATH.")

# --- Punto de Entrada Principal del Script ---

if __name__ == "__main__":
    # Este bloque se ejecuta solo cuando el script se corre directamente.
    # No se ejecuta si el script se importa como un módulo en otro archivo.
    print("\n--- 🎧 Descargador Profesional de Audio MP3 de YouTube 🚀 ---")
    print("Este script te ayudará a obtener el audio de tus videos favoritos.")

    while True: # Bucle para permitir múltiples descargas
        link = str(input(" \n➡️ Ingresa el enlace del video de YouTube (o 'q' para salir): ")).strip()

        if link.lower() == 'q':
            print("👋 Saliendo del programa. ¡Hasta pronto!")
            break
        elif link: # Procesa el enlace si no está vacío
            download_audio_mp3(link)
        else:
            print("⚠️ No se ingresó ningún enlace válido. Por favor, intenta de nuevo.")