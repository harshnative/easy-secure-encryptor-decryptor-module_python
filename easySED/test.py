from cryptography.fernet import Fernet
import onetimepad
import copy
import hashlib


def isSubString(string, subString):
    lengthOfSubString = len(subString)
    try:
        for i, j in enumerate(string):
            if(j == subString[0]):
                if(subString == string[i:i+lengthOfSubString]):
                    return True
                else:
                    pass
        return False
    except Exception as e:
        return False



class ED:

    def __init__(self):

        # pin for salting password key
        self.__pin = None
        self.__password = None
        self.__convPass = None

    # function for checking if a password contain all lower , upper , nums and special case characters and also if is of required length or not 
    def checkPass(self , string , minLength = 8 , lowerCase = True , upperCase = True , nums = True , specialChar = True):

        # checking for 12 digit length 
        if(len(string) < minLength):
            return False

        # lower case list
        lowerCaseList = ['a','s','d','f','g','h','j','k','l','z','x',
                    'c','v','b','n','m','q','w','e','r','t','y','u'
                    ,'i','o','p']

        # upper case list 
        upperCaseList = []
        for i in lowerCaseList:
            upperCaseList.append(i.upper())


        # nums and special characters
        spChar = ['~','!','@','$','%','^','&','*','(',')','_','-','=',
                '`','/','+','/','<','>','[',']','{','}','.',':',';',
                '|','#']

        numsList = ['1','2','3','4','5','6','7','8','9','0']

        # tempList for checking if contains lowers uppers etc
        tempList = []

        for s in string:
            # if lower is present
            if(s in lowerCase):
                tempList.append("l")
            
            # if upper is present
            elif(s in upperCase):
                tempList.append("u")

            # if num is present
            elif(s in spChar):
                tempList.append("s")

            # if special char is present
            elif(s in numsList):
                tempList.append("n")


        if("l" in tempList):
            if(not(lowerCase)):
                return False

        if("u" in tempList):
            if(not(upperCase)):
                return False

        if("s" in tempList):
            if(not(specialChar)):
                return False

        if("n" in  tempList):
            if(not(nums)):
                return False

        return True

    
        

    # function for setting the password , pin
    def setPassword_Pin(self , password , pin = 123456):

        if(len(str(pin)) > 6):
            raise Exception("pin cannot be more than 6 digit long")

        self.__pin = copy.copy(int(pin))
        self.__password = str(copy.copy(self.getEncryptedPassword(str(password))))
    
        self.__convPass = self.convPassword()

    # function to add salt to the password
    def convPassword(self):
        
        count = 1  
        myList = []
        tempString = ""

        for i in self.__password:
            tempString = tempString + i

            if(count == 4):
                count = 1
                myList.append(tempString)
                tempString = ""
                continue
            
            count += 1

        convPass = ""

        for i in str(self.__pin):
            convPass = convPass + myList.pop(int(i))

        for i in myList:
            convPass = convPass + i

        return convPass

        
            



    # function to check if everything is set up
    def checkIfPossible(self):
        if(self.__password == None):
            raise Exception("please set password")
            
        if(self.__pin == None):
            raise Exception("please set pin")

        if(self.__convPass == None):
            raise Exception("please set password and pin")
    

    
    # function to encrypt things
    def encrypter(self , stringToEncrypt):

        self.checkIfPossible()
            
        stringToReturn = ""

        # key
        key = Fernet.generate_key()
        
        # conv key from bytes to str 
        newKey = key.decode("utf-8")

        # encryting the key using the conv pass and keysalts
        keyToAdd = onetimepad.encrypt(newKey , self.__convPass)

        # conv string to bytes
        stringToPass = bytes(stringToEncrypt , "utf-8")

        cipher_suite = Fernet(key)
        encoded_text = cipher_suite.encrypt(stringToPass)
        stringToAdd = encoded_text.decode("utf-8")

        stringToReturn = keyToAdd + stringToAdd

        return stringToReturn

    


    def decrypter(self , stringToDecrypt):

        self.checkIfPossible()

        # getting the key
        newKey = onetimepad.decrypt(stringToDecrypt[:88] , self.__convPass)

        # conv strings to bytes
        key = bytes(newKey , "utf-8")

        cipher_suite = Fernet(key)
        decoded_text = cipher_suite.decrypt(bytes(stringToDecrypt[88:] , "utf-8"))

        return decoded_text.decode("utf-8")


    
    def getEncryptedPassword(self , password):
        sha_signature = hashlib.sha256(password.encode()).hexdigest()
        return sha_signature

    
    def returnPassForStoring(self):
        return self.__convPass

    def authenticatePassword(self, storedPass , passwordInput , pinInput = 123456):
        
        tempPass = self.__password
        tempPin = self.__pin
        tempConvPass = self.__convPass

        self.setPassword_Pin(passwordInput , pinInput)

        if(str(self.__convPass) == str(storedPass)):
            self.__password = tempPass
            self.__pin = tempPin
            self.__convPass = tempConvPass

            del tempPass
            del tempPin
            del tempConvPass

            return True
            
        else:
            self.__password = tempPass
            self.__pin = tempPin
            self.__convPass = tempConvPass

            del tempPass
            del tempPin
            del tempConvPass

            return False

        

        



import random



myListLower = ['a','s','d','f','g','h','j','k','l','z','x',
          'c','v','b','n','m','q','w','e','r','t','y','u'
          ,'i','o','p'] 

myListUpper = []
for i in myListLower:
    myListUpper.append(i.upper())

myListEtc =  ['~','!','@','$','%','^','&','*','(',')','_','-','=',
             '`','/','+','/','<','>','[',']','{','}','.',':',';',
             '|','#' , ' ', ' ' , ' ' , ' ']  

nums = ['1','2','3','4','5','6','7','8','9','0']

myList = []

for i in myListLower:
    myList.append(i)

for i in myListUpper:
    myList.append(i)

for i in myListEtc:
    myList.append(i)

for i in nums:
    myList.append(i)



toDo = int(input("Enter the number of test : "))

error = 0
errorList = []
exList = []

e = ED()


for i in range(toDo):
    print("on - " , i)

    string = ""

    rand = random.randint(256 , 123456)

    for j in range(rand):
        string = string + str(random.choice(myList))

    password = ""
    for j in range(3):
        password = password + str(random.choice(myListLower))
    
    for j in range(3):
        password = password + str(random.choice(myListUpper))
    
    for j in range(3):
        password = password + str(random.choice(myListEtc))
    
    for j in range(3):
        password = password + str(random.choice(nums))

    
    pin = random.randint(0 , 999999)


    try:
        e.setPassword_Pin(password , pin)
        enc = e.encrypter(string)
        dec = e.decrypter(enc)

        if(dec != string):
            error += 1
            tempList = []
            tempList.append(string)
            tempList.append(dec)
            errorList.append(tempList)

    except Exception as ex:
        tempList = []
        tempList.append(ex)
        tempList.append(password)
        tempList.append(pin)
        tempList.append(string)
        exList.append(tempList)

    



print("error = ",  error)

with open("result.txt" , "w") as fil:

    fil.write("error = {}\n\n\n".format(error))
    fil.write("errorList = \n")

    for i in errorList:
        for j in i:
            fil.write(str(j))
            fil.write("\n")
        fil.write("\n")

    for i in exList:
        for j in i:
            fil.write(str(j))
            fil.write("\n")
        fil.write("\n")


    



