import json
import subprocess

def read_json_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def mute_segments(input_video, segments):
    output_file = "muted_video2.mp4"
    tmp_cmd = ""
    cmd = ['ffmpeg', '-i', input_video, "-af"]

    for segment in segments:
        start_time = segment["start_time"]
        end_time = segment["end_time"]
        tmp_cmd += f"volume=enable='between(t,{start_time},{end_time})':volume=0,"

    #print(tmp_cmd)
    cmd += [tmp_cmd,output_file]
    #print(cmd)

    try:
        subprocess.Popen(cmd)
        print(f"Video segment between {start_time:.2f}s and {end_time:.2f}s muted successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error executing FFmpeg command: {e}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    json_file_path = "gm_shuffle_youtube_long_5.1.23.profanities.json"  # Replace with the actual path to your JSON file
    json_data = read_json_file(json_file_path)
    
    input_video_file = "BBB-watermark.ts"  # Replace with the actual path to your input video file
    segments_to_mute = json_data["results"]
    
    mute_segments(input_video_file, segments_to_mute)
