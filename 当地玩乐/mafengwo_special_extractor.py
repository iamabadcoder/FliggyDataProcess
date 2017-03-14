# coding: utf-8
import json
import os, re


def get_section(MD, pattern):
    '''\n(#+?) (?:(?:最佳旅游时间)|(?:最佳旅行时间))'''
    get = re.compile(pattern).search(MD)
    if not get:
        return '', -1
    next_mark = re.compile('\n#{{,{0}}} '.format(len(get.group(1)))).search(MD[get.end():])
    pos = next_mark.start() + get.end() if next_mark else len(MD)
    return MD[get.end():pos], len(get.group(1)) + 1


def check(MD_lines, sharps):
    result = []
    for idx in range(len(MD_lines)):
        line = MD_lines[idx]
        get = re.compile('^' + (sharps * '#') + ' ').search(line.strip())
        if get:
            result.append(idx)
    return result


def grade_format(MD_lines, prefix, sharps):
    strs = []
    if len(MD_lines) == 0:
        return strs
    if len(MD_lines) == 1:
        strs.append(prefix + MD_lines[0].strip('# '))
    level_lines = check(MD_lines, sharps)
    # print sharps, level_lines, prefix
    if len(level_lines) == 1 and level_lines[0] == 0:
        strs.extend(grade_format(MD_lines[1:], prefix + MD_lines[0].strip('# ') + '>>>>>', sharps + 1))
    else:
        pre = 0
        for i in level_lines:
            if i <= pre:
                continue
            if pre + 1 == i:
                strs.append(prefix + MD_lines[pre].strip('# '))
            else:
                strs.extend(
                    grade_format(MD_lines[pre + 1:i], prefix + MD_lines[pre].strip('# ') + '>>>>>', sharps + 1))
            pre = i
        if pre + 1 == len(MD_lines):
            strs.append(prefix + MD_lines[pre].strip('# '))
        else:
            strs.extend(grade_format(MD_lines[pre + 1:], prefix + MD_lines[pre].strip('# ') + '>>>>>', sharps + 1))
    return strs


def output(strs):
    rep_set = ["Catalogue", "catalogue", "Special", "Specials", "Highligts", "Highlights", '★', "景点"]
    marks = {}
    for line in strs:
        tips = []
        for tip in line.split('>>>>>'):
            for rep in rep_set:
                tip = tip.replace(rep, '')
            if tip != '':
                tips.append(tip.strip())
        if not tips:
            continue
        if len(tips) == 1:
            marks.setdefault("extra", [])
            marks['extra'].append(tips[0])
        elif len(tips) == 2:
            marks.setdefault(tips[0], [])
            marks[tips[0]].append(tips[1])
        else:
            start_title = -1
            for i in range(len(tips) - 1):
                idx = len(tips) - i - 2
                if len(tips[idx]) < 60:
                    start_title = idx
                    break
            if start_title != -1:
                marks.setdefault(tips[start_title], [])
                for tip in tips[start_title:]:
                    if tip not in marks[tips[start_title]] and tip is not tips[start_title]:
                        marks[tips[start_title]].append(tip)
            else:
                # error
                pass
    return marks


if __name__ == '__main__':
    path = 'mafengwo_md'
    cnt = 0
    all_citys = []
    for file in os.listdir(path):
        # if file != '额济纳旗.html.md':
        #     continue
        print '\n\n', file
        with open(os.path.join(path, file), 'r') as f:
            md = ''.join(f.readlines())
            highlight_text, len_sharp_h = get_section(md[1000:], '\n(#+?) (?:亮点) ?\n')
            special_text, len_sharp_s = get_section(md, '\n(#+?) (?:特别推荐) ?\n')
            build_levels = grade_format(highlight_text.split('\n'), '', len_sharp_h)
            marks = output(build_levels)
            mark_format = [{'key': k, 'value': v} for k, v in marks.items()]

            build_levels2 = grade_format(special_text.split('\n'), '', len_sharp_s)
            marks2 = output(build_levels2)
            mark_format2 = [{'key': k, 'value': v} for k, v in marks2.items()]

            all_citys.append({"dest": file.strip('.htmld'), "亮点": mark_format, "特别推荐": mark_format2})
    with open("special.json", 'w') as fout:
        fout.write(json.dumps(all_citys, ensure_ascii=False))
    print cnt
