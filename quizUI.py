import tkinter
from tkinter import ttk, filedialog
from tkinter.filedialog import askopenfile
import os
import multiprocessing
import time


from questionFileReader import *
from quizController import *
from quizGenerator import *
from quizLogFileGenerator import *

win = tkinter.Tk()
FilepathLabel = tkinter.Label(win, text="", font=("Times New Romans", 11) )
RedTextLabel = tkinter.Label(win, text="File does not exist or meet the format", font=("Times New Romans", 11, "bold"), fg = "red")
filepath = "None"
doneBefore = False
firstTime = True

def startWinApplication():
	win.geometry("700x350")
	win.title("Quiz Generator")
	label = tkinter.Label(win, text="Welcome to the Quiz Generator Application", font=("Times New Roman", 15, "bold")).pack()
	label = tkinter.Label(win, text="Author: Sarah Moore", font=("Times New Roman", 15)).pack()
	label = tkinter.Label(win, text="Version: 2.0.0", font=("Times New Roman", 15)).pack()
	label = tkinter.Label(win, text="ReleaseDate : 03/27/2022", font=("Times New Roman", 15)).pack()

	label = tkinter.Label(win, text="Click the Button to browse for a Question File", font=("Times New Roman", 13, "bold"))
	label.pack(pady=10)
	ttk.Button(win, text="Browse", command=open_file).pack(pady=20)

	win.mainloop()

def open_file():
	global doneBefore 
	global FilepathLabel
	global RedTextLabel 
	global filepath

	file = filedialog.askopenfile(mode='r', filetypes=[('Q Files', '*.q')])

	if file:
		filepath = os.path.abspath(file.name)
		if (doneBefore == False):
			FilepathLabel.config(text = "The file is located at : " + str(filepath))
			FilepathLabel.pack()
			ttk.Button(win, text="Next Page", command=lambda: reviewQuestionInformation(win, filepath)).pack()
			doneBefore=True
		else:
			FilepathLabel.config(text ="The file is located at : " + str(filepath))	
	
	readQuestionFile(str(filepath))


def reviewQuestionInformation(window, filename):
	window.destroy()
	infoWindow = tkinter.Tk()
	infoWindow.geometry("700x350")
	infoWindow.title("Quiz Generator")
	
	numberOfQuestions  = getNumberOfQuestions()

	options = []
	x = 0
	for x in range (numberOfQuestions):
		options.append(str(x))

	clicked = tkinter.StringVar(infoWindow)
	clicked.set("1")

	numberOfQuestionsDrop = tkinter.OptionMenu(infoWindow, clicked, *options)
	numberOfQuestionsLabel = ttk.Label(infoWindow, text="How many questions should the quiz ask?", font=("Times New Roman", 13))
	

	ttk.Label(infoWindow, text="Select Quiz Options", font=("Times New Roman", 15, "bold")).grid(row=0)
	numberOfQuestionsLabel.grid(row=1,column=0)
	numberOfQuestionsDrop.grid(row=1,column=1)

	ttk.Label(infoWindow, text="Should the quiz be timed?", font=("Times New Roman", 13)).grid(row=3, column=0)

	timedSelection = tkinter.StringVar()
	timedRadioButton = ttk.Radiobutton(infoWindow, text="no", value= "no", variable=timedSelection)
	timedRadioButton.grid(row=3, column=3)
	timedRadioButton = ttk.Radiobutton(infoWindow, text="yes", value= "yes", variable=timedSelection)
	timedRadioButton.grid(row=3, column=2)
	enterTime = ttk.Label(infoWindow, text="Please enter the time in seconds if you selected yes above:", font=("Times New Roman", 13)).grid(row=4, column=0)
	
	text = "0"
	inputTime = tkinter.Text(infoWindow, height=1, width=10)
	inputTime.grid(row=4, column=1)
	inputTime.insert('end', text)

	ttk.Label(infoWindow, text="Do you want to see past results?", font=("Times New Roman", 13)).grid(row=5, column=0)

	pastSelection = tkinter.StringVar()
	pastRadioButton = ttk.Radiobutton(infoWindow, text="no", value= "no", variable=pastSelection )
	pastRadioButton.grid(row=5, column=3)
	pastRadioButton = ttk.Radiobutton(infoWindow, text="yes", value= "yes", variable=pastSelection )
	pastRadioButton.grid(row=5, column=2)

	ttk.Button(infoWindow, text="Start the Quiz", command=lambda: startQuizWin(pastSelection.get(), timedSelection.get(), clicked.get(), inputTime.get("1.0", 'end'), infoWindow) ).grid(row=9, column=0)

	infoWindow.mainloop()

