# -*- coding: utf-8 -*-

afinn = {}

for line in open("./../AFINN/AFINN-111-pt.txt"):
    item = line.split('\t')
    afinn[item[0]] = int(item[1])

tweet = "Fone da samsung é o mais .. bosta q tem".lower()

value = sum(map(lambda word: afinn.get(word, 0), tweet.split()))

print value
