from time import sleep
from datetime import datetime
from sh import gphoto2 as gp
import signal, os, subprocess


# kill gphoto2 process that starts
# whenever we connect the camera / Start raspbian
#def killgphoto2Process():
#  p = subprocess.Popen(['ps', '-A'], stdout=subprocess.PIPE)
#  out, err = p.communicate()
#
#  #search for the line that has the process
#  #we want to kill
#
#for line in out.splitlines():
#    if b'gvfsd-gphoto2' in line:
#        #Kill the process!
#        pid = int(line.split(None,1)[0])
#        os.kill(pid,signal.SIGKILL)

import psutil
def killgphoto2Process():
#PROCNAME = "gvfsd-gphoto2"

for proc in psutil.process_iter():
    # check whether the process name matches
    if proc.name() ="gvfsd-gphoto2":
        proc.kill()

        
shot_date = datetime.now().strftime("%Y-%m-%d")
shot_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
picID="Picontrolledcapture"

clearCommand = ["--folder", "/store_00020001/DCIM/103CANON", \
                "-R --delete-all-files"]
triggerCommand = ["--trigger-capture"]
downloadCommand = ["--get-all-files"]

folder_name = shot_date + picID
save_location = "/home/pi/gphoto2/images"+ folder_name

def createSaveFolder():
    try:
        os.makedirs(save_location)
    except:
        print("Failed to create the directory")
    os.chdir(save_location)

def captureImages():
    gp(triggerCommand)
    sleep(3) #time required to save the picture on the SD Card
    gp(downloadCommand)
    gp(clearCommand)

def renameFiles(ID):
    for filename in os.listdir("."):
        if len(filename) < 13:
            if filename.endswith(".JPG"):
                os.rename(filename,(shot_time + ID + ".JPG"))
                print("Renamed the JPG")
            elif filename.endswith(".CR2"):
                 os.rename(filename,(shot_time + ID + ".CR2"))
                 print("Renamed the CR2")



killgphoto2Process()  #finktuiniert nicht!
gp(clearCommand)      #funktionier tnicht!

while True:
                      createSaveFolder()
                      captureImages()
                      renameFiles(picID)
                      sleep(10) # time between two pcitures
