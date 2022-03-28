import random
import sys
import os
import platform
import tkinter
from tkinter import ttk, filedialog
from tkinter.filedialog import askopenfile
import time

numberOfQuestionsAsked = 0
winUpdatedList=[]
winNumQuestionToAsk = 0
firstTime = True
winTimeout = 0

def startQuiz(numberOfQuestionsToAsk, questionList, numberOfCorrectAnswers, numberOfIncorrectAnswers, newstdin='Nope', timeout=0):
    global numberOfQuestionsAsked
    global winUpdatedList
    global winNumQuestionToAsk
    global firstTime 
    global winTimeout
    numberOfIncorrectAnswers.value = numberOfQuestionsToAsk
    
    updatedList = random.sample(questionList, numberOfQuestionsToAsk)
    my_os = platform.system()
    if (my_os == 'Linux'):
        while numberOfQuestionsToAsk > numberOfQuestionsAsked:
            displayQuestion(updatedList[numberOfQuestionsAsked])
            obtainAnswer(updatedList[numberOfQuestionsAsked], newstdin, numberOfCorrectAnswers, numberOfIncorrectAnswers)
            numberOfQuestionsAsked = numberOfQuestionsAsked + 1
    else:
       winUpdatedList = updatedList
       numberOfQuestionsAsked  = 0
       firstTime = True
       winNumQuestionToAsk = numberOfQuestionsToAsk
       winTimeout = timeout
       winApplicationQuiz(numberOfCorrectAnswers, numberOfIncorrectAnswers)

def winApplicationQuiz(numberOfCorrectAnswers, numberOfIncorrectAnswers, questionWindow='Nope', tic=0):
    global numberOfQuestionsAsked
    global winUpdatedList
    global winNumQuestionToAsk
    global firstTime
    global winTimeout

    if(firstTime == False):
        numberOfQuestionsAsked = numberOfQuestionsAsked + 1

    if (winTimeout != 0) & (firstTime == False) :
        toc = time.perf_counter()
        winTimeout = winTimeout - (toc - tic)

    if questionWindow != 'Nope':
        questionWindow.destroy()

    if winTimeout < 0:
        print("SARAH " + str(winTimeout))
        return

    if winNumQuestionToAsk > numberOfQuestionsAsked:
         firstTime = False
         displayQuestion(winUpdatedList[numberOfQuestionsAsked], numberOfCorrectAnswers, numberOfIncorrectAnswers)

def displayQuestion(formattedQuestion, numberOfCorrectAnswers=0, numberOfIncorrectAnswers=0):
    global numberOfQuestionsAsked
    qNumber = numberOfQuestionsAsked + 1

    my_os = platform.system()
    if (my_os == 'Linux'):
        print("Question #" + str(qNumber) )
        print(formattedQuestion['question'])
        for x in range(len(formattedQuestion['choices'])):
            questionNum = x + 1
            print( str(questionNum) + " ) " + formattedQuestion['choices'][x])
    else: 
        questionWindow = tkinter.Tk()
        questionWindow.geometry("700x350")
        questionWindow.title("Quiz Generator")

        global winTimeout
        if winTimeout != 0:
            questionWindow.after(1000*int(winTimeout), lambda:questionWindow.destroy())
        ttk.Label(questionWindow, text="Question #" + str(qNumber), font=("Times New Roman", 12, "bold")).grid(row=0)
        ttk.Label(questionWindow, text=formattedQuestion['question'], font=("Times New Roman", 12)).grid(row=1)
        userAnswer = tkinter.StringVar()
        for x in range(len(formattedQuestion['choices'])):
            questionNum = x + 1
            userAnswerButton = ttk.Radiobutton(questionWindow, text=str(questionNum) + " ) " + formattedQuestion['choices'][x], value= questionNum, variable=userAnswer )
            userAnswerButton.grid(row=2+x, column=0)

        tic = time.perf_counter()
        ttk.Button(questionWindow, text="Submit", command=lambda: winObtainAnswer(questionWindow, userAnswer.get(), formattedQuestion,numberOfCorrectAnswers, numberOfIncorrectAnswers, tic)).grid(row=9, column=0)
        questionWindow.mainloop()


def winObtainAnswer(questionWindow, userAnswer, formattedQuestion, numberOfCorrectAnswers, numberOfIncorrectAnswers, tic=0):
    questionWindow.destroy()
    questionWindow = tkinter.Tk()
    questionWindow.geometry("700x350")
    questionWindow.title("Quiz Generator")
    
    if (tic != 0):
        global winTimeout
        toc = time.perf_counter()
        winTimeout = int(winTimeout - (toc - tic))
        questionWindow.after(1000*winTimeout , lambda: questionWindow.destroy())
      

    if userAnswer == str(formattedQuestion['answer']):
        ttk.Label(questionWindow, text="CORRECT", font=("Times New Roman", 12)).grid(row=1)
        numberOfCorrectAnswers.value = numberOfCorrectAnswers.value + 1
        numberOfIncorrectAnswers.value = numberOfIncorrectAnswers.value - 1
    else:
        ttk.Label(questionWindow, text="INCORRECT. The answer is " + formattedQuestion['answer'], font=("Times New Roman", 12)).grid(row=1)

    timer = time.perf_counter()
    ttk.Button(questionWindow, text="Next Question", command=lambda: winApplicationQuiz(numberOfCorrectAnswers, numberOfIncorrectAnswers, questionWindow, timer)).grid(row=9, column=0)
    questionWindow.mainloop()

def obtainAnswer(formattedQuestion, newstdin, numberOfCorrectAnswers, numberOfIncorrectAnswers):
    if newstdin != 'Nope':
        sys.stdin = newstdin
    answer = str(input("What is the answer?  "))

    if answer == str(formattedQuestion['answer']):
        print("Correct!")
        numberOfCorrectAnswers.value = numberOfCorrectAnswers.value + 1
        numberOfIncorrectAnswers.value = numberOfIncorrectAnswers.value - 1
    else:
        print("Incorrect. The answer is " + formattedQuestion['answer'] )
    
    print("\n\r")


    
