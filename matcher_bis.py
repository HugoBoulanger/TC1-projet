##Projet de TC1


from os import system, listdir, getcwd, chdir, mkdir, access, F_OK
from os.path import isfile, join, basename
from subprocess import check_call, DEVNULL
from time import time
import os.path
import sys
import os

working_dir = os.path.abspath(os.path.dirname(sys.argv[0]))
working_dir += "/Documents/TC1/"
print(working_dir)

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
            #print(f'{i}:{line} => match {m}')
            if m is not None:
                in_data.append((m[0], m[1], m[2]))
        except:
            print(f'Exception at line {i}')
        i += 1
    print(in_data[:10])
    f = open(working_dir + 'curated_input.txt', 'w')
    json.dump(in_data, f)
    f.close()
    f = open(working_dir + 'merged.txt', 'w')
    json.dump(dic, f)
    f.close()
    inp.close()
    return in_data, dic


def unique_city_name(l):
    dic = {}
    for e in l:
        if e[1] in dic:
            if e[2] in dic[e[1]]:
                dic[e[1]][e[2]] += 1
            else:
                dic[e[1]][e[2]] = 1
        else:
            dic[e[1]] = {e[2] : 1}
    f = open(working_dir + 'unique_city.txt', 'w')
    json.dump(dic, f)
    f.close()
    return dic 
    
def unique_CN_code(l):
    dic = {}
    for elt in l:
        if elt[2] in dic:
            if elt[1] in dic[elt[2]]:
                dic[elt[2]][elt[1]] += 1
            else:
                dic[elt[2]][elt[1]] = 1
        else:
            dic[elt[2]] = {elt[1] : 1}
    f = open(working_dir + 'unique_CN.txt', 'w')
    json.dump(dic, f)
    f.close()
    return dic     
    
def nb_country(d):
    dic = {}
    print(len(d.keys()))
    for elt in d.keys():
        nb = len(d[elt])
        if nb in dic:
            dic[nb] += 1
        else:
            dic[nb] = 1
    return dic
    
def write_city_name(dic):
    f = open(working_dir + "city_name.txt","w")
    sorted_cities = list(dic.keys())
    sorted_cities.sort()
    print(sorted_cities[:10])
    for elt in sorted_cities:
        f.write(f"{elt}\n")
    f.close()

if __name__ == '__main__':
    in_data, dic = inputs_to_jsons(working_dir + 'Problem 3 Input Data.txt')
    f = open(working_dir + 'curated_input.txt', 'r')
    l = json.load(f)
    f.close()
    unique_city = unique_city_name(l)
    unique_CN = unique_CN_code(l)
    nbc = nb_country(unique_city)
    nbcn = nb_country(unique_CN)
    write_city_name(unique_city)