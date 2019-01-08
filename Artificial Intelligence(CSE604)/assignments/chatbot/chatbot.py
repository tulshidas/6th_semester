from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import WordNetLemmatizer
import nltk
import dateparser
import time
from nltk.corpus import stopwords
from datetime import date
import datetime
import re
import calendar
import types
import string
import numpy as np

need_semester = False
sem2 = [("sunday", ["SE206", "8:00-9:50", "MZH"], ["GE212", "10:00-10:50", "KMR"], ["CSE211", "11:00-12:50", "ZB"],
         ["", "", ""]),
        ("monday", ["GE212", "10:00-10:50", "KMR"], ["STAT203", "11:00-12:50", "SH"], ["", "", ""],
         ["", " ", " "]),
        ("tuesday", ["SE206", "8:00-9:50", "MSS"], ["CSE201", "10:00-10:50", "NAN"], ["STAT203", "11:00-11:50 ", "SH"],
         ["CSE211", "12:00-12:50", "ZB"]),
        ("wednesday", ["MATH204", "8:00-9:50", "CP"], ["CSE201", "11:00-12:50", "NAN"], ["", " ", " "],
         ["", " ", " "]),
        ("thursday", ["CSE211", "9:00-9:50", "ZB"], ["CSE201", "10:00-11:50", "NAN"], ["MATH204", "12:00-12:50", "CP"],
         ["", " ", " "])
        ]
sem4 = [("sunday", ["CSE403", "8:00-9:50", "MZH"], ["CSE404", "10:00-10:50", "MS"], ["SE406", "11:00-12:50", "NAN"],
         ["", " ", " "]),
        ("monday", ["BUS405", "10:00-10:50", "IA"], ["GE402", "11:00-12:50", "TK"], ["CSE401", "2:00-3;50", "BMH"],
         ["", " ", " "]),
        ("tuesday", ["CSE404", "10:00-10:50", "MS"], ["CSE403", "11:00-12:50", "MSI"], ["CSE404", "2:00-3:50 ", "MS"],
         ["", "", ""]),
        ("wednesday", ["SE406", "10:00-10:50", "NAN"], ["GE402", "11:00-12:50", "TK"], ["", " ", " "],
         ["", " ", " "]),
        ("thursday", ["BUS405", "10:00-11:50", "ZB"], ["SE406", "12:00-12:50", "NAN"], ["CSE401", "2:00-3:50", "BMH"],
         ["", " ", " "])

        ]
sem6 = [("sunday", ["SE605", "9:00-10:50", "NAN"], ["BUS602", "11:00-12:50", "SAK"], ["SE606", "2:00-3:50", "NAT"],
         ["", " ", " "]),
        ("monday", ["SE605", "10:00-10:50", "MSS"], ["CSE604", "11:00-12:50", "AK"], ["GE603", "2:00-3;50", "RS"],
         ["", " ", " "]),
        ("tuesday", ["GE603", "9:00-9:50", "RS"], ["CSE604", "10:00-10:50", "AK"], ["CSE601", "11:00-12:50 ", "KKR"],
         ["BUS602", "2:00-3:50", "SAK"]),
        ("wednesday", ["GE603", "9:00-10:50", "RS"], ["SE605", "11:00-11:50", "MSS"], ["SE606", "2:00-3:50", "NAT"],
         ["", " ", " "]),
        ("thursday", ["CSE601", "8:00-10:50", "KKR"], ["GE603", "11:00-12:50", "RS"], ["SE606", "2:00-2:50", "NAT"],
         ["CSE604", "3:00-3:50", "AK"])
        ]
sem8 = [("sunday", ["CSE802", "11:00-12:50", "SAK"], ["", " ", " "], ["", " ", " "],
         ["Nothing", " ", " "]),
        ("monday", ["SE843", "8:00-8:50", "MSS"], ["CSE803", "9:00-10:50", "MAJ"], ["", "", ""],
         ["", " ", " "]),
        ("tuesday", ["CSE802", "11:00-12:50", "SAK"], ["", " ", " "], ["", " ", " "],
         ["", " ", " "]),
        ("wednesday", ["SE843", "8:00-9:50", "MSS"], ["CSE837", "2:00-3:50", "BMH"], ["", " ", " "],
         ["Nothing", " ", " "]),
        ("thursday", ["SE843", "8:00-8:50", "MSS"], ["CSE803", "9:00-10:50", "MAJ"], ["CSE837", "11:00-12:50", "BMH"],
         ["", " ", " "])
        ]

