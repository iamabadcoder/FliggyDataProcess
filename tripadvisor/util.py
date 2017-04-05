# coding: utf-8
import re
from bs4 import Tag


class Util:
    def __init__(self):
        pass

    @staticmethod
    def get_css_box(css):
        rule_pattern = re.compile('\.([_a-z0-9]+)\{(.+?)\}')
        attr_pattern = re.compile('(.+?):(.+?);')
        css_box = {}
        end_idx_rule = 0
        one_rule = rule_pattern.search(css, end_idx_rule)
        while one_rule:
            css_box.setdefault(one_rule.group(1), {})
            end_idx_attr = 0
            one_attr = attr_pattern.search(one_rule.group(2), end_idx_attr)
            while one_attr:
                tmp_text = one_attr.group(2)
                num = re.compile(u'([.0-9]+?)px$').search(tmp_text.strip())
                try_to_num = float(num.group(1)) if num else tmp_text
                css_box[one_rule.group(1)].setdefault(one_attr.group(1), try_to_num)
                end_idx_attr = one_attr.end(0)
                one_attr = attr_pattern.search(one_rule.group(2), end_idx_attr)
            end_idx_rule = one_rule.end(0)
            one_rule = rule_pattern.search(css, end_idx_rule)
        return css_box

    @staticmethod
    def try_to_num(text):
        num = re.compile(u'([.0-9]+?)px$').search(text.strip())
        return

    @staticmethod
    def get_css(class_name, element):
        if isinstance(element, Tag):
            for i in element['class']:
                if i.startswith(class_name):
                    return i
        return None

    @staticmethod
    def update_dict(a, bs):
        for b in bs:
            for i, j in b.items():
                a.setdefault(i, {})
                for kk, vv in j.items():
                    a[i].setdefault(kk, {})
                    for k, v in vv.items():
                        if isinstance(v, int):
                            a[i][kk].setdefault(k, 0)
                            a[i][kk][k] += v
                        elif isinstance(v, list):
                            a[i][kk].setdefault(k, [])
                            a[i][kk][k].extend(v)
        return a
