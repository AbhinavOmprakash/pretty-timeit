# ptimeit
[![codecov](https://codecov.io/gh/AbhinavOmprakash/ptimeit/branch/main/graph/badge.svg?token=QCRpIcv84o)](https://codecov.io/gh/AbhinavOmprakash/ptimeit)

***Pretty timeit.***   

## Why did I write this?
timeit is a great module, but whenever I wanted to use it, I had to look up the syntax, and even after that it was tricky to get things working. So I wanted something that had similar functionality of timeit but had an easier, and more intuitive syntax.   
Under the hood, I take the same approach as timeit does-
- Everything is imported once.
- The garbage collector is disabled when the function is run.
- By default the function runs 1 milllion times.

## Installation

With pip.

```Bash
$ pip install ptimeit
```

With poetry.

```Bash
$ poetry add ptimeit
```

## Usage.

### A simple example.

```Python
from ptimeit import timethis, Timer

# although this is a decorator, your original function will not be modified.
@timethis() 
def function_to_be_timed():
    lst = [i for i in range(10)]

Timer.run() # Call this at the end of the file.
```

output
```Console
name                 | Execution time
function_to_be_timed | 0.5608107
```
Note: By default `Timer.run()` Prints the results to the console. 
If you want it to return a string, do this.

```Python
Timer.run(print_results=False) # returns a string
```


### Mixing positional arguments with keyword arguments.
Positional Arguments must be passed inside a list even if there is one argument.  
Keyword arguments must be passed inside a dictionary.   
Note the order follows the common idiom of `function(*args, **kwargs)`.

```Python
@timethis( [10], {"second_count_up_to":10} )
def function_to_be_timed(count_up_to, second_count_up_to=100):
    lst = [i for i in range(count_up_to)]
    lst2 = [i for i in range(second_count_up_to)]

Timer.run()
```

### adding custom descriptive names to your functions
If you want to see a different name other than the function name in the final report you can pass that to the decorator using `name=""` argument.
```Python
@timethis([10], name="A list comprehension that counts up to 10")
def function_to_be_timed(count_up_to):
    lst = [i for i in range(count_up_to)]
Timer.run()
```

```Console
name                                      | Execution time
A list comprehension that counts up to 10 | 0.5393135
``` 

### changing the number of times the function is repeated.
By default, like timeit, The function is repeated 1 million times,
but this can be changed by passing a `repeat=` to `Timer.run()` like this.

```Python
Timer.run(repeat=100) #The function to be timed will loop for hundred times.
```

### comparing functions.
A common use case that I have found for the timeit module, is to compare
the runtime speed of two different algorithms, this is very easy to do in p-timeit.

```Python
@timethis(100, name="using a for loop")
def my_func(count_up_to):
    lst=[]
    for i in range( count_up_to): 
        lst.append(i)

@timethis(100, name="using a List comprehension")
def my_func_2(count_up_to):
    lst = [i for i in range(count_up_to)]

Timer.run(compare=True)
```
Output
```console
rank | name                       | Execution time
1    | using a List comprehension | 2.3460704000000003
2    | using a for loop           | 4.37266
```
As you can see the list comprehension is faster than using a for loop.

Note: you can compare as many functions as you like. Not just two.
The `compare=True` flag formats the output, And orders the results from The fastest functions to the slowest.
You can still run multiple functions with `Timer.run()`.

Here's an example without compare

```python
@timethis([10], name="using a for loop")
def my_func(count_up_to):
    lst=[]
    for i in range( count_up_to): 
        lst.append(i)

@timethis([10], name="using a List comprehension")
def my_func_2(count_up_to):
    lst = [i for i in range(count_up_to)]

@timethis([10], name="using two lists")
def my_func_3(count_up_to):
    lst = [i for i in range(count_up_to)]
    lst2 = [i for i in range(count_up_to)]

Timer.run()
```
output
```Console
name                       | Execution time
using a for loop           | 0.7021932000000001
using a List comprehension | 0.6186622999999999
using two lists            | 1.0627897000000002
```
Notice that the functions are ordered as they were defined
and not by execution time.
