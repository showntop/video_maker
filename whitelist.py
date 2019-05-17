import os


def whitelist(filename):
    listset = set([])
    with open(filename, 'r') as file:
        lines = file.readlines()
    for line in lines:
        listset.add(line.strip())
    return listset
