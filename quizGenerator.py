# Sarah Moore
# CS 553 - West Virginia University
# Developing Portable Software
#
# Assignment 1: Quiz Generator
#
 
from questionFileReader import *
from quizController import *

numberOfQuestionsToAsk = 0
readFile = True

def printIntroMessage():
    print("Welcome to the Quiz Generator Application")
    print("Author: Sarah Moore")
    print("Version: 1.0.0")
    print("Release Date: 02/10/2022")
    print("\n\r\n\r")

def obtainQuestionFile():
    global readFile
    path = input("Please enter in the full path of the question file: ")
    try:
        readQuestionFile(path)
    except FileNotFoundError:
        retry = input("Bad File name given. Would you like to try again (y/n): ")
        if retry == "y" or retry == "Y":
            obtainQuestionFile()
        else:
            readFile=False
    print("\n\r")

def obtainQuizInformation():
    numberOfQuestions  = getNumberOfQuestions()
    global numberOfQuestionsToAsk
    try:
        numberOfQuestionsToAsk = int(input(str(numberOfQuestions) + " has been read in by the application... \
          How many would you like to appear in your quiz? Please enter an integer: "))
    except ValueError:
        retry = input("A non-numerical value was provided. Would you like to try again (y/n): ")
        if retry == "y" or retry == "Y":
            obtainQuizInformation()
        else:
            numberOfQuestionsToAsk = 0
            return
    
    
    if numberOfQuestionsToAsk > numberOfQuestions:
        print("Questions requested on quiz is more than the input file. Will only ask \
              " + str(numberOfQuestions) + " questions in the quiz.")
        numberOfQuestionsToAsk = numberOfQuestions
        return

    if numberOfQuestionsToAsk < 0:
        retry = input("A negative number value was probided. Would you like to try again (y/n): ")
        if retry == "y" or retry == "Y":
            obtainQuizInformation()
        else:
            numberOfQuestionsToAsk = 0
            return

    if numberOfQuestionsToAsk == 0:
        print("Zero was inputted as number of questions to ask. Goodbye.")

def displayMetrics():
    correct = getNumberOfCorrectAnswers()
    incorrect = getNumberOfIncorrectAnswers()
    global numberOfQuestionsToAsk

    percentCorrect  = (correct / numberOfQuestionsToAsk)   * 100
    percentInorrect = (incorrect / numberOfQuestionsToAsk) * 100

    print("Quiz Metrics")
    print("Percentage of Correct Answers: " + str(percentCorrect))
    print("Percentage of Incorrect Answers: " + str(percentInorrect))


def main():
    global numberOfQuestionsToAsk
    global readFile

    printIntroMessage()
    obtainQuestionFile()
    if readFile == False:
        quit()

    obtainQuizInformation()
    print("\n\r")
    if numberOfQuestionsToAsk == 0:
        quit()

    qlist = getQuestionList()
    startQuiz(numberOfQuestionsToAsk, qlist)

    displayMetrics()

if __name__ == "__main__":
    main()


