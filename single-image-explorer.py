import shutil
import exif
import time
import os
import re
import concurrent.futures
import logging
import rawpy
import imageio
import matplotlib.pyplot as plt
import pandas as pd
import struct 
logging.basicConfig(filename='example.log', level=logging.DEBUG)
validExtensions = ["jpg", "nef", "png", "tiff", "dng"]
threads = []

imagePath = input("Image to analyze:")
splitted = imagePath.split(".")
try:
    if len(splitted)>1:
        extension = splitted[-1]
    else:
        extension = "none"
except:
    extension = "none"
data = []




class NEFImage:
    def __init__(self, imagePath):
        self.regexDate = r'(([12]\d{3}):(0[1-9]|1[0-2]):(0[1-9]|[12]\d|3[01]) ([0-2]\d{1}):(\d{2}):(\d{2}))'
        self.name = os.path.basename(imagePath)
        self.NoTIFFError = ValueError(
            f"{self.name} is not recognized as a TIFF file")
        
    @property
    def direction(self):
        if not hasattr(self, "_direction"):
            self.image_file.seek(0)
            byteOrder = str(self.image_file.read(2))[2:-1]
            if byteOrder == "II":
                self._direction = "<"
            elif byteOrder == "MM":
                self._direction = ">"
            else:
                raise self.NoTIFFError
        return self._direction

    @property
    def image_file(self):
        if not hasattr (self, "_image_file"): self._image_file = open(f'{imagePath}', 'rb')
        return self._image_file

    @property
    def verifiyDirection(self):
        self.image_file.seek(2)
        if str(self.image_file.read(2))[2:-1] == 42:
            return 0
        else:
            raise self.NoTIFFError

    @property
    def date(self):
        _, year, month, day, hour, minute, second = re.search(self.regexDate, str(self.image_file.read())).groups()
        return [year,month,day,hour,minute,second]

    @property
    def model(self):
        modelRE = re.compile("(NIKON [^CORPORATION][A-Za-z0-9]*)")
        return modelRE.search(str(self.image_file.read())).group(0)

    @property
    def iso(self):
        isoRE = re.compile("(ISO)")
        return isoRE.search(str(self.image_file.read())).group(0)
    
    @property
    def SN(self):
        snRE = re.compile("([1-9]\d{6})")
        return snRE.search(str(self.image_file.read())).group(0)

        
