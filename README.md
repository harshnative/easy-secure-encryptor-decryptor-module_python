# Easy Secure Encryptor Decryptor module

This module to used to add military level encryption system to your project

Main Users : 
Hunders of security oriented applications


install module using pip command
```shell
pip install easySED
```

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

Pin can you of max 6 digits.

It is recommend that you use at least a 12 digit password containing all lower case , upper case , nums , special char for better security

To check if the level of password matches your requirements use this method
```python
obj.checkPass(passwordInput , minLength = 8 , lowerCase = True , upperCase = True , nums = True , specialChar = True)
```

Above method will return True or False according to level matches or not 
EX - You can make any of the specialChar = False if you think that is not necessary in your password

It recommend that you deallocate the password from your script by using del operator , As the password is securely stored in the obj


#### Store the password + pin (123456 by default) in the encrypted form for further authentication stuff

Password is encrypted using SHA512 , SHA256 , stringSalting combinely here

```python
passYouCanStore = obj.returnEncryptedPassword(password)
```

now you can store this encrypted string any where

#### Authenticate the input password and pin (123456 by default if not provided) using previously stored password

Password is encrypted using SHA256 algo here

```python
isCorrect = obj.authenticatePassword(storedPass , passwordInput , pinInput = 123456)
```

This function returns True or False depending on if the password + pin input matches the stored password + pin


## encrypting

after setting the password call this method and pass on the string to be encrypted here

```python
encrypted_string = obj.encrypter(passStringHere)
```

this is going to diff next time even if you set the same stuff

## decrypting

after setting the password call this method and pass on the ecnrypted string here

```python
decrypted_string = obj.decrypter(passStringHere)
```


## making things more secure 

It is recommend that follow these steps for a unbreakable encrytion

1. set a password with at least 12 characters containing all lower case , upper case , numbers , special characters etc 

2. set a 6 digit pin (passed into password set function)

3. you non guessable passwords i.e password does not reflect your daily habits etc


## Sample program - 
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

### Contibute & report bugs  - 

[Post any issues on github](https://github.com/harshnative/easy-secure-encryptor-decryptor-module_python)

[Check out code on github](https://github.com/harshnative/easy-secure-encryptor-decryptor-module_python)

