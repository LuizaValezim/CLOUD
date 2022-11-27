#!/bin/bash
sudo apt update
sudo apt install -y stress
stress --cpu 8 --timeout 300