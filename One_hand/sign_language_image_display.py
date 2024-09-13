"""

            -- Translation system: --

0 - nặng
1 - hỏi
2 - ngã
3 - sắc
4 - huyền

5 - ư, ơ
6 - ô, â, ê
7 - ă

"""


import cv2

text = ["lồn","á"]
sign = " 01234"
alphabet = "abcdeghiklmnopqrstuvxy" + sign
accented = ["aạảãáà", "eẹẻẽéè", "iịỉĩíì", "oọỏõóò", "uụủũúù", "ăặẳẵắằ", "âậẩẫấầ","êệểễếề","ôộổỗốồ","ơợởỡớờ","ưựửữứừ"]

def doit(word):
    i = 0
    uniword = word
    while i < len(uniword):
        if uniword[i] not in alphabet:
            for ind in range(5):
                if uniword[i] in accented[ind]:
                    ind1 = accented[ind].index(uniword[i])
                    uniword = uniword[:i] + accented[ind][0] + sign[ind1] + uniword[i + 1:]
            if uniword[i] in accented[5]:
                ind = accented[5].index(uniword[i])
                if ind == 0:
                    uniword = uniword[:i] + "a7" + uniword[i + 1:]
                else:
                    uniword = uniword[:i] + "a7"+ sign[ind] + uniword[i + 1:]
            elif uniword[i] in accented[6]:
                ind = accented[6].index(uniword[i])
                if ind == 0:
                    uniword = uniword[:i] + "a6" + uniword[i + 1:]
                else:
                    uniword = uniword[:i] + "a6"+ sign[ind] + uniword[i + 1:]
            elif uniword[i] in accented[7]:
                ind = accented[7].index(uniword[i])
                if ind == 0:
                    uniword = uniword[:i] + "e6" + uniword[i + 1:]
                else:
                    uniword = uniword[:i] + "e6"+ sign[ind] + uniword[i + 1:]
            elif uniword[i] in accented[8]:
                ind = accented[8].index(uniword[i])
                if ind == 0:
                    uniword = uniword[:i] + "o6" + uniword[i + 1:]
                else:
                    uniword = uniword[:i] + "o6"+ sign[ind] + uniword[i + 1:]
            elif uniword[i] in accented[9]:
                ind = accented[9].index(uniword[i])
                if ind == 0:
                    uniword = uniword[:i] + "o5" + uniword[i + 1:]
                else:
                    uniword = uniword[:i] + "o5"+ sign[ind] + uniword[i + 1:]
            elif uniword[i] in accented[10]:
                ind = accented[10].index(uniword[i])
                if ind == 0:
                    uniword = uniword[:i] + "u5" + uniword[i + 1:]
                else:
                    uniword = uniword[:i] + "u5"+ sign[ind] + uniword[i + 1:]
            if uniword[i] == "đ":
                uniword = uniword[:i] + "8" + uniword[i + 1:]
        print(uniword)
        img = cv2.imread("VSL_Dict/" + uniword[i] + ".png", cv2.IMREAD_ANYCOLOR)
        cv2.imshow(word, img)
        cv2.waitKey(400)
        i += 1

i = 0
while i < len(text):
    j = 0
    doit(text[i])
    i += 1
    cv2.destroyAllWindows()