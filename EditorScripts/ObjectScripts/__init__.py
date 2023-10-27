import os

for file in os.listdir(os.path.dirname(__file__)):
    if file == "__init__.py" or file[-3:] != ".py":
        continue
    __import__(file[:-3], locals(), globals(), [], 1)
del file
