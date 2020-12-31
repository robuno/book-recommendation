import random

def main():
    newusername = input("What is your name? ")
    password = input("What is your password? ")

    passwordcheck(newusername,password)
    passworddata = passwordcheck(newusername,password)
    
    #Rating to nested list
    ratingsfile = "ratings.txt"
    openrating = open(ratingsfile, 'r')
    ratinglines = openrating.readlines()     #ratinglines is a list which includes existing user's name, ratings

    ratinglist =[]                           #ratinglist includes only ratings of the existing users
    countline = 2
    for line in ratinglines:
        if countline % 2 != 0:
            ratinglist.append(line.split())
        countline +=1

    #books to list
    booksfile = "books.txt"
    openbooks = open(booksfile, 'r')
    booklines = openbooks.readlines()       #booklines is a list which includes all books and author's name seperated by comma

    booklist =[]                            #booklist is a list which includes books' name and author' name in appropriate format for recommendation
    for line in booklines:
        changedline= line.rstrip()
        currentline= changedline.split(",")                            #currentline[0] means that name of the author
        tempname = "{} by {}".format(currentline[1],currentline[0])    #currentline[1] means that name of the book
        booklist.append(tempname)                                      #tempname is a form of name of the book, "by" and name of the author

    #getting new customers name and votes
    numberofbooks = len(booklist)
    newuservotes = [0] * numberofbooks     #creating a list list full of zeros for each book

    randombookindex= []                    #choosing random book indexes from booklist to recommend and get rating from new user 
    while len(randombookindex) != 10:
        randseq = random.randrange(len(booklist))
        if randseq not in randombookindex:
            randombookindex.append(randseq)

    for i in randombookindex:
        print(booklist[i])                       #printing random book according to the queue of the "randombookindex" list
        vote = int(input())                      #getting rate input from new user
        newuservotes[i] = vote                   #adding the rate of the book to the new user's ratings list
    numbers = " ".join(map(str,newuservotes))    #new user's book rates seperated by blank space in the form of string
 
    choose = input("I can make recommendations based on 3 different algorithms\nWhich algorithm ? A,B or C\n")
    
    if choose == "A":
        algorithma(booklist,ratinglist,newuservotes)                           
        recommendindexes = algorithma(booklist,ratinglist,newuservotes)      #taking the return of algoithma function
    if choose == "B":
        algorithmb(booklist,ratinglist,newuservotes)
        recommendindexes = algorithmb(booklist,ratinglist,newuservotes)      #taking the return of algoithmb function
    if choose == "C":
        algorithmc(booklist,ratinglist,newuservotes)
        recommendindexes = algorithmc(booklist,ratinglist,newuservotes)      #taking the return of algoithmc function
    
    print("\nRecommending based on Algorithm {}\n+++++++++++++++++++++++++++++++++++".format(choose))
    recommend(booklist,recommendindexes)                                     
    writetotxt(ratingsfile,newusername,numbers,ratinglines,passworddata)
    exit()

def passwordcheck(newusername,password):
    """creating a password.txt file and checking the input password if is the same with in the password.txt file"""
    with open("password.txt", "a+") as passwordfile:
        passwordread = open("password.txt", "r")
        passworddata = passwordread.readlines()                                #all usernames and the passwords are an element of passworddata list
        if (len(passworddata) == 0) or (len(passworddata) != 0 and newusername+"\n" not in passworddata):                                             #no password checking for the first time register
                print("Before I can recommend some new books for you to read,\nyou need to tell me your opinion on a few books.\n \nIf you haven\'t read the book, answer 0 but otherwise use this scale\n -5 Hated it!\n -3 Didn\'t like it.\n  1 OK\n  3 Liked it.\n  5 Really liked it.\n ")
                passworddata.append(newusername+"\n")
                passworddata.append(password+"\n")                             #adding new user's name and password to the passworddata list
        else:
            count =0
            for i in range(0,len(passworddata),2):                             #at each element in list whose index is multiple of 2 represents passwords
                if passworddata[i] == newusername+"\n":
                    break                                                      #finding the line(index) of the new user's password to check it later
                else:
                    count+=2
     
            if password+"\n"== passworddata[count+1]:
                print("Before I can recommend some new books for you to read,\nyou need to tell me your opinion on a few books.\n \nIf you haven\'t read the book, answer 0 but otherwise use this scale\n -5 Hated it!\n -3 Didn\'t like it.\n  1 OK\n  3 Liked it.\n  5 Really liked it.\n ")
            while password+"\n" != passworddata[count+1]:
                print("Wrong Password! Please try again.")
                main()                                                         #starting program again    
    return passworddata 

