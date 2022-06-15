import os


def getBaseName(pathFile):
    basename = os.path.splitext(os.path.basename(pathFile))[0]
    return basename


def getFileFormatExtension(pathFile):
    ext = os.path.splitext(os.path.basename(pathFile))[1]
    return ext


def getFolderPath(pathFile):
    pathFolder = os.path.dirname(pathFile) + '/'
    return pathFolder


def deleteFilesInFolder(path):
    if len(os.listdir(path)) != 0:
        for file in os.listdir(path):
            os.remove(path+file)
