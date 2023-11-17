#import os
#import importlib

#def import_objects(path):
 #   for file in os.listdir(f"{os.path.dirname(__file__)}/{path}"):
  #      if file == "__init__.py" or file[-3:] != ".py":
   #         if os.path.isdir(f"{os.path.dirname(__file__)}/{path}{file}"):
    #            import_objects(f"{path}{file}/")
     #       continue
#
 #       path = path.replace("/", ".")
  #      print(f"{path}{file[:-3]}")
   #     importlib.__import__(f"{path}{file[:-3]}", globals(), locals(), [], 1)
    #    del file

#import_objects("")

#print(globals())
