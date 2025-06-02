import yt_dlp

def download_video(link):
    ydl_opts = {
        'format': 'bestvideo + bestaudio/best', # best quality
        'outtmpl': '%(title)s.%(ext)s',
        'merge_output_format': 'mp4'
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([link])
        print("Download completed successfully!")
    except Exception as e:
        print(f"An error occurred: {e}")
        return

link = str(input("Enter the YouTube video link: ")).strip()
download_video(link)