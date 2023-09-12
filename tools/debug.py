"""debug.py debug marco
"""

class __Debug:
    def __init__(self) -> None:
        self.ON = False
    
    def PRINT(self, *args) -> None:
        if self.ON:
            print(*args)

DEBUG = __Debug()