#!/usr/bin/python3
import sys
import subprocess
import datetime

    
def getPackageName(packageName):
    apps = subprocess.getoutput("adb shell pm list packages -f "+packageName+" | tr '=' '\t' | rev | awk '{print $1}' | rev")
    packages = apps.splitlines()
    packagesQuantity = packages.__len__()
    if (packagesQuantity > 1):
        print(apps)
        response = input('Are you sure you want to download '+str(packagesQuantity)+' apps [y/n] \n')
        if (response == 'y'):
            return packages
        elif(response == 'n'):
            exit()
        else:
            print('incorrect input')  
    return packages

def getAPK(packageNames):
    #banner('No APK found')
    print(packageNames)
    for packageName in packageNames:
        path = subprocess.getoutput("adb shell pm path "+packageName+" | tr ':' '\t' | awk '{print $2}'")
        splitAPK = path.splitlines()
        time = datetime.datetime.now().strftime("%Y-%m-%d-%H:%M:%S")
        if(splitAPK.__len__() > 1):
            for apps in splitAPK:
                splitAPKName = subprocess.getoutput("echo "+apps+"| tr '==/' '\t' | rev| awk '{print $1}' | rev")
                fileName = "./"+packageName+"-"+time+splitAPKName
                subprocess.run(["adb", "pull",apps,fileName])
        else:
            fileName = "./"+packageName+"-"+time+".apk"
            subprocess.run(["adb", "pull",path,fileName])

def getFiles(packageNames):
    for package in packageNames:
        sdcardPath = "sdcard/"+package+""
        dataPath = "/data/data/"+package+"/"
        subprocess.getoutput("adb shell su -c 'mkdir "+sdcardPath+"'")
        subprocess.getoutput("adb shell su -c 'cp -r "+dataPath+" "+sdcardPath+"'")
        subprocess.getoutput("adb pull "+sdcardPath+" "+package+"")
        subprocess.getoutput("adb shell su -c 'rm -rf "+sdcardPath+"'")

def banner(text):
    print("""              
     _    ____  _  __  _____      _                  _             
    / \  |  _ \| |/ / | ____|_  _| |_ _ __ __ _  ___| |_ ___  _ __ 
   / _ \ | |_) | ' /  |  _| \ \/ / __| '__/ _` |/ __| __/ _ \| '__|
  / ___ \|  __/| . \  | |___ >  <| |_| | | (_| | (__| || (_) | |   
 /_/   \_\_|   |_|\_\ |_____/_/\_\\___|_|  \__,_|\___|\__\___/|_|                                                                   

        """+text+"""                                        

        -h: help
        -d: Download an APK <App Name>
        -f: Download APK files <App Name>
        example: ./apkExtractor.py <App Name> # download both the APK and it files
        example: ./apkExtractor.py -f <App Name>
       """)

def main(argv):
    if(argv[0]=='-d'):
        packageName = getPackageName(argv[1])
        getAPK(packageName)            
    elif(argv[0]=='-f'):
        packageName = getPackageName(argv[1])
        getFiles(packageName)
    elif(argv[0]=='-h'):
        banner('')
    else:
        packageName = getPackageName(argv[0])
        getAPK(packageName)
        getFiles(packageName)

    sys.exit()

if __name__ == "__main__":    
    if(sys.argv.__len__()>1):
        main(sys.argv[1:])
    else:
       banner('')

