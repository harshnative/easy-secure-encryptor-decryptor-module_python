# Easy Secure Encryptor Decryptor module

This module to used to add military level encryption system to your project

Main Users : 
Hunders of security oriented applications


install module using pip command
```shell
pip install easySED
```

### This module is used for encryting and decrypting things in the easy sqlite module 

## To import in project - 

```python
from easySED import SED
```

Then make a object instance of ED class
```python
obj = SED.ED()
```

## How this algorithm works

generates a random key of length 44 length

            ||
            ++

Takes a password and salt to with the pin provided (123456 is used if not provided)

Salting works with this function
```python
count = 0
        
newPass = passwordProvided

for i in pinProvided:
   digit = int(i)
   newPass = newPass[:digit] + self.saltList[count] + newPass[digit:]
   count += 1

return newPass
```

Salt list is setted by default - ["This" , "is" , "an" , "industry" , "level" , "encryption"]

            ||
            ++

Then we encrypt this key using the world class one time pad crytography

This is encrypted by key which is salted password (using pin and salt list) + keySalt (by default = "harshnative)

then we encrypt the string passed using the key and add it to encrypted key

and done


### Note - if you want the thing to be decryted on any computer with the help of password and pin , then it is recommend to not change the salt list and keysalt


## How secure is this

If you change all the salt list , pin , set a 12 digit pass , set security level to high , and keysalt then this encypted string should be unbreakable by any super computer in the world at least in a persons life time.

One time cryptography is the safest technique to encryt anything

Also this method combines the one time pad with pythons built in cryptography technique for more security

Also the encrypted string is always changed


## Methods - 

#### Set the password and (Optional - pin , keysalt)

```python
obj.setPassword_Pin_keySalt(password , pin = 123456 , keySalt = "harshnative")
```

By default security level is set to high , so you have to pass the password containing all lower case , upper case , nums , special character else it will raise error

to remove this you have to set security level to low
```python 
obj.setSecurityLevel_toLow()     # not recommended
```


Also is it recommend that you deallocate the password from your script by using del operator

As password is stored in the object created for further encyrption and decryption using the same object


#### Optional - Set your own salt list for more security

```python
obj.setOwnSaltList(saltListPass)
```

Remember length of the list must be 6 containing strings


#### Store the password in the encrypted form for further authentication stuff

Password is encrypted using SHA256 algo here
```python
encrypted_password = obj.returnEncryptedPassword(password)
```

now you can store this encrypted string any where

you can also encrypt the pin with the help of this


#### Authenticate the input password using previously stored password

Password is encrypted using SHA256 algo here

```python
isCorrect = obj.authenticatePassword(passwordInput , hashedPassword)
```

This function returns True or False depending on if the password input matches the stored password


## encrypting

after setting the password and optional things like keysalt , pin , saltlist etc
call this method and pass on the string to be encrypted here

```python
encrypted_string = obj.encrypter(passStringHere)
```


## decrypting

after setting the password and optional things like keysalt , pin , saltlist etc
call this method and pass on the ecnrypted string here

```python
decrypted_string = obj.decrypter(passStringHere)
```


## making things more secure 

It is recommend that follow these steps for a unbreakable encrytion

1. set a password with at least 12 characters containing all lower case , upper case , numbers , special characters etc (passed into password set function)

2. set a 6 digit pin (passed into password set function)

3. set your own key salt (passed into password set function)

4. set your own salt list (passed into saltListSet function)

#### Note - you need to remember only the password and pin , you can make key salt and keyList specific for a program , but do note you need all of these to decryt your data back






## Sample program - 
```python 
from easySED import SED

e = SED.ED()    

saltList = ["This" , "is" , "an" , "industry" , "level" , "encryption"]

e.setSecurityLevel_toLow()
e.setPassword_Pin_keySalt("#123" , "236598" , "letscodeofficial.com")
e.setOwnSaltList(saltList)

encoded  = e.encrypter("hello world")
print(encoded)
decoded = e.decrypter(encoded)
print(decoded)


# output - 

# 035103231523001408274507110236205c0d3f5d17304e1f0506010a21010607125922202a2030262d0b000fgAAAAABffDaHXlCSSqh7bDAqe3AbosJJ06DSuxbhCqQMYg0SEHNVk4LAkQqP6j-eugXsLEvjgVpV6PQPAAX4d-cPiMZt70iBdw==
# hello world
```

### Contibute - 

[Post any issues on github](https://github.com/harshnative/easy-secure-encryptor-decryptor-module_python)

[Check out code on github](https://github.com/harshnative/easy-secure-encryptor-decryptor-module_python)

