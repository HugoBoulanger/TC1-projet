import re
import sys
import os
import time
import json



def inputs_to_jsons(path):
    city_cc = re.compile(r"(\'.*?\')\|(\'[A-Z]{2}\')")

    inp = open(path, 'r')
    in_data = []
    dic = {}
    i = 0
    l = True
    while l:
        try:
            line = inp.readline()
            if line == '':
                l = False
            if line in dic:
                dic[line] += 1
            else:
                dic[line] = 1
            m = city_cc.match(line)
            print(f'{i}:{line} => match {m}')
            if m is not None:
                in_data.append((m[0], m[1], m[2]))
        except:
            print(f'Exception at line {i}')
        i += 1

    print(in_data[:20])
    f = open('curated_input.txt', 'w')
    json.dump(in_data, f)
    f.close()
    f = open('merged.txt', 'w')
    json.dump(dic, f)
    f.close()
    inp.close()


def unique_city_name(l):
    dic = {}
    for e in l:
        if e[1] in dic:
            if e[2] in dic[e[1]]:
                dic[e[1]][e[2]] += 1
            else:
                dic[e[1]].append(e[2])
        else:
            dic[e[1]] = [e[2]]

    f = open('unique_city.txt', 'w')
    json.dump(dic, f)
    f.close()

if __name__ == '__main__':
    f = open('curated_input.txt', 'r')
    l = json.load(f)
    f.close()
    unique_city_name(l)