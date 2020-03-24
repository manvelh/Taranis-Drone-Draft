import os
import shutil
import webbrowser as wb
import re
import subprocess
from Transformer import Transformer
# import gdaltools

strDDD = '\DD_Directory'
strDKH = '\Download_KML_File_Here'
strDDI = '\Save_KML.kml&LL.kml_Here'
strPFP = '\Processed_FlightPlans'

dir_path = os.path.dirname(os.path.realpath(__file__))

if not os.path.exists(dir_path+'\DD_Directory'):
    os.makedirs(dir_path+'\DD_Directory')
    print("\nCREATED DD_DIRECTORY\n\nX\n")
else:
    print("\nDD_DIRECTORY DETECTED\n\n1\n")

MainDirectory = dir_path+'\DD_Directory'
 
if not os.path.exists(MainDirectory+'\Download_KML_File_Here'):
    os.makedirs(MainDirectory+'\Download_KML_File_Here')
    print("\nCREATED DOWNLOAD DIRECTORY\n\nX\n")
else:
    print("\nDOWNLOAD DIRECTORY DETECTED\n\n2\n")

DownloadDirectory = MainDirectory+'\Download_KML_File_Here'

if not os.path.exists(MainDirectory+'\Save_KML.kml&LL.kml_Here'):
    os.makedirs(MainDirectory+'\Save_KML.kml&LL.kml_Here')
    print("\nCREATED PROCESS DIRECTORY\n\nX\n")
else:
    print("\nPROCESS DIRECTORY DETECTED\n\n3\n")

ProcessDirectory = MainDirectory+'\Save_KML.kml&LL.kml_Here'

if not os.path.exists(MainDirectory+'\Processed_FlightPlans'):
    os.makedirs(MainDirectory+'\Processed_FlightPlans')
    print("\nCREATED POST DIRECTORY\n\nX\n")
else:
    print("\nPOST DIRECTORY DETECTED\n\n4\n")

PostDirectory = MainDirectory+'\Processed_FlightPlans'

# CHECK IF FILES EXIST WHERE THEY SHOULD
checkForFiles = os.listdir(DownloadDirectory)

if len(checkForFiles) < 1:    
    # PRINT STATEMENT TO INFORM USER THAT WHAT THEY NEED TO ACCHOMPLISH SO PROGRAM CAN CREATE THE 3D PATH
    print("\nNO FILES DETECTED IN %s\n\nPLEASE DOWNLOAD FROM ATLAS\n\nALSO MAKE SURE\n\n%s\n\nIS DEFAULT DOWNLOAD DIRECTORY FOR REMAINDER OF FLIGHT PLANNING\n" % (
        DownloadDirectory, DownloadDirectory))
    # OPENS TAB DIRECTLY TO THE ATLAS DASHBOARD
#    wb.open_new_tab(
#    'https:/taranis.atlassian.net/secure/RapidBoard.jspa?rapidView=117&projectKey=OPS')

else:
    print("\nFILES DETECTED in %s\n"%(DownloadDirectory))

    #KILLSWITCH
    j = 0
    while j < 1:

        pathToPolyJSON = ""
        pathToLLJSON = ""
        llcheck = 0

        Transformer.transKML("opening")

        #NOW WE CAN TRUST THE PROGRAM HAS THE CORRECT DIRECTORIS IN PLACE FOR MOVING FILES WITH SHUTIL
        for root, dirs, files in os.walk(ProcessDirectory):
            for theFile in files:
 #                   print("File is: ", theFile)
                    PolypostDownloadPath = ""
                    LLpostDownloadPath = ""
                    if theFile.startswith('KML.kml'):
#                        print(root)
                        PolypostDownloadPath = root+'/'+str(theFile)
 #                       print(PolypostDownloadPath)
                        
                        Transformer.transKML("Poly")
                        pathToPolyJSON = ProcessDirectory+'\poly.json'

                    if theFile.startswith("LL.kml"):
                        llcheck = 1
  #                      print(root)
                        LLpostDownloadPath = root+'/'+str(theFile)
   #                     print(LLpostDownloadPath)
                        
                        Transformer.transKML("LL")
                        pathToLLJSON = ProcessDirectory+'\ll.json'



#        print("\n\nPath to Poly JSON\n\n%s\n\nPath to LL JSON\n\n%s\n\nWas there a LL.kml?\n\n%s"%(pathToPolyJSON, pathToLLJSON, llcheck))
       

        if llcheck == 1:
            Transformer.transKML("3DPathW")
            Transformer.transKML("3DFinal")
        elif llcheck == 0:
            Transformer.transKML("3DPathWO")
            Transformer.transKML("3DFinal")


        Transformer.transKML("exiting")

        os.startfile(dir_path+'\DD_Directory/Save_KML.kml&LL.kml_Here/finalPath.kml')

        decision = str(input("\nReady to Upload to Litchi?\n"))
        
        if decision == 'Yes' or decision == 'Y' or decision == 'yes' or decision == 'y':
            wb.open_new_tab('https://www.flylitchi.com/hub')

            for root, dirs, files in os.walk(DownloadDirectory):
                    for theFile in files:
                            print("\nFiles in %s\n"%(DownloadDirectory))
                            print("\n\n%s\n\n"%(theFile[:len(theFile)-4]))


            decision = str(input("\nRe-Process?\n"))
            if decision == 'Yes' or decision == 'Y' or decision == 'yes' or decision == 'y':
                print("\n*** Re-Processing ***\n")
            else:
                print("\n***Ending Program***\n")
                j = 1



        if j < 1:
            print("*** Drone Draft Still Active ***")


