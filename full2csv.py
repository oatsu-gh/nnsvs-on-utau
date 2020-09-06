#! /usr/bin/env python3
# coding: utf-8
# Copyright (c) 2020 oatsu
"""
HTS-Full-Context-Label をCSVに変換してExcelで見るようにする。
"""
import re


def full2csv(path_in, path_out):
    with open(path_in, mode='r', encoding='utf-8') as f:
        lines = [line.rstrip('\n') for line in f.readlines()]

    keys = []
    keys.append('start')
    keys.append('stop')
    keys.append(','.join([f'p{i+1}' for i in range(16)]))
    keys.append(','.join([f'a{i+1}' for i in range(5)]))
    keys.append(','.join([f'b{i+1}' for i in range(5)]))
    keys.append(','.join([f'c{i+1}' for i in range(5)]))
    keys.append(','.join([f'd{i+1}' for i in range(9)]))
    keys.append(','.join([f'e{i+1}' for i in range(60)]))
    keys.append(','.join([f'f{i+1}' for i in range(9)]))
    keys.append(','.join([f'g{i+1}' for i in range(2)]))
    keys.append(','.join([f'h{i+1}' for i in range(2)]))
    keys.append(','.join([f'i{i+1}' for i in range(2)]))
    keys.append(','.join([f'j{i+1}' for i in range(3)]))

    l = []
    l.append([','.join(keys)])

    for line in lines:
        tmp = re.sub('/.:', '@', line)
        l.append(re.split('[{}]'.format(re.escape(' =+-~!@#$%^&;_|[]')), tmp))
    l_of_str = [','.join(v) for v in l]
    str_lines_out = '\n'.join(l_of_str)
    with open(path_out, mode='w', encoding='utf-8') as f:
        f.write(str_lines_out)


def main():
    path_in = input('path of full-label: ').strip('"')
    path_out = 'result.csv'
    full2csv(path_in, path_out)
    print('ok')


if __name__ == '__main__':
    main()
