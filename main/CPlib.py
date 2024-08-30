#!/usr/bin/python3
import smtplib, ssl, re, sqlite3, datetime,subprocess
#import blockLib as lib

def way_of_file(way_to_name_of_file): #0 le fichier n'y est pas, 1 il y est
    proc = subprocess.Popen(f"locate {way_to_name_of_file}",stdout = subprocess.PIPE, shell = True)
    test = proc.stdout.read()
    test = test.decode("utf-8")
    list = test.split("\n")
    if(len(test) == 0):
        return 0
    else:
        return list


def path_firefox_history():# if return 0 then print("firefox not found")
    list = way_of_file("places.sqlite")
    if(list == 0):
        return 0
    else:
        for path in list:
            pieces = path.split('/')
            try:
                if((pieces[3] == ".mozilla") and (pieces[len(pieces) - 1] == "places.sqlite")):
                    return [path]
            except:
                pass
        return 0

def path_others_history():# on retourn la liste vide si on a pas d'autres chemins
    paths = []
    list = way_of_file("History")
    if(list == 0):
        return 0
    else:
        for path in list:
            pieces = path.split('/')
            try:
                if((pieces[3] == ".config") and (pieces[len(pieces) - 1] == "History")):
                    paths.append(path)
                    #print(paths)
            except:
                pass
        return paths

def time_addition(first_time,second_time):
    print(first_time,second_time)
    T0 = first_time.split(':')
    T1 = second_time.split(':')
    seconde = int(T0[2]) + int(T1[2])
    minutes = int(T0[1]) + int(T1[1])
    hours   = int(T0[0]) + int(T1[0])
    wast = seconde/60
    seconde = int(seconde % 60)
    minutes = minutes + wast
    wast = minutes/60
    minutes = int(minutes % 60)
    hours   = int(hours + wast)
    print(f"{hours}:{minutes}:{seconde}")
    return f"{hours}:{minutes}:{seconde}"
