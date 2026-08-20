
# Bee Standard Library


## Standard Library


Standard library contains:

- Type system
- Mathematics
- System library

## Data rules


Introspection Rules


| Table |
| --- |
| rule | Purpose |
| type | type name |
| size | type size |



# Bee Type System


## Composite Types


| Table |
| --- |
| rule | Purpose |
| length | type length |
| capacity | type capacity |
| min | type minim limit |
| max | type maxim limit |



List & strings Type


| Table |
| --- |
| rule | Purpose |
| split | Split a string into a list / array |
| join | Join a list into a string |
| find | Search one sub-string in a string |
| replace | Replace one sub-string in a string |
| trim | Remove blank spaces from string |
| right | Align string to right by adding spaces |
| left | Align string to left by adding spaces |
| center | Align string to center by adding spaces |



Numeric Type


| Table |
| --- |
| rule | Purpose |
| round | Convert one real into an integer |
| floor | Convert one real into an integer |
| parse | Convert one string into one number |
| random | Create random numbers |



## Date Time


Modules for date and time will contain all required rules.


time


| Table |
| --- |
| rule | Purpose |
| now | get current time |



date


| Table |
| --- |
| rule | Purpose |
| now | get current date |



## Error Type


Bee has pre-define Error objects with codes in range (1..200):


```
** global type
type Error: {code ∈ Z, message ∈ S} <: Object;
```


```
** exception objects
$zero_division  := {100,"division by zero"}     ∈ Error;
$null_reference := {101,"null reference usage"} ∈ Error;
$value_overflow := {102,"value overflow"}       ∈ Error;
$out_of_range   := {103,"value out of range"}   ∈ Error;
$type_mismatch  := {104,"data type mismatch"}   ∈ Error;
$user_error     := {200,"user defined error"}   ∈ Error;
...
** Standard error
$standard_error  := {1,"standard error"}    ∈ Error;
$unexpected_error:= {2,"unexpected error"}  ∈ Error;
```


# Mathematic Rules


Math library will implement extra rules that are not available until you import "math" library. These are functions you rarely use and require extra memory space to be available in your program.


| Table |
| --- |
| rule | Purpose |
| sin | sinus |
| cos | cousin |
| tan | tangent |
| pow | power |
| sqr | square root |
| fac | factorial |
| mod | module rule y := |x| |



## System Library


Interaction with operating system require load from library.


```
+-------------------------
\bee
  |
  |-- system
  |     |-- io.bee
  |
  |-- db
  ...
-------------------------+
```


## File IO


To read and print into files and save to disk, we must use system.io library. This library define type "F" : file handler. It offer support for file input/output.


rules


Next is a fragment from system.io library that define rules open and close.


```
rule .open(name ∈ S, mode ∈ A) => (file ∈ File);
rule .close(file ∈ File);
rule .list(folder ∈ Folder) ∈ (S);
rule .exist(name ∈ S) ∈ L;
rule ,delete(name ∈ S);
rule ,rename(name, new_name ∈ S);
...
```


remember: public rules start with dot: "."


File IO


System IO rules


| Table |
| --- |
| rule | Purpose |
| open | Open a file |
| close | Close a file |
| exist | Check if file or folder exist on disk |
| list | Read a list of files and folders from directory |
| tree | Read tree of directory in memory |
| delete | Remove a file / directory |
| rename | Make a new directory |



Two data types must be available: File, Folder

- clean -- erase all data in the file
- flush -- save file buffer to disk
- change -- modify file attributes
- select -- select this folder as working folder
- purge -- remove all files from folder
- change -- modify folder attributes

```
new file_name   := File.open('name','w');
new folder_name := Folder.open('name');
```
---

[Go back](graphics.md)
