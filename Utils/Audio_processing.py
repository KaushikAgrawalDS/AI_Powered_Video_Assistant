import yt_dlp
import os
from pydub import AudioSegment
import subprocess

DOWNLOAD_DIR = 'downloades'
os.makedirs(DOWNLOAD_DIR,exist_ok=True)

def download_youtube_audio(url:str) -> str:
    output_path = os.path.join(DOWNLOAD_DIR, "%(title)s.%(ext)s")
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": output_path,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "wav",
                "preferredquality": "192",
            }
        ],
        "quiet": True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info).replace(".webm", ".wav").replace(".m4a", ".wav")
    return filename

def convert_to_wav(input_path: str) -> str:
    output_path = os.path.splitext(input_path)[0] + "_converted.wav"
    subprocess.run([
        "ffmpeg", "-y", "-i", input_path,
        "-vn", "-ar", "16000", "-ac", "1",
        output_path
    ], check=True)
    return output_path

def chunk_audio(wav_path: str,chunk_minute: int =10) -> list:
    audio = AudioSegment.from_wav(wav_path)
    chunk_ms = chunk_minute*60*1000
    chunks =[]
    for i,start in enumerate(range(0,len(audio),chunk_ms)):
        chunk = audio[start: start + chunk_ms]
        chunk_path = f"{wav_path}_chunk_{i}.wav"
        chunk.export(chunk_path,format = "wav")
        chunks.append(chunk_path)
    return chunks

def process_input(source: str) -> str:
    if source.startswith('http://') or source.startswith('https://'):
        print("Detected Youtube URL. Downloading audio...")
        wav_path = download_youtube_audio(source)
    else:
        print("Detected local file. Converting to Wav...")
        wav_path = convert_to_wav(source)
    print("Chunking audio ...")
    chunks = chunk_audio(wav_path)
    print(f"Audio ready - {len(chunks)}chunks created.")
    return chunks