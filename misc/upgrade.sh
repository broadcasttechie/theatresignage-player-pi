#!/bin/bash

echo "Theatre Signage Player upgrader"


sudo apt-get update

sudo apt-get install -y xosd-bin

cd "$HOME/ts"

git pull

