# Blossom Package

This python package includes all the basics necessary to run your
Blossom robot to make it perform various gestures and sequences.

## About Blossom

Blossom is an open-hardware, open-source tensile robot that you can handcraft and accessorize to your liking. You can read more about the project in [Evan Ackerman's IEEE Spectrum article](https://spectrum.ieee.org/automaton/robotics/home-robots/blossom-a-creative-handmade-approach-to-social-robotics-from-cornell-and-google).

You can visit the Blossom github repository at: https://github.com/hrc2/blossom-public/

Here are two examples of Blossom robots:

<img src="http://guyhoffman.com/wp-content/uploads/2017/08/blossom-bunny-corner-e1502812175733-300x189.jpg" width="300">
<img src="http://guyhoffman.com/wp-content/uploads/2017/08/blossom-jellyfish-768x606.jpg" width="300" >

## Setup Software Dependencies

Make sure you're using [Python `3`]

To make sure you setup the dependencies without error, the easiest way is to use anaconda or virtualenv to create a virtual environment with python 3.8.5 installed. 

Although the orignial blossompy codebase was tested with a lower version of python, in this version, we included a python-based UI using PyQt5, which does rely on more up-to-date python version. 

The current codebase is being actively tested with python 3.8.5.

Also ensure that [pip3 is installed](https://pip.pypa.io/en/stable/installing/).
To install:\
Ubuntu: `sudo apt install python3-pip`\
Mac: `curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py`, then `python3 get-pip.py`

Virtual environments (`venv`) should be installed, but if not:\
Ubuntu: `sudo apt-get install python3-venv`\
Mac: `brew install python3-venv`

Make a `venv` (virtual environment) in the top `blossom` directory and activate it:
```
python -m venv blossom_venv
source blossom_venv/bin/activate
```

For Anaconda user, you can run the following line to setup a virtual environment with the correct python verion

```
conda create -n blossom_env python=3.8.5 anaconda
conda activate blossom_env
```

After setting up the virtual environment, the next step is to install all the required packages in the requirement.txt file, and more detailed instructions are included as below.


### General Setup


_Ubuntu_: You may need to run:

```
sudo apt-get install build-essential libssl-dev libffi-dev python3-dev
```
and
```
pip install wheel
```

To install dependencies, run in the main `blossom` directory:
```
pip install -r requirements.txt
```

_Mac OSX: You may need to append `--user` to the `pip` command to circumvent installation issues:_
```
pip install -r requirements.txt --user
```
_If this still doesn't work, you may have to append `sudo` before `pip`:_
```
sudo pip install -r requirements.txt --user
```
_This may require you to run in `sudo` for subsequent steps._

_It may take a while to install the dependencies; you may want to run `pip` verbose to make sure that it's still downloading: `pip install -rv requirements.txt`_

_If you run into an error opening a port, try changing Blossom's permissions: `sudo chmod 777 /dev/ttyACM0`. Alternatively, rerun everything with admin privileges._

_If you're using OSX and getting strange errors, try:_
```
sudo chown -R $USER /Library/Python/3.5
```
_Installation will take longer on a Raspberry Pi, and you may need additional dependencies:_
```
sudo apt-get install xvfb
```

## Running Blossom

### CLI
To start the CLI, plug Blossom in and run
```
python start.py
```
_Error: could not open port. You may need to run `sudo chmod 777 <the name of the port>.`
Ex: `sudo chmod 777 /dev/ttyACM0`


Additional flags:
```
-b do not start up Web UI
-p denote the port
-i specify an IP address (won't work with localhost)
```
_Linux may default to a loopback IP (`127.0.1.1`); in this case you **must** specify the IP address using `-i`._

For example, to make Blossom nod with the `yes` sequence, type:

`s` -> Enter -> `yes`

Available commands:
- `l`: list available sequences
- `s`: perform a sequence, followed by the Enter key and the sequence name
- To perform an idler (looped gesture), enter two sequence names separated by `=`, e.g. `s` -> Enter -> `yes=no` (play `yes` then loop `no` indefinitely until another sequence is played).  
- `q`: quit

## Running Breathing gestures

This Blossom package specifically implements breathing exercises that can be
used in socially assistive human robot interaction in a variety of applications.


To run the breathing demo with only audial instructions, plug Blossom in and run:
```
python breathingdemo.py
```
To run the video led breathing demo, plug Blossom in and run:
```
python breathingdemoVIDEO.py
```
To run the specific breathing controls, plug Blossom in and run:
```
python breathingexercise.py
```
