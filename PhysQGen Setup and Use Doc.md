# Setting Up & Working

## Virtual Machine

- [ ] TODO: figure out VM stuff

***From this point in the file onwards, assume everything is done inside the VM.***

## Github

### Setting Up Github

1. Create Github Classroom Account with a link from Ms. Edwards.
2. Using your school email, click the Create Account button on the initial login screen, then go through prompts.
   - Make sure to join the team PhysQGen so you can access the project files.

### Using Github

Repo url: [https://github.com/MHS-CSCE/sdp-physqgen](https://github.com/MHS-CSCE/sdp-physqgen)

- [ ] TODO: add any other pertinent info

## Git

### Installing Git

1. Download the correct installer from [https://git-scm.com/downloads](https://git-scm.com/downloads)
2. Run the installer, and complete the installation process
    - Once this is done, git should be set up on the VM, there is no more set up needed.

### Installing / Cloning Git Repositories

This is the process for starting a new workspace folder, not for updating / pulling changes from Github.

1. Create a folder to contain the project on the VM. This should probably not be on the Desktop or in Downloads, Documents is probably a good place for it.
2. Type `cmd` into the search bar and hit enter. This will open a command prompt in that location.
3. Then, type `git clone https://github.com/MHS-CSCE/sdp-physqgen` into the command line and hit enter. This will prompt you to login. I still have to figure out how to authorize you, but it'll probably work if you join my team for the project when you set up your account.
4. Once you go through the authorization process, the most up to date version of the repo will be downloaded in that folder. For now, it is named `sdp-physgen`.

### Using Git

#### Updating Your Local Project Folder

This is the process of "pulling" any changes any other members have made and "pushed" to Github. You should always do this before you start working on something, so that you don't revert others' work in those same files.

1. In the bash terminal (see the `Git in VSCode` header below), write `git pull` and hit enter. This should fetch any changes that have been made. Doing this (probably) overwrites any un-pushed (or maybe un-commited) changes you have made, so be aware.

#### Updating the Github Repository

This is the process of "pushing" changes you have made to the project to Github, so that others can "pull" them to their computers. When you are done implementing something, you should push it to Github to minimize the chance of work accidentally getting overwritten.

In the bash terminal (see the `Git in VSCode` header below):

1. Type `git add .` to add all changes you have made to the "stage". You can also subsitute relative file paths for the "." but that is rarely necessary.
    - **If you change files after this point, you need to re-type this command or the following command wil only commit part of your work**
2. When you are ready, type `git commit --m="commit message"` and replace "commit message" with a description of what you have changed, implemented, removed, fixed, etc.
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
    2. `Python`,
    3. `SQLite`,
    4. `SQLite Viewer`,
    5. `SQLTools`,
    6. `SQLTools SQLite`
2. Also, you probably want to install the Git History Extension, although I don't think it's necessary as most of the git essentials are included in base VSCode.
3. You may also want to look for a theme to change how VSCode looks.

#### Setting Up VSCode Workspace

1. In the top left toolbar, click `File > Open Folder...` and select the parent folder for the project, which you cloned with git in the `Installing / Cloning Git Repositories` section.
2. Go to the File menu again, and click `File > Save Workspace As...`. Feel free to save the Workspace file to the project folder, I will be including a file in the project that will stop git from including it whenever you push your changes to the folder on Github servers.
3. If you are prompted whether to trust the workspace, then trust it. This should only pop up the first time.
    - When you want to work on this project, open the workspace folder with VSCode, and it will save all your progress and open things exactly where you left off, assuming you saved. **VSCode is not like Replit, you have to save manually. It's fastest to regularly use the hotkey `ctrl+S`, although `File > Save` also works.**

### Using VSCode

#### Python in VSCode

- When you want to run a python file, click on it in the Explorer panel / otherwise open it in your view.
- Then, either go to the Toolbar in the top left of the screen and select `Run > Run Without Debugging` or `Run > Start Debugging`.
- `Run Without Debugging` will work faster, and `Start Debugging` will essentially skip you to the exact place and position of the program if it errors, including showing you the value of all variables in the Run & Debug left panel.
- (You can also use the ctrl+f5 and f5 hotkeys respectively)

#### Git in VSCode

1. If you want to use git / other terminal tools, click on the Terminal button in the top left toolbar, then click New Terminal.
    - (I'll probably set the project upon to use a Python "virtual environment", but VSCode should handle the whole process of activating it here.)
2. The buttons to the right of the terminal are different tabs. If there is no "bash" terminal, click on the arrow next to the + button in the top right of the terminal area and select the "Git Bash option.
    - This is the terminal where you will enter any git commands in the future.
