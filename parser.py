import yt_dlp
import time

links = [
    "https://www.youtube.com/watch?v=huggqeMowXk",
    "https://www.youtube.com/watch?v=VJNsC8x083M",
]

timestamps = [
    [("0:30", "3:20")],
    [("0:50", "3:10")],
]

def parse_time_string(time_str):
    """Парсинг строки времени в секунды"""
    minutes, seconds = map(int, time_str.split(':'))
    return minutes * 60 + seconds

def extract_video_id(url):
    """Извлечение видео ID из URL"""
    if "v=" in url:
        return url.split("v=")[1]
    elif "youtu.be/" in url:
        return url.split("youtu.be/")[1]
    else:
        raise ValueError("Не удалось извлечь видео ID из ссылки.")

def download_and_trim_video(url, start_time, end_time, output_file):
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': output_file,
        'postprocessors': [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp4',
        }],
        'postprocessor_args': [
            '-ss', start_time,
            '-to', end_time,
            '-threads', '2',  
        ],
        'ffmpeg_location': 'Z:/Google downloads 2.0/ffmpeg-master-latest-win64-gpl/bin/ffmpeg.exe',
        'ffmpeg-location': 'Z:/Google downloads 2.0/ffmpeg-master-latest-win64-gpl/bin/ffmpeg.exe'
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

def process_videos_sequentially(links, timestamps):
    for idx, (link, times) in enumerate(zip(links, timestamps)):
        video_id = extract_video_id(link)
        for t_idx, (start, end) in enumerate(times):
            start_time = f"{parse_time_string(start) // 3600:02}:{(parse_time_string(start) % 3600) // 60:02}:{parse_time_string(start) % 60:02}"
            end_time = f"{parse_time_string(end) // 3600:02}:{(parse_time_string(end) % 3600) // 60:02}:{parse_time_string(end) % 60:02}"

            output_file = f"{video_id}_clip_{t_idx + 1}.mp4"
            
            download_and_trim_video(link, start_time, end_time, output_file)
            
            time.sleep(10)

process_videos_sequentially(links, timestamps)