msse2 = [("sunday", ["", " ", " "], ["", " ", " "], ["", " ", " "],
         ["", " ", " "]),
         ("monday", ["", " ", " "], ["", " ", " "], ["", " ", " "],
          ["", " ", " "]),
        ("tuesday", ["MS1044", "11:00-12:50", "AK"], ["MS1041", "2:00-3:50", "NAT"], ["", " ", " "],
         ["", " ", " "]),
         ("wednesday", ["MS1044", "11:00-12:50", "AK"], ["MS1041", "2:00-3:50", "NAT"], ["", " ", " "],
          ["", " ", " "]),
         ("thursday", ["", " ", " "], ["", " ", " "], ["", " ", " "],
          ["", " ", " "])
        ]
sub2 = ["se206", "ge212", "cse211", "stat203", "cse201", "math204"]
day = ["sunday", "monday", "tuesday", "wednesday", "thursday", "friday", " saturday", "today", "tomorrow", "todays",
       "today\'s","tomorrows","tomorrow\'s","nextday"]
sub4 = ["cse403", "cse404", "se406", "bus405", "ge402", "cse403"]
sub6 = ["se605", "bus602", "se606", "ge603", "cse604", "cse601"]
sub8 = ["cse802", "se843", "cse803", "cse802", "cse837"]
mse2 = ["ms1044","ms1041"]
teacher = ["mzh", "ak", "ms", "mss", "nan", "nat", "bmh", "nat", "rs", "kkr", "sak", "cp", "tk", "kmr", "sh", "ia",
           "maj", "msi"]
pattern = [(["date", "sub", "time"], "teacher", ["who", "give", "tell", "show", "answer", "say", "suggest", "reply"]),
           (["date", "time", "teacher"], "sub", ["which","what", "what", "give", "tell", "show", "say", "suggest", "reply"]),
           (["sub", "time", "teacher"], "date", ["which", "what", "when", "give", "tell", "show", "say", "suggest", "reply"]),
           (["date", "sub", "teacher"], "time", ["when", "what", "which", "give", "tell", "show", "say", "suggest", "reply"]),
           (["date", "sub", "time", "sem"], "teacher",
            ["who", "give", "tell", "show", "answer", "say", "suggest", "reply"]),
           (["date", "time", "teacher", "sem"], "sub", ["which","what", "give", "tell", "show", "say", "suggest", "reply"]),
           (["sub", "time", "teacher", "sem"], "date", ["which","what", "when", "give", "tell", "show", "say", "suggest", "reply"]),
           (["date", "sub", "teacher", "sem"], "time", ["when","what","which", "give", "tell", "show", "say", "suggest", "reply"]),
           (["sub", "teacher"], "date,time",["when", "what", "which", "give", "tell", "show", "say", "suggest", "reply"]),
           (["time", "teacher"], "date,sub", ["which", "what", "when", "give", "tell", "show", "say", "suggest", "reply"]),
           (["sub", "time"], "date,teacher", ["who", "which", "what", "when", "give", "tell", "show", "say", "suggest", "reply"]),
           (["date", "teacher"], "sub,time", ["when", "which", "what", "when", "give", "classlist","classes","class","routine","routinelist""classsechedule", "tell", "show", "say", "suggest", "reply"]),
           (["date", "time"], "sub,teacher", ["who", "which", "what", "when", "give", "tell", "show", "say", "suggest", "reply"]),
           (["date", "sub"], "time,teacher", ["who", "which", "what","when", "give", "tell", "show", "say", "suggest", "reply"]),
           (["date", "sem"], "sub,time,teacher", ["who", "which", "what", "when", "give", "tell","classlist","classes","class","routine","routinelist""classsechedule", "show", "suggest", "say", "reply"]),
           (["sub"], "date,time,teacher", ["who", "which", "what", "when", "give", "tell","classlist","class","classes","classsechedule" ,"routine","routinelist", "suggest", "show", "say", "reply"]),
           (["time"], "date,sub,teacher", ["who", "which", "what", "when", "give", "tell","classlist","class","classes","classsechedule" , "suggest","routine","routinelist", "show", "say", "reply"]),
           (["teacher"], "date,sub,time", ["which", "what", "when", "give", "tell", "suggest","classlist","class","classes","classsechedule" ,"routine","routinelist", "show", "say", "reply"]),
           (["date"], "sub,time,teacher", ["who", "which", "what", "when", "give", "tell", "suggest","classlist","class","classes","classsechedule" ,"routine","routinelist", "show", "say", "reply"])
           ]

