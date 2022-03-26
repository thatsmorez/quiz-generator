import random
import sys
import os

numberOfQuestionsAsked = 0

def startQuiz(numberOfQuestionsToAsk, questionList, numberOfCorrectAnswers, numberOfIncorrectAnswers, newstdin='Nope'):
    global numberOfQuestionsAsked
    numberOfIncorrectAnswers.value = numberOfQuestionsToAsk
    
    updatedList = random.sample(questionList, numberOfQuestionsToAsk)
    
    while numberOfQuestionsToAsk > numberOfQuestionsAsked:
        displayQuestion(updatedList[numberOfQuestionsAsked])
        obtainAnswer(updatedList[numberOfQuestionsAsked], newstdin, numberOfCorrectAnswers, numberOfIncorrectAnswers)
        numberOfQuestionsAsked = numberOfQuestionsAsked + 1

def displayQuestion(formattedQuestion):
    global numberOfQuestionsAsked
    qNumber = numberOfQuestionsAsked + 1
    print("Question #" + str(qNumber) )
    print(formattedQuestion['question'])
    for x in range(len(formattedQuestion['choices'])):
        questionNum = x + 1
        print( str(questionNum) + " ) " + formattedQuestion['choices'][x])

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


    


