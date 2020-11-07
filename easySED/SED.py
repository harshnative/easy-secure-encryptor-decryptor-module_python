from cryptography.fernet import Fernet
import onetimepad
import copy
import hashlib

import platform

class ED:

    def __init__(self):

        # pin for salting password key
        self.__pin = None
        self.__password = None
        self.__convPass = None


        self.isOnWindows = False
        self.isOnLinux = True

        # Checking weather the user is on windows or not
        osUsing = platform.system()

        if(osUsing == "Windows"):
            self.isOnWindows = True
        else:
            self.isOnLinux = True

    # function for checking if a password contain all lower , upper , nums and special case characters and also if is of required length or not 
    def checkPass(self , passwordInput , minLength = 8 , lowerCase = True , upperCase = True , nums = True , specialChar = True):

        string = passwordInput

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

        del string

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

        # this password is stored in the memory for encrypting and decrypting using same obj of the class ED
        sha_signature = hashlib.sha256(password.encode()).hexdigest()
        return sha_signature

    
    def returnPassForStoring(self):

        # this password will be used as a reference for authentication stuff
        sha_signature = hashlib.sha512(self.__convPass.encode()).hexdigest()
        return sha_signature

    def authenticatePassword(self, storedPass , passwordInput , pinInput = 123456):
        
        # storing values for that they can be restored
        tempPass = self.__password
        tempPin = self.__pin
        tempConvPass = self.__convPass

        # setting the password provided
        self.setPassword_Pin(passwordInput , pinInput)

        # if the password provided after encryption matches the already stored password then it the right user
        if(str(hashlib.sha512(self.__convPass.encode()).hexdigest()) == str(storedPass)):

            # restoring things 
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

    # method to encrypt any file
    # takes the file at filePath and encryptes it and outputs a encrypted file data in a txt format in destPath
    # also a file named __key will be outputed at the destPath cotaining the encrypted key , the password encrypted using SHA512 for authentication and the file name which is going to be encrypted
    # the above key file is very important , it is necessary for decrypting the file
    def encryptFile(self , filePath , destPath):

        fileName = ""
        tempCount = 0

        # getting the file name
        for i in filePath[::-1]:
            
            if(self.isOnWindows):
                if((i == "\\")):
                    break
                else:
                    fileName = fileName + i
            else:
                if(i == "/"):
                    break
                else:
                    fileName = fileName + i         

            tempCount += 1   

        fileName = fileName[::-1]

        # getting the key file path = destPath + filename + __key.txt
        if(self.isOnWindows):
            keyFilePath = destPath + "\\" + fileName + "__key.txt"
        else:
            keyFilePath = destPath + "/" + fileName + "__key.txt"

        # opening the file 
        with open(filePath , 'rb') as file:
            data = file.read()

            # 0 is for file is opened completely
            yield 0

            key = Fernet.generate_key()

            # writing the key file 
            with open(keyFilePath , "w+") as keyFile:

                # bytes key to string to encrypted string using SED
                newKey = key.decode('utf-8')
                encodedKey = self.encrypter(newKey)

                encryptedPass = self.returnPassForStoring()

                # key , pass for storing , fileName
                keyFile.write(encodedKey + "________" + encryptedPass + "________" + fileName)

                # 1 represent writing key file is completed
                yield 1

            # encrypting the actual file
            cipher_suite = Fernet(key)
            encoded_text = cipher_suite.encrypt(data)

            # 2 represent the file as been encrypted
            yield 2 

            # output file path = destPath + fileName + __enc.txt
            if(self.isOnWindows):
                destFilePath = destPath + "\\" + fileName + "__enc.txt"
            else:
                destFilePath = destPath + "/" + fileName + "__enc.txt"

            # writing the encrypted data
            with open(destFilePath , 'w+b') as f:
                f.write(encoded_text)

                # 3 represent that the project is done
                yield 3


    # method to decrypt a file
    # file path is the path to file which is encrypted using same module
    # key file path is the file path which was outputted when the file was been encrypted
    # destPath is the path were the decrypted file will be present
    def decryptFile(self , filePath , keyFilePath , destPath):

        # opening the encryted file
        with open(filePath , 'rb') as file:
            encodedData = file.read()

            # 0 represent the file read is completed
            yield 0

            # opening the key file
            with open(keyFilePath , 'r') as keyFile:
                tempText = keyFile.read()

                tempList = tempText.split("________")

                # first was encrypted key
                encryptedKey = tempList[0]

                # second was the ecrypted Pass
                encryptedPass = tempList[1]

                if(encryptedPass != self.returnPassForStoring()):
                    raise RuntimeError("password / pin does not match ... ")

                # third was the file name
                fileName = tempList[2]

                newKey = self.decrypter(encryptedKey)
                key = newKey.encode('utf-8')

                # 1 represent that the reading of key file was completed
                yield 1
                
                cipher_suite = Fernet(key)

                decoded = cipher_suite.decrypt(encodedData)

                # 2 represent that the decrypting was completed
                yield 2
            
                # dest file path = destPath + dec__ + fileName
                if(self.isOnWindows):
                    destFilePath = destPath + "\\" + "dec__" + fileName 
                else:
                    destFilePath = destPath + "/" + "dec__" + fileName

                # generating the original file
                with open(destFilePath , 'wb') as a:
                    a.write(decoded)   

                    # 3 represent that the process is completed
                    yield 3
        



if __name__ == "__main__":
    e = ED()

    e.setPassword_Pin("#123hello" , "236598")

    filex = r"C:\Users\harsh\Desktop\hello.mp3"

    obj1 = e.encryptFile(filex , r"C:\Users\harsh\Desktop\hello")
    obj2 = e.decryptFile(r"C:\Users\harsh\Desktop\hello\hello.mp3__enc.txt" , r"C:\Users\harsh\Desktop\hello\hello.mp3__key.txt" , r"C:\Users\harsh\Desktop\hello")

    for i in obj1:
        print(i)

    for i in obj2:
        print(i)

    # encoded  = e.encrypter("hello world , my name is harsh native and I love programming")
    # print("encypted string = " , encoded)
    # decoded = e.decrypter(encoded)
    # print("\ndecrypted string = " , decoded)

    # # password you can store for further authentication 
    # objStore = e.returnPassForStoring()

    # print("\npassword you can store for further authentication = " , objStore)

    # if(e.authenticatePassword(objStore , "#123hello" , "236598")):
    #     print("\nyou are rigth user")
    
    # if(e.authenticatePassword(objStore , "#123world" , "236598")):
    #     print("\nshould not be here")
    # else:
    #     print("\nwrong user")


   
    

        

