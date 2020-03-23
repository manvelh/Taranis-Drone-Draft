from pynput.keyboard import Key, Controller
import time
keyboard = Controller()


class Transformer:
    @staticmethod
    def transKML(kmlType):
        commandDict = {
            #Access bash shell
            "bashInto":"bash",
            #Say some kind of message
            "message": "echo Hello in Bash",
            #Transform KML.kml into poly.json
            "processPoly": "ogr2ogr -f GeoJSON poly.json KML.kml",
            #Transform LL.kml into ll.json
            "processLL": "ogr2ogr -f GeoJSON ll.json LL.kml",
            #Run Python Script for FPA.py without LL.kml
            "processFlightPlanWO": "python3 FPA.py 1",
            #Run Python Script for FPA.py with LL.kml
            "processFlightPlanW": "python3 FPA.py 0",
            #Transform finalPath.json to finalPath.kml
            "processFP": "ogr2ogr -f KML finalPath.kml finalPath.json",
            
            #Exit bash or powerhsell
            "getOut": "exit"
        }


        if kmlType == "opening":
            keyboard.press(Key.cmd)
            keyboard.release(Key.cmd)

            time.sleep(1)

            for command in commandDict["bashInto"]:
                for ch in command:
                    keyboard.press(ch)
                    keyboard.release(ch)
            time.sleep(.5)
            keyboard.press(Key.enter)
            keyboard.release(Key.enter)

        elif kmlType == "LL":
            time.sleep(.5)
            keyboard.press(Key.enter)
            keyboard.release(Key.enter)

            for command in commandDict["processLL"]:
                for ch in command:
#                    time.sleep(.01)
                    keyboard.press(ch)
                    keyboard.release(ch)

            time.sleep(.5)
            keyboard.press(Key.enter)
            keyboard.release(Key.enter)
            

        elif kmlType == "Poly":
            time.sleep(.5)
            for command in commandDict["processPoly"]:
                for ch in command:
 #                   time.sleep(.01)
                    keyboard.press(ch)
                    keyboard.release(ch)
            time.sleep(.5)
            keyboard.press(Key.enter)
            keyboard.release(Key.enter)

        elif kmlType == "3DPathWO":
            time.sleep(.5)
            for command in commandDict["processFlightPlanWO"]:
                for ch in command:
  #                  time.sleep(.01)
                    keyboard.press(ch)
                    keyboard.release(ch)
       
            time.sleep(.5)
            keyboard.press(Key.enter)
            keyboard.release(Key.enter)

        elif kmlType == "3DPathW":
            time.sleep(.5)
            for command in commandDict["processFlightPlanW"]:
                for ch in command:
   #                 time.sleep(.05)
                    keyboard.press(ch)
                    keyboard.release(ch)
       
            time.sleep(.5)
            keyboard.press(Key.enter)
            keyboard.release(Key.enter)


        elif kmlType == "3DFinal":
            time.sleep(.5)
            for command in commandDict["processFP"]:
                for ch in command:
    #                time.sleep(.05)
                    keyboard.press(ch)
                    keyboard.release(ch)
       
            time.sleep(.5)
            keyboard.press(Key.enter)
            keyboard.release(Key.enter)
 

        elif kmlType == "exiting":
            time.sleep(.5)
            for command in commandDict["getOut"]:
                for ch in command:
     #               time.sleep(.01)
                    keyboard.press(ch)
                    keyboard.release(ch)

            time.sleep(.5)
            keyboard.press(Key.enter)
            keyboard.release(Key.enter)