month = ['january', 'jan', 'february', 'feb', 'march', 'mar', 'april', 'apr', 'may', 'june', 'jun', 'july', 'jul',
         'august', 'aug',
         'september', 'sep', 'october', 'oct', 'november', 'nov', 'december', 'dec']
sem_dic = {'2': 'sem2', '4': 'sem4', '6': 'sem6', '8': 'sem8', 'second': 'sem2', 'fourth': 'sem4', 'sixth': 'sem6',
           'eight': 'sem8', '2nd': 'sem2', '4th': 'sem4', '6th': 'sem6', '8th': 'sem8','six':'sem6','four':'sem4','eighth':'sem8','msse2':'msse2'}
class_list = ['class','classes','classlist', 'classsechedule','routine','routinelist',]
lemmatiser = WordNetLemmatizer()

wordsFiltered = []
array_find = ''
query = []
table = []
answer = []
keywords = []
verb_or_Wh = []
date_array = []
increment = 0
increaser = 0
length = 0
mr = dateparser.parse('jan 12')
def processing(sent):
    sent = sent.lower()

    words = word_tokenize(sent)
    tagged = nltk.pos_tag(words)
    for w in words:
        wordsFiltered.append(w)
    global length
    length = len(tagged) - 1

    for item in tagged:

        if item[1][0] == 'V' and item[0] not in sub2:
            verb_or_Wh.append(lemmatiser.lemmatize(item[0], pos="v"))
        elif item[1][0] == 'W':
            verb_or_Wh.append(item[0])
        elif item[0] in class_list:
            verb_or_Wh.append(item[0])


def find_similarity():
    with open('similar.txt') as f:
        lines = f.readlines()
        for item in lines:
            str = item.split('|')
            search = str[0].split(',')
            count = 0
            for tr in search:
                new_str = tr.split(' ')
                for l in new_str:
                    for m in wordsFiltered:

                        if l.lower() == m or tr.lower() == m:
                            if count == 0:
                                pos = wordsFiltered.index(m)
                                wordsFiltered[pos] = str[1].lower().strip()
                                count = count + 1
                            else:
                                wordsFiltered.remove(m)


def clearVariables():
    wordsFiltered.clear()
    keywords.clear()
    query.clear()
    answer.clear()
    table.clear()
    verb_or_Wh.clear()
    date_array.clear()
    global increment
    global increaser
    global  length
    length = 0
    increment = 0
    increaser = 0
    array_find = ' '


def findsubject(wordsFiltered):
    global array_find
    for i in wordsFiltered:
        if i in sub2:
            query.append("sub")
            keywords.append(i)
            array_find = 'sem2'
        elif i in sub4:
            query.append("sub")
            keywords.append(i)
            array_find = 'sem4'
        elif i in sub6:
            query.append("sub")
            keywords.append(i)
            array_find = 'sem6'
        elif i in sub8:
            query.append("sub")
            keywords.append(i)
            array_find = 'sem8'

        elif i in mse2:
            query.append("sub")
            keywords.append(i)
            array_find = 'msse2'


