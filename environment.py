import sys

class Environment:
    def __init__(self, parent=None, iterable=None):
        if iterable != None:
            self.contents = dict(iterable)
        else:
            self.contents = dict()
        self.parent = parent
        #print("Creating a new environment")
    
    def assignEnvironment(self, name, value):
        self.contents[name] = value
        #print("Adding variable:", name, "with value:", value)
        return value

    def lookupEnvironment(self,name):
        if name in self.contents:
            #print("In local")
            return self.contents[name]
        elif self.parent:
            #print("In parent")
            return self.parent.lookupEnvironment(name)
        else:
            print("Error. Variable", name, "does not exist")
            sys.exit(1)

    def updateEnvironment(self, name, value):
        if(name in self.contents):
            self.contents[name] = value
           # print("Updating variable:", name, "New value is:", value)
        elif(self.parent):
            self.parent.updateEnvironment(name,value)
        else:
            print("Error. Variable:", name, "does not exist.")

    def extendEnvironment(self, toAdd=None):
        #print("Extending the evnironment with", str(toAdd))
        return Environment(self,toAdd)

    def printEnvironment(self):
        for k,v in self.contents.items():
            print("{",k,":",v,"}")
