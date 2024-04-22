# Physics Question Generator

TODO: introduction

## Installation

1. Install [Git]() and [Python 3.12.x]().
2. Choose a folder to store the program in. The installation will create a subfolder in this folder, where everything related to the software will go.
3. Open a command prompt in the folder. On Windows, this can be done by clicking in the region next to the path in a file explorer window, and entering `cmd`, and hitting \<Enter>.
    - Enter the following: `git clone https://github.com/MHS-CSCE/sdp-physqgen.git`, and hit enter.
4. Create a python virtual environment in the folder. This can be done with the following command: `python -m venv .venv`
5. Initialize the virtual environment with: `.venv\\Scripts\\activate`.
    - IMPORTANT: This also has to be done whenever you run the server or admin app.
6. Install the project with: `pip install .`, with the virtual environment still active.

## How to Use

In order to run the following commands, you will need to have a terminal open with the Python virtual environment enabled.

On Windows, this can be done by clicking on the blank space next to the file path (it should highlight the whole path like text), and replacing it with `cmd`, then hitting enter. This should open a command prompt in that folder. To enable the virtual enviornment, run `.venv\\Scripts\\activate` to enable the virtual environment.

Run `flask run -h "0.0.0.0"` in `src/physqgen/app` in order to start the server. To navigate to this folder in the terminal, use the command `cd src\\physqgen\\app`. This will monopolize the command prompt, you cannot use the same window to run the admin app.

Run `python admin.py` in the root folder of the project in order to launch the app used to view information about question submission and completion. Beware, closing the command prompt will close this window. This command prompt is also monopolized by the app, you cannot use this same prompt to run the server.

### Configuration

See the [configuration file docs](https://github.com/MHS-CSCE/sdp-physqgen/blob/main/docs/Configuration%20Files.md) for information on the structure of the configuration files.

## Hacking

See [`PhysQGen Development Setup.md`](https://github.com/MHS-CSCE/sdp-physqgen/blob/main/docs/PhysQGen%20Development%20Setup.md) for info on setting up to contribute. TODO: fix any problems, check back here. will need to make sure installation works correctly

## Sources

TODO
