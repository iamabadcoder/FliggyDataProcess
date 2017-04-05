# coding: utf-8
import os
import re
from copy import copy
from util import Util
from bs4 import BeautifulSoup, Tag


def page_element_cmp(a, b):
    mid = cssBox['w0']['width'] / 2
    if (a['left'] < mid and b['left'] < mid) or (a['left'] > mid and b['left'] > mid):
        if abs(int(b['bottom'] - a['bottom'])) < 3:
            return int(a['left'] - b['left'])
        else:
            return int(b['bottom'] - a['bottom'])  # ignore decimal， roughly compare
    else:
        return int(a['left'] - b['left'])


def hearder_footer_filter(element):
    header = 0.94 * cssBox['h0']['height']
    footer = 0.02 * cssBox['h0']['height']
    return element.has_key('bottom') and element['bottom'] < header and element['bottom'] > footer


def special_filter(element):
    return element['zzz'] != '·'


def area_filter(element, areas):
    b = element['bottom']
    l = element['left']
    for area in areas:
        if l > area[0] and l < area[1] and b > area[2] and b < area[3]:
            return False
    return True


def get_links(eachPage_html):
    link_area = []
    matrix = re.compile('left:(.*?)px;bottom:(.*?)px;width:(.*?)px;height:(.*?)px')
    links = eachPage_html.find_all('a', class_='l')
    for a in links:
        style = list(a.children)[0]['style']
        area = matrix.search(style)
        link_area.append((float(area.group(1)), float(area.group(1)) + float(area.group(3)), float(area.group(2)),
                          float(area.group(2)) + float(area.group(4))))
    # print link_area
    return link_area


def get_contents(eachPage_html):
    link_areas = get_links(eachPage_html)
    element_list = []
    for eachStr in list(eachPage_html.strings):
        if eachStr.strip(u' ·.…') == '':
            continue
        element = {}
        element.setdefault('zzz', eachStr.strip(u' ·.…').encode('utf-8'))
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
        if hearder_footer_filter(element) and special_filter(element) and area_filter(element, link_areas):
            element_list.append(element)
    element_list = sorted(element_list, cmp=page_element_cmp)
    return element_list


def get_element_list(allPages):
    element_list = []
    for i in list(allPages.find_all('div', class_=re.compile('^pc'))):
        onePage = get_contents(i)
        element_list.extend(onePage)
    idx = 0
    length = len(element_list)
    while idx < length:
        ele = element_list[idx]
        # print ele['zzz']
        # print '------------------------------------------------'
        if (get_rgb(ele['color']) > 150 or ele['font-size'] > 40) and (
                        ele['zzz'].startswith('问') or re.compile('D[1-9].*').match(ele['zzz'])
                or re.compile('No\.').match(ele['zzz'])):
            last = element_list[idx - 1]
            next = element_list[idx + 1]
            # print idx - 1, last['zzz']
            # print idx, ele['zzz']
            # print idx + 1, next['zzz']
            # print '================================================'
            if last['font-size'] == next['font-size'] and last['color'] == next['color'] and abs(
                            last['left'] - next['left']) < 3 and abs(next['bottom'] - last['bottom']) < ele[
                'font-size'] / 2:
                # and last['font-family'] == next['font-family']:
                element_list[idx], element_list[idx - 1] = element_list[idx - 1], element_list[idx]
                idx -= 1
                continue
        idx += 1

    return tuple(element_list)


def joint_equal(ele_now, ele_pre):
    # todo check contents
    if int(ele_now['bottom'] - ele_pre['bottom']) == 0 and ele_now['color'] == ele_pre['color'] \
            and ele_now['font-size'] == ele_pre['font-size']:
        return True
    if ele_now['font-family'] == ele_pre['font-family'] and ele_now['color'] == ele_pre['color'] \
            and ele_now['font-size'] == ele_pre['font-size'] \
            and (ele_now['left'] - ele_pre['left'] < 1 and ele_now['left'] - ele_pre['left'] > -50):
        return True
    return False


def unit_special_filter(unit_list):
    new_unit_list = []
    for unit in unit_list:
        flag = True
        zzz = get_zzz(unit)
        if re.compile('.*?by.*?').search(zzz):
            flag = False
        if flag:
            new_unit_list.append(unit)
    return new_unit_list


