import os, platform, sys
from datetime import date

#common variables which will be used in multiple functions
USER_START     = "@USER"
INPUT_START    = "@INPUT"
NUMQ_START     = "@NUMQ"
SCORE_START    = "@SCORE"
DATE_START     = "@DATE"


def generateLogFile(correct, numQuestions, questionFile, filepath ):

    os.umask(0)
    f = open(os.open(filepath, os.O_CREAT | os.O_WRONLY, 0o777), 'a')

    
    my_os = platform.system()
    if (my_os == 'Linux'):
        newline = '\n'
    else:
        newline = '\n\r'
    f.write(newline + "--------------------------------------------------------" + newline)
    user = os.environ.get('USER')
    f.write(USER_START + " : " + str(user) + newline)
    f.write(INPUT_START + " : " + questionFile + newline)
    f.write(NUMQ_START + " : " + str(numQuestions) + newline)
    score = (correct / numQuestions ) * 100
    f.write(SCORE_START + " : " + str(score) + newline)
    d1 = date.today().strftime("%d/%m/%Y")
    f.write(DATE_START + " : " + d1 + newline)
    f.close()
    os.chmod(filepath, 0o700)
    
def viewUserData(filename):
    if (os.path.exists(filename) == False):
        print("Past Histroy Logfile doesn't exist. Please try again.")
        return
    
    os.chmod(filename, 0o777)
    
    f = open(filename, "r")
    status = 0
    user = os.environ.get('USER')
    for line in f:
        if line[0] != "-" and len(line) != 1:
            if status == 0:
                if line.startswith(USER_START):
                    if user in line:
                        print(line)
                        status = 1
            elif status == 1:
                if line.startswith(INPUT_START):
                    print(line)
                    status = 2
            elif status == 2:
                if line.startswith(NUMQ_START):
                    print(line)
                    status = 3
            elif status == 3:
                if line.startswith(SCORE_START):
                    print(line)
                    status = 4
            else:
                if line.startswith(DATE_START):
                    print(line)
                    print("-----------------------------------")
                    status = 0
                    
    f.close()
        
    os.chmod(filename, 0o700)
    