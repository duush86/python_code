import json
import subprocess

def read_json_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def beep_segments(input_video, segments):
    output_file = "beep_video.mp4"
    tmp_cmd = ""
    cmd = ['ffmpeg', '-i', input_video, "-af"]

    for segment in segments:
        start_time = segment["start_time"]
        st_milliseconds = start_time*1000
        end_time = segment["end_time"]
        duration_time = segment["end_time"] - segment["start_time"]
        tmp_cmd += f"volume=enable='between(t,{start_time},{end_time})':volume=0[main];sine=d={duration_time}:f=800,adelay={st_milliseconds}s,pan=stereo|FL=c0|FR=c0[beep];[main][beep]amix=inputs=2,"

    # ffmpeg -y -i BBB-watermark.ts -af 
    #     "volume=enable='between(t,5,10)':volume=0[main];sine=d=5:f=800,adelay=5s,pan=stereo|FL=c0|FR=c0[beep];[main][beep]amix=inputs=2,
    #      volume=enable='between(t,15,20)':volume=0[main];sine=d=5:f=800,adelay=15s,pan=stereo|FL=c0|FR=c0[beep];[main][beep]amix=inputs=2, 
    #      volume=enable='between(t,40,50)':volume=0[main];sine=d=10:f=800,adelay=40s,pan=stereo|FL=c0|FR=c0[beep];[main][beep]amix=inputs=2" 
    # output.wav
    
    print(tmp_cmd)

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
    segments_to_beep = json_data["results"]
    
    beep_segments(input_video_file, segments_to_beep)
