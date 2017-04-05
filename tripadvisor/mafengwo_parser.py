# coding:utf-8
import os
import re
from collections import OrderedDict
from copy import copy

from bs4 import NavigableString, BeautifulSoup
from bs4 import Tag

from util import Util


def page_element_cmp(a, b):
    mid = cssBox['w0']['width'] / 2
    if (a['left'] < mid and b['left'] < mid) or (a['left'] > mid and b['left'] > mid):
        if abs(int(b['bottom'] - a['bottom'])) < 3:
            return int(a['left'] - b['left'])
        else:
            return int(b['bottom'] - a['bottom'])  # ignore decimal， roughly compare
    else:
        return int(a['left'] - b['left'])


def get_names(unit_list):
    global names
    for idx in range(len(unit_list)):
        unit = unit_list[idx]
        if get_zzz(unit).find('封面提供') != -1:
            for u in unit:
                names += u['zzz']
        elif get_zzz(unit).find('图文提供') != -1:
            for u in unit:
                names += u['zzz']
        elif get_zzz(unit).find('图提供：') != -1:
            for u in unit:
                names += u['zzz']
        elif get_zzz(unit).find('蜂蜂：') != -1:
            for u in unit:
                names += u['zzz']
        elif get_zzz(unit).find('感谢：') != -1:
            for u in unit:
                names += u['zzz']
        elif get_zzz(unit).find('封面：') != -1:
            for u in unit:
                names += u['zzz']
        elif get_zzz(unit).find('致谢') != -1:
            names += get_zzz(unit_list[idx + 1])
            # names.replace(' ', '')


def names_filter(unit_list):
    global cssSet
    # print names
    idx = 0
    while idx < len(unit_list) - 1:
        unit = unit_list[idx]
        if unit[0]['zzz'].strip().replace(' ', '') in names and not re.compile(u'[0-9]+').match(unit[0]['zzz'].strip()):
            if get_rgb(unit[0]['color']) > 200:
                if int(unit_list[idx + 1][0]['bottom'] - unit[0]['bottom']) == 0:
                    cssSet.add(unit[0]['color'])
        idx += 1
    # print cssSet
    cssSet.add(u'rgb(203,110,29)')
    # print cssSet
    new_unit = []
    idx = 0
    while idx < len(unit_list) - 1:
        unit = unit_list[idx]
        if unit[0]['color'] in cssSet:
            if int(unit_list[idx + 1][0]['bottom'] - unit[0]['bottom']) == 0:
                idx += 1  # skip a unit
        else:
            new_unit.append(unit)
        idx += 1
    new_unit.append(unit_list[-1])
    return new_unit


def hearder_footer_filter(element):
    header = 0.90 * cssBox['h0']['height']
    footer = 0 * cssBox['h0']['height']
    return element.has_key('bottom') and element['bottom'] < header and element['bottom'] > footer


def special_filter(element):
    return element['zzz'] != 'www.mafengwo.cn' and element['zzz'] != '蚂蜂窝旅游攻略'


def get_contents(eachPage_html):
    element_list = []
    for eachStr in list(eachPage_html.strings):
        if eachStr.strip() == '':
            continue
        element = {}
        element.setdefault('zzz', eachStr.encode('utf-8'))
        for parent in list(eachStr.parents):
            if parent is not None and isinstance(parent, Tag) and parent.get('class') is not None:
                for cls in parent['class']:
                    if cls in cssBox:
                        for k, v in cssBox[cls].items():
                            if not element.has_key(k):
                                element.setdefault(k, v)
                            else:
                                if k == 'bottom' or k == 'left':
                                    element[k] += v
        if hearder_footer_filter(element) and special_filter(element):
            element_list.append(element)
    element_list = sorted(element_list, cmp=page_element_cmp)
    return element_list


def joint_equal(ele_now, ele_pre):
    # todo check contents
    if int(ele_now['bottom'] - ele_pre['bottom']) == 0 and ele_now['color'] == ele_pre['color'] \
            and ele_now['font-size'] == ele_pre['font-size']:
        return True
    if ele_now['font-family'] == ele_pre['font-family'] and ele_now['color'] == ele_pre['color'] \
            and ele_now['font-size'] == ele_pre['font-size'] and \
            (ele_now['font-size'] > 32 or abs(ele_now['bottom'] - ele_pre['bottom']) < 15):
        return True
    return False


def joint(element_list):
    new_element_list = []
    unit = []
    pre = element_list[0]
    unit.append(pre)
    for ele in element_list[1:]:
        if joint_equal(ele, pre):
            unit.append(ele)
        else:
            new_element_list.append(tuple(unit))
            unit = []
            unit.append(ele)
        pre = ele
    return tuple(new_element_list)


def grade_cmp(a, b):
    # todo: campare a,b according to css
    # if abs(int(a[0][0] - b[0][0])) < 4 and (a[0][0] < 40 or b[0][0] < 40):  # 字号
    if ((get_rgb(a[0][1]) > 150 or get_rgb(b[0][1]) > 150) and abs(int(a[0][0] - b[0][0])) <= 4 and (
                    a[0][0] < 40 or b[0][0] < 40)) or a[0][0] == b[0][0]:
        if abs(get_rgb(a[0][1]) - get_rgb(b[0][1])) < 100:  # 颜色类似
            cnt_a = a[1][0]
            cnt_b = b[1][0]
            # for unit_idx in a[1]:
            #     cnt_a += len(get_zzz(unit_list[unit_idx]))
            # for unit_idx in b[1]:
            #     cnt_b += len(get_zzz(unit_list[unit_idx]))
            if abs(cnt_a - cnt_b) < 20 * 3:
                return a[1][1] - b[1][1]  # 按顺序??????
            else:
                # print cnt_a, cnt_b, a[0], b[0], a[1], b[1]
                return cnt_a - cnt_b
        else:
            return get_rgb(b[0][1]) - get_rgb(a[0][1])  # 按颜色
    else:
        return int(b[0][0] - a[0][0])  # 按字号


