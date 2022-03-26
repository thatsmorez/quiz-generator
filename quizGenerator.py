# Sarah Moore
# CS 553 - West Virginia University
# Developing Portable Software
#
# Assignment 1: Quiz Generator
#
 
from questionFileReader import *
from quizController import *
from quizLogFileGenerator import *
import time
import platform
import sys
import argparse
from os.path import expanduser
import multiprocessing

numberOfQuestionsToAsk = 0
readFile = True

def printIntroMessage():
    print("Welcome to the Quiz Generator Application")
    print("Author: Sarah Moore")
    print("Version: 2.0.0")
    print("Release Date: 03/26/2022")
    print("\n\r")

def obtainQuestionFile(path):
    global readFile
    try:
        readQuestionFile(path)
    except FileNotFoundError:
        print("Bad File name given (%s). Please Verify this path exists and try again.", path)
        readFile=False
    print("\n\r")

def obtainQuizInformation(numQuestion):
    numberOfQuestions  = getNumberOfQuestions()
    global numberOfQuestionsToAsk
    numberOfQuestionsToAsk = numQuestion
    
    
    if numberOfQuestionsToAsk > numberOfQuestions:
        print("Questions requested on quiz is more than the input file. Will only ask " + str(numberOfQuestions) + " questions in the quiz.")
        numberOfQuestionsToAsk = numberOfQuestions
        return
    
    if numberOfQuestionsToAsk < 0:
        numberOfQuestionsToAsk = 0
        return
    

def displayMetrics(tic, toc, correct, incorrect):
    global numberOfQuestionsToAsk

    percentCorrect  = (correct / numberOfQuestionsToAsk)   * 100
    percentInorrect = (incorrect / numberOfQuestionsToAsk) * 100

    print("Quiz Metrics")
    print("Number of Questions Asked: " + str(numberOfQuestionsToAsk))
    print("Percentage of Correct Answers: " + str(percentCorrect))
    print("Percentage of Incorrect Answers: " + str(percentInorrect))
    print(f"Quiz duration: {toc - tic:0.4f} seconds")

def main():
    global numberOfQuestionsToAsk
    global readFile
    global numberOfCorrectAnswers
    global numberOfIncorrectAnswers
    my_os = platform.system()
    if (my_os == 'Linux'):
        # Arguments:
        # Question File Location (required)
        # Number of Questions to Ask (required)
        # Time Limit (optional)
        # Location of LogFile (optional)
        # Display past results (optional)
        parser = argparse.ArgumentParser()
        parser.add_argument('--QuestionFilePath', type=str, help='The full file path to the question file.',required=True)
        parser.add_argument('--NumQuestions', type=int, help='The number of questions to be asked during the quiz. Note that if the number of questions exceedes the number of question in the file, then you will just be asked the max number of questions.',required=True)
        parser.add_argument('--TimeLimit', type=int, help='The time limit to take the generated quiz. If no input is given, then the quiz will run until the user completes it.',required=False, default=0)
        parser.add_argument('--DisplayPastResults', type=str, help='Whether or not to display past results. The default is not to.',required=False, choices=['y', 'n'], default='n')
        args = parser.parse_args()

        printIntroMessage()
        obtainQuestionFile(args.QuestionFilePath)
        if readFile == False:
            quit()
        
        obtainQuizInformation(args.NumQuestions)
        if numberOfQuestionsToAsk <= 0:
            quit()

        qlist = getQuestionList()
        numberOfCorrectAnswers = multiprocessing.Value('i', 0)
        numberOfIncorrectAnswers = multiprocessing.Value('i', 0)
        
        if(args.TimeLimit != 0):
            if(args.TimeLimit <= 0 ):
                quit()
            newstdin = os.fdopen(os.dup(sys.stdin.fileno()))
            lock = multiprocessing.Lock()
            lock.acquire()
            p = multiprocessing.Process(target=startQuiz, name="startQuiz", args=(numberOfQuestionsToAsk,qlist, numberOfCorrectAnswers, numberOfIncorrectAnswers, newstdin))
            p.start()
            tic = time.perf_counter()
            
            while ( time.perf_counter() - tic <= args.TimeLimit ) :
                if p.is_alive():
                    time.sleep(0.1)
                else:
                    break
            lock.release()
            p.terminate()

            toc = time.perf_counter()
            displayMetrics(tic, toc, numberOfCorrectAnswers.value, numberOfIncorrectAnswers.value)
        else:
            tic = time.perf_counter()
            startQuiz(numberOfQuestionsToAsk, qlist, numberOfCorrectAnswers, numberOfIncorrectAnswers)
            toc = time.perf_counter()
            displayMetrics(tic, toc, numberOfCorrectAnswers.value, numberOfIncorrectAnswers.value)
        
        
        generateLogFile(numberOfCorrectAnswers.value, numberOfQuestionsToAsk, args.QuestionFilePath, '/home/smoore/.quizLogfile')
        if(args.DisplayPastResults == 'y'):
            viewUserData('/home/smoore/.quizLogfile')

    elif (my_os == 'Windows'):
        print("I'm working on it")
    else :
        sys.exit("Unsupported Operating System. Please run on either a Linux or Windows environment")

if __name__ == "__main__":
    main()


