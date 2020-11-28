from cryptography.fernet import Fernet
import onetimepad
import copy
import hashlib
import os
import platform

# global variable for operating system detection
class GlobalDataFO:
    isOnWindows = False
    isOnLinux = True

# Checking weather the user is on windows or not
osUsing = platform.system()

if(osUsing == "Windows"):
    GlobalDataFO.isOnWindows = True
    GlobalDataFO.isOnLinux = False


class GlobalMethods:

    @classmethod
    def isDrive(cls , path = None):
        count = 0
        if(path == None):
            return None
        else:
            for i in path:
                if((i == '\\') or (i == "/")):
                    count += 1
        
        if(count <= 2):
            return True
        else:
            return False






    @classmethod
    # function to get the files list in folder passed
    def getSubFilesList(cls , root, files=True, dirs=False, hidden=False, relative=True, topdown=True):
        root = os.path.join(root, '')  # add slash if not there
        for parent, ldirs, lfiles in os.walk(root, topdown=topdown):
            if relative:
                parent = parent[len(root):]
            if dirs and parent:
                yield os.path.join(parent, '')
            if not hidden:
                lfiles   = [nm for nm in lfiles if not nm.startswith('.')]
                ldirs[:] = [nm for nm in ldirs  if not nm.startswith('.')]  # in place
            if files:
                lfiles.sort()
                for nm in lfiles:
                    nm = os.path.join(parent, nm)
                    yield nm

    

    @classmethod
    # function to get the folders to be generated
    def getFolderNameToBeGenerated(cls , pathToFile):

        if(GlobalDataFO.isOnLinux):
            new = pathToFile.split("/")
            lenNew = len(new)

            folderPath = ""
            for j in range(lenNew-1):
                folderPath = folderPath + new[j] + "/"


        else:
            new = pathToFile.split("\\")
            lenNew = len(new)

            folderPath = ""
            for j in range(lenNew-1):
                folderPath = folderPath + new[j] + "\\"

            
        return folderPath


    @classmethod
    # function to get the folders to be generated
    def getFileName(cls , pathToFile):

        if(GlobalDataFO.isOnLinux):
            new = pathToFile.split("/")
            return new[-1]


        else:
            new = pathToFile.split("\\")
            return new[-1]

        



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

        # opening the file 
        with open(filePath , 'rb') as file:
            data = file.read()

            # 0 is for file is opened completely
            yield 0

            key = Fernet.generate_key()

            # writing the key file 
            keyFileWrite = ""

            # bytes key to string to encrypted string using SED
            newKey = key.decode('utf-8')
            encodedKey = self.encrypter(newKey)

            encryptedPass = self.returnPassForStoring()

            # key , pass for storing , fileName
            keyFileWrite = encodedKey + "----------" + encryptedPass + "----------" + fileName
            # 1 represent writing key file is completed
            yield 1

            # encrypting the actual file
            cipher_suite = Fernet(key)
            encoded_text = cipher_suite.encrypt(data)

            # 2 represent the file as been encrypted
            yield 2 

            # output file path = destPath + fileName + __enc.txt
            if(self.isOnWindows):
                destFilePath = destPath + "\\" + fileName + "__enc"
            else:
                destFilePath = destPath + "/" + fileName + "__enc"

            # writing the encrypted data
            with open(destFilePath , 'w+b') as f:
                f.write(encoded_text)
                f.write(bytes("\n" , encoding="utf-8"))
                f.write(bytes(keyFileWrite , encoding="utf-8"))

                # 3 represent that the project is done
                yield 3


    # method to decrypt a file
    # file path is the path to file which is encrypted using same module
    # destPath is the path were the decrypted file will be present
    def decryptFile(self , filePath , destPath):

        # opening the encryted file
        with open(filePath , 'rb') as file:
            encodedDataFromFile = file.readlines()

            encodedData = encodedDataFromFile[0]

            # 0 represent the file read is completed
            yield 0

            # working on key
            tempText = encodedDataFromFile[1]
            tempText = str(tempText , encoding="utf-8")
            tempList = tempText.split("----------")

            # first was encrypted key
            encryptedKey = tempList[0]

            # second was the ecrypted Pass
            encryptedPass = tempList[1]

            # encryptedPass = ""

            # for i in oldEncryptedPass:
            #     if(i != "_"):
            #         encryptedPass = encryptedPass + i

            
            # third was the file name
            fileName = tempList[2]

            if(encryptedPass != self.returnPassForStoring()):
                raise RuntimeError("password / pin does not match ... ")


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
                destFilePath = destPath + "\\" + fileName 
            else:
                destFilePath = destPath + "/" + fileName

            # generating the original file
            with open(destFilePath , 'wb') as a:
                a.write(decoded)   

                # 3 represent that the process is completed
                yield 3


    # function to ecrypt the whole dir
    def encryptDir(self , dirPath , destPath):

        fileCount = 0

        # counting the number of file in dir
        for i in GlobalMethods.getSubFilesList(dirPath , hidden=True):
            fileCount = fileCount + 1 

        yield fileCount

        # encrypting
        for i in GlobalMethods.getSubFilesList(dirPath , hidden=True):

            # getting the source name and folder name so that we can pass that to encrypt file function
            if(GlobalDataFO.isOnLinux):
                source = dirPath + "/" + i
                folderToBeGenerated = destPath + "/" + GlobalMethods.getFolderNameToBeGenerated(i)
            else:
                source = dirPath + "\\" + i
                folderToBeGenerated = destPath + "\\" + GlobalMethods.getFolderNameToBeGenerated(i)

            # making the necessary required parent folders to store the encypted file 
            try:
                os.makedirs(folderToBeGenerated)
            except FileExistsError:
                pass
            
            # encryting the file
            for i in self.encryptFile(source , folderToBeGenerated):
                pass

            fileCount = fileCount - 1
            yield fileCount

    # function to decrypt a dir that was encrypted with this module
    def decryptDir(self , dirPath , destPath):

        fileCount = 0

        # counting the number of file 
        for i in GlobalMethods.getSubFilesList(dirPath , hidden=True):
            fileCount = fileCount + 1 

        yield fileCount

        for i in GlobalMethods.getSubFilesList(dirPath , hidden=True):

            # generating the source and dest path to pass the decryptFile method
            if(GlobalDataFO.isOnLinux):
                source = dirPath + "/" + i
                folderToBeGenerated = destPath + "/" + GlobalMethods.getFolderNameToBeGenerated(i)
            else:
                source = dirPath + "\\" + i
                folderToBeGenerated = destPath + "\\" + GlobalMethods.getFolderNameToBeGenerated(i)

            # making the necessary parent folders to store the decrypted file
            try:
                os.makedirs(folderToBeGenerated)
            except FileExistsError:
                pass

            tries = 0

            # decrypting the file , program will try 3 time max for a file 
            for i in range(3):
                try:
                    for i in self.decryptFile(source , folderToBeGenerated):
                        pass
                    break
                except RuntimeError:
                    tries += 1

            if(tries > 3):
                raise Exception("could not decrypt")
                
            fileCount = fileCount - 1
            yield fileCount




