# Easy Secure Encryptor Decryptor module


[For reading docs on website , click here ...](https://letscodeofficial.com/pySEDDocs)

This module to used to add military level encryption system to your project , encrypt strings , files and even whole directories etc"

Main Users : 
Hunders of security oriented applications


install module using pip command
```shell
pip install easySED
```

#### Before you start - it is important that you note the version of this module before installing as sometimes the core method which are outsourced may get updated in pythons next version and make your encrypted file absolite , you remember the version so that you can install that version and prevent the data loss

#### This module is used for encryting and decrypting things in the easy sqlite module also 

## To import in project - 

```python
from easySED import SED
```

Then make a object instance of ED class
```python
obj = SED.ED()
```

## How this algorithm works

Takes your password and convert to the SHA256 encrypted hash form , this hash form is further rearranged into a diff string by using the values provided in the pin , if the pin is not provided then 123456 is used by default

So now  [ password ] -> [ SHA256 (password) ] -> [ PIN (SHA256 (password)) ] or let say this as X

Now we generate a random 44 digit string say Y and encrypt this key using onetimepad encryption tech with key = X and lets say this becomes A

now We encypt the actaul string with the Y using pythons cryptoraphy fernet tech and lets say this becomes Z

now we combine A and Z and output it 


## How secure is this

This algo combines the three of most secure encryption techniques in the world which includes SHA256 , onetimepad , cryptography fernet tech .

So any string encrypted using this algo must be unbreakable by any super computer at least in a persons lifetime .

But to be on the safe side, it is recommended that you at least 12 digit password containing all lower case , upper case , numbers and special chars as well . Also he password should be guessable i.e it should not be relatable with you daily habits etc 

Also you can use pin for security which is set to 123456 by default

#### Also if encypting the same string again yields diff result , so no one can even map the result outcomes

## Methods - 

#### Set the password and (Optional - pin)

```python
obj.setPassword_Pin(password , pin = 123456)
```

Pin can be of max 6 digits.

It is recommend that you use at least a 12 digit password containing all lower case , upper case , nums , special char for better security

To check if the level of password matches your requirements use this method
```python
obj.checkPass(passwordInput , minLength = 8 , lowerCase = True , upperCase = True , nums = True , specialChar = True)
```

Above method will return True or False according to level matches or not 
EX - You can make any of the specialChar = False if you think that is not necessary in your password

It recommend that you deallocate the password from your script by using del operator , As the password is securely stored in the obj of this module


#### Store the password + pin (123456 by default) in the encrypted form for further authentication stuff

As you see that string encrypted using this module is different each time , you if you large amounts of data to be decryted and encrypted like when encrypting dirs or data base , then it is better to store a reference password so that the module and check whether the password provided at the time of decryption is same by which the data was encrypted 

Password is encrypted using SHA512 , SHA256 , stringSalting combined together

so no one can guess the actual password by looking as the referenced password

```python
passYouCanStore = obj.returnEncryptedPassword(password)
```

now you can store this encrypted string any where and then pass this string in below method to authenticate 

#### Authenticate the input password and pin (123456 by default if not provided) using previously stored password

```python
isCorrect = obj.authenticatePassword(storedPass , passwordInput , pinInput = 123456)
```

This function returns True or False depending on if the password + pin input matches the stored password + pin


## encrypting string data types 

after setting the password call this method and pass on the string to be encrypted here

```python
encrypted_string = obj.encrypter(passStringHere)
```

this is going to diff next time even if you set the same stuff , which gives it a unbreable security 

## decrypting string data types

after setting the password call this method and pass on the ecnrypted string here

```python
decrypted_string = obj.decrypter(passStringHere)
```


## encrypting file

after setting the password call this method and pass the file path here which is going to be encrypted

Here the crypto fernet encryption technique is used to encrypt the bytes data of the file

```python
for i in obj.encryptFile(path_to_file , path_to_destination):
   pass
```

path to destination is the folder path were the encrypted file is going to be stored

function is set to yield the status update while running so you require a loop to run the method 

i will be reveice the status codes of the method which can be used to make loading bars for large files 

1. 0 represent that the file is successfully opened for encryption

2. 1 represent that the key is generated suucessfully

3. 2 represent that the file is been encrypted 

4. 3 represent that the encrypted file is been written suucessfully


## decrypting file

after setting the password call this method and pass the encrypted file path here which is going to be decrypted

```python
for i in obj.decryptFile(path_to_encrypted_file , path_to_destination):
   pass
```

path to destination is the folder path were the decrypted file is going to be stored

function is set to yield the status update while running so you require a loop to run the method 

i will be reveice the status codes of the method which can be used to make loading bars for large files 

1. 0 represent that the file is successfully opened for decryption

2. 1 represent that the key is readed suucessfully

3. 2 represent that the file is been decrypted 

4. 3 represent that the decrypted file is been written suucessfully


It will raise a RuntimeError("password / pin does not match ... ") if the password and pin entered are incorrect 

sometimes - one in thousands you can face this error even if you enter the exact password , then you should try again and error should be resolved 

## encrypting directiories

after setting the password call this method and pass the dir path here which is going to be encrypted

this method encrytes every file inside the dir recursively that is files inside sub folder are also taken into consideration

```python
for i in obj.encryptDir(path_to_dir , path_to_destination):
   pass
```

path to destination is the folder path were the encrypted directory is going to be stored


function is set to yield the status update while running so you require a loop to run the method 

i will be reveice the status codes of the method which can be used to make loading bars for large dirs

first the total no of files will be yield and then after one file is encrypted it will yield how many files are left till no file is left 

note - please do not store any other file in this folder as then the decryption will be possible 


## encrypting directiories

after setting the password call this method and pass the dir path here which is going to be encrypted

Note - any other file found other than the files encrypted using this module will result in hault of the decryption process 

```python
for i in obj.decryptDir(path_to_encryptedDir , path_to_destination):
   pass
```

path to destination is the folder path were the decrypted directory is going to be stored

it will be same as the dir which is used to make the encrypted dir just hidden folder will now be visible , you have to make them hidden again if you want 


function is set to yield the status update while running so you require a loop to run the method 

i will be reveice the status codes of the method which can be used to make loading bars for large dirs

first the total no of files will be yield and then after one file is decrypted it will yield how many files are left till no file is left 


## making things more secure 

It is recommend that follow these steps for a unbreakable encrytion

1. set a password with at least 12 characters containing all lower case , upper case , numbers , special characters etc 

2. set a 6 digit pin (passed into password set function)

3. you non guessable passwords i.e password does not reflect your daily habits etc


## Sample program for string data types - 
```python 
from easySED import SED

e = SED.ED()    

e.setPassword_Pin("#123hello" , "236598")

encoded  = e.encrypter("hello world , my name is harsh native and I love programming")
print("encypted string = " , encoded)
decoded = e.decrypter(encoded)
print("\ndecrypted string = " , decoded)

# password you can store for further authentication 
objStore = e.returnPassForStoring()

print("\npassword you can store for further authentication = " , objStore)

if(e.authenticatePassword(objStore , "#123hello" , "236598")):
   print("\nyou are rigth user")

if(e.authenticatePassword(objStore , "#123world" , "236598")):
   print("\nshould not be here")
else:
   print("\nwrong user")


# output on run 1 -
 
# encypted string =  78785041096701754b4b4364653222732a31557d503024721f552a7204795b1f457d5f0b41796d1d746c7c05gAAAAABfgZ9pXArC7XWbDmqUErbVR0h2uJT0_cXOgrdg0SCb6ZbcYpQAmjIzrk0b9pau6_mbuxR0CA_x2rGE6UpQ1Zcu_lvvxToI4AXCR0BjY9HzRiEsMW6NXMyVy7Pw3Korf8HmInUhTnzc_QjLnlm8LBVVwjloow==       

# decrypted string =  hello world , my name is harsh native and I love programming

# password you can store for further authentication =  e6095d7d7d130f53d02841f606e0526dbac9c8a41f5dfd8ea7c8fa295cd7a8cb271c999cb878551e66b367948fadca1d7e0493609b419f5715dcfa9c69b0f847

# you are rigth user

# wrong user





# output on run 2 - 

# encypted string =  6a6556710e6602615b1f6958622a2d42080214077d312a7c2c062b41737909080254622054686d1c79616405gAAAAABfgZ-P_6PKpmfZGxTeO32_toMUOrQ1tdiR34JNTgGgVA2ydp8P1g31ZLg73KfsI1DDQUoDJb15V9lzLkwjrw_-RhKWbOk_Z78ElCh5yWp5-csPIHslZZ4bcFKlE-vErSCXHDuo5jxeJO529P5kC1i2o1O8Xg==       

# decrypted string =  hello world , my name is harsh native and I love programming

# password you can store for further authentication =  e6095d7d7d130f53d02841f606e0526dbac9c8a41f5dfd8ea7c8fa295cd7a8cb271c999cb878551e66b367948fadca1d7e0493609b419f5715dcfa9c69b0f847

# you are rigth user

# wrong user


# As you can see in output , both time the encrypted string is diff 
```


## Sample program for file - 
```python 
from easySED import SED

e = SED.ED()    

e.setPassword_Pin("#123hello" , "236598")

for i in e.encryptFile(r"Z:\docx\python.docx" , r"C:\Users\harsh\Desktop"):
   pass

for i in e.decryptFile(r"C:\Users\harsh\Desktop\python.docx__enc"  , r"C:\Users\harsh\Desktop"):
   pass

```

## Sample program for Dir - 
```python 
from easySED import SED

e = SED.ED()    

e.setPassword_Pin("#123hello" , "236598")

for i in e.encryptDir(r"Z:\docx" , r"C:\Users\harsh\Desktop\hello"):
   print(i)

for i in e.decryptDir(r"C:\Users\harsh\Desktop\hello" , r"C:\Users\harsh\Desktop\hello2"):
   print(i)

```





### Contibute & report bugs  - 

[Post any issues on github](https://github.com/harshnative/easy-secure-encryptor-decryptor-module_python)

[Check out code on github](https://github.com/harshnative/easy-secure-encryptor-decryptor-module_python)

