# -*- coding: utf-8 -*-
"""
Created on Sat Apr 24 05:34:34 2021
CPU sheduler project
"""


import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np
import sys 
import os

def resource_path(relative_path):
     """Function that allows GUI images to be built into the exe."""
     if hasattr(sys, '_MEIPASS'):
         return os.path.join(sys._MEIPASS, relative_path)
     return os.path.join(os.path.abspath("."), relative_path)

class Queue:
    """Class created to assist the RR algorithm"""
    def __init__(self,l=None):
        if(l == None):
            self.q=[]
        else:
            self.q = list(l)

    def __str__(self):
        return str(self.q)
    def __repr__(self):
        return self.q

    def push(self,elem):
        self.q.append(elem)

    def pop(self):
        temp = self.q[0]
        self.q = self.q[1:]
        return temp

    def empty(self):
        if(len(self.q) == 0): return 1
        return 0 


class SJF(object):
    """SJF scheduler implementation and GUI."""
    def fig_init(self, processes_name, total_burst):
        
        #Declaring a figure
        self.fig, self.ax = plt.subplots()  
        self.processes_name= processes_name

        #Setting x-axis and y-axis limits
        self.ax.set_ylim(0, len(processes_name))
        self.ax.set_xlim(0, total_burst)

        #Labels 
        self.ax.set_ylabel('Processes')
        self.ax.set_xlabel('Time Taken by Each Process')

        #Setting y-axis ticks
        ytick = [(i + 1) * 10 for i in range(len(processes_name) + 1)]
        self.ax.set_xticks(np.arange(0, total_burst + 1, 1))
        self.ax.set_yticks(ytick)

        self.ax.grid(axis='x')

    def draw(self, name, start_time, end_time):

        no = int(name[1:])
        name = name.title()
        colors = ['blue','#1f77b4','#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
          '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf', '#1f77b4','#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
          '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf', 'blue','#1f77b4','#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
          '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf', '#1f77b4','#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
          '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']

        # Declearing a bar in the schedule
        
        self.ax.broken_barh([(start_time, end_time - start_time)], (0,8), facecolors=colors[no])

        for _ in range(0, len(self.processes_name)):
            x = start_time + (end_time-start_time)/2
            y = 4
            s = name[0:]
            self.ax.text(x, y, s=s, ha='center',va='bottom', fontsize =10, fontweight = "bold")

        self.ax.spines['left'].set_visible(False)
        self.ax.spines['bottom'].set_visible(False)
        self.ax.spines['top'].set_visible(False)
        self.ax.spines['right'].set_visible(False)
        self.ax.set_axisbelow(True) 


    def swapPositions(self,list, pos1, pos2):
        list[pos1], list[pos2] = list[pos2], list[pos1]
        return list

    def get_min_pos(self,list):
        Min = 0
        for x in range(len(list)):
            Min = list[x]
            if Min > 0:
                break

        for x in range(len(list)):
            for y in range(x + 1, len(list)):
                if (list[y] < Min and list[y] > 0):
                    Min = list[y]
        return Min

    def sjf(self,processesNames,burstTime,arrivalTime,numberProcesses,Preemptive):
        self.fig_init(processesNames, sum(burstTime) + 10 + max(arrivalTime))
        last_x = 0
        flag = 0
        newBurstList = []
        newProcessesList = []
        arrivedList = []
        avgWaitingTime = []
        sumAvgTime = 0
        
        if not (Preemptive):
            # Sorting based on arrival time
            for x in range(numberProcesses):
                for y in range(x + 1, numberProcesses):
                    if arrivalTime[x] > arrivalTime[y]:
                        self.swapPositions(arrivalTime, x, y)
                        self.swapPositions(burstTime, x, y)
                        self.swapPositions(processesNames, x, y)
                    elif arrivalTime[x] == arrivalTime[y]:
                        if burstTime[x] > burstTime[y]:
                            self.swapPositions(burstTime, x, y)
                            self.swapPositions(processesNames, x, y)
            # Graphing the processes
            for z in range(numberProcesses):
                for count in range(numberProcesses):
                    if last_x >= arrivalTime[count]:
                        flag = 1
                        arrivedList.append(arrivalTime[count])
                        newBurstList.append(burstTime[count])
                        newProcessesList.append(processesNames[count])
                if sum(newBurstList) == 0:
                    flag = 0
                if (flag):
                    min_value = self.get_min_pos(newBurstList)
                    minIndex = newBurstList.index(min_value)
                    self.draw(newProcessesList[minIndex], last_x, last_x + newBurstList[minIndex])
                    last_x = last_x + newBurstList[minIndex]
                    flag = 0
                    index_of_sepec_process = processesNames.index(newProcessesList[minIndex])
                    avgWaitingTime.append(last_x - arrivalTime[index_of_sepec_process]
                                            - burstTime[index_of_sepec_process])
                    burstTime[index_of_sepec_process] = 0
                elif not (flag):
                    if last_x < arrivalTime[z]:
                        self.draw(processesNames[z], arrivalTime[z], arrivalTime[z] + burstTime[z])
                        last_x = arrivalTime[z] + burstTime[z]
                        burstTime[z] = 0
                    else:
                        self.draw(processesNames[z], last_x, last_x + burstTime[z])
                        last_x = last_x + burstTime[z]
                        avgWaitingTime.append(last_x - arrivalTime[z]
                                                - burstTime[z])
                        burstTime[z] = 0
                newBurstList = []
                newProcessesList = []
                arrivedList = []

            sumAvgTime = sum(avgWaitingTime) / numberProcesses

        elif Preemptive:
            # Sorting by arrival time
            for x in range(numberProcesses):
                for y in range(x + 1, numberProcesses):
                    if arrivalTime[x] > arrivalTime[y]:
                        self.swapPositions(arrivalTime, x, y)
                        self.swapPositions(burstTime, x, y)
                        self.swapPositions(processesNames, x, y)
                    elif arrivalTime[x] == arrivalTime[y]:
                        if burstTime[x] > burstTime[y]:
                            self.swapPositions(burstTime, x, y)
                            self.swapPositions(processesNames, x, y)
            
            # Printing all until final arrival time
           
            for i in range(numberProcesses):
                arrivedList.append(arrivalTime[i])
                newBurstList.append(burstTime[i])
                newProcessesList.append(processesNames[i])
                while (1):
                    min_value = self.get_min_pos(newBurstList)
                    minIndex = newBurstList.index(min_value)
                    index_of_sepec_process = processesNames.index(newProcessesList[minIndex])
                    if i != len(arrivalTime) - 1:
                        if last_x < arrivalTime[i]:
                            if arrivalTime[i + 1] > (arrivalTime[i] + newBurstList[minIndex]):
                                self.draw(newProcessesList[minIndex], arrivalTime[i], arrivalTime[i] +
                                          newBurstList[minIndex])
                                last_x = arrivalTime[i] + newBurstList[minIndex]
                                newBurstList[minIndex] = 0
                            else:
                                self.draw(newProcessesList[minIndex], arrivalTime[i],
                                          arrivalTime[i + 1])
                                last_x = arrivalTime[i + 1]
                                newBurstList[minIndex] = newBurstList[minIndex] - (
                                            last_x - arrivalTime[i])
                                if newBurstList[minIndex] == 0:
                                    avgWaitingTime.append(last_x - arrivalTime[index_of_sepec_process]
                                                            - burstTime[index_of_sepec_process])

                        else:
                            if arrivalTime[i + 1] > (last_x + newBurstList[minIndex]):
                                self.draw(newProcessesList[minIndex], last_x, last_x + newBurstList[minIndex])
                                last_x = last_x + newBurstList[minIndex]
                                newBurstList[minIndex] = 0
                                avgWaitingTime.append(last_x - arrivalTime[index_of_sepec_process]
                                                        - burstTime[index_of_sepec_process])
                            else:
                                self.draw(newProcessesList[minIndex], last_x, arrivalTime[i + 1])
                                newBurstList[minIndex] = newBurstList[minIndex] - (
                                            arrivalTime[i + 1] - last_x)
                                last_x = arrivalTime[i + 1]
                                if newBurstList[minIndex] == 0:
                                    avgWaitingTime.append(last_x - arrivalTime[index_of_sepec_process]
                                                            - burstTime[index_of_sepec_process])

                    elif i == len(arrivalTime) - 1:
                        if last_x < arrivalTime[i]:
                            self.draw(newProcessesList[minIndex], arrivalTime[i], arrivalTime[i] +
                                      newBurstList[minIndex])
                            last_x = arrivalTime[i] + newBurstList[minIndex]
                            newBurstList[minIndex] = 0
                        else:
                            self.draw(newProcessesList[minIndex], last_x, last_x + newBurstList[minIndex])
                            last_x = last_x + newBurstList[minIndex]
                            newBurstList[minIndex] = 0
                            avgWaitingTime.append(last_x - arrivalTime[index_of_sepec_process]
                                                    - burstTime[index_of_sepec_process])
                    if i == numberProcesses - 1:
                        break

                    elif (arrivalTime[i + 1] - last_x) == 0 or sum(newBurstList) == 0:
                        break

                # Sorting by burst time
            for x in range(numberProcesses):
                for y in range(x + 1, numberProcesses):
                    if newBurstList[x] > newBurstList[y]:
                        self.swapPositions(newBurstList, x, y)
                        self.swapPositions(arrivedList, x, y)
                        self.swapPositions(newProcessesList, x, y)
                    elif newBurstList[x] == newBurstList[y]:
                        if arrivedList[x] > arrivedList[y]:
                            self.swapPositions(arrivedList, x, y)
                            self.swapPositions(newProcessesList, x, y)
            # Drawing after final arrival time

            for i in range(numberProcesses):
                if newBurstList[i] > 0:
                    self.draw(newProcessesList[i], last_x, last_x + newBurstList[i])
                    last_x = last_x + newBurstList[i]
                    index_of_sepec_process = processesNames.index(newProcessesList[i])
                    avgWaitingTime.append(last_x - arrivalTime[index_of_sepec_process]
                                            - burstTime[index_of_sepec_process])

            sumAvgTime = sum(avgWaitingTime) / numberProcesses

        red_patch = mpatches.Patch(label="The Average Waiting Time is: {}".format(sumAvgTime), fill=False)
        plt.legend(handles=[red_patch])
        plt.show()  

    def click(self):
            """Function that connects values obtained by GUI to sorting algorithm."""
            numberOfProcesses = int(self.textEdit_3.toPlainText())
            value_of_textedit_2 = self.textEdit_2.toPlainText()
            arrivalTime = value_of_textedit_2.splitlines()
            value_of_textedit = self.textEdit.toPlainText()
            burstTime = value_of_textedit.splitlines()
            processesNames = []
            i = 0

            for i in range(numberOfProcesses):
                arrivalTime[i] = float(arrivalTime[i])
                burstTime[i] = float(burstTime[i])
                processesNames.append("p" + str(i + 1))
            Preemptive = self.radioButton.isChecked()
            
            self.sjf(processesNames, burstTime, arrivalTime, numberOfProcesses, Preemptive)
               
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(876, 866)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("bigger.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        resource_path("bigger.png")
        MainWindow.setWindowIcon(icon)
        MainWindow.setAutoFillBackground(False)
        MainWindow.setStyleSheet("background-color: white;")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.radioButton = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButton.setGeometry(QtCore.QRect(490, 170, 301, 31))
        self.radioButton.setStyleSheet("\n"
"font: 12pt \"Montserrat\"; font-weight: bold; color: black;")
        self.radioButton.setObjectName("radioButton")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(490, 250, 411, 51))
        self.label_4.setAutoFillBackground(False)
        self.label_4.setStyleSheet("font: 12pt \"Montserrat\"; color: black; font-weight: bold;")
        self.label_4.setObjectName("label_4")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(90, 250, 301, 51))
        self.label_3.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.label_3.setAutoFillBackground(False)
        self.label_3.setStyleSheet("font: 12pt \"Montserrat\"; color: black; font-weight: bold;")
        self.label_3.setObjectName("label_3")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(90, 130, 231, 101))
        self.label_5.setAutoFillBackground(False)
        self.label_5.setStyleSheet("font: 12pt \"Montserrat\"; color: black; font-weight: bold;")
        self.label_5.setObjectName("label_5")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(150, 40, 651, 101))
        self.label.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.label.setAutoFillBackground(False)
        self.label.setStyleSheet("font: 16pt \"Montserrat\"; color: black ; font-weight: bold;\n"
" font-weight:bold;")
        self.label.setObjectName("label")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(290, 730, 271, 91))
        self.pushButton.setStyleSheet("font: 14pt \"Montserrat\";  font-weight: bold; color:#FF5757;  font-size: 14;")
        self.pushButton.setObjectName("pushButton")
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(490, 310, 291, 371))
        self.textEdit.setStyleSheet("border: 2px  solid black; font: 75 20pt")
        self.textEdit.setObjectName("textEdit")
        self.textEdit_2 = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit_2.setGeometry(QtCore.QRect(90, 310, 291, 371))
        self.textEdit_2.setStyleSheet("border: 2px  solid black; font: 75 20pt")
        self.textEdit_2.setObjectName("textEdit_2")
        self.textEdit_3 = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit_3.setGeometry(QtCore.QRect(330, 150, 91, 61))
        self.textEdit_3.setStyleSheet("border: 2px  solid black; font: 75 20pt")
        self.textEdit_3.setObjectName("textEdit_3")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        
        #Connecting to the Run Button 
        self.pushButton.clicked.connect(self.click)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "CPU Job Scheduler"))
        self.radioButton.setText(_translate("MainWindow", "Preemptive or not?"))
        self.label_4.setText(_translate("MainWindow", "Burst Time of Each Process"))
        self.label_3.setText(_translate("MainWindow", "Arrival time of Each Process"))
        self.label_5.setText(_translate("MainWindow", "Number of Processes"))
        self.label.setText(_translate("MainWindow", "PLEASE ENTER THE FOLLOWING INPUTS:"))
        self.pushButton.setText(_translate("MainWindow", "RUN"))


