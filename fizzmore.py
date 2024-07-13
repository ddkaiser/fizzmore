##############################
#The MIT License (MIT)
#
#Copyright © 2024 David Kaiser <dkaiser@dkaiser.org>
#
#Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
#The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
#THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
##############################
# fizzmore.py - a script to split FIZMO OS upgrade SysEx messages out of MIDI file
##############################

import getopt, sys, hashlib
import mido

sha1sums = {
    '1.10': [
        '5c6a1fc95e77bd848fdcd3ef13c0b31915412d4f',
        '6fded8be957fd99a22c3a8cbd941aebbf23d4cc8',
        '27b941116c43eb1480b9232f586b408404b52f65',
        '54e26b9fbbaded75295d97dc129dafa71b3eba20',
        '9dd3545d15447abeac3706e66cb9a7ed5f6b368a',
        '45c28ba59f45afddce9563e3cd93c0d3dcb95af8',
        '5cda4ff9415d5f455548972c88b5bb2a1da8edfa',
        '00b214ce99f4f19d0a16a4030dbabdff958f53b3',
        'dd82f665bf30d8bea6ebfb471314282286899d09',
        '17d305fbdbe4fdf7bb7892fbb494941076c638fb',
        '84e84fcaee9cfe288d2c7005eb20ac43459d3628',
        '2675559f38b73b26c6fc5fa5fe98e821e78c2fc1',
        '5348d7e0f152f396ab02c6292f44f8d4599eaade',
        'ecf05e1e761d94608d096b46dc54cec66768e63a'
    ],
    '1.11': [
        '5c6a1fc95e77bd848fdcd3ef13c0b31915412d4f',
        'd5823c2de0f0b4b645f60c77c07439d39abdc4a4',
        'df54a57c080d49011f2163da6a5a093609ffee21',
        '7a9533133dce312857d3aea10e0eddbf94453c22',
        'd4f10d205e5813db27900970d9f43c0e7fd022be',
        '9d787c22c55c58f8803fbd2d23b1a3c3a2ddf91a',
        '890d61e02a62be9d8d139358c7b00987c7016381',
        '40105b12557bd921b597ff4a98d7fccb029e63c5',
        '84b24c7252d30bb4e761604b283d924c34e9845c',
        '112666f77efd3fe7573880a4939e48299c394c12',
        'e44206f1e15d87aee9c35e32b50aabbfefc38fdb',
        '51096a699650b39128dfd8d6db2b026b890e179b',
        '73ed02408bc3e366c52d9d3e7aa909ebf285eaa5',
        'ecf05e1e761d94608d096b46dc54cec66768e63a'
    ],
    '1.12': [
        '5c6a1fc95e77bd848fdcd3ef13c0b31915412d4f',
        '2470a9cf670c9375f4f8d4ca6c49954ec02d5593',
        '563d2103c393d8bf78ab94c5be6f2f1e532223fe',
        '3e4b6446650912e3d01831224184916a7fe8d6a7',
        'd4f10d205e5813db27900970d9f43c0e7fd022be',
        '9d787c22c55c58f8803fbd2d23b1a3c3a2ddf91a',
        '389bab65851da2afe1c24b8e3aed9fd631961d95',
        '40b2a05e6b66cdb0ca53aab1adeb1682d1bfa48f',
        '4b844c72038a75979bc51dee97a3cf8d4b123f5f',
        '36550a4000afb86b21a40652da8d85271cdc5474',
        '78263325f0ded5339c05cd4c2eecc1626684366d',
        'fe33ca523febf4240cad3e519deac12c3e689ef6',
        'b55795fd6ac1ccd5db281764482d0a71f53f6ba1',
        'ecf05e1e761d94608d096b46dc54cec66768e63a'
    ]
}

inputFile = None
port = None
checkversion = None

argumentList = sys.argv[1:]

# i = 'inputFile'
# c = 'check' sha1sum
options = ""
long_options = ["inputFile=", "check="]

try:
    # Parsing argument
    arguments, values = getopt.getopt(argumentList, options, long_options)
    
    # checking each argument
    for currentArgument, currentValue in arguments:

        if currentArgument in ("--inputFile"):
            inputFile = currentValue
            print ("Using file {} for OS input source".format(inputFile))
     
        elif currentArgument in ("--check"):
            checkversion = currentValue
            print ("Checking sha1sum results for version {}.".format(checkversion))
                
except getopt.error as err:
    # output error, and return with an error code
    print (str(err))

#midifilename = "fizmo_os.mid"
if inputFile is None:
    sys.exit("Please specify '.mid' inputFile name with --inputFile= ")

midifile = mido.MidiFile(inputFile)
print("Processing MIDI file {}.".format(midifile.filename))

track = midifile.tracks[0].copy()
syxcount = 1

# Iterate messages in the only track
for message in track:
    sharesult = ''
    if message.is_meta == True:
        print("Skipping Meta Type Message: length:{} ({})".format(len(message.bin()),message.type))
    if message.type == 'sysex':
        messagelength = len(message.bin())
        syxfilename = "fizmo_os_message{0:02d}.syx".format(syxcount)
        if checkversion is not None:
            sharesult = 'SHA1SUM:         **** FAIL ****'
            sha1hash = hashlib.sha1(message.bin()).hexdigest()
            if sha1hash == sha1sums[checkversion][syxcount-1]:
                sharesult = "sha1sum: pass"
        print("SysEx Message: length:{:>6d}, writing file:{} {}".format(messagelength,syxfilename,sharesult))
        file = open(syxfilename,'wb')
        file.write(message.bin())
        file.close()
        syxcount += 1

