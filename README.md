# Descargador de Audio MP3 de YouTube

Este script de Python descarga el audio de vídeos de YouTube como archivos MP3 de alta calidad. Incluye la incrustación automática de metadatos (título, artista) y la carátula del álbum, ofreciendo una experiencia de audio completa y organizada.

## Características

- Descarga el audio en formato MP3.
- Obtiene la mejor calidad de audio disponible.
- Incrusta el título del video como título de la canción.
- Intenta incrustar el nombre del canal/uploader como artista.
- Incrusta la miniatura del video como carátula del álbum en el archivo MP3.
- Guarda los archivos en una carpeta dedicada `Downloads_Mp3`.

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

# Problemas Comunes y Soluciones con yt-dlp

Este apartado documenta problemas frecuentes que pueden surgir al usar `yt-dlp` para descargas de YouTube, especialmente cuando se realizan múltiples operaciones o se requiere autenticación, y sus soluciones.

---

## 1. Error de Conexión: `Remote end closed connection without response` (o similar)

### Descripción del Problema

Este error (`http.client.RemoteDisconnected: Remote end closed connection without response`) indica que la conexión entre `yt-dlp` y el servidor de YouTube se cerró inesperadamente antes de que la descarga o la solicitud de información pudiera completarse.

Las causas más comunes incluyen:

* **Bloqueo o "Throttling" por IP de YouTube:** YouTube es muy activo en detectar y limitar la actividad de descarga intensa o repetitiva desde una misma dirección IP. Si se realizan muchas descargas en un corto período, YouTube puede cerrar las conexiones para esa IP.
* **Conexión a Internet inestable:** Fallos temporales en la red, cortes de internet o fluctuaciones pueden romper la conexión.
* **Firewall o Antivirus:** El software de seguridad puede interpretar la actividad de `yt-dlp` como sospechosa y bloquear la conexión.
* **`User-Agent` obsoleto:** Un `User-Agent` en las opciones de `yt-dlp` que es muy antiguo puede hacer que YouTube rechace la conexión, interpretando la solicitud como proveniente de un cliente no válido o desactualizado.
* **Contenido Restringido/Autenticación:** Aunque menos frecuente si las cookies funcionan, si el video es privado, de pago o tiene restricciones y la autenticación falla por alguna razón sutil, YouTube podría cortar la conexión.

### Solución Probada y Recomendada

La solución más efectiva y confirmada para el bloqueo por IP es **cambiar tu dirección IP pública**. Esto se puede lograr de varias maneras:

* **Usar una VPN (Red Privada Virtual):** Conectar tu dispositivo a una VPN te permite cambiar tu dirección IP visible para YouTube. Si estás usando una VPN y el problema persiste, intenta **cambiar a un servidor VPN diferente** para obtener una nueva IP.
* **Reiniciar tu Router/Módem:** En muchos casos, los proveedores de servicios de Internet (ISP) asignan IPs dinámicas. Reiniciar tu router puede forzar un cambio de tu dirección IP pública.
* **Usar un Proxy (con precaución):** Configurar un proxy puede enrutar tu tráfico a través de una IP diferente. Sin embargo, los proxies gratuitos suelen ser lentos e inestables.

Además, para mejorar la resiliencia de las descargas y evitar este tipo de errores de conexión, se recomienda la siguiente configuración en las opciones de `yt-dlp`:

* **`retries` y `fragment_retries`:** Aumenta el número de veces que `yt-dlp` intentará reconectar o reintentar la descarga de un fragmento si la conexión se pierde.
* **`timeout`:** Aumenta el tiempo máximo que `yt-dlp` esperará una respuesta del servidor.
* **`sleep_interval_requests` y `sleep_interval_fragments`:** Introduce pequeñas pausas entre las solicitudes y los fragmentos descargados, lo que puede ayudar a reducir la probabilidad de ser detectado y bloqueado por YouTube.
* **`user_agent`:** **Es fundamental usar un `User-Agent` actualizado y representativo de un navegador moderno.** Un `User-Agent` obsoleto es una causa común de rechazo de conexión por parte de los servidores.

## 2. Error de Carga/Descifrado de Cookies

### Descripción del Problema

Pueden surgir dos tipos principales de errores relacionados con las cookies del navegador:

* **`TypeError: _parse_browser_specification() takes from X to Y positional arguments but Z were given`**: Este error ocurre cuando la opción `cookiesfrombrowser` se configura con un formato de tupla que no coincide con lo que la versión específica de `yt-dlp` espera para un navegador dado. Por ejemplo, pasar `('chrome',)` o `('brave', 'Default')` podría ser incorrecto si la función interna espera un número diferente de argumentos.
* **`ERROR: Could not copy Chrome cookie database. See ... for more info`** o **`ERROR: Failed to decrypt with DPAPI. See ... for more info`**: Estos errores indican que `yt-dlp` no pudo acceder o descifrar la base de datos de cookies de tu navegador (Chrome o Brave). Esto es casi siempre porque el navegador está abierto y tiene el archivo de cookies bloqueado o porque el proceso de Python no tiene los permisos para descifrar el archivo (el descifrado por DPAPI está ligado al usuario y al proceso que lo cifró).

### Solución Probada y Recomendada

Existen dos enfoques principales para manejar las cookies, y la elección dependerá de si deseas mantener el navegador abierto o prefieres un método más robusto:

#### Opción A: Usar `cookiesfrombrowser` (requiere navegador cerrado)