class Queue:
    """Class created to assist the RR algorithm"""
    def __init__(self,l=None):
        if(l == None):
            self.q=[]
        else:
            self.q = list(l)

    def __str__(self):
        return str(self.q)
    def __repr__(self):
        return self.q

    def push(self,elem):
        self.q.append(elem)

    def pop(self):
        temp = self.q[0]
        self.q = self.q[1:]
        return temp

    def empty(self):
        if(len(self.q) == 0): return 1
        return 0 

class rr(object):
    """RR scheduler algorithm implementation and GUI."""
        
    def fig_init(self, processes_name, total_burst):
        
        #Declaring a figure
        self.fig, self.ax = plt.subplots()  
        self.processes_name= processes_name

        #Setting x-axis and y-axis limits
        self.ax.set_ylim(0, len(processes_name))
        self.ax.set_xlim(0, total_burst)

        #Labels 
        self.ax.set_ylabel('Processes')
        self.ax.set_xlabel('Time Taken by Each Process')

        #Setting y-axis ticks
        ytick = [(i + 1) * 10 for i in range(len(processes_name) + 1)]
        self.ax.set_xticks(np.arange(0, total_burst + 1, 1))
        self.ax.set_yticks(ytick)
        self.ax.grid(axis='x')
        
    def draw(self, name, start_time, end_time):
        no = int(name[1:])
        name = name.title()
        colors = ['blue','#1f77b4','#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
          '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf', '#1f77b4','#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
          '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf', 'blue','#1f77b4','#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
          '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf', '#1f77b4','#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
          '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
        
        self.ax.broken_barh([(start_time, end_time - start_time)], (0,8), facecolors=colors[no])
        for _ in range(0, len(self.processes_name)):
            x = start_time + (end_time-start_time)/2
            y = 4
            s = name[0:]
            self.ax.text(x, y, s=s, ha='center',va='bottom', fontsize =10, fontweight = "bold")

        self.ax.spines['left'].set_visible(False)
        self.ax.spines['bottom'].set_visible(False)
        self.ax.spines['top'].set_visible(False)
        self.ax.spines['right'].set_visible(False)
        self.ax.set_axisbelow(True) 

    def Round_Robin(self, processesNames, burstTime, arrivalTime, numberProcesses, quantum):
        turnAround = [i for i in range(len(processesNames))]
        total = sum(burstTime) + 10 + max(arrivalTime)
        self.fig_init(processesNames, total)

        # first step of sorting 
        for i in range(numberProcesses):
            swapping = False
            for j in range(numberProcesses - i - 1):
                if (arrivalTime[j] > arrivalTime[j + 1]):
                    arrivalTime[j], arrivalTime[j + 1] = arrivalTime[j + 1], arrivalTime[j]
                    processesNames[j], processesNames[j + 1] = processesNames[j + 1], processesNames[j]
                    burstTime[j], burstTime[j + 1] = burstTime[j + 1], burstTime[j]
                    swapping = True

                elif (arrivalTime[j] == arrivalTime[j + 1]):
                    if (int(processesNames[j][1:]) > int(processesNames[j + 1][1:])):
                        arrivalTime[j], arrivalTime[j + 1] = arrivalTime[j + 1], arrivalTime[j]
                        processesNames[j], processesNames[j + 1] = processesNames[j + 1], processesNames[j]
                        burstTime[j], burstTime[j + 1] = burstTime[j + 1], burstTime[j]
                        swapped = True
            if (swapping == False): break

        burstCopy = list(burstTime)
        termination =0
        i=0
        queue = Queue()

        flag=[0 for i in range (numberProcesses)]
        firstTime=1
        while(termination < numberProcesses):
            last_x = arrivalTime[i]
            queue.push([processesNames[i], burstTime[i]])

            while(not queue.empty()):

                temp = queue.pop()
                if(temp[1] <= quantum):
                    duration = min(temp[1],quantum)
                    self.draw(temp[0] , last_x, last_x +duration )
                    old_x=last_x
                    last_x=last_x+duration
                    turnAround[ processesNames.index(temp[0])] = last_x-arrivalTime[ processesNames.index(temp[0])]
                    termination=termination+1
                    flag[ processesNames.index(temp[0]) ] =1
                    if (firstTime):
                        for it in range(1, len(arrivalTime)):
                            if (arrivalTime[it] > last_x): 
                                break
                            if (arrivalTime[it] >= old_x and arrivalTime[it] <= last_x and temp[0] !=
                                    processesNames[it]):
                                queue.push(
                                    [processesNames[it], burstTime[it]])
                    else:
                        for it in range(len(arrivalTime)):
                            if (arrivalTime[it] > last_x): 
                                break
                            if (arrivalTime[it] > old_x and arrivalTime[it] <= last_x and temp[0] !=
                                    processesNames[it]):
                                queue.push(
                                    [processesNames[it], burstTime[it]])

                else:
                    duration = quantum
                    self.draw(temp[0] , last_x, last_x +duration)
                    old_x=last_x
                    last_x=last_x+duration
                    temp[1] = temp[1]-quantum

                    if (firstTime):
                        for it in range(1,len(arrivalTime)):
                            if (arrivalTime[it] > last_x): break
                            if (arrivalTime[it] >= old_x and arrivalTime[it] <= last_x and temp[0] != processesNames[it]):
                                queue.push(
                                    [processesNames[it], burstTime[it]])
                    else:
                        for it in range(len(arrivalTime)):
                            if (arrivalTime[it] > last_x): 
                                break
                            if (arrivalTime[it] > old_x and arrivalTime[it] <= last_x and temp[0] != processesNames[it]):
                                queue.push(
                                    [processesNames[it], burstTime[it]])

                    queue.push(temp)
                    firstTime = 0

            # If the queue is empty
            if (termination == numberProcesses): 
                break
            else:
                for f in range(numberProcesses):
                    if(flag[f] == 0):
                        i=f
                        break

        waiting = []
        for i in range(len(processesNames)):
            waiting.append(turnAround[i] - burstCopy[i])

        avgWaitingTime = sum(waiting) / len(waiting) 

        red_patch = mpatches.Patch(label="The Average Waiting Time is: {}".format(avgWaitingTime), fill=False)
        plt.legend(handles=[red_patch])
        plt.show()

    def click(self):
        
            numberProcesses = int(self.textEdit_4.toPlainText())

            value_of_textedit_2 = self.textEdit_2.toPlainText()
            arrivalTime = value_of_textedit_2.splitlines()

            value_of_textedit_3 = self.textEdit_3.toPlainText()
            burstTime = value_of_textedit_3.splitlines()

            quantum = float(self.textEdit_5.toPlainText())
            processesNames = []
            i = 0
            for i in range(numberProcesses):
                 arrivalTime[i] = float(arrivalTime[i])
                 burstTime[i] = float(burstTime[i])
                 processesNames.append("p" + str(i + 1))
            self.Round_Robin(processesNames, burstTime, arrivalTime, numberProcesses, quantum)
                
                
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(828, 900)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("scheduler (1).png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setAutoFillBackground(False)
        MainWindow.setStyleSheet("background-color: white;")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(50, 160, 231, 101))
        self.label_5.setAutoFillBackground(False)
        self.label_5.setStyleSheet("font: 12pt \"Montserrat\"; color: black; font-weight: bold;")
        self.label_5.setObjectName("label_5")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(110, 60, 651, 101))
        self.label.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.label.setAutoFillBackground(False)
        self.label.setStyleSheet("font: 16pt \"Montserrat\"; color: black ; font-weight: bold;\n"
" font-weight:bold;")
        self.label.setObjectName("label")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(50, 270, 341, 71))
        self.label_3.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.label_3.setAutoFillBackground(False)
        self.label_3.setStyleSheet("font: 12pt \"Montserrat\"; color: black; font-weight: bold;")
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(440, 280, 411, 51))
        self.label_4.setAutoFillBackground(False)
        self.label_4.setStyleSheet("font: 12pt \"Montserrat\"; color: black; font-weight: bold;")
        self.label_4.setObjectName("label_4")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(450, 160, 111, 101))
        self.label_6.setAutoFillBackground(False)
        self.label_6.setStyleSheet("font: 12pt \"Montserrat\"; color: black; font-weight: bold;")
        self.label_6.setObjectName("label_6")
        self.textEdit_2 = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit_2.setGeometry(QtCore.QRect(50, 340, 291, 371))
        self.textEdit_2.setStyleSheet("border: 2px  solid black; font: 75 20pt")
        self.textEdit_2.setObjectName("textEdit_2")
        self.textEdit_3 = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit_3.setGeometry(QtCore.QRect(440, 340, 291, 371))
        self.textEdit_3.setStyleSheet("border: 2px  solid black; font: 75 20pt")
        self.textEdit_3.setObjectName("textEdit_3")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(260, 750, 271, 91))
        self.pushButton.setStyleSheet("font: 14pt \"Montserrat\";  font-weight: bold; color:#FF5757;  font-size: 14;")
        self.pushButton.setObjectName("pushButton")
        self.textEdit_4 = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit_4.setGeometry(QtCore.QRect(290, 180, 91, 61))
        self.textEdit_4.setStyleSheet("border: 2px  solid black; font: 75 20pt")
        self.textEdit_4.setObjectName("textEdit_4")
        self.textEdit_5 = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit_5.setGeometry(QtCore.QRect(570, 180, 91, 61))
        self.textEdit_5.setStyleSheet("border: 2px  solid black; font: 75 20pt")
        self.textEdit_5.setObjectName("textEdit_5")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        
        #Connecting to the Run Button 
        self.pushButton.clicked.connect(self.click)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "CPU Job Scheduler"))
        self.label_5.setText(_translate("MainWindow", "Number of Processes"))
        self.label.setText(_translate("MainWindow", "PLEASE ENTER THE FOLLOWING INPUTS:"))
        self.label_3.setText(_translate("MainWindow", "Arrival time of Each Process"))
        self.label_4.setText(_translate("MainWindow", "Burst Time of Each Process"))
        self.label_6.setText(_translate("MainWindow", "Quantum"))
        self.pushButton.setText(_translate("MainWindow", "RUN"))



