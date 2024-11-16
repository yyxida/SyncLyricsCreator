import re
from tkinter import filedialog
import soundfile as sf
import os


def file_name_walk(file_dir):
    for root, dirs, files in os.walk(file_dir):
        return files  # 当前路径下所有非目录子文件


def dict_lits_puls(dict_lits):
    timetag = []
    # for i in dict_lits:
    #     timetag.append(int(i["time_ms"]))
    # print(timetag)

    for i in range(len(dict_lits) - 1):

        for j in range(len(dict_lits[i + 1]["lrc_dict"])):
            for k in range(i+1):

                dict_lits[i + 1]['lrc_dict'][j]['start'] += dict_lits[k]['time_ms']
                dict_lits[i + 1]['lrc_dict'][j]['end'] += dict_lits[k]['time_ms']

    return dict_lits

def save_to_file(file_name, contents):
    fh = open(file_name, 'w',encoding="utf-8")
    fh.write(contents)
    fh.close()



def all_dict_lits_to_lrc(all_dict_lits):
    lrc_txt=''
    for i in all_dict_lits:
        for j in i['lrc_dict']:

            group3=round(j['start'] / 10) % 100
            group2=int(round(j['start'] / 10) / 100)%60
            group1=int(int(round(j['start'] / 10) / 100)/60)

            group6=round(j['end'] / 10) % 100
            group5=int(round(j['end'] / 10) / 100)%60
            group4=int(int(round(j['end'] / 10) / 100)/60)

            if group1 <10:
                group1='0'+str(group1)
            group1 = str(group1)

            if group2 <10:
                group2='0'+str(group2)
            group2 = str(group2)

            if group3 <10:
                group3='0'+str(group3)
            group3 = str(group3)

            if group4 <10:
                group4='0'+str(group4)
            group4 = str(group4)
            if group5<10:
                group5='0'+str(group5)
            group5 = str(group5)

            if group6 <10:
                group6='0'+str(group6)
            group6 = str(group6)



            lrc_txt=lrc_txt+"["+group1+":"+group2+"."+group3+"]"+j['word']+"\n["+group4+":"+group5+"."+group6+"]\n"

    return lrc_txt



if __name__ == '__main__':
    # f = sf.SoundFile('01-ぶたさん線香.mp3')
    # print('samples = {}'.format(f.frames))
    # print('sample rate = {}'.format(f.samplerate))
    # print('seconds = {}'.format(f.frames / f.samplerate))
    full_dict_lits = []
    all_dict_lits = []
    Folderpath = filedialog.askdirectory()
    file_list = file_name_walk(Folderpath)

    for i in file_list:
        if os.path.splitext(i)[-1] == ".mp3" or os.path.splitext(i)[-1] == ".wav" or os.path.splitext(i)[
            -1] == ".flac" or os.path.splitext(i)[-1] == ".m4a":

            file_dict = {"filename": "",
                         "time_ms": "",
                         "lrc_dict": []}

            f = sf.SoundFile(Folderpath + "/" + i)
            file_dict["filename"] = os.path.splitext(i)[0]
            file_dict["time_ms"] = round(f.frames / f.samplerate * 1000)
            lrc_file = open(Folderpath + "/" + file_dict["filename"] + '.lrc', encoding='utf-8')
            lrc_word = lrc_file.read()
            lrc_word = lrc_word.replace('\n', '')
            all_start_word_end = re.findall('\[([0-9]{2}\:[0-9]{2}.[0-9]{2})](.*?)\[([0-9]{2}\:[0-9]{2}.[0-9]{2})\]',
                                            lrc_word)
            for start_word_end in all_start_word_end:
                start_word_end_dict = {}
                # 拆分，分 秒 毫
                start_time_re = re.match('([0-9]{2})\:([0-9]{2}).([0-9]{2})', start_word_end[0])
                end_time_re = re.match('([0-9]{2})\:([0-9]{2}).([0-9]{2})', start_word_end[2])

                # 转换为int毫秒
                start_time = int(start_time_re.group(1)) * 60000 + int(start_time_re.group(2)) * 1000 + int(
                    start_time_re.group(3)) * 10
                end_time = int(end_time_re.group(1)) * 60000 + int(end_time_re.group(2)) * 1000 + int(
                    end_time_re.group(3)) * 10

                # 输出到dict
                start_word_end_dict['start'] = start_time
                start_word_end_dict['word'] = start_word_end[1]
                start_word_end_dict['end'] = end_time
                file_dict["lrc_dict"].append(start_word_end_dict)

            all_dict_lits.append(file_dict)

    all_dict_lits=dict_lits_puls(all_dict_lits)


    save_to_file(Folderpath+"/all.lrc",all_dict_lits_to_lrc(all_dict_lits))
