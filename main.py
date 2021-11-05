#Authors: Hatem Mamdoh, Hussien Ashraf
#IDs: 20170085, 2017093

import re
import operator
import json
from PyQt5 import QtWidgets
import sys
from itertools import islice

from ui import Ui_MainWindow

#ui
app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(MainWindow)
MainWindow.show()

dictionary = {}
temp_prob_dic = {}
temp_dic = {}


print("Please load or train the program")

#load the dictionary from pre-trained file
def load():
    global dictionary
    with open('output.txt', 'r', encoding="utf8") as file:
        dictionary = json.load(file)
    print("Loaded")

#train the dictionary on the fiven text file
def train():
    global temp_prob_dic
    global temp_dic
    global dictionary
    f = open("Text 1.txt", "r", encoding="utf8")
    the_text = f.read()
    print("Started Training")
    split = re.split('[\\s\.]+', the_text)  #separate each word

    #loop across the entire words
    for i in range(len(split)-2):
        temp = split[i] + " " + split[i + 1]
        if temp in dictionary:  #check if word already inside dictionary
            values = dictionary[temp]
            if split[i+2] in values:
                dictionary[temp][split[i + 2]] += 1
            else:
                dictionary[temp][split[i+2]] = 1

        else:
            new_dect = {}
            new_dect [split[i+2]] = 1
            dictionary[temp] = new_dect
    print("Finished training")
    #writes the dictionary to file so it doesn''t need to train again
    with open('output.txt', 'w', encoding="utf8") as file:
        file.write(json.dumps(dictionary))

#another slower version of train UNUSED
def train2():
    global dictionary

    f = open("Text 1.txt", "r", encoding="utf8")
    the_text = f.read()
    print("Started Training")
    split = re.split('[\\s\.]+', the_text)
    tokensArray = []

    for i in range(len(split) - 1):
        temp = split[i] + " " + split[i + 1]
        tokensArray.append(temp)
    unique = set(split)
    unique = list(filter(None, unique)) #remove any existing white spaces
    unique_sentences = set(tokensArray)
    for i in unique_sentences:
        temp_prob_dic = {}
        words = re.findall("{} \w+".format(i), the_text) #gets all third words that came after the two words in (i)
        if len(words) != 0:
            count1 = calculate_occurence(the_text, i)
            for j in words:
                splitted = re.split('[\\s\.]+', j) #split words on space
                last_word = splitted[-1] #get the last word only

                count2 = calculate_occurence(the_text, i + " " + last_word)
                temp_prob_dic[last_word] = count2 / count1 #calculate probability of the third word occuring after the two words

        dictionary[i] = temp_prob_dic
    print("Finished training")

    with open('output.txt', 'w', encoding="utf8") as file:
        file.write(json.dumps(dictionary))

#calculates the number of occuranc of string1 in text
def calculate_occurence(text, string1):
    result = re.findall(string1, text)
    return len(result)

#used to display the expecteed word in the gui
view_array = []

#finds the next expected words given the text
def search(text):
    global view_array
    global dictionary
    view_array.clear()
    if text in dictionary:
        A = dict(sorted(dictionary[text].items(), key=operator.itemgetter(1), reverse=True)[:5]) #sort based on highest probability or occurance
        #display maximum 5 highest
        if (len(A) <= 5):
            for i in A:
                view_array.append(i)
        else:
            counter = 0
            for i in A:
                counter += 1
                if counter >= 5:
                    break
                view_array.append(i)

def slice_and_make_string(array):
    ui.listWidget.clear()
    global view_array
    res = list(islice(reversed(array), 0, 2))
    res.reverse()
    search(res[0] + " " + res[1])


def toprint():
    global view_array
    text = ui.lineEdit.text()
    val = re.split(" ", text)
    val = list(filter(None, val))
    if (len(val) >= 2):
            slice_and_make_string(val)
            ui.listWidget.addItems(view_array)
    else:
        ui.listWidget.clear()


def searchUI():
    global view_array
    load()
    text = ui.lineEdit.text()
    search(text)
    ui.listWidget.addItems(view_array)


ui.pushButton.clicked.connect(
    load
)
ui.pushButton_2.clicked.connect(
    train
)
ui.lineEdit.textChanged.connect(
    toprint
)


def onClicked(item):
    if item is not None:
        lineText = ui.lineEdit.text()
        toShow = lineText + item.text() + " "
        ui.lineEdit.setText(toShow)


ui.listWidget.itemDoubleClicked.connect(
    onClicked
)

sys.exit(app.exec_())