class FCFS(object):
    """FCFS scheduler algorithm implementation and GUI."""
    def fig_init(self, processes_name, total_burst):
        
        #Declaring a figure
        self.fig, self.ax = plt.subplots()  # must be global
        self.processes_name= processes_name

        #Setting x-axis and y-axis limits
        self.ax.set_ylim(0, len(processes_name))
        self.ax.set_xlim(0, total_burst)
        #Labels 
        self.ax.set_ylabel('Processes')
        self.ax.set_xlabel('Time Taken by Each Process')

        #Setting y-axis ticks
        ytick = [(i + 1) * 10 for i in range(len(processes_name) + 1)]

        self.ax.set_xticks(np.arange(0, total_burst + 1, 1))
        self.ax.set_yticks(ytick)
        ######self.ax.set_yticklabels(["self.processes_name"," "," "," "])
        #self.ax.grid(True)
        self.ax.grid(axis='x')
        
    def draw(self, name, start_time, end_time):
        no = int(name[1:])
        name = name.title()
        colors = ['blue','#1f77b4','#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
          '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf', '#1f77b4','#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
          '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
        color = []

        for i in range(0,len(self.processes_name)+1):
            
            color = colors[i]
   
        # Declearing a bar in the schedule
        #self.ax.broken_barh([(start_time, end_time - start_time)], ((no * 10) - 4, 7), facecolors=('tab:blue'))
        
        self.ax.broken_barh([(start_time, end_time - start_time)], (0,8), facecolors=colors[no])
        for i in range(0, len(self.processes_name)):
            x = start_time + (end_time-start_time)/2
            y = 4
            s = name[0:]
            self.ax.text(x, y, s=s, ha='center',va='bottom', fontsize =10, fontweight = "bold")
        self.ax.spines['left'].set_visible(False)
        self.ax.spines['bottom'].set_visible(False)
        self.ax.spines['top'].set_visible(False)
        self.ax.spines['right'].set_visible(False)
        self.ax.set_axisbelow(True) 
    def sort(self,arrival_time, process_name, burst_time):
        for i in range(len(arrival_time)):
            swapped = False
            for j in range(len(arrival_time) - i - 1):
                if (arrival_time[j] > arrival_time[j + 1]):
                    arrival_time[j], arrival_time[j + 1] = arrival_time[j + 1], arrival_time[j]
                    process_name[j], process_name[j + 1] = process_name[j + 1], process_name[j]
                    burst_time[j], burst_time[j + 1] = burst_time[j + 1], burst_time[j]
                    swapped = True
                elif (arrival_time[j] == arrival_time[j + 1]):
                    if (burst_time[j]>burst_time[j+1]):
                        arrival_time[j], arrival_time[j + 1] = arrival_time[j + 1], arrival_time[j]
                        process_name[j], process_name[j + 1] = process_name[j + 1], process_name[j]
                        burst_time[j], burst_time[j + 1] = burst_time[j + 1], burst_time[j]
                        swapped = True
                    elif(burst_time[j]==burst_time[j+1]):
                        if(int(process_name[j][1:]) > int(process_name[j + 1][1:])):
                            arrival_time[j], arrival_time[j + 1] = arrival_time[j + 1], arrival_time[j]
                            process_name[j], process_name[j + 1] = process_name[j + 1], process_name[j]
                            burst_time[j], burst_time[j + 1] = burst_time[j + 1], burst_time[j]
                            swapped = True

            if (swapped == False):
                return

    def fcfs(self,Processes_Names,Burst_Time_List,Arrival_Time_List,Number_Of_Processes):
        turn_around = []
        ####
 
        self.fig_init(Processes_Names, sum(Burst_Time_List) + 20 + max(Arrival_Time_List))
        # sorrrrrrt
        self.sort(Arrival_Time_List,Processes_Names,Burst_Time_List)

        #####
        last_x = Arrival_Time_List[0]
        for i in range(len(Processes_Names)):
            if (last_x < Arrival_Time_List[i]):
                last_x = Arrival_Time_List[i]

            self.draw(Processes_Names[i], last_x, Burst_Time_List[i] + last_x)
            last_x = last_x + Burst_Time_List[i]
            turn_around.append(last_x - Arrival_Time_List[i])

        waiting_time = []
        for k in range(len(turn_around)):
            waiting_time.append(turn_around[k] - Burst_Time_List[k])

        average_waiting = sum(waiting_time) / len(Processes_Names)

        red_patch = mpatches.Patch(label="The Average Waiting Time is: {}".format(average_waiting), fill=False)
        plt.legend(handles=[red_patch])
        plt.show()
        
    def click(self):
        #try:
            Number_Of_Processes = int(self.textEdit_4.toPlainText())

            value_of_textedit_2 = self.textEdit_2.toPlainText()
            Arrival_Time_List = value_of_textedit_2.splitlines()

            value_of_textedit_3 = self.textEdit_3.toPlainText()
            Burst_Time_List = value_of_textedit_3.splitlines()
            

            Processes_Names = []
            i = 0
            x = 0
            for i in range(Number_Of_Processes):
                Arrival_Time_List[i] = float(Arrival_Time_List[i])
                Burst_Time_List[i] = float(Burst_Time_List[i])
                Processes_Names.append("p" + str(i + 1))
            self.fcfs(Processes_Names, Burst_Time_List, Arrival_Time_List, Number_Of_Processes)
                
            
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(872, 859)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("bigger.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        resource_path("bigger.png")
        MainWindow.setWindowIcon(icon)
        MainWindow.setAutoFillBackground(False)
        MainWindow.setStyleSheet("background-color: white;")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(150, 50, 651, 101))
        self.label.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.label.setAutoFillBackground(False)
        self.label.setStyleSheet("font: 16pt \"Montserrat\"; color: black ; font-weight: bold;\n"
" font-weight:bold;")
        self.label.setObjectName("label")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(450, 260, 411, 71))
        self.label_4.setAutoFillBackground(False)
        self.label_4.setStyleSheet("font: 12pt \"Montserrat\"; color: black; font-weight: bold;")
        self.label_4.setObjectName("label_4")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(60, 280, 341, 41))
        self.label_3.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.label_3.setAutoFillBackground(False)
        self.label_3.setStyleSheet("font: 12pt \"Montserrat\"; color: black; font-weight: bold;")
        self.label_3.setObjectName("label_3")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(60, 150, 231, 101))
        self.label_5.setAutoFillBackground(False)
        self.label_5.setStyleSheet("font: 12pt \"Montserrat\"; color: black; font-weight: bold;")
        self.label_5.setObjectName("label_5")
        self.textEdit_2 = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit_2.setGeometry(QtCore.QRect(60, 330, 291, 371))
        self.textEdit_2.setStyleSheet("border: 2px  solid black; font: 75 20pt")
        self.textEdit_2.setObjectName("textEdit_2")
        self.textEdit_3 = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit_3.setGeometry(QtCore.QRect(450, 330, 291, 371))
        self.textEdit_3.setStyleSheet("border: 2px  solid black; font: 75 20pt")
        self.textEdit_3.setObjectName("textEdit_3")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(280, 730, 271, 91))
        self.pushButton.setStyleSheet("font: 14pt \"Montserrat\";  font-weight: bold; color:#FF5757;  font-size: 14;")
        self.pushButton.setObjectName("pushButton")
        self.textEdit_4 = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit_4.setGeometry(QtCore.QRect(300, 180, 91, 61))
        self.textEdit_4.setStyleSheet("border: 2px  solid black; font: 75 20pt")
        self.textEdit_4.setObjectName("textEdit_4")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        #Connecting to the Run Button 
        self.pushButton.clicked.connect(self.click)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "CPU Job Scheduler"))
        self.label.setText(_translate("MainWindow", "PLEASE ENTER THE FOLLOWING INPUTS:"))
        self.label_4.setText(_translate("MainWindow", "Burst Time of Each Process"))
        self.label_3.setText(_translate("MainWindow", "Arrival time of Each Process"))
        self.label_5.setText(_translate("MainWindow", "Number of Processes"))
        self.pushButton.setText(_translate("MainWindow", "RUN"))