imagen = NEFImage(imagePath)
# print (imagen)
# print(imagen.date)
# print(imagen.model)
# print(imagen.iso)
# print(imagen.SN)
print(imagen.direction)


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
tags = {0:"GPSVersionID", 1:"GPSLatitudeRef", 2:"GPSLatitude", 3:"GPSLongitudeRef", 4:"GPSLongitude", 5:"GPSAltitudeRef", 6:"GPSAltitude", 7:"GPSTimeStamp", 8:"GPSSatellites", 9:"GPSStatus", 10:"GPSMeasureMode", 11:"GPSDOP", 12:"GPSSpeedRef", 13:"GPSSpeed", 14:"GPSTrackRef", 15:"GPSTrack", 16:"GPSImgDirectionRef", 17:"GPSImgDirection", 18:"GPSMapDatum", 19:"GPSDestLatitudeRef", 20:"GPSDestLatitude", 21:"GPSDestLongitudeRef", 22:"GPSDestLongitude", 23:"GPSDestBearingRef", 24:"GPSDestBearing", 25:"GPSDestDistanceRef", 26:"GPSDestDistance", 27:"GPSProcessingMethod", 28:"GPSAreaInformation", 29:"GPSDateStamp", 30:"GPSDifferential", 254:"NewSubfileType", 255:"SubfileType", 256:"ImageWidth", 257:"ImageLength", 258:"BitsPerSample", 259:"Compression", 262:"PhotometricInterpretation", 263:"Threshholding", 264:"CellWidth", 265:"CellLength", 266:"FillOrder", 269:"DocumentName", 270:"ImageDescription", 271:"Make", 272:"Model", 273:"StripOffsets", 274:"Orientation", 277:"SamplesPerPixel", 278:"RowsPerStrip", 279:"StripByteCounts", 280:"MinSampleValue", 281:"MaxSampleValue", 282:"XResolution", 283:"YResolution", 284:"PlanarConfiguration", 285:"PageName", 286:"XPosition", 287:"YPosition", 288:"FreeOffsets", 289:"FreeByteCounts", 290:"GrayResponseUnit", 291:"GrayResponseCurve", 292:"T4Options", 293:"T6Options", 296:"ResolutionUnit", 297:"PageNumber", 301:"TransferFunction", 305:"Software", 306:"DateTime", 315:"Artist", 316:"HostComputer", 317:"Predictor", 318:"WhitePoint", 319:"PrimaryChromaticities", 320:"ColorMap", 321:"HalftoneHints", 322:"TileWidth", 323:"TileLength", 324:"TileOffsets", 325:"TileByteCounts", 326:"BadFaxLines", 327:"CleanFaxData", 328:"ConsecutiveBadFaxLines", 330:"SubIFDs", 332:"InkSet", 333:"InkNames", 334:"NumberOfInks", 336:"DotRange", 337:"TargetPrinter", 338:"ExtraSamples", 339:"SampleFormat", 340:"SMinSampleValue", 341:"SMaxSampleValue", 342:"TransferRange", 343:"ClipPath", 344:"XClipPathUnits", 345:"YClipPathUnits", 346:"Indexed", 347:"JPEGTables", 351:"OPIProxy", 400:"GlobalParametersIFD", 401:"ProfileType", 402:"FaxProfile", 403:"CodingMethods", 404:"VersionYear", 405:"ModeNumber", 433:"Decode", 434:"DefaultImageColor", 512:"JPEGProc", 513:"JPEGInterchangeFormat", 514:"JPEGInterchangeFormatLength", 515:"JPEGRestartInterval", 517:"JPEGLosslessPredictors", 518:"JPEGPointTransforms", 519:"JPEGQTables", 520:"JPEGDCTables", 521:"JPEGACTables", 529:"YCbCrCoefficients", 530:"YCbCrSubSampling", 531:"YCbCrPositioning", 532:"ReferenceBlackWhite", 559:"StripRowCounts", 700:"XMP", 18246:"Image.Rating", 18249:"Image.RatingPercent", 32781:"ImageID", 32932:"Wang Annotation", 33421:"CFARepeatPatternDim", 33422:"CFAPattern", 33423:"BatteryLevel", 33432:"Copyright", 33434:"ExposureTime", 33437:"FNumber", 33445:"MD FileTag", 33446:"MD ScalePixel", 33447:"MD ColorTable", 33448:"MD LabName", 33449:"MD SampleInfo", 33450:"MD PrepDate", 33451:"MD PrepTime", 33452:"MD FileUnits", 33550:"ModelPixelScaleTag", 33723:"IPTC/NAA", 33918:"INGR Packet Data Tag", 33919:"INGR Flag Registers", 33920:"IrasB Transformation Matrix", 33922:"ModelTiepointTag", 34016:"Site", 34017:"ColorSequence", 34018:"IT8Header", 34019:"RasterPadding", 34020:"BitsPerRunLength", 34021:"BitsPerExtendedRunLength", 34022:"ColorTable", 34023:"ImageColorIndicator", 34024:"BackgroundColorIndicator", 34025:"ImageColorValue", 34026:"BackgroundColorValue", 34027:"PixelIntensityRange", 34028:"TransparencyIndicator", 34029:"ColorCharacterization", 34030:"HCUsage", 34031:"TrapIndicator", 34032:"CMYKEquivalent", 34033:"Reserved", 34034:"Reserved", 34035:"Reserved", 34264:"ModelTransformationTag", 34377:"Photoshop", 34665:"Exif IFD", 34675:"InterColorProfile", 34732:"ImageLayer", 34735:"GeoKeyDirectoryTag", 34736:"GeoDoubleParamsTag", 34737:"GeoAsciiParamsTag", 34850:"ExposureProgram", 34852:"SpectralSensitivity", 34853:"GPSInfo", 34855:"ISOSpeedRatings", 34856:"OECF", 34857:"Interlace", 34858:"TimeZoneOffset", 34859:"SelfTimeMode", 34864:"SensitivityType", 34865:"StandardOutputSensitivity", 34866:"RecommendedExposureIndex", 34867:"ISOSpeed", 34868:"ISOSpeedLatitudeyyy", 34869:"ISOSpeedLatitudezzz", 34908:"HylaFAX FaxRecvParams", 34909:"HylaFAX FaxSubAddress", 34910:"HylaFAX FaxRecvTime", 36864:"ExifVersion", 36867:"DateTimeOriginal", 36868:"DateTimeDigitized", 37121:"ComponentsConfiguration", 37122:"CompressedBitsPerPixel", 37377:"ShutterSpeedValue", 37378:"ApertureValue", 37379:"BrightnessValue", 37380:"ExposureBiasValue", 37381:"MaxApertureValue", 37382:"SubjectDistance", 37383:"MeteringMode", 37384:"LightSource", 37385:"Flash", 37386:"FocalLength", 37387:"FlashEnergy", 37388:"SpatialFrequencyResponse", 37389:"Noise", 37390:"FocalPlaneXResolution", 37391:"FocalPlaneYResolution", 37392:"FocalPlaneResolutionUnit", 37393:"ImageNumber", 37394:"SecurityClassification", 37395:"ImageHistory", 37396:"SubjectLocation", 37397:"ExposureIndex", 37398:"TIFF/EPStandardID", 37399:"SensingMethod", 37500:"MakerNote", 37510:"UserComment", 37520:"SubsecTime", 37521:"SubsecTimeOriginal", 37522:"SubsecTimeDigitized", 37724:"ImageSourceData", 40091:"XPTitle", 40092:"XPComment", 40093:"XPAuthor", 40094:"XPKeywords", 40095:"XPSubject", 40960:"FlashpixVersion", 40961:"ColorSpace", 40962:"PixelXDimension", 40963:"PixelYDimension", 40964:"RelatedSoundFile", 40965:"Interoperability IFD", 41483:"FlashEnergy", 41484:"SpatialFrequencyResponse", 41486:"FocalPlaneXResolution", 41487:"FocalPlaneYResolution", 41488:"FocalPlaneResolutionUnit", 41492:"SubjectLocation", 41493:"ExposureIndex", 41495:"SensingMethod", 41728:"FileSource", 41729:"SceneType", 41730:"CFAPattern", 41985:"CustomRendered", 41986:"ExposureMode", 41987:"WhiteBalance", 41988:"DigitalZoomRatio", 41989:"FocalLengthIn35mmFilm", 41990:"SceneCaptureType", 41991:"GainControl", 41992:"Contrast", 41993:"Saturation", 41994:"Sharpness", 41995:"DeviceSettingDescription", 41996:"SubjectDistanceRange", 42016:"ImageUniqueID", 42032:"CameraOwnerName", 42033:"BodySerialNumber", 42034:"LensSpecification", 42035:"LensMake", 42036:"LensModel", 42037:"LensSerialNumber", 42112:"GDAL_METADATA", 42113:"GDAL_NODATA", 48129:"PixelFormat", 48130:"Transformation", 48131:"Uncompressed", 48132:"ImageType", 48256:"ImageWidth", 48257:"ImageHeight", 48258:"WidthResolution", 48259:"HeightResolution", 48320:"ImageOffset", 48321:"ImageByteCount", 48322:"AlphaOffset", 48323:"AlphaByteCount", 48324:"ImageDataDiscard", 48325:"AlphaDataDiscard", 50215:"Oce Scanjob Description", 50216:"Oce Application Selector", 50217:"Oce Identification Number", 50218:"Oce ImageLogic Characteristics", 50341:"PrintImageMatching", 50706:"DNGVersion", 50707:"DNGBackwardVersion", 50708:"UniqueCameraModel", 50709:"LocalizedCameraModel", 50710:"CFAPlaneColor", 50711:"CFALayout", 50712:"LinearizationTable", 50713:"BlackLevelRepeatDim", 50714:"BlackLevel", 50715:"BlackLevelDeltaH", 50716:"BlackLevelDeltaV", 50717:"WhiteLevel", 50718:"DefaultScale", 50719:"DefaultCropOrigin", 50720:"DefaultCropSize", 50721:"ColorMatrix1", 50722:"ColorMatrix2", 50723:"CameraCalibration1", 50724:"CameraCalibration2", 50725:"ReductionMatrix1", 50726:"ReductionMatrix2", 50727:"AnalogBalance", 50728:"AsShotNeutral", 50729:"AsShotWhiteXY", 50730:"BaselineExposure", 50731:"BaselineNoise", 50732:"BaselineSharpness", 50733:"BayerGreenSplit", 50734:"LinearResponseLimit", 50735:"CameraSerialNumber", 50736:"LensInfo", 50737:"ChromaBlurRadius", 50738:"AntiAliasStrength", 50739:"ShadowScale", 50740:"DNGPrivateData", 50741:"MakerNoteSafety", 50778:"CalibrationIlluminant1", 50779:"CalibrationIlluminant2", 50780:"BestQualityScale", 50781:"RawDataUniqueID", 50784:"Alias Layer Metadata", 50827:"OriginalRawFileName", 50828:"OriginalRawFileData", 50829:"ActiveArea", 50830:"MaskedAreas", 50831:"AsShotICCProfile", 50832:"AsShotPreProfileMatrix", 50833:"CurrentICCProfile", 50834:"CurrentPreProfileMatrix", 50879:"ColorimetricReference", 50931:"CameraCalibrationSignature", 50932:"ProfileCalibrationSignature", 50933:"ExtraCameraProfiles", 50934:"AsShotProfileName", 50935:"NoiseReductionApplied", 50936:"ProfileName", 50937:"ProfileHueSatMapDims", 50938:"ProfileHueSatMapData1", 50939:"ProfileHueSatMapData2", 50940:"ProfileToneCurve", 50941:"ProfileEmbedPolicy", 50942:"ProfileCopyright", 50964:"ForwardMatrix1", 50965:"ForwardMatrix2", 50966:"PreviewApplicationName", 50967:"PreviewApplicationVersion", 50968:"PreviewSettingsName", 50969:"PreviewSettingsDigest", 50970:"PreviewColorSpace", 50971:"PreviewDateTime", 50972:"RawImageDigest", 50973:"OriginalRawFileDigest", 50974:"SubTileBlockSize", 50975:"RowInterleaveFactor", 50981:"ProfileLookTableDims", 50982:"ProfileLookTableData", 51008:"OpcodeList1", 51009:"OpcodeList2", 51022:"OpcodeList3", 51041:"NoiseProfile", 51089:"OriginalDefaultFinalSize", 51090:"OriginalBestQualityFinalSize", 51091:"OriginalDefaultCropSize", 51107:"ProfileHueSatMapEncoding", 51108:"ProfileLookTableEncoding", 51109:"BaselineExposureOffset", 51110:"DefaultBlackRender", 51111:"NewRawImageDigest", 51112:"RawToPreviewGain", 51125:"DefaultUserCrop"}
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


