import sys
from pathlib import Path

# Add the src directory to the Python path to allow imports from other scripts
sys.path.append(str(Path(__file__).parent))

import youtube_audio_downloader
import youtube_mp3_downloader
import youtube_video_downloader

def main_menu():
    """
    Displays the main menu and handles user input.
    """
    while True:
        print("\n--- Menu Principal de Descargas ---")
        print("1. Descargar Audio de YouTube (Video o Playlist)")
        print("2. Descargar Audio de YouTube Music (Playlist)")
        print("3. Descargar Video de YouTube")
        print("4. Salir")

        choice = input("Elige una opción (1-4): ").strip()

        if choice == '1':
            youtube_audio_downloader.main()
        elif choice == '2':
            youtube_mp3_downloader.main()
        elif choice == '3':
            youtube_video_downloader.main()
        elif choice == '4':
            print("¡Hasta pronto!")
            break
        else:
            print("Opción no válida. Por favor, elige una opción del 1 al 4.")

if __name__ == "__main__":
    main_menu()