Esta opción permite a `yt-dlp` intentar leer directamente las cookies del navegador.

1.  **Asegúrate de que el navegador esté completamente cerrado:** Antes de ejecutar el script, **cierra todas las instancias de Brave (o Chrome)** y verifica en el Administrador de Tareas (Windows) o Monitor de Actividad (macOS/Linux) que no queden procesos del navegador ejecutándose en segundo plano. Esto libera el bloqueo sobre la base de datos de cookies y permite a `yt-dlp` intentar accederlas y descifrarlas.
2.  **Ajusta el formato de `cookiesfrombrowser`:** Para evitar el `TypeError` inicial, la configuración de la tupla puede variar. Prueba con las siguientes opciones hasta encontrar la que funcione para tu navegador y versión de `yt-dlp`:
    * Para Chrome: `('chrome', 'Default')` o `('chrome',)`.
    * Para Brave: `('brave',)` o `'brave'` (como una cadena simple).

    *Ejemplo para Brave:*
    ```python
    'cookiesfrombrowser': 'brave', # O quizás ('brave',)
    ```

#### Opción B: Usar `cookiefile` (método más robusto y universal)

Esta es la solución más fiable si la Opción A sigue dando problemas o si necesitas mantener tu navegador abierto. Implica exportar las cookies a un archivo de texto y hacer que `yt-dlp` lo lea.

1.  **Instala una extensión de navegador:**
    * Para **Chrome** o **Brave** (o cualquier navegador basado en Chromium), busca e instala la extensión **"Get cookies.txt"** desde la Chrome Web Store.
    * Para **Firefox**, busca e instala la extensión **"Export Cookies"** o similar que genere un archivo en formato Netscape.
2.  **Inicia sesión en YouTube/YouTube Music:** Asegúrate de estar autenticado en la plataforma en tu navegador.
3.  **Exporta las cookies:** Haz clic en el icono de la extensión (generalmente en la barra de herramientas del navegador) y selecciona la opción para exportar las cookies. Esto descargará un archivo llamado `cookies.txt` (o similar) en tu carpeta de descargas.
4.  **Copia el archivo `cookies.txt` localmente:** Mueve el archivo `cookies.txt` descargado a la **misma carpeta donde se encuentra tu script de Python**. Esto es crucial para que `yt-dlp` pueda encontrarlo.
5.  **Modifica tu código Python:**
    * Comenta o elimina la línea `'cookiesfrombrowser': ...`.
    * Descomenta y asegúrate de que la opción `'cookiefile': 'cookies.txt'` esté presente y activa en tus `YDL_OPTS_MP3`.

    *Ejemplo de configuración en código:*
    ```python
    # ... (otras configuraciones)

    YDL_OPTS_MP3 = {
        # ... (tus opciones existentes)

        # --- Opciones de Autenticación (elije una) ---
        # 'cookiesfrombrowser': ('brave', 'Default'), # Opción A: Descomentar si usas este método
        'cookiefile': 'cookies.txt',               # Opción B: Descomentar si usas este método y tienes el archivo local

        'verbose': True, # Mantener en True para depuración, cambiar a False en producción.

        # ... (resto de opciones de conexión y User-Agent)
    }

    # ... (resto de tu script)
    ```

---

### Implementación en el Código (Ejemplo Completo y Unificado)

Asegúrate de que tus opciones de `yt-dlp` (`YDL_OPTS_MP3` en tu script) incluyan los siguientes parámetros:

```python
import yt_dlp
from pathlib import Path

# --- Configuración Global / Constantes ---
DOWNLOAD_DIR = "Downloads_Mp3"

YDL_OPTS_MP3 = {
    'format': 'bestaudio/best',
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
    'progress_hooks': [],
    'verbose': True, # Mantener en True para depuración, cambiar a False en producción.

    # --- Opciones de Autenticación (ELIGE SÓLO UNA) ---
    # Opción A: Leer cookies directamente del navegador (requiere que el navegador esté CERRADO)
    'cookiesfrombrowser': 'brave', # Para Brave. Prueba también ('brave',)
    # 'cookiesfrombrowser': ('chrome', 'Default'), # Para Chrome. Prueba también ('chrome',)

    # Opción B: Leer cookies desde un archivo (más robusto, si el navegador necesita estar abierto o hay problemas de descifrado)
    # 'cookiefile': 'cookies.txt', # Descomentar esta línea y comentar la anterior si usas este método.

    # --- Opciones Recomendadas para Estabilidad de Conexión ---
    'retries': 10,                 # Número de reintentos para conexiones fallidas
    'fragment_retries': 10,        # Número de reintentos para fragmentos de descarga fallidos
    'buffer_size': 1048576,        # Tamaño del búfer de lectura (1MB)
    'http_chunk_size': 1048576,    # Tamaño de los fragmentos HTTP para descargas
    'timeout': 600,                # Tiempo máximo de espera para la respuesta del servidor (en segundos, 10 minutos)
    'sleep_interval_requests': 1,  # Esperar 1 segundo entre solicitudes HTTP
    'sleep_interval_fragments': 0.5, # Esperar 0.5 segundos entre la descarga de fragmentos
    'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36', # ¡MUY IMPORTANTE! Usar un User-Agent actual.

    # ... (otras opciones si las tienes, como 'outtmpl' que se setea dinámicamente)
}

# --- Resto del código (funciones ensure_download_directory_exists, download_audio_mp3, main) ---
# ... (todo el código que ya tienes)