def finddate(wordsFiltered):
    cnt = 0
    converted_date = ''

    for i in wordsFiltered:
        if i == 'next':

            pos = wordsFiltered.index(i)
            if wordsFiltered[pos + 1] == 'day':
                tomorrow = calendar.day_name[(date.today() + datetime.timedelta(1)).weekday()]
                keywords.append(tomorrow.lower())
                query.append('date')
        if i in day and cnt == 0:
            query.append('date')
            if i == "today" or i == 'today\'s' or i == 'todays':
                week_day = calendar.day_name[date.today().weekday()]
                keywords.append(week_day.lower())

            elif i == "tomorrow" or i == 'tomorrow\'s' or i == 'tomorrows' or i == 'nextday':

                tomorrow = calendar.day_name[(date.today() + datetime.timedelta(1)).weekday()]
                keywords.append(tomorrow.lower())
            else:
                keywords.append(i)
            cnt = cnt + 1


        else:
            """for w in wordsFiltered:"""
            if (i == 'on' or i == "date") and cnt == 0:

                indx = wordsFiltered.index(i)
                if indx + 3 <= len(wordsFiltered):
                    m = indx + 3
                else:
                    m = indx + (len(wordsFiltered) - indx)

                for t in range(indx + 1, m):
                    res = 0
                    new_date = []
                    for ch in wordsFiltered[t]:
                        if ch.isdigit() or not ch.isalpha():
                            new_date.append(ch)

                    if len(new_date) != 0:

                        my_date = new_date
                        dt = "".join(my_date)

                        if res == 0:
                            date_array.append(dt)
                        elif int(dt) >= 2018 or wordsFiltered[t - 1] in month:
                            date_array.append(dt)
                        new_date.clear()
                        res = res + 1

                    if wordsFiltered[t] in month:
                        date_array.append(wordsFiltered[t])
                        res = res + 1

                for t in date_array:
                    converted_date = converted_date + t + ' '

                tr = dateparser.parse(converted_date)

                if type(tr) is type(mr):
                    query.append("date")

                    keywords.append(calendar.day_name[tr.weekday()].lower())
                    cnt = cnt + 1


def findtime(wordsFiltered):
    for i in wordsFiltered:
        if i == 'at' or i == "time":
            count = 0
            t = 0
            indx = wordsFiltered.index(i)

            for t in range(indx + 1, indx + 2):
                for ch in wordsFiltered[t]:
                    if ch.isdigit() or ch == ':':
                        continue
                    else:
                        count = count + 1
                        break

            if count == 0:
                query.append("time")

                if wordsFiltered[t].find(":00") == -1:
                    wordsFiltered[t] = wordsFiltered[t] + ":00"

                    keywords.append(wordsFiltered[t])


def findteacherName(wordsFiltered):
    for i in wordsFiltered:
        if i in teacher:
            query.append("teacher")
            keywords.append(i)


def findsemester(wordsFiltered):
    global array_find
    if 'sem' in wordsFiltered:
        pos = wordsFiltered.index('sem')
        """query.append("sem")"""
        if wordsFiltered[pos - 1] in sem_dic.keys():
            array_find = sem_dic[wordsFiltered[pos - 1]]

        elif wordsFiltered[pos + 1] in sem_dic.keys():
            array_find = sem_dic[wordsFiltered[pos + 1]]


    elif 'semester' in wordsFiltered:
        pos = wordsFiltered.index('semester')
        """query.append("sem")"""
        if wordsFiltered[pos - 1] in sem_dic.keys():
            array_find = sem_dic[wordsFiltered[pos - 1]]

        elif wordsFiltered[pos + 1] in sem_dic.keys():
            array_find = sem_dic[wordsFiltered[pos + 1]]


def takeInput(reply):
    #print("Which semester?")
    #reply = input()
    reply = reply.lower()
    reply = reply.strip()
    new_ar = []
    new_words = word_tokenize(reply)
    for j in new_words:
        new_ar.append(j)
    if len(new_words) == 1:
        if new_words[0] in sem_dic.keys():
            global array_find
            array_find = sem_dic[reply]

    else:

        findsemester(new_words)


def matchPattern(query):
    for i in pattern:
        if i[0] == query:
            for j in verb_or_Wh:
                if j in i[2]:
                    answer.append(i[1])
                    """if len(query) == 1:
                        takeInput()"""
                    return True


