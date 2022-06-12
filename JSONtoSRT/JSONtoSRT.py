import json
import os
import math
import sys


def convertir_tiempo(sec):
    hours = sec / 1000 / 60 / 60

    if hours >= 1:
        minutes, hours = math.modf(hours)
        minutes = minutes*60
        seconds, minutes = math.modf(minutes)
        hoursString = list('%.0f' % hours)
        if hoursString.__len__() == 1:
            hoursString = ["0"] + hoursString

    else:
        hoursString = ["0", "0"]
        minutes = sec / 1000 / 60
        seconds, minutes = math.modf(minutes)

    if minutes >= 1:
        minutesString = list('%.0f' % minutes)
        #seconds = seconds*60*1000

        millis, seconds = math.modf(seconds*60)
        millis = millis*1000
        # print(seconds)
        # print(seconds)
        # print(millis)
        secondsString = list('%.0f' % seconds)
        millisString = list('%.0f' % millis)

        if minutesString.__len__() == 1:
            minutesString = ["0"] + minutesString

        if secondsString.__len__() == 1:
            secondsString = ["0"] + secondsString
        elif secondsString.__len__() == 0:
            secondsString = ["0"] + ["0"]

        if millisString.__len__() == 1:
            millisString = millisString + ["0"] + ["0"]
        elif millisString.__len__() == 2:
            millisString = millisString + ["0"]
        elif millisString.__len__() == 0:
            millisString = ["0"] + ["0"] + ["0"]

        elif millisString.__len__() >= 3:
            millisString = millisString[0:3]

        tiempo = hoursString + minutesString + secondsString + millisString
       
        if tiempo.__len__() == 6 and minutesString.__len__() == 2:
            tiempo = tiempo + [0]

    else:
        segundos = list(str(sec))
        tiempo = segundos
        

    return tiempo[::-1]


def crear_formato(result):
    timer = list("000000000")

    for i in range(len(timer)):
        if i >= result.__len__():
            break
        timer[-i - 1] = result[i]

    timer.insert(2, ":")
    timer.insert(5, ":")
    timer.insert(8, ",")
    return timer


def convertir_subtitulos(inicio, final, step):
    if step == 1:
        timerStart = crear_formato(convertir_tiempo(inicio))
        timerEnd = crear_formato(convertir_tiempo(inicio+final))
        return str("").join(timerStart), str("").join(timerEnd)
    else:
        timerStart = crear_formato(convertir_tiempo(inicio))
        timerEnd = crear_formato(convertir_tiempo(final))
        return str("").join(timerStart), str("").join(timerEnd)


def main(f, step):
    print("Procesando ...")

    index = 1
    if step == 1:
        start = 0
    else:
        start = 1
    lenEvents = f['events'].__len__()
    for i in range(start, lenEvents, step):
        if i+1 >= lenEvents:

            if 'segs' in f['events'][i] and 'dDurationMs' in f['events'][i]:
                if step == 1:
                    inicio = f['events'][i]['tStartMs']

                    final = (f['events'][i]['dDurationMs'])
                else:
                    inicio = f['events'][i]['tStartMs']

                    final = (f['events'][i]['tStartMs'])

                text1, text2 = convertir_subtitulos(inicio, final, step)
                lenSegs = f['events'][i]['segs'].__len__()
                # (i['segs'][0]['utf8'] != '\n'

                if lenSegs > 0:
                    file.write(str(index) + "\n")
                    file.write(str(text1) + "  -->  " + str(text2) + "\n")

                    for j in range(lenSegs):
                        file.write((f['events'][int(i)]['segs'][j]['utf8']))
                    index += 1
                file.write("\n\n")
            break
        if ('segs' in f['events'][int(i)] and 'dDurationMs' in f['events'][i]):
            if step == 1:
                inicio = f['events'][i]['tStartMs']

                final = (f['events'][i]['dDurationMs'])
            else:
                inicio = f['events'][i]['tStartMs']

                final = (f['events'][int(i + 1)]['tStartMs'])

   
            text1, text2 = convertir_subtitulos(inicio, final, step)
            lenSegs = f['events'][int(i)]['segs'].__len__()
      

            if lenSegs > 0:
                file.write(str(index) + "\n")
                file.write(str(text1) + "  -->  " + str(text2) + "\n")

                for j in range(lenSegs):
                    file.write((f['events'][int(i)]['segs'][j]['utf8']))
                index += 1
            file.write("\n\n")


if __name__ == "__main__":
    # Opening JSON file
    if len(sys.argv) == 4:
        try:
            f = open(sys.argv[1],  encoding='utf-8' )
            archivo = str(sys.argv[2])
            archivo = archivo + '.srt'
            f = json.load(f)

            if sys.argv[3] == "aut":
                step = 2
            elif sys.argv[3] == "org":
                step = 1
            else:
                raise Exception
            if os.path.isfile(archivo):
                print("Existe")
                os.unlink(archivo)
                file = open(archivo, 'a', encoding='utf-8')
            else:
                file = open(archivo, 'a', encoding='utf-8')

            main(f, step)
            print("Listo!")

        except Exception as e:
            print(e)
            exit(1)

    else:
        print("Error: Usage python JSONtoSRT.py jsonFile.json NameOutput ")
