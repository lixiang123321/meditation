import librosa
import pandas as pd
from datetime import datetime

audio_path = "30_1.m4a"
subtitle_path = "30_1.srt"
updated_subtitle_path = "result_"+subtitle_path


# 解析字幕时间
def parse_subtitle_time(subtitle_param):
    print(subtitle_param)
    start, end = subtitle_param.split("-->")
    start_time = datetime.strptime(start.strip(), "%H:%M:%S.%f").time()
    end_time = datetime.strptime(end.strip(), "%H:%M:%S.%f").time()
    return start_time, end_time


# 读取音频文件
y, sr = librosa.load(audio_path)

# 设置振幅阈值
threshold = 0.02

# 找到振幅低于阈值的部分
silence_intervals = librosa.effects.split(y, top_db=threshold)

# 计算停顿时长
silence_durations = [(end - start) / sr for start, end in silence_intervals]

# 读取原始字幕文件
with open(subtitle_path, 'r') as file:
    subtitles = file.readlines()

# 根据时间戳匹配停顿信息到字幕中
for i, subtitle in enumerate(subtitles):
    subtitle_start_time, subtitle_end_time = parse_subtitle_time(subtitle)
    for start, end, duration in zip(silence_intervals[:-1], silence_intervals[1:], silence_durations):
        if start >= subtitle_start_time and end <= subtitle_end_time:
            # 在字幕的每一行末尾插入停顿信息
            subtitles[i] = subtitle.strip() + f" (Pause: {duration:.2f} seconds)\n"
            break

# 将更新后的字幕写回文件
with open(updated_subtitle_path, 'w') as file:
    file.writelines(subtitles)