def makeAnswerFor3():
    counter = 0
    result = ''
    if len(array_find) == 0:
        need_semester = True
        return "no semister"
       # takeInput()
    if array_find == 'sem2':
        ar = sem2
    elif array_find == 'sem4':
        ar = sem4
    elif array_find == 'sem6':
        ar = sem6
    elif array_find == 'sem8':
        ar = sem8
    elif array_find == 'msse2':
        ar = msse2

    if 'date' not in answer:
        count_matching = 0
        for t in ar:

            if t[0] in keywords:
                count_matching = count_matching + 1
                for j in t:

                    timer = j[1]
                    name = j[2]
                    pr = timer.split('-')
                    if j[0].lower() in keywords:
                        if timer in keywords:
                            result = "Course " + j[0] + " will be taken by " + name
                        elif name.lower() in keywords:

                            result = "Class " + j[0] + " will held on  " + timer
                        else:
                            if pr[0] in keywords:
                                result = "Class " + j[
                                    0] + " will held on  " + timer + ". And teacher's name is " + name
                            else:
                                """ ekhane jodi time vul thake tahole right time dekhabe"""
                                result = "You make a mistake on class time.Class " + j[
                                    0] + " will held on  " + timer + ". And teacher's name is " + name

                    elif timer in keywords or pr[0] in keywords:
                        if name.lower() in keywords and 'sub' not in answer:
                            result = "No class at " + keywords[1] + "  for course " + j[0] + ". But " + j[0] + \
                                     " will held at time " + pr[0] + \
                                     " on  " + t[0]
                        elif name.lower() in keywords and 'sub' in answer:
                            result = j[0] + ' class held at ' + pr[0]
                        elif 'sub' in answer:
                            result = "No class for " + keywords[2].upper() + " at " + pr[0] + ". But " + name + \
                                     " will take " + j[0] + " at " + pr[0]

                    elif name.lower() in keywords:
                        result = "You make a mistake on course name.On " + t[0] + " teacher " + name + \
                                 " will take course " + j[0]

        if result == '':
            global increaser
            increaser = counter
            if 'sub' in answer:
                keywords.remove(keywords[1])
                query.remove(query[1])
                print_message(ar, increaser)

            elif 'time' in answer:
                keywords.remove(keywords[2])
                query.remove(query[2])
                print_message(ar, increaser)
            elif 'teacher' in answer:
                keywords.remove(keywords[1])
                query.remove(query[1])
                print_message(ar, increaser)
            print_table(table)
        else:
            print(result)

    else:
        flag = False
        for t in ar:

            for j in t:
                timer = j[1]
                name = j[2]
                pr = timer.split('-')

                if j[0].lower() in keywords:

                    if timer in keywords:
                        if name.lower() in keywords:
                            result = t[0]
                        else:
                            result = "Opps, you make a mistake  writing teacher name for the course.Teacher " + name + \
                                     " take the class and it is " + t[0]

                    elif pr[0] in keywords:

                        if name.lower() in keywords:
                            result = " class for " + j[0] + " will held on " + t[0]

                        else:

                            result = "Opps, you make a mistake  writing teacher name for the course.Teacher " + name + \
                                     " take the class and it is " + t[0]

                    elif name.lower() in keywords:
                        result = name + " will take class at " + pr[0]

                    else:
                        print("No such day for class " + j[0] + " on time " + keywords[
                            1] + ".The schedule of this course-")
                        keywords.remove(keywords[1])
                        keywords.remove(keywords[1])
                        query.remove(query[1])
                        query.remove(query[1])
                        makeAnswerFor1()
                        flag = True
                        return

                elif timer in keywords or pr[0] in keywords:
                    if name.lower() in keywords:
                        result = " No class for course" + keywords[0] + ". But " + j[0] + " held at time " + pr[0] + \
                                 " and teacher is" + name

        if result == '' and flag == False:
            print(" No schedule for this class")
        if len(result) != 0:
            print(result)


def print_table(table):
    for r in table:
        for c in r:
            print(c)


def find_Next(ar, key, new_ar):
    indx = 0
    answer_table = []
    if key not in day:
        for j in ar:
            array = [j[1]] + [j[2]] + [j[3]] + [j[4]]
            for t in array:
                sub_name = t[0]
                timer = t[1]
                t_name = t[2]
                pr = timer.split('-')
                if sub_name.lower() in keywords:
                    answer_table.insert(indx, [j[0] + " ----> " + t[1] + " ----> " + t[2]])
                    indx = indx + 1
                elif timer in keywords or pr[0] in keywords:
                    answer_table.insert(indx, [j[0] + " ----> " + t[0] + " ----> " + t[2]])
                    indx = indx + 1

                elif t_name.lower() in keywords:
                    answer_table.insert(indx, [j[0] + " ----> " + t[0] + " ----> " + t[1]])
                    indx = indx + 1

    my_day = calendar.day_name[date.today().weekday()]
    next_day = []
    for i in range(1, 7):
        next_day.append(calendar.day_name[(date.today() + datetime.timedelta(days=i)).weekday()].lower())

    if len(answer_table) > 1:

        for j in range(0, 6):
            for i in answer_table:
                for c in i:
                    tr = c.split('---->')
                    for m in tr:
                        m = m.strip()

                        if m == next_day[j]:
                            table.insert(0, [c])
                            return 0

    else:
        for i in answer_table:
            for c in i:
                table.insert(0, [c])
                return 0


