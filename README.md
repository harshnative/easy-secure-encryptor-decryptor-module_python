# easyFileShare module

This module to used to quickly add network file sharing capabilities to a python project

Main Users : 
1. Jarvis - command line personal assistant for windows , linux and mac. [click here to visit jarvis website](https://harshnative.github.io/JarvisWebsite)
2. 100's of little school project


install module using pip command
```shell
pip install easyFileShare
```


### To import in project - 
```python
from easyFileShare import FS
```

Then make a object instance of FileShareClass
```python
obj = FS.FileShareClass()
```

Now just call the start_fileShare() method and pass on the folder path to share
```python
obj.start_fileShare("C:/Users/UserName/Desktop")
```

Default server will start at PORT = 8000 , you can change that by passing port number also
```python
obj.start_fileShare("C:/Users/UserName/Desktop" , 5000)
```

##### Port Number must be a four digit integer

To stop the server - press CTRL + C

Visit the Provided link  on any device connected to the same wifi network to browser or download the files


### Other methods - 

All methods are called automatically by start_fileShare() method. 

1. obj.setPort(port) - To set custom port number
2. obj.setSharePath(folderPath) - To set folder path to share
	
   Some getters - 
3. obj.getSharePath()
4. obj.get_ip_address()
5. obj.getPort()
6. obj.getPort()

7. obj.startServerAtFolderSetted() - to start the server




### Sample program - 
```python 
from easyFileShare import FS

obj = FS.FileShareClass()

obj.start_fileShare("C:/Users/UserName/Desktop")

# output - 

# Starting file share ...

# Visit http://192.168.1.9:8000 to browse or download the files

# Files only available to devices present in the same network connection

# press { CTRL + C } to stop file sharing

```

### Contibute - 

[Post any issues on github](https://github.com/harshnative/easyFileShare_module)

[Check out code on github](https://github.com/harshnative/easyFileShare_module)