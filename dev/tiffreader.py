import os
import logging
import struct
import json
import time

class tagsIFD:
    def __init__(self):
        pass

class TIFFImage:

    @property
    def tags(self):
        return {0:'GPSVersionID', 1:'GPSLatitudeRef', 2:'GPSLatitude', 3:'GPSLongitudeRef', 4:'GPSLongitude', 5:'GPSAltitudeRef', 6:'GPSAltitude', 7:'GPSTimeStamp', 8:'GPSSatellites', 9:'GPSStatus', 10:'GPSMeasureMode', 11:'GPSDOP', 12:'GPSSpeedRef', 13:'GPSSpeed', 14:'GPSTrackRef', 15:'GPSTrack', 16:'GPSImgDirectionRef', 17:'GPSImgDirection', 18:'GPSMapDatum', 19:'GPSDestLatitudeRef', 20:'GPSDestLatitude', 21:'GPSDestLongitudeRef', 22:'GPSDestLongitude', 23:'GPSDestBearingRef', 24:'GPSDestBearing', 25:'GPSDestDistanceRef', 26:'GPSDestDistance', 27:'GPSProcessingMethod', 28:'GPSAreaInformation', 29:'GPSDateStamp', 30:'GPSDifferential', 254:'NewSubfileType', 255:'SubfileType', 256:'ImageWidth', 257:'ImageLength', 258:'BitsPerSample', 259:'Compression', 262:'PhotometricInterpretation', 263:'Threshholding', 264:'CellWidth', 265:'CellLength', 266:'FillOrder', 269:'DocumentName', 270:'ImageDescription', 271:'Make', 272:'Model', 273:'StripOffsets', 274:'Orientation', 277:'SamplesPerPixel', 278:'RowsPerStrip', 279:'StripByteCounts', 280:'MinSampleValue', 281:'MaxSampleValue', 282:'XResolution', 283:'YResolution', 284:'PlanarConfiguration', 285:'PageName', 286:'XPosition', 287:'YPosition', 288:'FreeOffsets', 289:'FreeByteCounts', 290:'GrayResponseUnit', 291:'GrayResponseCurve', 292:'T4Options', 293:'T6Options', 296:'ResolutionUnit', 297:'PageNumber', 301:'TransferFunction', 305:'Software', 306:'DateTime', 315:'Artist', 316:'HostComputer', 317:'Predictor', 318:'WhitePoint', 319:'PrimaryChromaticities', 320:'ColorMap', 321:'HalftoneHints', 322:'TileWidth', 323:'TileLength', 324:'TileOffsets', 325:'TileByteCounts', 326:'BadFaxLines', 327:'CleanFaxData', 328:'ConsecutiveBadFaxLines', 330:'SubIFDs', 332:'InkSet', 333:'InkNames', 334:'NumberOfInks', 336:'DotRange', 337:'TargetPrinter', 338:'ExtraSamples', 339:'SampleFormat', 340:'SMinSampleValue', 341:'SMaxSampleValue', 342:'TransferRange', 343:'ClipPath', 344:'XClipPathUnits', 345:'YClipPathUnits', 346:'Indexed', 347:'JPEGTables', 351:'OPIProxy', 400:'GlobalParametersIFD', 401:'ProfileType', 402:'FaxProfile', 403:'CodingMethods', 404:'VersionYear', 405:'ModeNumber', 433:'Decode', 434:'DefaultImageColor', 512:'JPEGProc', 513:'JPEGInterchangeFormat', 514:'JPEGInterchangeFormatLength', 515:'JPEGRestartInterval', 517:'JPEGLosslessPredictors', 518:'JPEGPointTransforms', 519:'JPEGQTables', 520:'JPEGDCTables', 521:'JPEGACTables', 529:'YCbCrCoefficients', 530:'YCbCrSubSampling', 531:'YCbCrPositioning', 532:'ReferenceBlackWhite', 559:'StripRowCounts', 700:'XMP', 18246:'Image.Rating', 18249:'Image.RatingPercent', 32781:'ImageID', 32932:'Wang_Annotation', 33421:'CFARepeatPatternDim', 33422:'CFAPattern', 33423:'BatteryLevel', 33432:'Copyright', 33434:'ExposureTime', 33437:'FNumber', 33445:'MD_FileTag', 33446:'MD_ScalePixel', 33447:'MD_ColorTable', 33448:'MD_LabName', 33449:'MD_SampleInfo', 33450:'MD_PrepDate', 33451:'MD_PrepTime', 33452:'MD_FileUnits', 33550:'ModelPixelScaleTag', 33723:'IPTC_NAA', 33918:'INGR_Packet_Data_Tag', 33919:'INGR_Flag_Registers', 33920:'IrasB_Transformation_Matrix', 33922:'ModelTiepointTag', 34016:'Site', 34017:'ColorSequence', 34018:'IT8Header', 34019:'RasterPadding', 34020:'BitsPerRunLength', 34021:'BitsPerExtendedRunLength', 34022:'ColorTable', 34023:'ImageColorIndicator', 34024:'BackgroundColorIndicator', 34025:'ImageColorValue', 34026:'BackgroundColorValue', 34027:'PixelIntensityRange', 34028:'TransparencyIndicator', 34029:'ColorCharacterization', 34030:'HCUsage', 34031:'TrapIndicator', 34032:'CMYKEquivalent', 34033:'Reserved', 34034:'Reserved', 34035:'Reserved', 34264:'ModelTransformationTag', 34377:'Photoshop', 34665:'Exif_IFD', 34675:'InterColorProfile', 34732:'ImageLayer', 34735:'GeoKeyDirectoryTag', 34736:'GeoDoubleParamsTag', 34737:'GeoAsciiParamsTag', 34850:'ExposureProgram', 34852:'SpectralSensitivity', 34853:'GPSInfo', 34855:'ISOSpeedRatings', 34856:'OECF', 34857:'Interlace', 34858:'TimeZoneOffset', 34859:'SelfTimeMode', 34864:'SensitivityType', 34865:'StandardOutputSensitivity', 34866:'RecommendedExposureIndex', 34867:'ISOSpeed', 34868:'ISOSpeedLatitudeyyy', 34869:'ISOSpeedLatitudezzz', 34908:'HylaFAX_FaxRecvParams', 34909:'HylaFAX_FaxSubAddress', 34910:'HylaFAX_FaxRecvTime', 36864:'ExifVersion', 36867:'DateTimeOriginal', 36868:'DateTimeDigitized', 37121:'ComponentsConfiguration', 37122:'CompressedBitsPerPixel', 37377:'ShutterSpeedValue', 37378:'ApertureValue', 37379:'BrightnessValue', 37380:'ExposureBiasValue', 37381:'MaxApertureValue', 37382:'SubjectDistance', 37383:'MeteringMode', 37384:'LightSource', 37385:'Flash', 37386:'FocalLength', 37387:'FlashEnergy', 37388:'SpatialFrequencyResponse', 37389:'Noise', 37390:'FocalPlaneXResolution', 37391:'FocalPlaneYResolution', 37392:'FocalPlaneResolutionUnit', 37393:'ImageNumber', 37394:'SecurityClassification', 37395:'ImageHistory', 37396:'SubjectLocation', 37397:'ExposureIndex', 37398:'TIFF_EPStandardID', 37399:'SensingMethod', 37500:'MakerNote', 37510:'UserComment', 37520:'SubsecTime', 37521:'SubsecTimeOriginal', 37522:'SubsecTimeDigitized', 37724:'ImageSourceData', 40091:'XPTitle', 40092:'XPComment', 40093:'XPAuthor', 40094:'XPKeywords', 40095:'XPSubject', 40960:'FlashpixVersion', 40961:'ColorSpace', 40962:'PixelXDimension', 40963:'PixelYDimension', 40964:'RelatedSoundFile', 40965:'Interoperability_IFD', 41483:'FlashEnergy', 41484:'SpatialFrequencyResponse', 41486:'FocalPlaneXResolution', 41487:'FocalPlaneYResolution', 41488:'FocalPlaneResolutionUnit', 41492:'SubjectLocation', 41493:'ExposureIndex', 41495:'SensingMethod', 41728:'FileSource', 41729:'SceneType', 41730:'CFAPattern', 41985:'CustomRendered', 41986:'ExposureMode', 41987:'WhiteBalance', 41988:'DigitalZoomRatio', 41989:'FocalLengthIn35mmFilm', 41990:'SceneCaptureType', 41991:'GainControl', 41992:'Contrast', 41993:'Saturation', 41994:'Sharpness', 41995:'DeviceSettingDescription', 41996:'SubjectDistanceRange', 42016:'ImageUniqueID', 42032:'CameraOwnerName', 42033:'BodySerialNumber', 42034:'LensSpecification', 42035:'LensMake', 42036:'LensModel', 42037:'LensSerialNumber', 42112:'GDAL_METADATA', 42113:'GDAL_NODATA', 48129:'PixelFormat', 48130:'Transformation', 48131:'Uncompressed', 48132:'ImageType', 48256:'ImageWidth', 48257:'ImageHeight', 48258:'WidthResolution', 48259:'HeightResolution', 48320:'ImageOffset', 48321:'ImageByteCount', 48322:'AlphaOffset', 48323:'AlphaByteCount', 48324:'ImageDataDiscard', 48325:'AlphaDataDiscard', 50215:'Oce_Scanjob_Description', 50216:'Oce_Application_Selector', 50217:'Oce_Identification_Number', 50218:'Oce_ImageLogic_Characteristics', 50341:'PrintImageMatching', 50706:'DNGVersion', 50707:'DNGBackwardVersion', 50708:'UniqueCameraModel', 50709:'LocalizedCameraModel', 50710:'CFAPlaneColor', 50711:'CFALayout', 50712:'LinearizationTable', 50713:'BlackLevelRepeatDim', 50714:'BlackLevel', 50715:'BlackLevelDeltaH', 50716:'BlackLevelDeltaV', 50717:'WhiteLevel', 50718:'DefaultScale', 50719:'DefaultCropOrigin', 50720:'DefaultCropSize', 50721:'ColorMatrix1', 50722:'ColorMatrix2', 50723:'CameraCalibration1', 50724:'CameraCalibration2', 50725:'ReductionMatrix1', 50726:'ReductionMatrix2', 50727:'AnalogBalance', 50728:'AsShotNeutral', 50729:'AsShotWhiteXY', 50730:'BaselineExposure', 50731:'BaselineNoise', 50732:'BaselineSharpness', 50733:'BayerGreenSplit', 50734:'LinearResponseLimit', 50735:'CameraSerialNumber', 50736:'LensInfo', 50737:'ChromaBlurRadius', 50738:'AntiAliasStrength', 50739:'ShadowScale', 50740:'DNGPrivateData', 50741:'MakerNoteSafety', 50778:'CalibrationIlluminant1', 50779:'CalibrationIlluminant2', 50780:'BestQualityScale', 50781:'RawDataUniqueID', 50784:'Alias_Layer_Metadata', 50827:'OriginalRawFileName', 50828:'OriginalRawFileData', 50829:'ActiveArea', 50830:'MaskedAreas', 50831:'AsShotICCProfile', 50832:'AsShotPreProfileMatrix', 50833:'CurrentICCProfile', 50834:'CurrentPreProfileMatrix', 50879:'ColorimetricReference', 50931:'CameraCalibrationSignature', 50932:'ProfileCalibrationSignature', 50933:'ExtraCameraProfiles', 50934:'AsShotProfileName', 50935:'NoiseReductionApplied', 50936:'ProfileName', 50937:'ProfileHueSatMapDims', 50938:'ProfileHueSatMapData1', 50939:'ProfileHueSatMapData2', 50940:'ProfileToneCurve', 50941:'ProfileEmbedPolicy', 50942:'ProfileCopyright', 50964:'ForwardMatrix1', 50965:'ForwardMatrix2', 50966:'PreviewApplicationName', 50967:'PreviewApplicationVersion', 50968:'PreviewSettingsName', 50969:'PreviewSettingsDigest', 50970:'PreviewColorSpace', 50971:'PreviewDateTime', 50972:'RawImageDigest', 50973:'OriginalRawFileDigest', 50974:'SubTileBlockSize', 50975:'RowInterleaveFactor', 50981:'ProfileLookTableDims', 50982:'ProfileLookTableData', 51008:'OpcodeList1', 51009:'OpcodeList2', 51022:'OpcodeList3', 51041:'NoiseProfile', 51089:'OriginalDefaultFinalSize', 51090:'OriginalBestQualityFinalSize', 51091:'OriginalDefaultCropSize', 51107:'ProfileHueSatMapEncoding', 51108:'ProfileLookTableEncoding', 51109:'BaselineExposureOffset', 51110:'DefaultBlackRender', 51111:'NewRawImageDigest', 51112:'RawToPreviewGain', 51125:'DefaultUserCrop'}
   


    def readTIFFData(self, typeData, count, slotSize=None):
        if typeData in [1, 7]:
            structure = self.direction + "B"
            if typeData in [1]:
                bytesPerRead = 1
            if typeData in [7]:
                bytesPerRead = 1
        elif typeData in [2]:
            structure = self.direction + "c"
            if typeData in [2]:
                bytesPerRead = 1
        elif typeData in [3]:
            structure = self.direction + "H"
            if typeData in [3]:
                bytesPerRead = 2
        elif typeData in [4, 5]:
            structure = self.direction + "L"
            if typeData in [4]:
                bytesPerRead = 4
            if typeData in [5]:
                bytesPerRead = 4
        elif typeData in [6]:
            structure = self.direction + "b"
            if typeData in [6]:
                bytesPerRead = 1
        elif typeData in [8]:
            structure = self.direction + "h"
            if typeData in [8]:
                bytesPerRead = 2
        elif typeData in [9, 10]:
            structure = self.direction + "l"
            if typeData in [9]:
                bytesPerRead = 4
            if typeData in [10]:
                bytesPerRead = 4
        elif typeData in [11]:
            structure = self.direction + "f"
            if typeData in [11]:
                bytesPerRead = 4
        elif typeData in [12]:
            structure = self.direction + "f"
            if typeData in [12]:
                bytesPerRead = 8

        data = []
        read = 0
        totalReads = count
        if (typeData in [5, 10]):
            totalReads = count*2
        totalBytes = totalReads*bytesPerRead
        returnPos = 0
        if totalBytes > 4:
            returnPos = self.image_file.tell()
            self.image_file.seek(self.readTIFFData(4, 1))
            read = 4
        for _ in range(totalReads):
            data.append(struct.unpack(
                structure, self.image_file.read(bytesPerRead))[0])
            read += bytesPerRead
        if returnPos > 0:
            self.image_file.seek(returnPos+4)
        while ((slotSize != None) and (read < slotSize)):
            self.image_file.read(1)
            read += 1

        if typeData in [5, 10]:
            i = 0
            returnValues = []
            while (i < len(data)):
                returnValues.append(data[i]/data[i+1])
                i += 2
            if len(returnValues) > 1:
                return returnValues
            else:
                return returnValues[0]
        if typeData in [2]:
            auxString=""
            for value in data:
                auxString += str(value)[2:-1]
            return auxString[0:-4]
        if len(data) > 1:
            return data
        else:
            return data[0]