def print_message(ar, counter):
    if query[0] == 'date' and query[1] == 'sub':
        if counter == 0:
            print("No class for course", keywords[1].upper(), "on ", keywords[0], ". Next class - ")
            counter = counter + 1
        new_ar = ['date', 'time', 'teacher']
        find_Next(ar, keywords[1], new_ar)
    elif query[0] == 'date' and query[1] == 'time':
        if counter == 0:
            print("No class at ", keywords[1], "on", keywords[0], ". The next class  on this time -")
            counter = counter + 1
        new_ar = ['date', 'sub', 'teacher']
        find_Next(ar, keywords[1], new_ar)
    elif query[0] == 'date' and query[1] == 'teacher':
        if counter == 0:
            print("No class for ", keywords[1].upper(), " on ", keywords[0], ". The next class of ",
                  keywords[1].upper(), " -")
            counter = counter + 1
        new_ar = ['date', 'sub', 'time']
        find_Next(ar, keywords[1], new_ar)

    elif query[0] == 'sub' and query[1] == 'time':
        if counter == 0:
            print("Course", keywords[0].upper(), "will not happen at", keywords[1], ". The course time -")
            counter = counter + 1
            keywords.remove(keywords[1])
        createTableColumn3(0, table, ar)
    elif query[0] == 'sub' and query[1] == 'teacher':

        if counter == 0:
            print("Course ", keywords[0].upper(), " is not taken by ", keywords[1].upper(),
                  ". This course day, time and teacher - ")
            counter = counter + 1
            keywords.remove(keywords[1])
        createTableColumn3(0, table, ar)

    elif query[0] == 'time' and query[1] == 'teacher':
        if counter == 0:
            print("At time ", keywords[0], " teacher", keywords[1].upper(),
                  "do not take the class. The schedule of ", keywords[1].upper(), " -")
            counter = counter + 1
            keywords.remove(keywords[0])
        createTableColumn3(0, table, ar)
    global increaser
    increaser = counter
    "ei point e bug ase"


def createTableColumn2(indx, table, ar):
    for t in ar:
        new_ar = [t[1]] + [t[2]] + [t[3]] + [t[4]]
        if t[0] in keywords:
            for j in new_ar:

                sub_name = j[0]
                timer = j[1]
                t_name = j[2]
                pr = timer.split('-')
                if sub_name.lower() in keywords:
                    table.insert(indx, [t_name + " ----> " + timer])
                    indx = indx + 1
                elif timer in keywords or pr[0] in keywords:
                    table.insert(indx, [sub_name + " ----> " + t_name])
                    indx = indx + 1

                elif t_name.lower() in keywords:
                    table.insert(indx, [sub_name + " ----> " + timer])
                    indx = indx + 1




        else:

            for j in new_ar:
                sub_name = j[0]
                timer = j[1]
                t_name = j[2]
                pr = timer.split('-')
                if sub_name.lower() in keywords and t_name.lower() in keywords:

                    table.insert(indx, [t[0] + " ----> " + timer])
                    indx = indx + 1
                elif t_name.lower() in keywords and (timer in keywords or pr[0] in keywords):

                    table.insert(indx, [t[0] + " ----> " + sub_name])
                    indx = indx + 1
                elif sub_name.lower() in keywords and (timer in keywords or pr[0] in keywords):
                    table.insert(indx, [t[0] + " ----> " + t_name])
                    indx = indx + 1

    global increment
    if len(table) != 0:
        increment = indx + 1
    """if len(table) == 0:
        print_message(ar)"""
    return table


