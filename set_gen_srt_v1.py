import json
import datetime
from datetime import datetime, timedelta 
import srt 


# Function to convert Google Speech-to-Text JSON to SRT
def convert_json_to_srt(json_file, srt_file):
    with open(json_file, 'r') as json_data:
        data = json.load(json_data)

    subs = []
    # with open(srt_file, 'w') as srt_data:
    for results in data['results']:
        subs = break_sentences(22, subs, results['alternatives'][0])
            
    # print(subs)
    write_srt(subs, srt_file)

def break_sentences(max_chars, subs, alternative):
    """Breaks sentences by punctuations and maximum sentence length"""
    firstword = True
    charcount = 0
    idx = len(subs) + 1
    content = ""
    #check if there are alternatives 
    if "words" in alternative:
        for w in alternative['words']:
            if firstword:
                # first word in sentence, record start time
                 if "startTime" in w:
                    srt_start_time = convert_time_to_srt_format(w['startTime'])
                 else:
                    srt_start_time = convert_time_to_srt_format("0.000s")

            charcount += len(w['word'])
            content += " " + w['word'].strip()

            if ("." in w['word'] or "!" in w['word'] or "?" in w['word'] or
                    charcount > max_chars or
                    ("," in w['word'] and not firstword)):
                # break sentence at: . ! ? or line length exceeded
                # also break if , and not first word
                # print(srt_start_time.second)
                #print(content)
                str_end_time = convert_time_to_srt_format(w['endTime'])
                
                # sub = srt.Subtitle(index=idx,
                #                    start=timedelta(0, srt_start_time.second, srt_start_time.microsecond, 0, srt_start_time.minute, srt_start_time.hour),
                #                    end=timedelta(0, str_end_time.second, str_end_time.microsecond, 0,str_end_time.minute, str_end_time.hour),
                #                    content=srt.make_legal_content(content))
                # print(srt_start_time, str_end_time)
                # print(timedelta(0, srt_start_time.second, srt_start_time.microsecond, 0, srt_start_time.minute, srt_start_time.hour),
                #       timedelta(0, str_end_time.second, str_end_time.microsecond, 0,str_end_time.minute, str_end_time.hour), srt.make_legal_content(content))

                subs.append(srt.Subtitle(index=idx,
                                           start=timedelta(0, srt_start_time.second, srt_start_time.microsecond, 0, srt_start_time.minute, srt_start_time.hour),
                                           end=timedelta(0, str_end_time.second, str_end_time.microsecond, 0,str_end_time.minute, str_end_time.hour),
                                           content=srt.make_legal_content(content)))
                    
                firstword = True
                idx += 1
                content = ""
                charcount = 0
            else:
                firstword = False    
    return subs

def has_seconds(time_str):
    try:
        float_time = float(time_str)
        int_time = int(float_time)
        return float_time != int_time
    except ValueError:
        return False

def write_srt(subs, srt_file):
    """Writes SRT file"""
    # print("Writing {} subtitles to: {}".format(LANG, srt_file))
    f = open(srt_file, mode="w", encoding="utf-8")
    content = srt.compose(subs, reindex=True)
    f.writelines(str(content))
    f.close()
    return

def convert_time_to_srt_format(time_str):
    # Remove the "s" character from the end and split seconds and milliseconds
    time = time_str[:-1].replace('s', ',')

    if not has_seconds(time):
        if not time == "0.000":
            time = str(time) + ".00"
    seconds, milliseconds = time.split('.')
    
    # Convert to integers
    seconds = int(seconds)
    milliseconds = int(milliseconds)
    
    # Calculate hours, minutes, and remaining seconds
    hours, seconds = divmod(seconds, 3600)
    minutes, seconds = divmod(seconds, 60)
    time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d},{milliseconds:03d}"
    # print(time_str)
    time_object = datetime.strptime(time_str, '%H:%M:%S,%f').time()

    # Format the time in HH:MM:SS,mmm format
    return time_object

# Replace 'input.json' and 'output.srt' with your file paths
convert_json_to_srt('071222_DOMESTIC_VIOLENCE.json', '071222_DOMESTIC_VIOLENCE_1012P_NIGHT.srt')