class NEFImage(TIFFImage):
    def __init__(self, imagePath):
        self.fileName = os.path.basename(imagePath)
        splitted = self.fileName.split(".")
        self.extension = splitted[-1].lower()
        emptyString =""
        self.noExtName = emptyString.join(splitted[0:-1])
        # self.checkExtension()
        self.imagePath = imagePath
        self.findJSON()
        self._tags=[]
        self._numberOfTags=[]
        self.NoTIFFError = ValueError(
            f"{self.fileName} is not recognized as a TIFF file")
        
    def checkExtension(self):
        if not self.extension in ["nef","json"]:
            raise self.NoTIFFError
    
    def findJSON(self):
        jsonPath = os.path.join(os.path.dirname(self.imagePath),"JSON",f"{self.noExtName}.JSON")
        if os.path.isfile(jsonPath):
            self.jsonPath=jsonPath


    @property
    def direction(self):
        if not hasattr(self, "_direction"):
            pos = self.image_file.tell()
            self.image_file.seek(0)
            byteOrder = str(self.image_file.read(2))[2:-1]
            if byteOrder == "II":
                self._direction = "<"
            elif byteOrder == "MM":
                self._direction = ">"
            else:
                raise self.NoTIFFError
            self.image_file.seek(pos)
        return self._direction

    @property
    def image_file(self):
        if not hasattr(self, "_image_file"):
            self._image_file = open(f"{self.imagePath}", 'rb')
        return self._image_file

    @property
    def verifiyDirection(self):
        pos = self.image_file.tell()
        self.image_file.seek(2)
        result = self.readTIFFData(3,1)
        self.image_file.seek(pos)
        if result == 42:
            return 0
        else:
            raise self.NoTIFFError

    @property
    def offsetFirstIFD(self):
        if not hasattr(self,"_offsetFirstIFD"):
            pos = self.image_file.tell()
            self.image_file.seek(4)
            self._offsetFirstIFD = self.readTIFFData(4, 1)
            self.image_file.seek(pos)
        return self._offsetFirstIFD

    @property
    def firstIFD(self):
        if not hasattr(self,"_firstIFD"):
            pos = self.image_file.tell()
            self.image_file.seek(self.offsetFirstIFD)
            self._firstIFD = self.readTIFFData(4, 1)
            self.image_file.seek(pos)
        return self._firstIFD

    @property
    def numberOfTagsFirstIFD(self):
        if not hasattr(self,"_numberOfTagsFirstIFD"):
            pos = self.image_file.tell()
            self.image_file.seek(self.offsetFirstIFD)
            self._numberOfTagsFirstIFD = self.readTIFFData(3, 1)
            self.image_file.seek(pos)
        return self._numberOfTagsFirstIFD

    def getNumberOfTags(self, IFDId, offset):
        while len(self._numberOfTags)<(IFDId+1):
            self._numberOfTags.append(None)
        if self._numberOfTags[IFDId]==None:
            pos = self.image_file.tell()
            self.image_file.seek(offset)
            self._numberOfTags[IFDId] = self.readTIFFData(3, 1)
            self.image_file.seek(pos)
        return self._numberOfTags[IFDId]

    @property
    def tagsFirstIFD(self):
        if len(self._tags)==0:
            self._tags.append(tagsIFD())
            if hasattr(self, "jsonPath"):
                with open(self.jsonPath, "r") as json_file:
                    self._tags[0].__dict__.update(json.load(json_file))
            else:
                self.readIFD(0, self.offsetFirstIFD, self.numberOfTagsFirstIFD)

        return self._tags[0]
    

