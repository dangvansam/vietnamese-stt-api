#Transcript audio file use API (Vietnamese)
#sam 25/09/2019
import requests
import json
import os

def requestVTC(filename):
    url = "https://vtcc.ai/voice/api/asr/v1/rest/decode_file"
    headers = {
        'token': 'anonymous',
        'sample_rate': '16000',
        #'format':'S16LE',
        'num_of_channels':'1',
        #'asr_model': 'model code'
        }
    s = requests.Session()
    files = {'file': open(filename,'rb')}
    response = requests.post(url,files=files, headers=headers, verify='wwwvtccai.crt')

    res_json = response.json()
    if res_json[0]['status'] == 0:
        transcript = res_json[0]['result']['hypotheses'][0]['transcript_normed']
        #print('request VTC success')
        print('VTC transcript:',transcript)
        return transcript
    else:
        return None

def requestFPT(filename):
    url = 'https://api.fpt.ai/hmi/asr/general'
    payload = open(filename, 'rb').read()
    headers = {'api-key': 'sign in (https://console.fpt.ai/), enable STT api and paste your token here'} #examle: 'api-key': '3ISvE45DVemWTvrMTIgMtyfIjHnd8yAz'
    response = requests.post(url=url, data=payload, headers=headers)
    res_json = response.json()
    #print(res_json)
    if res_json['status'] == 0:
        transcript = res_json['hypotheses'][0]['utterance']
        #print('request FPT success')
        print('FPT transcript:',transcript)
        return transcript
    else:
        return None

def requestAndWriteFile(audio_dir_path = 'cuted', transcript_out_dir = 'cuted_transcript'):
    audio_dir = audio_dir_path + '/'
    if not os.path.exists(audio_dir):
        print('Audio dir: "{}" not found! Plase check input dir'.format(audio_dir_path))
        exit()
    transcript_dir = transcript_out_dir + '/'
    if not os.path.exists(transcript_dir):
        os.mkdir(transcript_dir)
    print('Input audio files dir: {}'.format(audio_dir))
    print('Output transcript files dir: {}'.format(transcript_dir))
    for f in os.listdir(audio_dir):
        name_label_file = transcript_dir + f.split('.')[0]+ '.txt'
        audio_path = audio_dir + f
        if os.path.isfile(name_label_file):
            print('Transript for: {} is exist in: {}. Skipped'.format(audio_path,name_label_file))
            continue
        else:
            label_file = open(name_label_file, 'w', encoding='utf-8')
            res = requestFPT(audio_path)
            if res == None:
                print('request vtc api failed. trying fpt api')
                res = requestVTC(audio_path)
                if res == None:
                    print('all api failed! skip')
            label_file.write(res)
            print('Transript success, file:{}'.format(name_label_file))
        break

requestAndWriteFile('cuted', 'cuted_transcript')