def startQuizWin(pastSelection, timedSelection, numQuestions, timeout, infoWindow):
	infoWindow.destroy()

	qlist = getQuestionList()
	numberOfCorrectAnswers = multiprocessing.Value('i', 0)
	numberOfIncorrectAnswers = multiprocessing.Value('i', 0)
      
	if (timedSelection == 'yes') & (int(timeout) > 0):
		tic = time.perf_counter()
		startQuiz(int(numQuestions), qlist, numberOfCorrectAnswers, numberOfIncorrectAnswers, 'Nope', int(timeout))
		toc = time.perf_counter()
		
	else:
		tic = time.perf_counter()
		startQuiz(int(numQuestions), qlist, numberOfCorrectAnswers, numberOfIncorrectAnswers)
		toc = time.perf_counter()

	winDisplayMetrics(tic, toc, numberOfCorrectAnswers.value, numberOfIncorrectAnswers.value, int(numQuestions), pastSelection)

def winDisplayMetrics(tic, toc, correct, incorrect, numberOfQuestionsToAsk, pastSelection ):
	global filepath 

	percentCorrect  = (correct / numberOfQuestionsToAsk)   * 100
	percentIncorrect = (incorrect / numberOfQuestionsToAsk) * 100
	duration = toc-tic

	user = os.getlogin()
	location = r'C:\\Users\\' + str(user)+'\\quizlog.dat'
	generateLogFile(correct, numberOfQuestionsToAsk, filepath, location )

	metricsWindow = tkinter.Tk()
	metricsWindow.geometry("700x350")
	metricsWindow.title("Quiz Generator")
	tkinter.Label(metricsWindow , text="Quiz Metrics", font=("Times New Roman", 15, "bold")).grid(row=1)
	tkinter.Label(metricsWindow , text="Number of Questions Asked: " + str(numberOfQuestionsToAsk), font=("Times New Roman", 12)).grid(row=2)
	tkinter.Label(metricsWindow , text="Percentage of Correct Answers: " + str(percentCorrect), font=("Times New Roman", 12)).grid(row=3)
	tkinter.Label(metricsWindow , text="Percentage of Incorrect Answers: " + str(percentIncorrect), font=("Times New Roman", 12)).grid(row=4)
	tkinter.Label(metricsWindow , text="Quiz duration: " + str(duration) + " seconds", font=("Times New Roman", 12)).grid(row=5)

	ttk.Button(metricsWindow, text="Retake Quiz", command=lambda: reviewQuestionInformation(metricsWindow, filepath) ).grid(row=7, column=0)
	ttk.Button(metricsWindow, text="End Application", command=lambda: exitApplication(metricsWindow) ).grid(row=7, column=2)

	if (pastSelection == 'yes'):
		displayPastSelection(location)

	metricsWindow.mainloop()

def exitApplication(window):
	window.destroy()

def displayPastSelection(location):

	pastMetricsWindow = tkinter.Tk()
	pastMetricsWindow.geometry("700x350")
	pastMetricsWindow.title("Quiz Generator: Past Results")

	user = os.getlogin()
	text = tkinter.Text(pastMetricsWindow)
	tkinter.Label(pastMetricsWindow, text="Past Results",font=("Times New Roman", 15, "bold")).pack()
	scrollbar = tkinter.Scrollbar(pastMetricsWindow, orient="vertical", command=text.yview)
	scrollbar.pack(side="right", fill="y")

	f = open(location, "r")
	status = 0

	for line in f:
		if status == 0:
			if line.startswith("@USER"):
				text.insert('end', line)
				status = 1
		elif status == 1:
			if line.startswith("@INPUT"):
				text.insert('end', line)
				status = 2
		elif status == 2:
			if line.startswith("@NUMQ"):
				text.insert('end', line)
				status = 3
		elif status == 3:
			if line.startswith("@SCORE"):
				text.insert('end', line)
				status = 4
		else:
			if line.startswith("@DATE"):
				text.insert('end', line)
				text.insert('end', "-------------------------------------\n\r")
				status = 0
	text.config(yscrollcommand=scrollbar.set)
	text.pack()  
	ttk.Button(pastMetricsWindow, text="Exit Window", command=lambda: exitApplication(pastMetricsWindow) ).pack()
	pastMetricsWindow.mainloop()


