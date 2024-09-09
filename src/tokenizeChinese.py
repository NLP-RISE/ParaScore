# encoding=utf-8
# script of python2.7
# the tokenization of Chinese text contains two steps: separate each Chinese characters (by utf-8 encoding); tokenize the non Chinese part (following the mteval script).
# Shujian Huang huangsj@nju.edu.cn
import re
import sys


def isChineseChar(uchar):
    if (
        uchar >= "\u3400" and uchar <= "\u4db5"
    ): # CJK Unified Ideographs Extension A, release 3.0
        return True
    elif uchar >= "\u4e00" and uchar <= "\u9fa5": # CJK Unified Ideographs, release 1.1
        return True
    elif uchar >= "\u9fa6" and uchar <= "\u9fbb": # CJK Unified Ideographs, release 4.1
        return True
    elif (
        uchar >= "\uf900" and uchar <= "\ufa2d"
    ): # CJK Compatibility Ideographs, release 1.1
        return True
    elif (
        uchar >= "\ufa30" and uchar <= "\ufa6a"
    ): # CJK Compatibility Ideographs, release 3.2
        return True
    elif (
        uchar >= "\ufa70" and uchar <= "\ufad9"
    ): # CJK Compatibility Ideographs, release 4.1
        return True
    elif (
        uchar >= "\u20000" and uchar <= "\u2a6d6"
    ): # CJK Unified Ideographs Extension B, release 3.1
        return True
    elif (
        uchar >= "\u2f800" and uchar <= "\u2fa1d"
    ): # CJK Compatibility Supplement, release 3.1
        return True
    elif (
        uchar >= "\uff00" and uchar <= "\uffef"
    ): # Full width ASCII, full width of English punctuation, half width Katakana, half wide half width kana, Korean alphabet
        return True
    elif uchar >= "\u2e80" and uchar <= "\u2eff": # CJK Radicals Supplement
        return True
    elif uchar >= "\u3000" and uchar <= "\u303f": # CJK punctuation mark
        return True
    elif uchar >= "\u31c0" and uchar <= "\u31ef": # CJK stroke
        return True
    elif uchar >= "\u2f00" and uchar <= "\u2fdf": # Kangxi Radicals
        return True
    elif uchar >= "\u2ff0" and uchar <= "\u2fff": # Chinese character structure
        return True
    elif uchar >= "\u3100" and uchar <= "\u312f": # Phonetic symbols
        return True
    elif (
        uchar >= "\u31a0" and uchar <= "\u31bf"
    ): # Phonetic symbols (Taiwanese and Hakka expansion)
        return True
    elif uchar >= "\ufe10" and uchar <= "\ufe1f":
        return True
    elif uchar >= "\ufe30" and uchar <= "\ufe4f":
        return True
    elif uchar >= "\u2600" and uchar <= "\u26ff":
        return True
    elif uchar >= "\u2700" and uchar <= "\u27bf":
        return True
    elif uchar >= "\u3200" and uchar <= "\u32ff":
        return True
    elif uchar >= "\u3300" and uchar <= "\u33ff":
        return True
    else:
        return False


def tokenizeString(sentence, lc=False):
    """
    :param sentence: input sentence
    :param lc: flag of lowercase. default=True
    :return: tokenized sentence, with \n
    """

   # sentence = sentence.decode("utf-8")

    sentence = sentence.strip()

    sentence_in_chars = ""
    for c in sentence:
        if isChineseChar(c):
            sentence_in_chars += " "
            sentence_in_chars += c
            sentence_in_chars += " "
        else:
            sentence_in_chars += c
    sentence = sentence_in_chars

    if lc:
        sentence = sentence.lower()

   # tokenize punctuation
    sentence = re.sub(r"([\{-\~\[-\` -\&\(-\+\:-\@\/])", r" \1 ", sentence)

   # tokenize period and comma unless preceded by a digit
    sentence = re.sub(r"([^0-9])([\.,])", r"\1 \2 ", sentence)

   # tokenize period and comma unless followed by a digit
    sentence = re.sub(r"([\.,])([^0-9])", r" \1 \2", sentence)

   # tokenize dash when preceded by a digit
    sentence = re.sub(r"([0-9])(-)", r"\1 \2 ", sentence)

   # one space only between words
    sentence = re.sub(r"\s+", r" ", sentence)

   # no leading space
    sentence = re.sub(r"^\s+", r"", sentence)

   # no trailing space
    sentence = re.sub(r"\s+$", r"", sentence)

   # sentence += "\n"

   # sentence = sentence.encode("utf-8")

    return sentence


def tokenizeSentence(sentences):
   # file_r = open(inputFile, 'r', encoding='utf-8') # input file
   # file_w = open(outputFile, 'w') # result file
    output = []
   # <seg id="1">-28 "老欧洲" Chef Found ， 就是背井离乡来到旧金山追求财富的巴西人 Mall</seg>

    for sentence in sentences:
        if sentence.startswith("<seg"):
            start = sentence.find(">") + 1
            end = sentence.rfind("<")
           # new_sentence = tokenizeString(sentence)
            new_sentence = (
                sentence[:start] + tokenizeString(sentence[start:end]) + sentence[end:]
            )
        else:
            new_sentence = tokenizeString(sentence)
       # file_w.write(new_sentence)
        output.append(new_sentence)

   # file_r.close()
   # file_w.close()
    return output


if __name__ == "__main__":
    tokenizeSentence(sys.argv[1])
