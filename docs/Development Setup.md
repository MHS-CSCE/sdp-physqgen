# Setting Up & Working

In order to start contributing, follow the same installation steps as given in the `README`, except, instead of `pip install .`, run `pip install -e .`. This will allow you to see your changes immediately instead of needing to reinstall the project every time.

## Git

Git should be installed as described in the `README` install process.

### Using Git

#### Updating Your Local Project Folder

This is the process of "pulling" any changes any other members have made and "pushed" to Github. You should always do this before you start working on something, so that you don't revert others' work in those same files, or need to deal with merging changes.

1. In the bash terminal (see the `Git in VSCode` header below), write `git pull` and hit enter. This should fetch any changes that have been made.

#### Updating the Github Repository

This is the process of "pushing" changes you have made to the project to Github, so that others can "pull" them to their computers. When you are done implementing something, you should push it to Github to minimize the chance of work accidentally getting overwritten.

In the terminal (see the `Git in VSCode` header below):

1. Type `git add .` to add all changes you have made to the "staging area". You can also subsitute relative file paths instead of the generic path `.` but that is rarely necessary.
    - **If you change files after this point, you need to re-type this command or the following command wil only commit part of your work**
2. When you are ready, type `git commit -m "commit message"` and replace "commit message" with a description of what you have changed, implemented, removed, fixed, etc.
3. To update Github, type `git push`. Hopefully, this will automatically merge your work with the repo that is stored on Github's servers.

## VSCode

### Installing & Setting Up VSCode

#### Downloading VSCode

1. Go to [https://code.visualstudio.com/Download](https://code.visualstudio.com/Download) and download the correct version.
2. Run the installer and go through the installation process.
    - You may need to create an account or similar when you actually launch it, I don't remember.

#### Setting up Extensions

In VSCode, on the leftmost panel, there should be a grid icon, called `Extensions`.

1. Search for and download these extensions:
    1. `Pylance`,
    2. `Python` (`Pylance` should install this automatically when you add it),
    3. `SQLite`,
    4. `SQLite Viewer`,
    5. `SQLTools`,
    6. `SQLTools SQLite`
2. Also, you probably want to install the Git History Extension, although I don't think it's necessary as most of the git essentials are included in base VSCode.
3. You may also want to look for a theme to change how VSCode looks.

#### Setting Up VSCode Workspace

1. In the top left toolbar, click `File > Open Folder...` and select the parent folder for the project, which you cloned with git in the initial installation.
2. Go to the File menu again, and click `File > Save Workspace As...`. Feel free to save the Workspace file to the project folder, the `.gitignore` file includes a pattern that will stop git from including it whenever you push your changes to Github servers.
3. If you are prompted whether to trust the workspace, then trust it. This should only pop up the first time.
    - When you want to work on this project, open the workspace file with VSCode, and it will save all your progress and open things exactly where you left off, assuming you saved. **VSCode is not like Replit, you have to save manually. It's fastest to regularly use the hotkey `ctrl+s`, although `File > Save` also works.**
4. Select the virtual environment you created in your original set up. This can be done by opening a Python file in vscode and clicking on the version number in the bottom right, next to `{} Python`. One pf the options should be the virtual environment you created.
    - This should automatically enable the virtual environment in any terminals you create in VSCode. If there is no indication it is active in a terminal, try closing it and opening a new one.

### Using VSCode

#### Python in VSCode

- When you want to run a python file (in this case `admin.py` or `main.py`), click on it in the Explorer panel / otherwise open it in your view.
- Then, either go to the Toolbar in the top left of the screen and select `Run > Run Without Debugging` or `Run > Start Debugging`.
- `Run Without Debugging` will work faster, and `Start Debugging` will essentially skip you to the exact place and position of the program if it errors, including showing you the value of all variables in the Run & Debug left panel.
  - (You can also use the `ctrl+f5` and `f5` hotkeys respectively)

You can also follow the steps in the `README`, or use the "play"-style button in the top right.

#### Git in VSCode

1. If you want to use git / other tools through the terminal, click on the `Terminal` button in the top left toolbar, then click `New Terminal` if you don't have any active.
2. The buttons to the right of the terminal are different tabs. The arrow next to the + button in the top right of the terminal area allows you to create different types of terminals.
