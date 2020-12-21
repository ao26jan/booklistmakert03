# coding:UTF-8
from django.shortcuts import redirect
from pyzbar.pyzbar import decode
from pyzbar.pyzbar import ZBarSymbol
from PIL import Image
from PIL import ImageEnhance
import cv2 #opencv version 4.4.0
import numpy as np
import datetime
import math
import re

message=''

context = {'message':message,
            }

def contrast(image, a):
    lut = [ np.uint8(255.0 / (1 + math.exp(-a * (i - 128.) / 255.))) for i in range(256)]
    #result_image = np.array( [ lut[value] for value in image.flat], dtype=np.uint8 )
    result_image = result_image.reshape(image.shape)
    return result_image

def img_to_isbn(img):

    #鏡面反射
    #image_mirror = frame[:,::-1]
    #frame = image_mirror

    #グレースケール化
    gray = img.convert('L')

    #コントラスト強調
    #frame = contrast(frame,10)

    #ISBN検出
    #d = decode(frame)
    d = decode(gray,symbols=[ZBarSymbol.EAN13])
    #d = decode(frame,symbols=[ZBarSymbol.CODE39])

    #decode結果が存在したら
    if d:
        data = d
        #データ件数カウント
        countdata = len(data)

        #code初期化
        code = '0'

        #ISBN確定
        #認識されたコードが１つ以上なら
        if countdata >= 1:
            #code1に１つめのコードをいれる
            code1 = data[0][0].decode('utf-8','ignore')
            #code1の1桁目が9ならば
            if code1[0] == '9':
                #codeにcode1をいれる
                code = code1
            #１つめがだめで、コードが2つあるなら
            elif countdata == 2:
                #code2に２つめのコードをいれる
                code2 = data[1][0].decode('utf-8','ignore')
                #code2の1桁目が9ならば
                if code2[0] == '9':
                    #codeにcode2をいれる
                    code = code2
            #1つめも2つめも9以外で始まるとコードだった場合
            else:
                context['message']='ISBNが読み取れませんでした'
                redirect ('../')
        #認識されたコードがなければ
        else:
            context['message']='ISBNが読み取れませんでした'
            redirect ('../')

        '''
        print('code:',code)
        print('code[0]:',code[0])
        print('len(code):',len(code))
        '''

        #最終チェック
        if code[0] == '9' and len(code) == 13:
            context['message']='ISBNを読み取りました\n'
            return code

    #decode結果がFalse or Noneの場合：デコードできなかった場合
    else:
        context['message']='ISBNが読み取れませんでした'
        redirect ('../')