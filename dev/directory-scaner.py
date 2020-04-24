import os, io
inputPath = input("Path to analyze:")
directories = os.walk(inputPath)
scanDirs = []
for directory in directories:
    scanDirs.append(directory[0])
print(scanDirs)