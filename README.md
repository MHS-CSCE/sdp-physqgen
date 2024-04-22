# Physics Question Generator

## Installation

TODO: clone git repo, create python venv (named .venv), initialize it, run `pip install .`.

## How to Use

In order to run the following commands, you will need to have a terminal open with the Python virtual environment enabled.

On Windows, this can be done by clicking on the blank space next to the file path (it should highlight the whole path like text), and replacing it with `cmd`, then hitting enter. This should open a command prompt in that folder. To enable the virtual enviornment, run `.venv\\Scripts\\activate` to enable the virtual environment.

Run `flask run -h "0.0.0.0"` in `src/physqgen/app` in order to start the server. To navigate to this folder in the terminal, use the command `cd src\\physqgen\\app`. This will monopolize the command prompt, you cannot use the same window to run the admin app.

Run `python admin.py` in the root folder of the project in order to launch the app used to view information about question submission and completion. Beware, closing the command prompt will close this window. This command prompt is also monopolized by the app, you cannot use this same prompt to run the server.

## Hacking

See [`PhysQGen Development Setup.md`](https://github.com/MHS-CSCE/sdp-physqgen/blob/main/docs/PhysQGen%20Development%20Setup.md) for info on setting up to contribute. TODO: fix any problems, check back here. will need to make sure installation works correctly
