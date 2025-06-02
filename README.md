# Descargador de Audio MP3 de YouTube

Este script de Python descarga el audio de vídeos de YouTube como archivos MP3 de alta calidad. Incluye la incrustación automática de metadatos (título, artista) y la carátula del álbum, ofreciendo una experiencia de audio completa y organizada.

## Características

- Descarga el audio en formato MP3.
- Obtiene la mejor calidad de audio disponible.
- Incrusta el título del video como título de la canción.
- Intenta incrustar el nombre del canal/uploader como artista.
- Incrusta la miniatura del video como carátula del álbum en el archivo MP3.
- Guarda los archivos en una carpeta dedicada `descargas_mp3`.

## Requisitos

- [Python 3.x](https://www.python.org/downloads/)
- [FFmpeg](https://ffmpeg.org/download.html) (esencial para la conversión de audio y la incrustación de metadatos/carátulas)

## Instalación

1.  **Clonar el repositorio (si usas Git) o descargar el proyecto:**
    '''bash
    git clone [https://github.com/tu_usuario/tu_proyecto_youtube_dl.git](https://github.com/tu_usuario/tu_proyecto_youtube_dl.git)
    cd tu_proyecto_youtube_dl
    '''
2.  **Crear y activar un entorno virtual:**
    '''bash
    python -m venv venv
    '''
    * En Windows:
        '''bash
        .\venv\Scripts\activate
        '''
    * En macOS/Linux:
        '''bash
        source venv/bin/activate
        '''
3.  **Instalar las dependencias:**
    '''bash
    pip install -r requirements.txt
    '''
4.  **Asegúrate de que FFmpeg esté instalado y en tu PATH del sistema.** (Consulta la documentación oficial de FFmpeg o tutoriales para tu sistema operativo si aún no lo tienes).

## Uso

1.  Asegúrate de que tu entorno virtual esté activado.
2.  Ejecuta el script principal:
    '''bash
    python src/main.py
    '''
3.  El script te pedirá que ingreses el enlace del video de YouTube. Pégalo y presiona Enter.
4.  El archivo MP3 resultante se guardará en la carpeta `descargas_mp3/`.

## Notas

- La información del "artista" se toma del uploader o del canal del video, y puede no coincidir con el artista musical real de la canción.
- La calidad de los metadatos y la carátula dependen de lo que esté disponible en YouTube.

## Contribución

¡Las contribuciones son bienvenidas! Si encuentras un error o tienes una mejora, por favor, abre un "issue" o envía un "pull request".

## Licencia

Este proyecto está bajo la Licencia MIT. (O la licencia que elijas)