def createTableColumn3(indx, table, ar):
    for t in ar:
        new_ar = [t[1]] + [t[2]] + [t[3]] + [t[4]]
        if t[0] in keywords:
            for j in new_ar:
                if len(j[0]) != 0:
                    table.insert(indx, [j[0] + " ----> " + j[1] + " ----> " + j[2]])
                    indx = indx + 1

        else:
            for j in new_ar:
                sub_name = j[0]
                timer = j[1]
                t_name = j[2]
                pr = timer.split('-')
                if sub_name.lower() in keywords:
                    table.insert(indx, [t[0] + " ----> " + j[1] + " ----> " + j[2]])
                    indx = indx + 1
                elif timer in keywords or pr[0] in keywords:
                    table.insert(indx, [t[0] + " ----> " + j[0] + " ----> " + j[2]])
                    indx = indx + 1

                elif t_name.lower() in keywords:
                    table.insert(indx, [t[0] + " ----> " + j[0] + " ----> " + j[1]])
                    indx = indx + 1
    global increment
    if len(table) != 0:
        increment = indx

    return table


def makeAnswerFor2():
    global table
    indx = 0
    global increment
    increment = indx
    global increaser
    counter = 0
    increaser = counter
    if array_find == 'sem2':
        table = createTableColumn2(increment, table, sem2)
        if len(table) == 0:
            print_message(sem2)

    elif array_find == 'sem4':
        table = createTableColumn2(increment, table, sem4)
        if len(table) == 0:
            print_message(sem4)
    elif array_find == 'sem6':
        table = createTableColumn2(increment, table, sem6)
        if len(table) == 0:
            print_message(sem6)
    elif array_find == 'sem8':
        table = createTableColumn2(increment, table, sem8)
        if len(table) == 0:
            print_message(sem8)
    elif array_find == 'msse2':
        table = createTableColumn2(increment, table, msse2)
        if len(table) == 0:
            print_message(msse2)
    else:
        table = createTableColumn2(increment, table, sem2)
        table = createTableColumn2(increment, table, sem4)
        table = createTableColumn2(increment, table, sem6)
        table = createTableColumn2(increment, table, sem8)
        table = createTableColumn2(increment, table, msse2)

    if increment == 0:
        if len(array_find) == 0:
            print_message(sem2, increaser)
            print_message(sem4, increaser)
            print_message(sem6, increaser)
            print_message(sem8, increaser)
            print_message(msse2, increaser)

        elif array_find == 'sem2':
            print_message(sem2, increaser)
        elif array_find == 'sem4':
            print_message(sem4, increaser)
        elif array_find == 'sem6':
            print_message(sem6, increaser)
        elif array_find == 'sem8':
            print_message(sem8, increaser)

        elif array_find == 'msse2':
            print_message(msse2, increaser)

        """print("Sorry i can not understand your question. Can you repeat the question?")"""

    if len(table) == 0:
        print("sorry, i think u miss some words to search")
    else:
        print_table(table)


def makeAnswerFor1():
    global table
    indx = 0
    global increment
    increment = indx
    if len(array_find) == 0:
        need_semester = True
        return "which semester?"
    if array_find == 'sem2':
        table = createTableColumn3(increment, table, sem2)
    elif array_find == 'sem4':
        table = createTableColumn3(increment, table, sem4)
    elif array_find == 'sem6':
        table = createTableColumn3(increment, table, sem6)
    elif array_find == 'sem8':
        table = createTableColumn3(increment, table, sem8)
    elif array_find == 'msse2':
        table = createTableColumn3(increment, table, msse2)

    if increment == 0:
        print("Sorry i can not understand your question. Can you repeat the question?")
    else:
        print_table(table)

def execute(sent):
    if need_semester:
        takeInput(sent)
    processing(sent)
    find_similarity()
    finddate(wordsFiltered)
    findsubject(wordsFiltered)
    findtime(wordsFiltered)
    findteacherName(wordsFiltered)
    findsemester(wordsFiltered)

    if matchPattern(query) == True:

        if len(keywords) == 3:
            makeAnswerFor3()

        elif len(keywords) == 2:
            makeAnswerFor2()

        elif len(keywords) == 1:

            makeAnswerFor1()

    else:
        print("Sorry i can not understand your question. Can you repeat the question?")
    clearVariables()

execute("give the classlist of nan today")
