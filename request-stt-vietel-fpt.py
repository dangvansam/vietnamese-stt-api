#Transcript audio file use API (Vietnamese)
#sam 25/09/2019
import requests
import json
import os
from lxml.html import fromstring

def get_proxies():
    url = 'https://free-proxy-list.net/'
    response = requests.get(url)
    parser = fromstring(response.text)
    proxies = set()
    for i in parser.xpath('//tbody/tr')[:10]:
        if i.xpath('.//td[7][contains(text(),"yes")]'):
            #Grabbing IP and corresponding PORT
            proxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
            proxies.add(proxy)
    return proxies

def requestVTC(filename, proxy): 
    url = "https://vtcc.ai/voice/api/asr/v1/rest/decode_file"
    headers = {
        'token': 'ulTkA-jNoKXB78VqO1Qg5GQ5eIeO91dlpi7n9WdnhvhADz6T0wzFxrw8iBkOCD4R',
        'sample_rate': '16000',
        #'format':'S16LE',
        'num_of_channels':'1',
        #'asr_model': 'model code'
        }
    #qpupDIOO3HY6HATdGde9ve0VzXMZl-SjSrT9RVv-Vz9nF3VsJtguOrpJzGzBad1o, anonymous
    
    s = requests.Session()
    files = {'file': open(filename,'rb')}
    if proxy != None:
        response = requests.post(url,files=files, headers=headers, verify='wwwvtccai.crt', proxy = proxy)
    else:
        response = requests.post(url,files=files, headers=headers, verify='wwwvtccai.crt')
    #print(response.text)
    res_json = response.json()
    #print(res_json)
    try:
        a = res_json[0]['status']
        if a == 0:
            transcript = res_json[0]['result']['hypotheses'][0]['transcript_normed']
            #print('request VTC success')
            print('VTC transcript:',transcript)
            if len(transcript) == 0:
                return None
            else:
                return transcript
    except:
        return None

def requestFPT(filename):
    url = 'https://api.fpt.ai/hmi/asr/general'
    payload = open(filename, 'rb').read()
    headers = {'api-key': 'eqJwxYhIkfgkCS1LB8ON5d7jKfEgj2na'} #examle: 'api-key': '3ISvE45DVemWTvrMTIgMtyfIjHnd8yAz' , qpupDIOO3HY6HATdGde9ve0VzXMZl-SjSrT9RVv-Vz9nF3VsJtguOrpJzGzBad1o
    try:
        response = requests.post(url=url, data=payload, headers=headers)
        print(response)
        res_json = response.json()
        print(res_json)
        a = res_json['status']
        if a == 0:
            transcript = res_json['hypotheses'][0]['utterance']
            #print('request FPT success')
            print('FPT transcript:',transcript)
            if len(transcript) == 0:
                return None
            else:
                return transcript
        else:
            return None
    except:
        return None
        
from time import sleep
def requestAndWriteFile(audio_dir_path, transcript_out_dir):
    audio_dir = audio_dir_path + '/'
    if not os.path.exists(audio_dir):
        print('Audio dir: "{}" not found! Plase check input dir'.format(audio_dir_path))
        exit()
    transcript_dir = transcript_out_dir + '/'
    if not os.path.exists(transcript_dir):
        os.mkdir(transcript_dir)
    print('Input audio files dir: {}'.format(audio_dir))
    print('Output transcript files dir: {}'.format(transcript_dir))
    proxies = {'118.174.232.237:48665', '202.29.237.213:3128', '101.109.243.99:8080'}#get_proxies()
    for f in os.listdir(audio_dir):
        name_label_file = transcript_dir + f.split('/')[-1].split('.')[0]+ '.txt'
        audio_path = audio_dir + f
        if os.path.isfile(name_label_file):
            print('Transript for: {} is exist in: {}. Skipped'.format(audio_path,name_label_file))
            continue
        else:
            #sleep(3)
            #res = requestFPT(audio_path)
            # if res == None:
            #     sleep(3)
            res = requestVTC(audio_path, None)
            sleep(1)
            # for ip in proxies:
            #     sleep(2)
            #     try:
            #         print('ip:',ip)
            #         ip = {"http": ip, "https": ip}
            #         res = requestVTC(audio_path,ip)
            #         print(res)
            #     except:
            #         res = None
            #     if res != None:
            #         print('success ip:',ip)
            #         break
            if res == None:
                continue
            else:
                label_file = open(name_label_file, 'w', encoding='utf-8')
                label_file.write(res)
                print('Transript success, file:{}'.format(name_label_file))
                sleep(2)
        #break
#print(get_proxies())
requestAndWriteFile('H:/ASR/dataset ASR/5000 file gốc/all_wav_thai_son', 'all_wav_thai_son_transcript')
#requestAndWriteFile('to_tieng_cuted', 'to_tieng_transcript')