# @property
#     def tagsFirstIFD(self):
#         if not hasattr(self, "_tagsFirstIFD"):
#             self._tagsFirstIFD=tagsIFD()
#             if hasattr(self, "jsonPath"):
#                 with open(self.jsonPath, "r") as json_file:
#                     self._tagsFirstIFD.__dict__.update(json.load(json_file))
#             else:
#                 pos = self.image_file.tell()
#                 for tagIndex in range(self.numberOfTagsFirstIFD):
#                     self.image_file.seek(self.offsetFirstIFD+2+tagIndex*12)
#                     tag = 0
#                     while tag == 0:
#                         tag = self.readTIFFData(3, 1)
#                     if tag != 0:
#                         tag_type=self.readTIFFData(3,1)
#                         tag_count=self.readTIFFData(4,1)
#                         tag_value=self.readTIFFData(tag_type, tag_count, slotSize=4)
#                         if isinstance(tag_value, str):
#                             tag_value=tag_value.replace("\'", "\\\'")
#                             tag_value=tag_value.replace("\"", "\\\"")
#                             string=f"self._tagsFirstIFD.{self.tags[tag]} = \'{tag_value}\'"
#                         else:
#                             string=f"self._tagsFirstIFD.{self.tags[tag]} = {tag_value}"
#                         exec(string)
#                 self.image_file.seek(pos)
#         return self._tagsFirstIFD
    


    def readIFD(self,IFDId, offset, numberOfTags):
        while len(self._tags)<(IFDId+1):
            self._tags.append(tagsIFD())
        pos = self.image_file.tell()
        for tagIndex in range(numberOfTags):
            self.image_file.seek(offset+2+tagIndex*12)
            tag = 0
            while tag == 0:
                tag = self.readTIFFData(3, 1)
            if tag != 0:
                tag_type=self.readTIFFData(3,1)
                tag_count=self.readTIFFData(4,1)
                tag_value=self.readTIFFData(tag_type, tag_count, slotSize=4)
                if isinstance(tag_value, str):
                    tag_value=tag_value.replace("\'", "\\\'")
                    tag_value=tag_value.replace("\"", "\\\"")
                    string=f"self._tags[{IFDId}].{self.tags[tag]} = \'{tag_value}\'"
                else:
                    string=f"self._tags[{IFDId}].{self.tags[tag]} = {tag_value}"
                exec(string)
        self.image_file.seek(pos)
        return self._tags[IFDId]


    @property
    def capyear(self):
        if hasattr(self.tagsFirstIFD, "DateTimeOriginal"):
            return self.tagsFirstIFD.DateTimeOriginal.split(" ")[0].split(":")[0]
            
    @property
    def capmonth(self):
        if hasattr(self.tagsFirstIFD, "DateTimeOriginal"):
            return self.tagsFirstIFD.DateTimeOriginal.split(" ")[0].split(":")[1]

    @property
    def capday(self):
        if hasattr(self.tagsFirstIFD, "DateTimeOriginal"):
            return self.tagsFirstIFD.DateTimeOriginal.split(" ")[0].split(":")[2]

    @property
    def capdhour(self):
        if hasattr(self.tagsFirstIFD, "DateTimeOriginal"):
            return self.tagsFirstIFD.DateTimeOriginal.split(" ")[1].split(":")[0]

    @property
    def capmin(self):
        if hasattr(self.tagsFirstIFD, "DateTimeOriginal"):
            return self.tagsFirstIFD.DateTimeOriginal.split(" ")[1].split(":")[2]

    @property
    def capsec(self):
        if hasattr(self.tagsFirstIFD, "DateTimeOriginal"):
            return self.tagsFirstIFD.DateTimeOriginal.split(" ")[1].split(":")[2]

    @property
    def capdevice(self):
        if hasattr(self.tagsFirstIFD, "Model"):
            return self.tagsFirstIFD.Model


    def createJSON (self, outpath=""):
        if not os.path.isdir(outpath): os.mkdir(outpath)
        if outpath!="": outFile = outpath+"/"+self.noExtName
        else: outFile=self.noExtName
        with open(f'{outFile}.json', 'w') as outfile:
            json.dump(self.tagsFirstIFD.__dict__, outfile, indent=4, sort_keys=True)

    def relocatePath(self,outputRootPath="", parameters=[]):
        valid_parameters = ["capyear", "capmonth", "capday",
                            "caphour", "capmin", "capsec", "capdevice"]
        outpath = outputRootPath
        if outputRootPath != "" and (not outputRootPath[-1] in ["\\","/"]):
            outpath += "/"
        for parameter in parameters:
            if (parameter in valid_parameters) and getattr(self, parameter)!=None:
                outpath+=getattr(self, parameter)+"/"
            else:
                outpath+="UNKNOWN/"
        return outpath

    def readContent(self,IFDId):
        if hasattr(self._tags[IFDId],"StripOffsets") and hasattr(self._tags[IFDId],"StripByteCounts"):            
            self.image_file.seek(self._tags[IFDId].StripOffsets)
            return self.readTIFFData(1,self._tags[IFDId].StripByteCounts)
            #return self.image_file.read(self._tags[IFDId].StripByteCounts)