class priority(object):
    """Priority scheduling algorithm implementation and GUI."""
    def fig_init(self, processes_name, total_burst):
        
        #Declaring a figure
        self.fig, self.ax = plt.subplots()  # must be global
        self.processes_name= processes_name
        #Setting x-axis and y-axis limits
        self.ax.set_ylim(0, len(processes_name))
        self.ax.set_xlim(0, total_burst)
        #Labels 
        self.ax.set_ylabel('Processes')
        self.ax.set_xlabel('Time Taken by Each Process')

        #Setting y-axis ticks
        ytick = [(i + 1) * 10 for i in range(len(processes_name) + 1)]

        self.ax.set_xticks(np.arange(0, total_burst + 1, 1))
        self.ax.set_yticks(ytick)
        ######self.ax.set_yticklabels(["self.processes_name"," "," "," "])
        #self.ax.grid(True)
        self.ax.grid(axis='x')
        
    def draw(self, name, start_time, end_time):
        no = int(name[1:])
        name = name.title()
        colors = ['blue','#1f77b4','#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
          '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf', '#1f77b4','#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
          '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
        color = []

        for i in range(0,len(self.processes_name)+1):
            
            color = colors[i]
   
        # Declearing a bar in the schedule
        #self.ax.broken_barh([(start_time, end_time - start_time)], ((no * 10) - 4, 7), facecolors=('tab:blue'))
        
        self.ax.broken_barh([(start_time, end_time - start_time)], (0,8), facecolors=colors[no])
        #for i in range(0, len(self.processes_name)):
         #   x = start_time + (end_time-start_time)/2
         #   y = 4
        s = name[0:]
        self.ax.text(start_time + (end_time-start_time)/2, 4, s=s, ha='center',va='bottom', fontsize =10, fontweight = "bold")
        self.ax.spines['left'].set_visible(False)
        self.ax.spines['bottom'].set_visible(False)
        self.ax.spines['top'].set_visible(False)
        self.ax.spines['right'].set_visible(False)
        self.ax.set_axisbelow(True) 

    def swapPositions(self,list, pos1, pos2):
         list[pos1], list[pos2] = list[pos2], list[pos1]
         return list

    def sorting(self,proc, arr, pior, Exc):
            for i in range(0, len(proc) - 1):
                for j in range(0, len(proc) - 1):

                    if (arr[j] > arr[j + 1]):
                        proc =self.swapPositions(proc, j, j + 1)
                        arr = self.swapPositions(arr, j, j + 1)
                        pior = self.swapPositions(pior, j, j + 1)
                        Exc = self.swapPositions(Exc, j, j + 1)
                    elif (arr[j] == arr[j + 1]):
                        if (pior[j] > pior[j + 1]):
                            proc = self.swapPositions(proc, j, j + 1)
                            arr = self.swapPositions(arr, j, j + 1)
                            pior = self.swapPositions(pior, j, j + 1)
                            Exc = self.swapPositions(Exc, j, j + 1)


    def get_min_pos(self, list):
        Min = 0
        for x in range(len(list)):
            Min = list[x]
            if Min > 0:
                break
        for x in range(len(list)):
            for y in range(x + 1, len(list)):
                if (list[y] < Min and list[y] > 0):
                    Min = list[y]
        return Min

    def priorit(self,Processes_Names,priority,Burst_Time_List,Arrival_Time_List,Preemptive,Number_Of_Processes):
        if not (Preemptive):
            self.sorting(Processes_Names, Arrival_Time_List, priority, Burst_Time_List)

            #########################
            last_time = []
            first_time = []
            done = []
            wt = []
            ########################## initial
            Avr_waiting_Time = []
            first_time.append(Arrival_Time_List[0])
            last_time.append(Arrival_Time_List[0] + Burst_Time_List[0])
            done.append(Processes_Names[0])
            last_x = last_time[0]
            Avr_waiting_Time.append(last_x - Arrival_Time_List[0] - Burst_Time_List[0])

            ################clear
            Processes_Names.remove(done[0])
            Arrival_Time_List.remove(Arrival_Time_List[0])
            priority.remove(priority[0])
            Burst_Time_List.remove(Burst_Time_List[0])
            #####################
            while not len(Processes_Names) == 0:

                for i in range(0, len(Processes_Names)):
                    if (Arrival_Time_List[i] <= last_x):
                        wt.append(i)
                #######wt not empty
                if not len(wt) == 0:
                    first_time.append(last_x)
                    index = wt[0]
                    min = priority[index]
                    for i in range(1, len(wt)):
                        if priority[wt[i]] < min:
                            min = priority[wt[i]]
                            index = wt[i]
                    done.append(Processes_Names[index])
                    last_x = last_x + Burst_Time_List[index]
                    last_time.append(last_x)
                    Avr_waiting_Time.append(last_x - Arrival_Time_List[index] - Burst_Time_List[index])
                    ##################
                    Processes_Names.remove(Processes_Names[index])
                    Arrival_Time_List.remove(Arrival_Time_List[index])
                    priority.remove(priority[index])
                    Burst_Time_List.remove(Burst_Time_List[index])
                    wt.clear()
                else:
                    done.append(Processes_Names[0])
                    first_time.append(Arrival_Time_List[0])
                    last_x = Arrival_Time_List[0] + Burst_Time_List[0]
                    last_time.append(last_x)
                    Avr_waiting_Time.append(last_x - Arrival_Time_List[0] - Burst_Time_List[0])
                    ################
                    Processes_Names.remove(Processes_Names[0])
                    Arrival_Time_List.remove(Arrival_Time_List[0])
                    priority.remove(priority[0])
                    Burst_Time_List.remove(Burst_Time_List[0])

            Sum_avg_time = sum(Avr_waiting_Time) / Number_Of_Processes

            for z in range(0, Number_Of_Processes):
                self.draw(done[z], first_time[z], last_time[z])
            ##########################################################################


        elif Preemptive:
            last_x = 0
            flag = 0
            New_list_burst = []
            New_list_Process = []
            Arrived_List = []
            New_priority = []
            Avr_waiting_Time = []
            #############################################################
            # Sorting Lists by Arrival Time
            ##########################################################
            for x in range(Number_Of_Processes):
                for y in range(x + 1, Number_Of_Processes):
                    if Arrival_Time_List[x] > Arrival_Time_List[y]:
                        self.swapPositions(Arrival_Time_List, x, y)
                        self.swapPositions(Burst_Time_List, x, y)
                        self.swapPositions(Processes_Names, x, y)
                        self.swapPositions(priority, x, y)
                    elif Arrival_Time_List[x] == Arrival_Time_List[y]:
                        if priority[x] > priority[y]:
                            self.swapPositions(Burst_Time_List, x, y)
                            self.swapPositions(Processes_Names, x, y)
                            self.swapPositions(priority, x, y)
            # Print until the Last Arrival Time
            for i in range(Number_Of_Processes):
                Arrived_List.append(Arrival_Time_List[i])
                New_list_burst.append(Burst_Time_List[i])
                New_list_Process.append(Processes_Names[i])
                New_priority.append(priority[i])
                while (1):
                    min_value = self.get_min_pos(New_priority)
                    index_Of_min = New_priority.index(min_value)
                    index_of_sepec_process = Processes_Names.index(New_list_Process[index_Of_min])
                    if i != len(Arrival_Time_List) - 1:
                        if last_x < Arrival_Time_List[i]:
                            if Arrival_Time_List[i + 1] > (Arrival_Time_List[i] + New_list_burst[index_Of_min]):
                                self.draw(New_list_Process[index_Of_min], Arrival_Time_List[i], Arrival_Time_List[i] +
                                          New_list_burst[index_Of_min])
                                last_x = Arrival_Time_List[i] + New_list_burst[index_Of_min]
                                New_list_burst[index_Of_min] = 0
                                New_priority[index_Of_min] = 0
                            else:
                                self.draw(New_list_Process[index_Of_min], Arrival_Time_List[i],
                                          Arrival_Time_List[i + 1])
                                last_x = Arrival_Time_List[i + 1]
                                New_list_burst[index_Of_min] = New_list_burst[index_Of_min] - (
                                        last_x - Arrival_Time_List[i])
                                if New_list_burst[index_Of_min] == 0:
                                    New_priority[index_Of_min] = 0
                                    Avr_waiting_Time.append(last_x - Arrival_Time_List[index_of_sepec_process]
                                                            - Burst_Time_List[index_of_sepec_process])

                        else:
                            if Arrival_Time_List[i + 1] > (last_x + New_list_burst[index_Of_min]):
                                self.draw(New_list_Process[index_Of_min], last_x, last_x + New_list_burst[index_Of_min])
                                last_x = last_x + New_list_burst[index_Of_min]
                                New_list_burst[index_Of_min] = 0
                                New_priority[index_Of_min] = 0
                                Avr_waiting_Time.append(last_x - Arrival_Time_List[index_of_sepec_process]
                                                        - Burst_Time_List[index_of_sepec_process])
                            else:
                                self.draw(New_list_Process[index_Of_min], last_x, Arrival_Time_List[i + 1])
                                New_list_burst[index_Of_min] = New_list_burst[index_Of_min] - (
                                        Arrival_Time_List[i + 1] - last_x)
                                last_x = Arrival_Time_List[i + 1]
                                if New_list_burst[index_Of_min] == 0:
                                    New_priority[index_Of_min] = 0
                                    Avr_waiting_Time.append(last_x - Arrival_Time_List[index_of_sepec_process]
                                                            - Burst_Time_List[index_of_sepec_process])

                    elif i == len(Arrival_Time_List) - 1:
                        if last_x < Arrival_Time_List[i]:
                            self.draw(New_list_Process[index_Of_min], Arrival_Time_List[i], Arrival_Time_List[i] +
                                      New_list_burst[index_Of_min])
                            last_x = Arrival_Time_List[i] + New_list_burst[index_Of_min]
                            New_list_burst[index_Of_min] = 0
                            New_priority[index_Of_min] = 0
                        else:
                            self.draw(New_list_Process[index_Of_min], last_x, last_x + New_list_burst[index_Of_min])
                            last_x = last_x + New_list_burst[index_Of_min]
                            New_list_burst[index_Of_min] = 0
                            New_priority[index_Of_min] = 0
                            Avr_waiting_Time.append(last_x - Arrival_Time_List[index_of_sepec_process]
                                                    - Burst_Time_List[index_of_sepec_process])

                    if i == Number_Of_Processes - 1:
                        break

                    elif (Arrival_Time_List[i + 1] - last_x) == 0 or sum(New_list_burst) == 0:
                        break
            #############################################################################
            # Sorting by Priority
            #############################################################################
            for x in range(Number_Of_Processes):
                for y in range(x + 1, Number_Of_Processes):
                    if New_priority[x] > New_priority[y]:
                        self.swapPositions(New_list_burst, x, y)
                        self.swapPositions(Arrived_List, x, y)
                        self.swapPositions(New_list_Process, x, y)
                        self.swapPositions(New_priority,x,y)
                    elif New_priority[x] == New_priority[y]:
                        if Arrived_List[x] > Arrived_List[y]:
                            self.swapPositions(Arrived_List, x, y)
                            self.swapPositions(New_list_Process, x, y)
                            self.swapPositions(New_list_burst, x, y)
            ##########################################################################
            # Drawing after last arrival time
            ##########################################################################
            for i in range(Number_Of_Processes):
                if New_list_burst[i] > 0:
                    self.draw(New_list_Process[i], last_x, last_x + New_list_burst[i])
                    last_x = last_x + New_list_burst[i]
                    index_of_sepec_process = Processes_Names.index(New_list_Process[i])
                    Avr_waiting_Time.append(last_x - Arrival_Time_List[index_of_sepec_process]
                                            - Burst_Time_List[index_of_sepec_process])
            ###############################################################################
            Sum_avg_time = sum(Avr_waiting_Time) / Number_Of_Processes
            ###############################################################################

        #####################################################################
        red_patch = mpatches.Patch(label="The Average Waiting Time is: {}".format(Sum_avg_time), fill=False)
        plt.legend(handles=[red_patch])
        plt.show()  # must be at last

    def click(self):
     #   try:
            Number_Of_Processes = int(self.textEdit_3.toPlainText())

            value_of_textedit_2 = self.textEdit_2.toPlainText()
            Arrival_Time_List = value_of_textedit_2.splitlines()

            value_of_textedit_4 = self.textEdit_4.toPlainText()
            Burst_Time_List = value_of_textedit_4.splitlines()

            value_of_textedit_5 = self.textEdit_5.toPlainText()
            priority = value_of_textedit_5.splitlines()
            Processes_Names = []
            x=0
            i = 0
            for i in range(Number_Of_Processes):
                Arrival_Time_List[i] = float(Arrival_Time_List[i])
                Burst_Time_List[i] = float(Burst_Time_List[i])
                Processes_Names.append("p" + str(i + 1))
                priority[i] = int(priority[i])
            Preemptive = self.radioButton.isChecked()
            self.fig_init(Processes_Names, sum(Burst_Time_List) + 10 + max(Arrival_Time_List))
            self.priorit(Processes_Names, priority, Burst_Time_List, Arrival_Time_List, Preemptive, Number_Of_Processes)
               

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1207, 836)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("bigger.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        resource_path("bigger.png")
        MainWindow.setWindowIcon(icon)
        MainWindow.setAutoFillBackground(False)
        MainWindow.setStyleSheet("background-color: white;")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(460, 240, 301, 91))
        self.label_4.setAutoFillBackground(False)
        self.label_4.setStyleSheet("font: 12pt \"Montserrat\"; color: black; font-weight: bold;")
        self.label_4.setObjectName("label_4")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(70, 260, 341, 51))
        self.label_3.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.label_3.setAutoFillBackground(False)
        self.label_3.setStyleSheet("font: 12pt \"Montserrat\"; color: black; font-weight: bold;")
        self.label_3.setObjectName("label_3")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(80, 120, 231, 101))
        self.label_5.setAutoFillBackground(False)
        self.label_5.setStyleSheet("font: 12pt \"Montserrat\"; color: black; font-weight: bold;")
        self.label_5.setObjectName("label_5")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(310, 20, 651, 101))
        self.label.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.label.setAutoFillBackground(False)
        self.label.setStyleSheet("font: 16pt \"Montserrat\"; color: black ; font-weight: bold;\n"
" font-weight:bold;")
        self.label.setObjectName("label")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(840, 280, 411, 31))
        self.label_6.setAutoFillBackground(False)
        self.label_6.setStyleSheet("font: 12pt \"Montserrat\"; color: black; font-weight: bold;")
        self.label_6.setObjectName("label_6")
        self.radioButton = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButton.setGeometry(QtCore.QRect(510, 160, 301, 31))
        self.radioButton.setStyleSheet("\n"
"font: 12pt \"Montserrat\"; font-weight: bold; color: black;")
        self.radioButton.setObjectName("radioButton")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(480, 720, 271, 91))
        self.pushButton.setStyleSheet("font: 14pt \"Montserrat\";  font-weight: bold; color:#FF5757;  font-size: 14;")
        self.pushButton.setObjectName("pushButton")
        self.textEdit_3 = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit_3.setGeometry(QtCore.QRect(330, 150, 91, 61))
        self.textEdit_3.setStyleSheet("border: 2px  solid black; font: 75 20pt")
        self.textEdit_3.setObjectName("textEdit_3")
        self.textEdit_2 = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit_2.setGeometry(QtCore.QRect(80, 320, 291, 371))
        self.textEdit_2.setStyleSheet("border: 2px  solid black; font: 75 20pt")
        self.textEdit_2.setObjectName("textEdit_2")
        self.textEdit_4 = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit_4.setGeometry(QtCore.QRect(460, 320, 291, 371))
        self.textEdit_4.setStyleSheet("border: 2px  solid black; font: 75 20pt")
        self.textEdit_4.setObjectName("textEdit_4")
        self.textEdit_5 = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit_5.setGeometry(QtCore.QRect(840, 320, 291, 371))
        self.textEdit_5.setStyleSheet("border: 2px  solid black; font: 75 20pt")
        self.textEdit_5.setObjectName("textEdit_5")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)


        #Connecting to the Run Button 
        self.pushButton.clicked.connect(self.click)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "CPU Job Scheduler"))
        self.label_4.setText(_translate("MainWindow", "Burst Time of Each Process"))
        self.label_3.setText(_translate("MainWindow", "Arrival time of Each Process"))
        self.label_5.setText(_translate("MainWindow", "Number of Processes"))
        self.label.setText(_translate("MainWindow", "PLEASE ENTER THE FOLLOWING INPUTS:"))
        self.label_6.setText(_translate("MainWindow", "Priority of Each Process"))
        self.radioButton.setText(_translate("MainWindow", "Preemptive or not?"))
        self.pushButton.setText(_translate("MainWindow", "RUN"))



