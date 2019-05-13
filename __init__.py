#!/usr/bin/env python
import sys
 
print('__init__')
print('__init__.__name__', __name__)
print('__init__.__package__', __package__)
 
print('sys.path', sys.path)
 
def main():
    print('__init__.main()')
