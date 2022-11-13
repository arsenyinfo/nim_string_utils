## Nim vs Python: a comparison of the two languages for simple string processing

That's a sandbox where I tried to use Nim functions in Python code. For the comparison, I picked several string processing tasks I recently used in a real python project to estimate the performance of the Nim code and complexitiy of embedding Nim code in Python.

*Disclaimer:* I spent one day familiariazing myself with Nim, so there maybe many imperfections in the code. 

Tasks: 
1. Checking if string contains one of the substrings from a list.
2. Checking if list of strings contains a constant substring.
3. Levenshtein distance between two strings.
4. Common substring between two strings (ABCED, AABCD => ABC).
5. Common sequence between two strings (ABCED, AABCD => ABCD).

### Benchmark
(Python 3.9, Nim 1.6.8, OS X, M1 Pro):

```
    Contains one of
Python: 0.069
Nim: 0.103
    Contains constant
Python: 0.032
Nim: 0.084
    Finding common string
Python: 0.333
Nim: 0.095
    Finding common sequence
Python: 5.872
Nim: 0.200
    Levenshtein distance
Python: 0.006
Nim: 0.123
```

### Conclusions
1. For too simple tasks (1-2), Nim is slower than Python.
2. For a moderately complex task of Levenshtein distance, Nim is slower than Python wrapper on top of heavily optimized `Levenshtein` library written in C.
3. For more complex tasks (4-5), Nim can be (significantly) faster than Python, while writing code in Nim takes very little overhead comparing to Python.

### Links
1. [Nim for Python programmers](https://github.com/nim-lang/Nim/wiki/Nim-for-Python-Programmers)
2. [nimpy](https://github.com/yglukhov/nimpy) - library for building Python modules from Nim