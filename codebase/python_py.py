### Hello World
print("Hello, World!")

### variable , var
x = "John"

### string
"hello"

### string
'hello'

### list , array
["Ford", "Volvo", "BMW"]


### map , dict
thisdict =	{
    "brand": "Ford",
    "model": "Mustang",
    "year": 1964
}

### tuples
("apple", "banana", "cherry")

### set
{"apple", "banana", "cherry"}

### set
set()

### if
if b > a:
    print("b is greater than a")
elif a == b:
    print("a and b are equal")
else:
    print("a is greater than b")

### for , loop
fruits = ["apple", "banana", "cherry"]
for x in fruits:
    if x == "banana":
        continue
    print(x)

### for , loop
for x in range(2, 6):
    print(x)

### while , loop
i = 1
while i < 6:
    print(i)
    f i == 3:
        break
    i += 1

### function , func , def
def my_function():
    print("Hello from a function")

### inline , function , func , lambda , inline
lambda a, b : a * b

### class , object
class Person:
    def __init__(mysillyobject, name, age):
        mysillyobject.name = name
        mysillyobject.age = age

    def myfunc(abc):
        print("Hello my name is " + abc.name)

### class , inheritance , inher , subclass
class Student(Person):
  def __init__(self, fname, lname, year):
    Person.__init__(self, fname, lname)
    self.graduationyear = year

  def welcome(self):
    print("Welcome", self.firstname, self.graduationyear)

### constructor
def __init__(self):
    pass

### pwd, path, dir
os.getcwd()

### ls, dir, path
for (rootpath, dirlist, filelist) in walk( _path ):
    flist = [ os.path.join(rootpath,f) for f in filelist ]
    dlist = [ os.path.join(rootpath,d) for d in dirlist ]

### is file, isfile, path
os.path.isfile( _path)

### path, ls, dir
os.listdir( _path)

### path, file, dir, long, absolute
os.path.realpath(_path)

### path, connect, join
os.path.join( _dir, _file)

### is, path, dir
os.path.isdir(_path)

### get dir, dir, path
os.path.dirname( _path)

### dir, path, name, basename
os.path.basename( _path)
