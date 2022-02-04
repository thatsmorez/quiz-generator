import logging

# Global variables used in multiple files
questionList = []
numberOfQuestions = 0

#common variables which will be used in multiple functions
Q_START     = "@Q"
A_START     = "@A"
A_END       = "@E"
MAC_EOL     = "\r"
UNIX_EOL    = "\n"
WINDOWS_EOL = "\r\n"

MAX_Q       = "1000"
MAX_Q_LINES = "10"

def readQuestionFile(filename):
    f = open(filename, 'r')
    global numberOfQuestions
    global questionList
    status = 0
    question = ""
    choices = []
    answer = ""

    for line in f:
        if line[0] != "*" and len(line) != 1:
            if status == 0:
                if line.startswith(Q_START):
                    # First line of the question was discovered
                    status = 1
                else:
                    logging.error("Question File Reader: unexpected line: " + line)
            elif status == 1:
                # Reading in a question or looking for answer start
                if line.startswith(A_START):
                    # Answer section started
                    status = 2
                else:
                    question += line
            elif status == 2:
                answer = line
                status = 3
            else:
                if line.startswith(A_END):
                    formattedQuestion = {'question': question, 'choices': choices, 'answer':answer}
                    questionList.append(formattedQuestion)
                    status = 0
                    numberOfQuestions = numberOfQuestions + 1
                    question = ""
                    choices = []
                    answer = ""
                else:
                    choices.append(line)

    f.close()

def getNumberOfQuestions():
    return numberOfQuestions

def getQuestionList():
    return questionList

def printQuestionFile():
    for x in range(len(questionList)):
        print(questionList[x])



    




                


    