def writetotxt(ratingsfile,newusername,numbers,ratinglines,passworddata):  
    """writes new user name and ratings to the end of the 'ratings.txt' and 'password.txt' file"""
    nameline= None
    for linenumbeer in range(len(ratinglines)):
        if ratinglines[linenumbeer] ==newusername+"\n":           #checks if the new user already exist in the ratings.txt file
            nameline = linenumbeer                                #if it exists nameline represents the line number of the user's name

    if newusername+"\n" in ratinglines:
        ratinglines[nameline+1] = numbers+"\n"                    #changes existing ratings with the new ratings
    else:
        ratinglines[-1] = ratinglines[-1][:-1]+"\n"               
        ratinglines.append(newusername+"\n")                      #adding new user name to the end of the end of the rating.txt in the form of list
        ratinglines.append(numbers+"\n")                          #adding new user ratings to the end of the end of the rating.txt in the form of list
            
    with open(ratingsfile ,"w") as file:
        file.writelines(ratinglines)                              #writes the new data list to the .txt file

    with open("password.txt", "w") as passwordsave:    
        passwordsave.writelines(passworddata)

def bookrater(booklist,ratinglist):
    """creates a list includes lists which have user's ratings on the same book"""
    bookrates = []                                                #every list represents same book ratings of all users
    for i in range(len(booklist)):
        tempbookrates = []                                        #all user's ratings of the same book                      
        for j in range(len(ratinglist)):
            tempbookrates.append(ratinglist[j][i])
        bookrates.append(tempbookrates)
    return bookrates

def unreadbooksbynewuser(newuservotes):
    """creates a list which includes which books(indexes) are not red by new user"""
    newuserunreadbooks = []       
    for i in range(len(newuservotes)): 
        if newuservotes[i] == 0:                                  #rating '0' means that user did not read the book
            newuserunreadbooks.append(i)
    return newuserunreadbooks

def vectormultiplication(ratinglist,newuservotes):
    """creates a list includes summation of multiplication of new user rating and existing user's rating """
    vectormultilist = []
    for i in range(len(ratinglist)):                                        #in each new book, summation is set 0
        summation = 0 
        for j in range(len(ratinglist[0])):
            for t in range(len(newuservotes)):
                if j == t:                                                  #to do calculation related to the same book(indexes)
                    multi = int(ratinglist[i][j]) * int(newuservotes[t])
                    summation += multi
        vectormultilist.append(summation)
    return vectormultilist

def recommendindexcreator(sortedaverageindex,newuserunreadbooks):
    """creates a list which includes list of book recommendation according to the chosen algorithm."""
    recommendedindexes = []
    for i in sortedaverageindex:
        if i in newuserunreadbooks:                                   #avoiding to recommend a book which is already red by new user
            recommendedindexes.append(i)
    return recommendedindexes

