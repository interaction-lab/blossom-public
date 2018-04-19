# Blossom
Python-based control library for Blossom or Dynamixel-controlled robots.
Written for computer-tethering and streamlining the pipeline from software tasks to robot control.

## Get repo
In a terminal, clone this repo
```
git clone https://github.com/hrc2/blossom-public/
```
_Download through a package will be added in the future._

## Setup

Make sure you're using [Python `2.7`](https://edu.google.com/openonline/course-builder/docs/1.10/set-up-course-builder/check-for-python.html).

Also ensure that [`pip` is installed](https://pip.pypa.io/en/stable/installing/).

Make a `venv` (virtual environment) in the top `blossom` directory:
```
virtualenv venv
source venv/bin/activate
```

### Interfaces
To be able to run the web UI or start the mobile app, install [yarn](https://yarnpkg.com/lang/en/docs/install/).

Then `cd` into the `blossom_web` directory and run `yarn install`.

### Server
To install dependencies, run
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
sudo chown -R $USER /Library/Python/2.7
```
_Installation will take longer on a Raspberry Pi, and you may need additional dependencies:_
```
sudo apt-get install xvfb
```

### CLI
To start the CLI, plug Blossom in and run
```
python start.py -n [robot_name]
```
For example, to start Woody:
```
python start.py -n woody
```

Additional flags:
```
-b do not start up web ui
-p denote the port
-i specify an IP address (won't work with localhost)
```
_Linux may default to a loopback IP (`127.0.1.1`); in this case you **must** specify the IP address using `-i`._

Available commands:
- `l`: list available sequences
- `s`: perform a sequence, followed by sequence name
  - e.g. `s` -> Enter -> `yes`
  - To perform an idler (looped gesture), enter two sequence names separated by `=`, e.g. `s` -> Enter -> `yes=no` (play `yes` then loop `no` indefinitely until another sequence is played).  
- `q`: quit

### GUI
The GUI _should_ be accessible via `localhost:8000` after starting up the CLI if `-b` was **not** specified. Otherwise, the CLI should print a message stating the server url.

### Mobile app
The app can be installed on iOS or Android via the Expo Client app (available in the respective app stores). From within the app, search for `https://exp.host/@michaelhu/blossom-app`.

_Android: if Blossom is not controllable at first, unfocus and refocus the app._

_iOS: [Expo now no longer supports QR scanning or URL entry](https://blog.expo.io/upcoming-limitations-to-ios-expo-client-8076d01aee1a), so you must have an Expo account to publish and "test" the app; instructions are in [BlossomApp](https://github.com/hrc2/blossom/tree/master/BlossomApp)._