# import matplotlib.pyplot as plt
# import matplotlib.image as mpimg
# import numpy as np
# t=time.time_ns()
# imagen=NEFImage("00 test_images/test3.NEF")
# print(imagen.tagsFirstIFD.RowsPerStrip)
# data = imagen.readContent(0)
# matrix=[]
# for j in range(120):
#     row = []
#     for i in range (160):
#         row.append(np.array([data[j*i*3],data[j*i*3+1],data[j*i*3+2]]))
#     matrix.append(np.array(row))
# # with open(f"test{0}.tiff","w+") as file:
# #     file.write(data)

# image = mpimg.imread("00 test_images/test3.NEF")
# plt.imshow(image)
# plt.show()

# '''
import numpy as np
import matplotlib.pyplot as plt
imagePath="00 test_images/test2.tiff"
imagen=NEFImage(imagePath)
print(imagen.tagsFirstIFD.__dict__)
matrix = []
data2 = imagen.readContent(0)
print("data2 loaded")
for j in range(imagen.tagsFirstIFD.ImageLength):
    row = []
    for i in range(imagen.tagsFirstIFD.ImageWidth):
        pixel=[]
        for k in range(imagen.tagsFirstIFD.SamplesPerPixel):
            pixel.append(data2[k+imagen.tagsFirstIFD.SamplesPerPixel*(i+j*imagen.tagsFirstIFD.ImageWidth)])
        row.append(pixel)
    matrix.append(row)