# def testing(obj):
#     e = obj
#     e.encryptDir(r"C:\Users\harsh\Desktop\hello" , r"C:\Users\harsh\Desktop\hello2")
#     e.decryptDir(r"C:\Users\harsh\Desktop\hello2" , r"C:\Users\harsh\Desktop\hello3")
                    
#     stringList1 = []
#     stringList2 = []

#     for i in GlobalMethods.getSubFilesList(r"C:\Users\harsh\Desktop\hello"):
#         with open(r"C:\Users\harsh\Desktop\hello" + "\\" + i , "r") as file:
#             string = file.read()

#             stringList1.append(string)

#     for i in GlobalMethods.getSubFilesList(r"C:\Users\harsh\Desktop\hello3"):
#         with open(r"C:\Users\harsh\Desktop\hello3" + "\\" + i , "r") as file:
#             string = file.read()

#             stringList2.append(string)

#     print(stringList1 == stringList2)

    







if __name__ == "__main__":
    e = ED()

    e.setPassword_Pin("#123hello" , "236598")

    filex = r"C:\Users\harsh\Desktop\hello.mp3"

    # obj1 = e.encryptFile(filex , r"C:\Users\harsh\Desktop\hello")
    # obj2 = e.decryptFile(r"C:\Users\harsh\Desktop\hello\hello.mp3__enc" , r"C:\Users\harsh\Desktop\hello")

    # for i in obj1:
    #     print(i)

    # for i in obj2:
    #     print(i)


    
    # testing(e)

    for i in e.encryptDir(r"Z:\docx" , r"C:\Users\harsh\Desktop\hello"):
        print(i)

    input()

    for i in e.decryptDir(r"C:\Users\harsh\Desktop\hello" , r"C:\Users\harsh\Desktop\hello2"):
        print(i)

    # for i in e.encryptFile(r"Z:\docx\python.docx" , r"C:\Users\harsh\Desktop"):
    #     pass

    # for i in e.decryptFile(r"C:\Users\harsh\Desktop\python.docx__enc" , r"C:\Users\harsh\Desktop"):
    #     pass

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


   
    

        