class Ui_MainWindow(object):
    """"Main UI Window class."""
    def Fcfs(self):
        self.window =QtWidgets.QMainWindow()
        self.ui= FCFS()
        self.ui.setupUi(self.window)
        self.window.show()


    def SJF(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = SJF()
        self.ui.setupUi(self.window)
        self.window.show()

    def rr(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = rr()
        self.ui.setupUi(self.window)
        self.window.show()

    def priority(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = priority()
        self.ui.setupUi(self.window)
        self.window.show()

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(927, 848)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("bigger.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        resource_path("bigger.png")
        MainWindow.setWindowIcon(icon)
        MainWindow.setAutoFillBackground(False)
        MainWindow.setStyleSheet("background-color: white;")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(190, 240, 651, 101))
        self.label.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.label.setAutoFillBackground(False)
        self.label.setStyleSheet("font: 12pt \"Montserrat\"; color: black ; font-weight: bold;\n"
" font-weight:bold;")
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(310, 40, 331, 211))
        self.label_2.setText("")
        self.label_2.setPixmap(QtGui.QPixmap("bigger.png"))
        resource_path("bigger.png")
        self.label_2.setObjectName("label_2")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(340, 330, 271, 91))
        self.pushButton.setStyleSheet("font: 12pt \"Montserrat\"; outline-color: blue; font-weight: bold")
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(340, 580, 271, 91))
        self.pushButton_2.setStyleSheet("font: 12pt \"Montserrat\"; outline-color: blue; font-weight: bold")
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(340, 460, 271, 91))
        self.pushButton_3.setStyleSheet("font: 12pt \"Montserrat\"; outline-color: blue; font-weight: bold")
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(340, 710, 271, 91))
        self.pushButton_4.setStyleSheet("font: 12pt \"Montserrat\"; outline-color: blue; font-weight: bold")
        self.pushButton_4.setObjectName("pushButton_4")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        
        # Connecting pushbuttons to the main window
        self.pushButton.clicked.connect(self.Fcfs)
        self.pushButton_2.clicked.connect(self.priority)
        self.pushButton_3.clicked.connect(self.SJF)
        self.pushButton_4.clicked.connect(self.rr)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "CPU Job Scheduler"))
        self.label.setText(_translate("MainWindow", "CHOOSE THE TYPE OF SCHEDULER TO GET STARTED:"))
        self.pushButton.setText(_translate("MainWindow", "FCFS Scheduler"))
        self.pushButton_2.setText(_translate("MainWindow", "Priority Scheduler"))
        self.pushButton_3.setText(_translate("MainWindow", "SJF Scheduler"))
        self.pushButton_4.setText(_translate("MainWindow", "Round Robin Scheduler"))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())