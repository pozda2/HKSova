#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 17 14:45:24 2022

@author: gimli2
"""

import csv
from collections import defaultdict


def load_ki(fn='ki2022-7-17.csv'):
    data = defaultdict(lambda: [])
    with open(fn, 'r', encoding='utf8', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in spamreader:
            data[row[1]].append(row)
    return data


def match_ki(kidata, players: list = None, team: str = ''):
    for p in players:
        r = kidata.get(p['name'])
        p['KI_src'] = 'name'
        # print(r)

        # cele jmeno nezname, nutno hledat dal dle nicku
        if r is None:
            r = kidata.get(p['publicname'])
            p['KI_src'] = 'publicname (nick)'

        # shoda a 1 vysledek
        if isinstance(r, list) and len(r) == 1:
            p['KI'] = float(r[0][4])
            p['KI_uid'] = r[0][0]
            p['KI_match'] = '1 shoda'
            continue

        # shoda a vice vysledku
        if isinstance(r, list) and len(r) > 1:
            # print('vice', r)

            # podle tymu
            found = False
            for i in r:
                if i[3] == team:
                    p['KI'] = float(i[4])
                    p['KI_uid'] = i[0]
                    p['KI_match'] = 'vice shoda - team'
                    found = True
                    break
            if found:
                continue

            # zkusime najit podle prezdivky
            found = False
            for i in r:
                if i[2] == p['publicname']:
                    p['KI'] = float(i[4])
                    p['KI_uid'] = i[0]
                    p['KI_match'] = 'vice shoda - nick'
                    found = True
                    break
            if found:
                continue

    return players


if __name__ == '__main__':
    data = load_ki()
    for jm in data.keys():
        if len(data[jm]) > 1:
            print(jm, len(data[jm]))
            print(data[jm])

    players = [
        {'name': 'Honza', 'publicname': ''},
        {'name': 'Honza', 'publicname': 'Zámyn'},
        {'name': 'Jindra Cincibuch', 'publicname': ''},
        {'name': 'takovytuneni', 'publicname': ''},
    ]

    print('-' * 40)
    kiplayers = match_ki(data, players, 'Zebra řez')
    for kp in kiplayers:
        print(kp)

    avgki = sum([p['KI'] for p in kiplayers if p.get('KI') is not None]) / len(kiplayers)
    print(avgki)