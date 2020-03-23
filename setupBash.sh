#!/bin/bash
sudo apt-get update 
sudo apt-get upgrade 
sudo add-apt-repository ppa:ubuntugis/ppa
sudo apt-get update
sudo apt-get install gdal-bin
sudo apt-get install python3-gdal 
sudo apt-get install python3-numpy
sudo apt-get install python3-pip
pip3 install shapely==1.6.4
pip3 install pyproj==1.9.6
pip3 install geojson


