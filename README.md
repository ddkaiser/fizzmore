Fizzmore - FIZMO OS update script
============

Fizzmore is a Python script which provides extracts individual sysex messages from the Ensoniq FIZMO MID upgrade file into individual SysEx bulk messages.

---

Fizzmore requires that you have installed a Python intrepreter v3.9 or higher.

--- 

## Installation
- create a python virtual environment
- in your virtual environment, use pip to install python-rtmidi and mido
  example: "pip3 install python-rtmidi; pip3 install mido"
- run fizzmore and specify the input file for "--inputFile" and version for "--check"

- Examples:
1. python3 fizzmore.py --inputFile=fizmo_os_1.12.mid --check=1.12

- When completed, use a SysEx tool to send each of the 14 files, in numbered order, to the FIZMO, and wait until the FIZMO is ready before sending each of the next messages.
