import shutil, exif, time
import os, re, concurrent.futures, logging
logging.basicConfig(filename='example.log', level=logging.DEBUG)

threads = []
def relocate(paths):
    imagePath, newImagePath = paths
    shutil.copy2(imagePath, newImagePath, follow_symlinks=True)
    print  (f"{os.path.basename(imagePath)} relocated")

def scanFile():
    imagePath = input("Image to analyze:")
    splitted = imagePath.split(".")
    try:
        extension = splitted[1]
    except:
        extension = "none"
    print (extension)
    if extension in validExtensions:
        with open(f'{imagePath}', 'rb') as image_file:
                try:
                    my_image = exif.Image(image_file)
                except:
                    print(f"{os.path.basename(imagePath)} no exif data found")
                    print(time.ctime(os.path.getctime(imagePath)))
                    return 

                if(my_image.has_exif):
                    for attribute in dir(my_image):
                        if attribute[0] == "_":
                            print(f"{attribute} irrelevant")
                        else:
                            try:
                                print(f"{attribute} : {getattr(my_image,attribute)}")
                            except:
                                print(f"{attribute} not printable")
                else:
                    print(os.path.getctime(imagePath))

                
                    
def scanDir():
    folderPath = input("Path to analyze:")
    for possibleImage in os.listdir(folderPath):
        splitted = possibleImage.split(".")
        try:
            extension = splitted[1]
        except:
            extension = "none"
        if extension in validExtensions:
            imagePath = f"{folderPath}\\{possibleImage}"
            with open(f'{imagePath}', 'rb') as image_file:
                with concurrent.futures.ThreadPoolExecutor() as executor:

                    try:
                        my_image = exif.Image(image_file)

                    except:
                        try: 
                            newImageDirectoy = f"D:\\RELOCATED\\NO EXIF"
                            newImagePath = f"{newImageDirectoy}\\{os.path.basename(imagePath)}"
                            if not os.path.exists(newImagePath):
                                if not os.path.exists(newImageDirectoy):
                                    os.makedirs(newImageDirectoy)
                                threads.append(executor.submit(relocate, [imagePath, newImagePath]))
                            else:
                                print(f"{os.path.basename(imagePath)} already relocated")
                        except:
                            print(f"{os.path.basename(imagePath)} is invalid")

                        continue

                    if(my_image.has_exif):
                        # for attribute in dir(my_image):
                        #     if attribute[0] == "_":
                        #         print(f"{attribute} irrelevant")
                        #     else:
                        #         try:
                        #             print(f"{attribute} : {getattr(my_image,attribute)}")
                        #         except:
                        #             print(f"{attribute} not printable")
                        if hasattr(my_image,"datetime_original"):
                            splittedDate = re.split(r':|\s',my_image.datetime_original)
                            try: 
                                year = splittedDate[0]
                                month = splittedDate[1]
                                day = splittedDate[2]
                                datePath = f"{year}\\{month}\\{day}"
                            except:
                                datePath = "desconocido"
                        else:
                            datePath = "desconocido"
                        if hasattr (my_image,"model"):
                            newImageDirectoy = f"D:\\RELOCATED\\{datePath}\\{my_image.model}"
                        elif hasattr (my_image, "software"):
                            newImageDirectoy = f"D:\\RELOCATED\\{datePath}\\{my_image.software}"
                        else:
                            newImageDirectoy = f"D:\\RELOCATED\\{datePath}\\desconocido"
        
                        newImagePath = f"{newImageDirectoy}\\{os.path.basename(imagePath)}"
                        try:    
                            if not os.path.exists(newImagePath):
                                if not os.path.exists(newImageDirectoy):
                                    os.makedirs(newImageDirectoy)                
                                threads.append(executor.submit(relocate, [imagePath,newImagePath]))  
                            else: 
                                print(f"{os.path.basename(imagePath)} already relocated")       
                        except:
                            logging.error(f"Error processing {os.path.basename(imagePath)}")
                                        # input()
                    else:
                        newImageDirectoy = f"D:\\RELOCATED\\NO EXIF"
                        newImagePath = f"{newImageDirectoy}\\{os.path.basename(imagePath)}"
                        if not os.path.exists(newImagePath):
                                if not os.path.exists(newImageDirectoy):
                                    os.makedirs(newImageDirectoy)
                                threads.append(executor.submit(relocate, [imagePath, newImagePath]))
                        else: 
                            print(f"{os.path.basename(imagePath)} already relocated")     


validExtensions = ["jpg","JPG","NEF","nef","PNG","png","TIFF","tiff","DNG","dng"]
while True:
    decision = input("directory or file? (d/f):")
    if decision == "d":
        scanDir()
    elif decision == "f":
        scanFile()
    else:
        break


