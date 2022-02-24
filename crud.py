# pylint: disable=import-outside-toplevel
# pylint: disable=import-error

import json
import os
import re
from typing import List, Union


def param_check(param: str) -> Union[bool, List[int]]:
    """パラメータをチェックする、例として：　'3~9,22~23,94~95' パラメータが正確
    であればtrueがリターンするはず逆に誤ったであれば　falseがリターンするはず"""
    try:
        rt = []
        l = param.split(",")
        if len(l) != 3:
            return False
        for i in l:
            d = i.split("~")
            if len(d) != 2:
                return False
            if not d[0].isnumeric() or not d[1].isnumeric():
                return False
            if int(d[0]) >= int(d[1]):
                return False
            rt.append(int(d[0]))
            rt.append(int(d[1]))
    except:
        return False
    return rt


def special_by_pdf(path: str, param: str):
    import pdfplumber
    resolution = 196
    target = param_check(param)
    if not target:
        return
    full_path = os.path.join(path, 'p4')
    if not os.path.exists(full_path):
        os.makedirs(full_path, 0o777)
    with pdfplumber.open(path + '/saiwai.pdf') as pdf:
        index = 0
        for i in range(target[0] - 1, target[1]):
            pdf.pages[i].to_image(resolution=resolution).save(
                f'p4/toki_{index}.png')
            index += 1
        index = 0
        for i in range(target[2] - 1, target[3]):
            pdf.pages[i].to_image(resolution=resolution).save(
                f'p4/shi_{index}.png')
            index += 1
        index = 0
        for i in range(target[4] - 1, target[5]):
            pdf.pages[i].to_image(resolution=resolution).save(
                f'p4/sasami_{index}.png')
            index += 1


# --------下は文字データの処理----------

json_map = {}


def dump_json_from_html(path: str, title_text: str):
    by_bsoup(path)
    json_map[0] = title_text
    json_path = path + "/data.json"
    with open(json_path, "w") as f:
        json.dump(json_map, f)
    return json_path


class P3:
    def __init__(self, index: int):
        json_map[index] = ""
        self.index = index

    def write(self, txt: str):
        json_map[self.index] += txt


def remove_ruby(soup):
    ruby_tags = []
    ruby_tags.extend(soup.find_all("rt"))
    print(ruby_tags)
    for i in ruby_tags:
        if "※" not in str(i):
            i.decompose()


def by_bsoup(path: str, index: int = 2):
    """BeautifulSoupでHTMLからデータ抽出"""
    from bs4 import BeautifulSoup, NavigableString, Tag
    global json_map
    if index == 2:
        json_map = {}
    soup = BeautifulSoup(open(f"{path}/{index}.html"), features="html.parser")
    remove_ruby(soup)
    soup.rt.decompose()
    ls: List[Tag] = soup.find_all(
        name='div', attrs={"class": re.compile("_idGenObjectStyleOverride-")})
    print(len(ls))
    p3 = None
    now_day = 1
    if index == 3:
        now_day = 16
    try:
        for i in range(len(ls)):
            tag = ls[i]
            if tag.p is not None and tag.p.get('class') is not None:
                # 聖書箇所
                if tag.p.get('class')[0] == 'みことば本文':
                    print(tag)
                    p3 = P3(now_day)
                    txt = tag.get_text().strip()
                    p3.write(txt)
                    now_day += 1
                if 'ノーマル' in tag.p.get('class')[0]:
                    if '聖書箇所' in tag.get_text():
                        txt = '\n' + tag.get_text().strip()
                        p3.write(txt)
                        p3.write('\n--\n')
                # 証し
                if 'コラム' in tag.p.get('class')[0]:
                    title = tag.previous_sibling
                    while isinstance(title, NavigableString):
                        title = title.previous_sibling
                    p3.write(title.get_text())
                    txt = tag.get_text()
                    p3.write(txt)

                # if 'コラムのみことば' in tag.p.get('class')[0]:
                #     txt = tag.get_text().strip()
                #     p3.write('- ' + txt)
                #     print(txt)
                #     print('---')
                # 解説
                if 'ParaOverride-' in tag.p.get('class')[0] or '扉本文' in tag.p.get('class')[0]:
                    txt = tag.get_text()
                    if '●' in txt:
                        p3.write('\n---\n')
                        p3.write(txt)
                        for j in range(1, 10):
                            txt = ls[i + j].get_text()
                            p3.write(txt)
                        p3.write('\n----\n')
    except:
        ...
        # print(json_map)
    if index == 2:
        by_bsoup(path, index=3)
