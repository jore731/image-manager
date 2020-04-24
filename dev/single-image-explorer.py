from tiffreader import *
import json
logging.basicConfig(filename='example.log', level=logging.DEBUG)

imagePath = input("Image to analyze:")


imagen = NEFImage(imagePath)

print(imagen.numberOfTagsFirstIFD)
#print(imagen.tagsFirstIFD.Model)
print(imagen.extension)
print(imagen.noExtName)
print(imagen.relocatePath("here" ,parameters=["capyear", "capmonth", "capday", "capdevice"]))
imagen.createJSON()
'''
import PIL.Image
imagefile = PIL.Image.open(imagePath)
for properties in dir(imagefile):
    print(f"{properties}: {getattr(imagefile, properties)}")
    print("-----------------------------")
try: 
    imagefile.verify()
except:
    print("not valid")
#3885933

#3885933                                                                                                        
#16034940
offsets = [8, 2664, 128000]
hexDic = {"0":0, "1":1, "2":2, "3":3, "4":4, "5":5, "6":6, "7":7, "8":8, "9":9, "a": 10, "b": 11, "c":12, "d":13, "e":14, "f":15}
def customUnpack(totalBytes = 2, isString = False):
    if not isString:
        if totalBytes==1:
            structure = direction
            structure += "B"
            return sum(struct.unpack(structure, image_file.read(totalBytes)))
        else:
            structure = direction
            wordSize = int(totalBytes/2)
            for _ in range(wordSize):
                structure+="H"
            return sum(struct.unpack(structure, image_file.read(wordSize*2)))
    else:
        returnString = ""
        for _ in range(totalBytes-1):
            returnString += str(image_file.read(1))[2:-1]
        return returnString
        

def TypeAndCount(dataType,count):
    if dataType in [1]:
        return [count<=4,1]
    elif dataType in [2]:
        return [count*2<=4,1]
    elif dataType in [3]:
        return [count*2<=4,2]
    elif dataType in [4]:
        return [count*4<=4,4]
    elif dataType in [5]:
        return [False,8]
    elif dataType in [6]:
        return [False,8]
    elif dataType in [5]:
        return [False,8]
  

if extension.lower() in validExtensions:
    with open(f'{imagePath}', 'rb') as image_file:
        header = str(image_file.read(2500000))
        capture_date_str = re.search(
            r'(([12]\d{3}):(0[1-9]|1[0-2]):(0[1-9]|[12]\d|3[01]) ([0-2]\d{1}):(\d{2}):(\d{2}))', header).groups()
        print(capture_date_str)
        splittedDate = re.split(r':|\s', str(capture_date_str[0]))

        # print(f"{splittedDate[0]} {splittedDate[1]} {splittedDate[2]}")
        length = 150000

        with open(f"{os.path.basename(imagePath)}_test.nef","wb") as f:
            content = bytearray(image_file.read(length))
            image_file.seek(0)
            f.write(content)
        with open(f"{os.path.basename(imagePath)}.txt","w+") as f:
            image_file.seek(0)
            for _ in range(length):
                byte = str(image_file.read(1))[2:-1]
                f.write(f"[{str(byte)}]\n")
            image_file.seek(0)
            byteOrder = str(image_file.read(2))[2:-1]
            if byteOrder == "II":   direction = "<"
            elif byteOrder == "MM": direction = ">"
            print(f"byte order:{byteOrder}")
            data = customUnpack()
            print(f"42: {data}")
            data = customUnpack(4)
            print(f"offset IFD 0: {data}")
            for offset in offsets:
                image_file.seek(offset)
                directoryEntries = customUnpack()
                print(f"Directory entries: {directoryEntries}")
                for i in range(directoryEntries):
                    tag = 0
                    while (tag == 0 and not (offset == 128000 and i == 0)):
                        tag = readTIFFData(3, 1)
                    if (offset == 128000 and i == 0):
                        tag = readTIFFData(3, 1)

                    if tag != 0 or (offset == 128000 and i == 0):
                        tag_type=readTIFFData(3,1)
                        tag_count=readTIFFData(4,1)
                        
                        tag_value=readTIFFData(tag_type, tag_count, slotSize=4)
                        print(f"{tag}-{tags[tag]}: type={tag_type} count={tag_count} value={tag_value}")
'''
# if extension in validExtensions:
#     with rawpy.imread(imagePath) as image_file:
#         txtPath = f"{os.path.basename(imagePath)}.txt"
#         f = open(txtPath, 'w+')
#         processed = image_file.postprocess(
#             no_auto_bright=True, use_auto_wb=False, gamma=None)
# for index, line in enumerate(processed):
#     for index2,data in enumerate(line):
#         for index3, data2 in enumerate(data):
#             if index in {0,1,2}:
#                 processed[index,index2,index3] = 0
#             f.write(f"{data2}")
# #     f.write(f"\n")
# processed.to_pickle("processed.pkl")
# print(processed[0])
# imageio.imwrite("test2.tiff", processed)
#     #f.write(f"\n")
# with open("test.nef", "w+") as p:
#     image_file = open (imagePath, "rb")
#     for line in image_file:
#             p.write(f"{line}")