plotable = np.array(matrix)
plt.imshow(plotable)
plt.show()
'''
import matplotlib.pyplot as plt
import PIL.Image
import numpy as np
imagefile = PIL.Image.open(imagePath)
a = np.array(imagefile)
print(imagen.tagsFirstIFD.SubIFDs)
tagsExif = imagen.getNumberOfTags(0,imagen.tagsFirstIFD.Exif_IFD)
subTags=[]
for index, subIFD in enumerate(imagen.tagsFirstIFD.SubIFDs):
    temp = imagen.getNumberOfTags(2+index,subIFD)
    while len(subTags)<index+1:
        subTags.append(tagsIFD)
    subTags[index] = imagen.readIFD(2+index,subIFD,temp)
    if hasattr(subTags[index],"JPEGInterchangeFormat") and hasattr(subTags[index],"JPEGInterchangeFormatLength") :
        imagen.image_file.seek(subTags[index].JPEGInterchangeFormat)
        # data = imagen.readTIFFData(7, subTags[0].JPEGInterchangeFormatLength)
        data = imagen.image_file.read(subTags[0].JPEGInterchangeFormatLength)
        with open(f"test{index}.jpeg","wb") as file:
            file.write(data)
    
imagen.image_file.seek(subTags[2].JPEGInterchangeFormat)
# data = imagen.readTIFFData(7, subTags[2].JPEGInterchangeFormatLength)
data = imagen.image_file.read(subTags[2].JPEGInterchangeFormatLength)
with open("test.jpeg","wb") as file:
    file.write(data)
input()
imagen.image_file.seek(imagen._tags[3].StripOffsets)
data2 = imagen.image_file.read(imagen._tags[3].StripByteCounts)
matrix=[]
for j in range(1,121):
    row = []
    for i in range(1,161):
        row.append([data2[j*i*3],data2[j*i*3+1],data2[j*i*3+2]])
    matrix.append(row)
plotable = np.array(matrix)

plt.imshow(plotable)
plt.show()
input()'''