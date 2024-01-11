import pysoem
from time import sleep

class NGIO_DRIVER:
    
    adapter = "\\Device\\NPF_{2AFC35B5-1EE7-49B9-927D-D2CE5EDC52DD}"
    
    def __init__(self):
        self.master = pysoem.Master()