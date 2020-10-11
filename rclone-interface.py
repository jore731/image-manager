import lib.rclone as rclone
import tempfile
from pathlib import Path
configString = """[DriveUC3M]
type = drive
client_id = 38903671259-n3jdtg8eddng16vh4r623p7uqihdelti.apps.googleusercontent.com
client_secret = L3do6wC-9THj8ofK86HtkHQC
scope = drive
token = {"access_token":"ya29.a0AfH6SMCD5Z_Pv2jeSvJWjKtL3hIoEWnVTvM7TQdLtJaGN6W_bSNl_Zk5FBCg1-3hFYXHJAMwKdl1F4rA3k4gxT3NQItBLj4smfYYJCkz9hU1672Zwo-bSEu8DBU38cHPZTDEPmiV5Zr4spFu_ssTre11i04bntCjAWmnkA","token_type":"Bearer","refresh_token":"1//03tXWxkV9IvvLCgYIARAAGAMSNwF-L9Irdvbm7qCSlJ9eDNy3HYb0rrH_NCFTAJYibx24ANWSKdik1NJ95JUEg0BulRZxncZ9eeQ","expiry":"2020-09-10T06:00:02.7060503+02:00"}
root_folder_id = 0AAIeFiIcsmiwUk9PVA"""

tempFolder = tempfile.TemporaryDirectory()
configFile = Path(tempFolder.name,"config.txt")
with open(configFile, "w") as confFile:
    confFile.write(configString)

rcloneHandler = rclone.RCloneWrapper(configString)

def analyzeFromRClone(url, RCloneHandler):
    with tempfile.NamedTemporaryFile(mode="wb",delete=True, dir=tempFolder.name) as tempFile:
        RCloneHandler.copy(url, tempFolder.name)
        print(tempFolder.name)
        #tempFile.write(data)
        input("waiting")

analyzeFromRClone("DriveUC3M:00 Colocar/01 Multimedia sin organizar/2001/04/28/desconocido/vcm_s_kf_repr_832x624.jpg",rcloneHandler)
# def analyzePicture(self,url):
#         path = Path(url.path()[1:])
#         try:
#             NEF = tiffreader.NEFImage(path)
#         except ValueError as err:
#             # print(format(err))
#             return
#         relPath = NEF.relocatePath(os.path.dirname(NEF.imagePath), ["capyear", "capmonth", "capday", "capdevice"])
#         self.createDir(relPath)
#         relFile = os.path.join(relPath,NEF.fileName)
#         print(relFile)
#         shutil.copy2(NEF.imagePath, relFile)