def readTIFFData(typeData,count, slotSize = None):
    if typeData in [1,7]:
        structure = direction + "B"
        if typeData in [1]: bytesPerRead = 1
        if typeData in [7]: bytesPerRead = 1
    elif typeData in [2]:
        structure = direction + "c"
        if typeData in [2]: bytesPerRead = 1
    elif typeData in [3]:
        structure = direction + "H"
        if typeData in [3]: bytesPerRead = 2
    elif typeData in [4,5]:
        structure = direction + "L"
        if typeData in [4]: bytesPerRead = 4
        if typeData in [5]: bytesPerRead = 4
    elif typeData in [6]:
        structure = direction + "b"
        if typeData in [6]: bytesPerRead = 1
    elif typeData in [8]:
        structure = direction + "h"
        if typeData in [8]: bytesPerRead = 2
    elif typeData in [9,10]:
        structure = direction + "l"
        if typeData in [9]: bytesPerRead = 4
        if typeData in [10]: bytesPerRead = 4
    elif typeData in [11]:
        structure = direction + "f"
        if typeData in [11]: bytesPerRead = 4
    elif typeData in [12]:
        structure = direction + "f"
        if typeData in [12]: bytesPerRead = 8
    
    data = []
    read = 0
    totalReads = count
    if (typeData in [5, 10]): totalReads = count*2
    totalBytes = totalReads*bytesPerRead
    returnPos = 0
    if totalBytes>4:
        returnPos = image_file.tell()
        image_file.seek(readTIFFData(4,1))
        read = 4
    for _ in range(totalReads):
        data.append(struct.unpack(structure, image_file.read(bytesPerRead))[0])
        read += bytesPerRead
    if returnPos>0: 
        image_file.seek(returnPos+4)
    while ((slotSize != None) and (read < slotSize)):
        image_file.read(1)
        read +=1

    if typeData in [5,10]:
        i = 0
        returnValues = []
        while (i < len(data)):
            returnValues.append(data[i]/data[i+1])
            i+=2
        return returnValues

    if len(data)>1:     return data
    else:               return data[0]
    
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
   
