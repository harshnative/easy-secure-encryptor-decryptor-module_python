# Easy Secure Encryptor Decryptor module

This module to used to add military level encryption system to your project

Main Users : 
Hunders of security oriented applications


install module using pip command
```shell
pip install easySED
```


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

Takes and password and salt to with the pin provided (123456 is used if not provided)
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
This is encrypted by key which is returnedNewpass + keySalt (by default = "harshnative)

then we encrypt the thing using the key and add it to encrypted key

and done


## How secure is this

if you change all the salt list , pin , set a 12 digit pass , set security level to high , and keysalt then this encypted string should be unbreakable by any super computer in the world at least in a persons life time


## Methods - 

1. 
```python
obj.setPassword_Pin_keySalt(password , pin = 123456 , keySalt = "harshnative")
```

By default security level is set to high , so you have to pass the password containing all lower case , upper case , nums , special character else it will raise error

to remove this you have to set security level to low
```python 
obj.setSecurityLevel_toLow()     # not recommended
```


2. you can also set your own salt list 

```python
obj.setOwnSaltList(saltListPass)
```

Remember length of the list must be 6

3. if you want to output the password in the encrypted form so that the decryptor can tell if it can decrypt the string correctly or not the you have to call this function

remember - avoid this were ever possible , as it makes the things less secure

```python
obj.setOutPutPass()
```

4. you can chech whether the string an be decrypted or not

```python
obj.canDecrypt()
```

return True or false 

or returns None if password was provided in the encrypted string


## encrypting

after setting the password and optional things like keysalt , pin , saltlist etc
call this method and pass on the string to be encrypted here

```python
obj.encrypter(passStringHere)
```


## decrypting

after setting the password and optional things like keysalt , pin , saltlist etc
call this method and pass on the ecnrypted string here

```python
obj.decrypter(passStringHere)
```

raise error if fails to decypt the things





## Sample program - 
```python 
from easySED import SED

e = SED.ED()

saltList = ["hello" , "is" , "an" , "my" , "level" , "encryption"]

e.setSecurityLevel_toLow()
e.setPassword_Pin_keySalt("#123" , "236598" , "letscodeofficial.com")
e.setOwnSaltList(saltList)

encoded  = e.encrypter("helloBoi")
print(encoded)
print(e.canDecrypt(encoded))
decoded = e.decrypter(encoded)
print(decoded)

# output - 

# 1b01192129380d23225231202e060b0d16350c1950753c0e005a02113d060b5f3c3505280a31322a1c3d5151gAAAAABfZzh-TaV4qNffIN7eu94lfzueGuIf_pcLr_BWhGkwTUAJm9DcCY5xq-Gj3k2FtysNPI0NjZZkS6YGyx6CCMww2A0g3Q==
# None
# helloBoi
```

### Contibute - 

[Post any issues on github](https://github.com/harshnative/easy-secure-encryptor-decryptor-module_python)

[Check out code on github](https://github.com/harshnative/easy-secure-encryptor-decryptor-module_python)