def get_zzz(unit):
    str = ''
    for i in unit:
        str += i['zzz']
    return str


def get_rgb(rgb):
    pt = re.compile('rgb\(([0-9]+),([0-9]+),([0-9]+)\)')
    mt = pt.match(rgb)
    return int(mt.group(1)) + int(mt.group(2)) + int(mt.group(3))


def hash(unit):
    st = ''
    for i in unit:
        st += '('
        st += i.__str__()
        st += ')'
    return st


def sect(unit_list, grade):
    global grades
    if len(unit_list) == 0:
        return
    fff_l = count_fsfcff(unit_list)
    if len(fff_l) == 0:
        return
    if len(fff_l[0][1]) == 1 and fff_l[0][1][0] == 0:
        # print 'now pick:', 0
        # print 'subsection', grade, ':', get_zzz(unit_list[0]), '\n'
        grades.setdefault(hash(unit_list[0]), grade)
        if fff_l[0][0][0] >= 40:
            sect(unit_list[1:], grade)
        else:
            sect(unit_list[1:], grade + 1)
        return
    # todo pick more
    sizes = set([i[0][0] for i in fff_l])
    line = len(sizes) / 5
    if line > 2: line = 2
    to_split = []
    for idx in range(len(fff_l)):
        if idx <= line:
            to_split.extend(fff_l[idx][1][1:])
    pre = 0
    # print 'now pick:', sorted(to_split), '\n'
    for i in sorted(to_split):
        sect(unit_list[pre:i], grade + 1)
        # print 'subsection', grade, ':', get_zzz(unit_list[i]), '\n'
        grades.setdefault(hash(unit_list[i]), grade)
        pre = i + 1
    sect(unit_list[pre:], grade + 1)


def count_fsfcff(unit_list):
    fsfcff_idxlist = {}
    for idx in range(len(unit_list)):
        unit = unit_list[idx]
        key = (unit[0]['font-size'], unit[0]['color'], unit[0]['font-family'])
        fsfcff_idxlist.setdefault(key, [0, ])
        fsfcff_idxlist[key].append(idx)
        fsfcff_idxlist[key][0] += len(get_zzz(unit))
    fsfcff_idxlist = fsfcff_idxlist.items()
    fsfcff_idxlist = sorted(fsfcff_idxlist, cmp=grade_cmp)
    # for i, j in fsfcff_idxlist[:3]:
    #     print i
    #     for k in j[1:]:
    #         print k,
    #         for con in unit_list[k]:
    #             print con['zzz'],
    #     print
    # print '\n'
    return fsfcff_idxlist


def get_element_list(allPages):
    element_list = []
    for i in list(allPages.find_all('div', class_=re.compile('^pc'))):
        onePage = get_contents(i)
        element_list.extend(onePage)
    return tuple(element_list)


def unit_special_filter(unit_list):
    new_unit_list = []
    for unit in unit_list:
        flag = True
        for element in unit:
            z = element['zzz']
            filter_set = ['www.mafengwo.cn', '蚂蜂窝旅游攻略', '蚂蜂窝精选推荐', '蚂蜂窝价：', '扫码即可购买', '蚂蜂窝网络科技', '致谢', '封面提供', '图文提供']
            for word in filter_set:
                if word in z:
                    flag = False
            if re.compile('.*?市场价：[0-9]+').match(z):
                flag = False
        if flag:
            new_unit_list.append(unit)
    return new_unit_list


if __name__ == '__main__':
    global cssBox, grades, names, cssSet, golbal_unit_list

    path = 'mafengwo_html/'
    out_path = 'mafengwo_md/'
    for html_doc in os.listdir(path):
        # if html_doc != '维也纳.html' and html_doc != '三亚.html' and html_doc != '东京.html':
        #     continue
        # if html_doc != '三亚.html':
        #     continue
        print html_doc
        cssSet = set()
        names = ''
        grades = {}
        whole = BeautifulSoup(open(os.path.join(path, html_doc)), 'html.parser')
        container = whole.find('div', attrs={'id': 'page-container'})
        css = ''.join(whole.find_all('style')[2].stripped_strings)
        cssBox = Util.get_css_box(css)
        element_list = get_element_list(whole)
        unit_list = joint(element_list)
        get_names(unit_list)
        unit_list = unit_special_filter(unit_list)
        unit_list = names_filter(unit_list)
        golbal_unit_list = copy(unit_list)
        sect(unit_list, 1)

        # for k, v in grades.items():
        #     print v, k

        with open(os.path.join(out_path, html_doc) + '.md', 'w') as f:
            for unit in unit_list:
                con = hash(unit)
                f.write('#' * grades[con] + ' ')
                f.write(get_zzz(unit) + '\n')
                f.flush()
