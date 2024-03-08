#youtubeのURLから文字起こしを行う（話者分離含む）
##必要なライブラリのインポート
import os
from yt_dlp import YoutubeDL
import ffmpeg
import glob
import whisper
from pyannote.audio import Pipeline,Audio
import speechbrain
import torch
import openai
import tempfile
import soundfile as sf

os.environ["OPENAI_API_KEY"] = "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"
client = openai.OpenAI()

##Youtubeのmp3取得
def Get_Youtube(strurl,strfilename):
    if not ".mp3" in strfilename:
        strfilename = strfilename + ".mp3"
    ydl_audio_opts = {
        "outtmpl":strfilename,
        "format":"bestaudio/best"
    }
    with YoutubeDL(ydl_audio_opts)as ydl:
        ydl.download(strurl)
    print("Youtube Download Finished...")
    return strfilename

##mp3のwavへの変換
def Mp3_To_Wav(strfilename_mp3):
    stream = ffmpeg.input(strfilename_mp3)
    strfilename_wav = strfilename_mp3.replace("mp3","wav")
    stream = ffmpeg.output(stream,strfilename_wav)
    ffmpeg.run(stream)
    print("mp3 Convert Finished...")
    return strfilename_wav

##wavの話者分離
def Speaker_Diarization(strfilename):
    pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization",use_auth_token="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")
    diarization = pipeline(strfilename)
    audio = Audio(sample_rate=16000,mono=True)
    listdictaudio = []
    for segment,_,speaker in diarization.itertracks(yield_label=True):
        waveform,sample_rate = audio.crop(strfilename,segment)
        dictaudio = {
            "speaker":speaker,
            "waveform":waveform.squeeze().numpy(),
            "sample_rate":sample_rate
        }
        listdictaudio.append(dictaudio)
    print("Speaker Diarization Finished...")
    return listdictaudio

##whisperによる文字起こし
def Talk_Text(listdictaudio,strfilename_wav):
    strfilename_text = strfilename_wav.replace("wav","txt")
    list_text = []
    for dictaudio in listdictaudio:
        speaker = dictaudio["speaker"]
        waveform = dictaudio["waveform"]
        sample_rate = dictaudio["sample_rate"]
        with tempfile.NamedTemporaryFile(delete=False,suffix=".wav") as audio:
            sf.write(audio.name,waveform,sample_rate)
            with open(audio.name,"rb")as f:
                try:
                    response  = client.audio.transcriptions.create(
                        model="whisper-1",
                        file=f,
                        prompt="以下の音源を文字起こししてください。ただし、必ず適切な位置に句読点を打ってください。",
                        language="ja",
                        response_format="text"
                    )
                except:
                    continue
        text = response
        speak_text = speaker + ":" + text
        list_text.append(speak_text)
    text_out = "\n".join(list_text)
    with open(strfilename_text,"w",encoding="utf_8_sig")as f:
        f.write(text_out)

if __name__ == "__main__":
    
    dictqueue={
        "NewsPicks":"https://youtu.be/Aot7-j-EoHc?si=kWoyygG5bLqYQ3K6"

    }
    for strfilename_mp3 in dictqueue:
        strurl = dictqueue[strfilename_mp3]
        strfilename_mp3 = Get_Youtube(strurl,strfilename_mp3)
        strfilename_wav = Mp3_To_Wav(strfilename_mp3)
        listdictaudio = Speaker_Diarization(strfilename_wav)
        Talk_Text(listdictaudio,strfilename_wav)
        os.remove(strfilename_mp3)
        os.remove(strfilename_wav)
    print("Talk To Text Finished!!!")