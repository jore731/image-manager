from PyQt5.QtWidgets import QWidget
import CommonVariables
import os
from dev import tiffreader
import concurrent.futures
import time
import json
import shutil
from pathlib import Path

class dragToOrganizeView(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(CommonVariables.desktopSize*0.5)
        self.move((CommonVariables.desktopSize.width()-self.width())/2,
                    (CommonVariables.desktopSize.height()-self.height())/2)
        self.setAcceptDrops(True)
        
    def dropEvent(self, event):
        t = time.time()
        _ = concurrent.futures.ThreadPoolExecutor().submit(self.analyzeSetOfPictures, [event.mimeData().urls(),t])
                             
        
        # total = len(event.mimeData().urls())
        # each = int(total/10)
        # first = event.mimeData().urls()[0:each]
        # del event.mimeData().urls()[0:each]
        # second = event.mimeData().urls()[0:each]
        # del event.mimeData().urls()[0:each]
        # third = event.mimeData().urls()[0:each]
        # del event.mimeData().urls()[0:each]
        # forth = event.mimeData().urls()[0:each]
        # del event.mimeData().urls()[0:each]
        # fifth = event.mimeData().urls()
        # with concurrent.futures.ProcessPoolExecutor(max_workers=10) as executor:

        #     executor.submit(
        #     {self.analyzePicture(url) for url in first}
        #     )
        #     executor.submit(
        #     {self.analyzePicture(url) for url in second}
        #     )
        #     executor.submit(
        #     {self.analyzePicture(url) for url in third}
        #     )
        #     executor.submit(
        #     {self.analyzePicture(url) for url in forth}
        #     )
        #     executor.submit(
        #     {self.analyzePicture(url) for url in fifth}
        #     )

                             
        # print(f'Time for multiprocessing processing: {time.time() - t}')

        # print("---------------------------------------------------------------")

    def analyzeSetOfPictures(self,kargs):
        urls = kargs [0]
        t = kargs[1]
        # print(f'Thread started: {self}')
        for url in urls:
            self.analyzePicture(url)
        # print(f'Time for multithreading processing: {time.time() - t}')


    def analyzePicture(self,url):
        path = Path(url.path()[1:])
        try:
            NEF = tiffreader.NEFImage(path)
        except ValueError as err:
            # print(format(err))
            return
        relPath = NEF.relocatePath(os.path.dirname(NEF.imagePath), ["capyear", "capmonth", "capday", "capdevice"])
        self.createDir(relPath)
        relFile = os.path.join(relPath,NEF.fileName)
        print(relFile)
        shutil.copy2(NEF.imagePath, relFile)
        # if not hasattr(NEF, "jsonPath"):
        #     NEF.createJSON(os.path.join(os.path.dirname(NEF.imagePath),"json"))
        # print(relPath)

    def createDir(self,path):
        splitted = path.split("/")
        for i in range (3,len(splitted)):
            newPath=""
            for split in splitted[0:i]:
                newPath = os.path.join(newPath,split)
            if not os.path.isdir(newPath): os.mkdir(newPath)