def joint(element_list):
    unit_list = []
    unit = []
    TBD = []
    pre = element_list[0]
    unit.append(pre)
    for ele in element_list[1:]:
        if joint_equal(ele, pre):
            for tbd in TBD:
                unit.append(tbd)
            unit.append(ele)
            TBD = []
            if re.compile(u'[\u4e00-\u9fa5]+').search(ele['zzz'].decode('utf-8')):
                pre = ele
        else:
            if re.compile(u'[\u4e00-\u9fa5]+').search(ele['zzz'].decode('utf-8')):
                unit_list.append(unit)
                unit = []
                if len(TBD) > 0:
                    for tbd in TBD:
                        unit.append(tbd)
                    if not (TBD[-1]['font-size'] == ele['font-size'] and TBD[-1]['color'] == ele['color']):
                        unit_list.append(unit)
                        unit = []
                unit.append(ele)
                TBD = []
                pre = ele
            else:
                TBD.append(ele)

    unit_list = unit_special_filter(unit_list)

    # new_unit_list = []
    # idx = 0
    # while idx < len(unit_list):
    #     ele = unit_list[idx][0]
    #     if ele['font-size'] > 40 and (ele['zzz'].startswith('问') or re.compile('D[1-9].*').match(ele['zzz'])
    #                                   or re.compile('No\.').match(ele['zzz'])):
    #         last = unit_list[idx - 1][0]
    #         next = unit_list[idx + 1][0]
    #         if last['font-size'] == next['font-size'] and last['color'] == next['color'] \
    #                 and last['font-family'] == next['font-family']:
    #             new_unit_list = new_unit_list[:-1]
    #             new_unit_list.append(unit_list[idx])
    #             unit = unit_list[idx - 1]
    #             unit.extend(unit_list[idx + 1])
    #
    #             new_unit_list.append(tuple(unit))
    #             # new_unit_list.append(unit_list[idx + 1])
    #             idx += 1
    #     else:
    #         new_unit_list.append(unit_list[idx])
    #     idx += 1
    # return tuple(new_unit_list)

    return tuple(unit_list)


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


def grade_cmp(a, b):
    # todo: campare a,b according to css
    if ((get_rgb(a[0][1]) > 150 or get_rgb(b[0][1]) > 150) and abs(int(a[0][0] - b[0][0])) <= 4 and (
                    a[0][0] < 40 or b[0][0] < 40)) or a[0][0] == b[0][0]:
        if abs(get_rgb(a[0][1]) - get_rgb(b[0][1])) < 100:  # 颜色类似
            cnt_a = a[1][0]
            cnt_b = b[1][0]
            if abs(cnt_a - cnt_b) < 20 * 3:
                return a[1][1] - b[1][1]  # 按顺序
            else:
                # print cnt_a, cnt_b, a[0], b[0], a[1], b[1]
                return cnt_a - cnt_b
        else:
            return get_rgb(b[0][1]) - get_rgb(a[0][1])  # 按颜色
    else:
        return int(b[0][0] - a[0][0])  # 按字号


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


def sect(unit_list, grade):
    global grades
    if len(unit_list) == 0:
        return
    fff_l = count_fsfcff(unit_list)
    if len(fff_l) == 0:
        return
    # if len(fff_l[0][1]) == 1 and fff_l[0][1][0] == 0:
    #     grades.setdefault(hash(unit_list[0]), grade)
    #     if fff_l[0][0][0] >= 40:
    #         sect(unit_list[1:], grade)
    #     else:
    #         sect(unit_list[1:], grade + 1)
    #     return
    # todo pick more
    sizes = set([i[0][0] for i in fff_l])
    line = len(sizes) / 5
    if line > 2: line = 2
    to_split = []
    for idx in range(len(fff_l)):
        if idx <= line:
            to_split.extend(fff_l[idx][1][1:])
    pre = 0
    for i in sorted(to_split):
        sect(unit_list[pre:i], grade + 1)
        grades.setdefault(hash(unit_list[i]), grade)
        pre = i + 1
    sect(unit_list[pre:], grade + 1)


if __name__ == '__main__':

    global cssBox, grades, names, cssSet, golbal_unit_list

    path = '/Users/caolei/PyWorkSpace/FliggyDataProcess/tripadvisor/oversea/test/'
    out_path = '/Users/caolei/PyWorkSpace/FliggyDataProcess/tripadvisor/oversea/md/'
    for html_doc in os.listdir(path):
        if '周边游' in html_doc:
            continue
        print html_doc
        cssSet = set()
        grades = {}
        whole = BeautifulSoup(open(os.path.join(path, html_doc)), 'html.parser')
        container = whole.find('div', attrs={'id': 'page-container'})
        css = ''.join(whole.find_all('style')[2].stripped_strings)
        cssBox = Util.get_css_box(css)

        chinese_words = 0
        total_words = 0
        for str in whole.strings:
            str = str.strip()
            c_w = re.compile(u'[\u4e00-\u9fa5]+').findall(str)
            if c_w:
                for word in c_w:
                    chinese_words += len(word)
            total_words += len(str)
        if float(chinese_words) / total_words < 0.001:
            continue  # messy doc

        element_list = get_element_list(whole)
        unit_list = joint(element_list)
        golbal_unit_list = copy(unit_list)
        sect(unit_list, 1)

        with open(os.path.join(out_path, html_doc) + '.md', 'w') as f:
            for unit in unit_list:
                con = hash(unit)
                f.write('#' * grades[con] + ' ')
                f.write(get_zzz(unit) + '\n')
                f.flush()
