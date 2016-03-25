#!/bin/bash


# Theatre Signage Player installer
# 25th March 2016

echo "Installing Theatre Signage Player"

echo "Use raspi-config to expand filesystem and set graphics split etc."
pause
sudo raspi-config

echo "Updating system"

sudo apt-get update
sudo apt-get upgrade

echo  

sudo apt-get install

