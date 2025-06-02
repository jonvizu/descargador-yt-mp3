import yt_dlp

def download_video(link):
    ydl_opts = {
        'format': 'bestaudio/best',  # Solo la mejor pista de audio.
        # <-- CAMBIO AQUÍ: Formato de nombre de archivo con artista y título.
        'outtmpl': '%(artist)s - %(title)s.%(ext)s',
        'writethumbnail': True,      # Descarga la miniatura del video.
        'postprocessors': [{
            'key': 'FFmpegExtractAudio', # Extrae el audio.
            'preferredcodec': 'mp3',    # Lo convierte a MP3.
            # <-- CAMBIO AQUÍ: Calidad de audio a '0' para la mejor posible.
            'preferredquality': '0',    # '0' significa la mejor calidad posible para MP3.
        }, {
            'key': 'EmbedThumbnail',     # Incrusta la miniatura descargada como carátula del álbum.
        }, {
            'key': 'FFmpegMetadata',     # Incrusta metadatos relevantes (título, artista, etc.).
        }],
        # Consideración: yt-dlp intenta inferir el 'artist' del uploader o de metadatos.
        # No todos los videos de YouTube tienen información clara de "artista" de canción.
        # Si %(artist)s no está disponible, yt-dlp usará el uploader o un valor por defecto.
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([link])
        print("¡Descarga de audio con metadatos y carátula completada exitosamente!")
    except Exception as e:
        print(f"Ocurrió un error: {e}")
        return

# Asegúrate de que las siguientes dos líneas estén al mismo nivel de indentación
# que la definición de la función 'def download_video(link):'
link = str(input("Ingresa el enlace del video de YouTube: ")).strip()
download_video(link)