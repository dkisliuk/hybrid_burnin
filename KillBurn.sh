#!/bin/bash

sudo pkill -f "root -l RunTests.cpp"
sudo pkill -f "python Master.py"
sudo pkill -f "python HybridGUI"
sudo pkill -f "hsioPipe --eth"
