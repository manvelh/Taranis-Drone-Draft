# Drone_Draft


To Start

	run Ubuntu 16.03 app

To Set Macros   

	Type "alias processONE='$PWD/singleScript.sh 2</dev/null' and hit Enter"
	Type "alias processMANY='$PWD/manyScript.sh 2</dev/null' and hit Enter"
	Type "alias splitMULTI='$PWD/splitMulti.sh.sh 2</dev/null' and hit Enter"

	or if you want shorter names ...

	Type "alias po='$PWD/singleScript.sh 2</dev/null' and hit Enter"
	Type "alias pm='$PWD/manyScript.sh 2</dev/null' and hit Enter"
	Type "alias sm='$PWD/splitMulti.sh.sh 2</dev/null' and hit Enter"

To process 1 KML
	
	save KML in Drone_Draft/Scripts/KML_Files folder on Google Earth and type "processONE" on the Ubuntu CL.
	Output should be finalPath.kml in Drone_Draft/Scripts/KML_Files/Processed folder.

To process > 1 KML

	save KML's in Drone_Draft/Scripts/KML_Files folder on Google Earth and type "processMANY" on the Ubuntu CL.
	Output should be in the Flights folder in Drone_Draft/Scripts/KML_Files/Processed folder.

To split Mulitpolygon KML's

	save KML('s) in Drone_Draft/Scripts/KML_Files folder on Google Earth and type "findDUPES" on Ubuntu CL.
	Output(s) should be in Drone_Draft folder with _(#Acres) attached to the end of their names.

To clear Ubuntu CL screen

	type "clear"

To Exit
	
	type "exit"
