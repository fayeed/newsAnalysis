import pandas as pd
import numpy as np


def getEmotionList(filename, arr):
    with open(filename, 'rb') as f:
        lines = f.readlines()[1:]
        for line in lines[1:]:
            line = str(line)
            l = line.split('\\t')
            l = l[1:]
            l.pop(1)
            l[1] = str(float(l[1][0:-5]))
            l[0] = "\"" + l[0] + "\""
            arr.append(l)


def makeEmotionData(data, outFile):
    arr = []
    isList = type(data) == list
    if(isList):
        for d in data:
            getEmotionList(d, arr)
    else:
        getEmotionList(data, arr)
    a = np.asarray(arr)
    np.savetxt(outFile, a, fmt='%s', delimiter=',',
               header="content,sentiment_value")


if __name__ == "__main__":
    makeEmotionData("data/unclean/EI-reg-En-anger-train.txt",
                    "data/clean/emotion_anger_regression.csv")
    makeEmotionData("data/unclean/EI-reg-En-fear-train.txt",
                    "data/clean/emotion_fear_regression.csv")
    makeEmotionData("data/unclean/EI-reg-En-joy-train.txt",
                    "data/clean/emotion_joy_regression.csv")
    makeEmotionData("data/unclean/EI-reg-En-sadness-train.txt",
                    "data/clean/emotion_sadness_regression.csv")
