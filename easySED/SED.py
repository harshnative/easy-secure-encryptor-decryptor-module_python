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

        # salting list
        self.saltList = ["This" , "is" , "an" , "industry" , "level" , "encryption"]

        # for salting fernet key
        self.keySalt1 = None
        self.keySalt2 = None

        self.securityLevelHigh = True
        self.outpass = False

    
    # function to set your own list
    def setOwnSaltList(self , saltList):
        if(len(saltList) != 6):
            raise Exception("please pass 6 strings in list")

        else:
            self.saltList = saltList



    # function for checking if a password contain all lower , upper , nums and special case characters and also if is of 12 digit or not 
    def checkPass(self , string):

        # checking for 12 digit length 
        if(len(string) != 12):
            return False

        # lower case list
        lowerCase = ['a','s','d','f','g','h','j','k','l','z','x',
                    'c','v','b','n','m','q','w','e','r','t','y','u'
                    ,'i','o','p']

        # upper case list 
        upperCase = []
        for i in lowerCase:
            upperCase.append(i.upper())


        # nums and special characters
        spChar = ['~','!','@','$','%','^','&','*','(',')','_','-','=',
                '`','/','+','/','<','>','[',']','{','}','.',':',';',
                '|','#']

        nums = ['1','2','3','4','5','6','7','8','9','0']

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
            elif(s in nums):
                tempList.append("n")

        count = 0
        if("l" in tempList):
            count = count + 1
        
        if("u" in tempList):
            count = count + 1

        if("s" in tempList):
            count = count + 1

        if("n" in  tempList):
            count = count + 1 

        if(count >=  4):
            return True
        else:
            return False


    
    # function for checking if the pin is of 6 digit or not 
    def checkPin(self , pin):

        if(len(pin) != 6):
            return False

        return True

    
    def setSecurityLevel_toLow(self):
        self.securityLevelHigh = False
        

    # function for setting the password , pin , keysalt
    # password must contain all lower , upper , nums , sp chars
    # pin must be of 6 digit
    def setPassword_Pin_keySalt(self , password , pin = 123456 , keySalt = "harshnative"):

        password = str(password)
        pin = str(pin)
        keySalt = str(keySalt)
        
        if(self.securityLevelHigh):
            if(self.checkPass(password)):
                self.__password = str(copy.copy(password))
            else:
                raise Exception("please set a 12 digit pass containing at least lower , upper , nums , special character \nOr you can set the security level to low")
        
        else:
            self.__password = str(copy.copy(password))
        
        if(self.checkPin(pin)):
            self.__pin = str(copy.copy(pin))
        else:
            raise Exception("please set a 6 digit pin \nOr you can set the security level to low")


        
        lenKeySalt = round(len(keySalt) / 2 )

        self.keySalt1 = keySalt[:lenKeySalt]
        self.keySalt2 = keySalt[lenKeySalt:]


    # function to add salt to the password
    def convPassword(self):
        if(self.__password == None):
            raise Exception("please set the password")

        count = 0
        
        newPass = self.__password

        for i in self.__pin:
            digit = int(i)
            newPass = newPass[:digit] + self.saltList[count] + newPass[digit:]
            count += 1

        return newPass


    # function to check if everything is set up
    def checkIfPossible(self):
        if(self.__password == None):
            raise Exception("please set password")
            
        if(self.__pin == None):
            raise Exception("please set pin")

        if((self.keySalt1 == None) and (self.keySalt2 == None)):
            raise Exception("please set key salt")
    

    
    # function to encrypt things
    def encrypter(self , stringToEncrypt):

        self.checkIfPossible()
            
        stringToReturn = ""

        convPass = self.convPassword()

        # key
        key = Fernet.generate_key()
        
        # conv key from bytes to str 
        newKey = key.decode("utf-8")

        # encryting the key using the conv pass and keysalts
        keyToAdd = onetimepad.encrypt(newKey , self.keySalt1 + convPass + self.keySalt2)


        # conv string to bytes
        stringToPass = bytes(stringToEncrypt , "utf-8")

        cipher_suite = Fernet(key)
        encoded_text = cipher_suite.encrypt(stringToPass)
        stringToAdd = encoded_text.decode("utf-8")

        stringToReturn = keyToAdd + stringToAdd

        return stringToReturn

    


    def decrypter(self , stringToDecrypt):

        self.checkIfPossible()

        convPass = self.convPassword()

        # getting the key
        newKey = onetimepad.decrypt(stringToDecrypt[:88] , self.keySalt1 + convPass + self.keySalt2)

        # conv strings to bytes
        key = bytes(newKey , "utf-8")

        cipher_suite = Fernet(key)
        decoded_text = cipher_suite.decrypt(bytes(stringToDecrypt[88:] , "utf-8"))

        return decoded_text.decode("utf-8")


    
    def returnEncryptedPassword(self , password):
        sha_signature = hashlib.sha256(password.encode()).hexdigest()
        return sha_signature.decode("utf-8")


    def authenticatePassword(self, passwordInput , hashedPassword):
        sha_signature = hashlib.sha256(passwordInput.encode()).hexdigest()

        if(sha_signature == hashedPassword):
            return True
        else:
            return False



if __name__ == "__main__":
    e = ED()

    saltList = ["This" , "is" , "an" , "industry" , "level" , "encryption"]

    e.setSecurityLevel_toLow()
    e.setPassword_Pin_keySalt("#123" , "236598" , "letscodeofficial.com")
    e.setOwnSaltList(saltList)

    encoded  = e.encrypter("hello world")
    print(encoded)
    decoded = e.decrypter(encoded)
    print(decoded)

    

        

