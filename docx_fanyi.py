# -*- coding: utf-8 -*-
# @File  : docx_fanyi.py
# @Author: Panbo
# @Date  : 2019/2/20
# @Desc  :



import time
import os
import traceback
import docx
from docx import Document


from googletrans import Translator


g_log = None

g_trans = Translator(service_urls=[
    'translate.google.cn',
])


def translate_buff(buff_para, buff_text, src, dest):
    joiner = '|||'
    tt = joiner.join(buff_text)
    msg = '\t正在翻译：共有 {} 个字'.format(len(tt))
    print(msg)
    if g_log:
        g_log.show.emit(msg)
    try:
        tr = g_trans.translate(tt, dest=dest, src=src)
    except:
        traceback.print_exc()
        msg = '\t<b>Google翻译异常，请稍后再试</b>'
        print(msg)
        if g_log:
            g_log.show.emit(msg)
        return
    tr = tr.text.split(joiner)
    for i, para in enumerate(buff_para):
        para.text += '\n' + tr[i]


def translate_docx(fn, src, dest):
    doc = Document(fn)
    buff_para = []
    buff_text = []
    buff_len = 0
    max_len = 4900
    for para in doc.paragraphs:
        text = para.text.strip()
        if not text: continue
        text_len = len(text.encode('utf8'))
        if buff_len + text_len < max_len:
            buff_para.append(para)
            buff_text.append(text)
            buff_len += text_len
            continue
        translate_buff(buff_para, buff_text, src, dest)
        msg = '休眠 10 秒钟再进行下一次翻译'
        print(msg)
        if g_log:
            g_log.show.emit(msg)
        time.sleep(10)
        buff_para = [para]
        buff_text = [text]
        buff_len = text_len
    if buff_para:
        translate_buff(buff_para, buff_text, src, dest)

    # save
    n_dir = os.path.dirname(fn)
    n_file = os.path.basename(fn)
    to_save = os.path.join(n_dir, 'fanyi-'+n_file)
    doc.save(to_save)
    return to_save


if __name__ == '__main__':
    from sys import argv
    fn = argv[1]
    src = 'en'
    dest = 'zh-cn'
    translate_docx(fn, src, dest)

