import socket
import os
import json

class Caliculation:

    def floor(x):
        return int(x // 1)
    
    def nroot(n, x):
        return x ** (1 / n)
    
    def reserve(s):
        return s[::-1]
    
    def validAnagram(str1, str2):
        return sorted(str1) == sorted(str2)
    
    def sort(strArr):
        return sorted(strArr)

print()