######      ###           ###               ALGORITHM A                       ###         ### 
def algorithma(booklist,ratinglist,newuservotes):
    """recommends a list of books according to which have most average ratings and are not read by new user"""
    bookrates = bookrater(booklist,ratinglist)
   
    averagebookrates = []                           #represents the total rate of each book
    for i in range(len(bookrates)):                 
        count = 0
        for j in range(len(bookrates[0])):
            count += int(bookrates[i][j])
        averagebookrates.append(count)
    
    numberofbooksread = []                                #represents the number of books which are read by existing users
    for i in range(len(bookrates)):
        count2= 0
        for j in range(len(bookrates[0])):
            if int(bookrates[i][j]) != 0:
                count2 +=1
        numberofbooksread.append(count2)

    newaveragebookrates = []                       #represents average ratings of eachbook
    for i in range(len(averagebookrates)):
        if numberofbooksread[i] == 0:
            newaveragebookrates.append(0)
        else:
            newaveragebookrates.append(averagebookrates[i] / numberofbooksread[i])

        newuserunreadbooks = unreadbooksbynewuser(newuservotes)                                              #getting which books are not read by new user
    sortedaverageindex = sorted(range(len(newaveragebookrates)), key=lambda k: newaveragebookrates[k])[::-1]    #sorting indexes of the average ratings of the books

    recommendedindexes = recommendindexcreator(sortedaverageindex,newuserunreadbooks)
    return recommendedindexes

######      ###           ###               ALGORITHM B                       ###         ### 
def algorithmb(booklist,ratinglist,newuservotes):
    """recommends a list of books according to a user who has most similar ratings(vector multiplication ratings) and are not read by new user"""
    vectormultilist = vectormultiplication(ratinglist,newuservotes)
    newuserunreadbooks = unreadbooksbynewuser(newuservotes)
    
    suggestorsindex = sorted(range(len(vectormultilist)), key=lambda k: vectormultilist[k])[::-1]       #sorting indexes of the ratings of the books according to vector multiplication
    suggestor = suggestorsindex[0]                                                                      #choosing the already existing user who is the most similar to the new user
    
    suggestorkitaplari = ratinglist[suggestor]                                                          #getting the most similar user's ratings
    sortedsuggestorkitaplari = sorted(range(len(suggestorkitaplari)), key=lambda k: suggestorkitaplari[k])[::-1]  #sorting indexes of the newuser's book ratings

    recommendedindexes = recommendindexcreator(sortedsuggestorkitaplari,newuserunreadbooks)
    return recommendedindexes

######      ###           ###               ALGORITHM C                       ###         ### 
def algorithmc(booklist,ratinglist,newuservotes):
    """recommends a list of books according to the book prediction rating and are not read by new user.
    book prediction rating is calculated by multiplication of vector multiplication of each book and the user's rating of the same book. """
    bookrates = bookrater(booklist,ratinglist)
    vectormultilistC = vectormultiplication(ratinglist,newuservotes)
    
    userprediction =[]                                                          #multiplication of user's book rating and the vector multiplication for the same book
    for t in range(len(vectormultilistC)):
        for i in range(len(ratinglist)):
            temp =[]
            for j in range(len(ratinglist[i])):
                if t == i:
                    multiC = int(ratinglist[i][j]) * vectormultilistC[t]
                    temp.append(multiC)
            if temp != []:
                userprediction.append(temp)
                
    prediction =[]                                                             #prediction rating of the books
    for i in range(len(userprediction[0])):
        countC = 0
        for j in range(len(userprediction)):
            countC += int(userprediction[j][i])                                #summation of multiplication of user's book rating and the vector multiplication for the same book
        prediction.append(countC)

        newuserunreadbooks = unreadbooksbynewuser(newuservotes)
    predictioncopy = prediction[:]                                                                                     #copying the prediction rating list
    predictionsortingindexes = sorted(range(len(predictioncopy)), key=lambda k: predictioncopy[k])[::-1]               #sorting indexes of most similar user's books

    recommendedindexes = recommendindexcreator(predictionsortingindexes,newuserunreadbooks)
    return recommendedindexes

def recommend(booklist,recommendindexes):
    """recommends 10 book according to the chosen algorithm"""
    for i in range(10):
        print(booklist[recommendindexes[i]])

if __name__ == "__main__":
    main()
