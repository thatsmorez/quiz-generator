import random

numberOfCorrectAnswers = 0
numberOfIncorrectAnswers = 0
numberOfQuestionsAsked = 0

def startQuiz(numberOfQuestionsToAsk, questionList):
    global numberOfQuestionsAsked
    updatedList = random.sample(questionList, numberOfQuestionsToAsk)

    while numberOfQuestionsToAsk > numberOfQuestionsAsked:
        displayQuestion(updatedList[numberOfQuestionsAsked])
        obtainAnswer(updatedList[numberOfQuestionsAsked])
        numberOfQuestionsAsked = numberOfQuestionsAsked + 1

def displayQuestion(formattedQuestion):
    global numberOfQuestionsAsked
    qNumber = numberOfQuestionsAsked + 1
    print("Question #" + str(qNumber) )
    print(formattedQuestion['question'])
    for x in range(len(formattedQuestion['choices'])):
        questionNum = x + 1
        print( str(questionNum) + " ) " + formattedQuestion['choices'][x])

def obtainAnswer(formattedQuestion):
    global numberOfCorrectAnswers
    global numberOfIncorrectAnswers

    answer = str(input("What is the answer?  "))

    if answer == str(formattedQuestion['answer']):
        print("Correct!")
        numberOfCorrectAnswers = numberOfCorrectAnswers + 1
    else:
        print("Incorrect. The answer is " + formattedQuestion['answer'] )
        numberOfIncorrectAnswers = numberOfIncorrectAnswers + 1
    
    print("\n\r")

def getNumberOfCorrectAnswers():
    return numberOfCorrectAnswers

def getNumberOfIncorrectAnswers():
    return numberOfIncorrectAnswers

    


