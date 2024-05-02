# Physics Question Generator

TODO: introduction

## Installation

1. Install [Git](https://git-scm.com/downloads) and [Python 3.12.x](https://www.python.org/downloads/).
2. Choose a folder to store the program in. The installation will create a subfolder in this folder, where everything related to the software will go.
3. Open a terminal in the selected folder. On Windows, this can be done by clicking in the blank region next to the path in a file explorer window, replacing the text with `cmd`, and hitting \<Enter>.
    - Use this terminal to enter all of the following commands.
4. In the terminal, enter the following: `git clone -b local https://github.com/MHS-CSCE/sdp-physqgen.git`, and hit enter.
5. Create a python virtual environment in the folder. This can be done with the following command: `python -m venv .venv`
6. Initialize the virtual environment with: `.venv\\Scripts\\activate`.
    - IMPORTANT: This also has to be done whenever you run the server or admin app.
7. Install the project with: `pip install .`, with the virtual environment active.

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

### Learn Concepts

|Source|Purpose|
|---|---|
|[stackoverflow](https://stackoverflow.com/questions/5119711/whats-the-easiest-way-to-put-space-between-2-side-by-side-buttons-in-asp-net)|Learn how to make a divider that separates buttons|
|[Learn to Code](https://learn.shayhowe.com/html-css/building-forms/)|Learn how to make a form using HTML|
|[2](https://learn.shayhowe.com/html-css/adding-media/ )|Learn how to add an image using HTML|
|[W3schools](https://www.w3schools.com/cssref/css3_pr_mediaquery.php)|CSS code if the screen is a certain size big or small|
|[stackoverflow](https://stackoverflow.com/questions/5411538/how-to-redirect-one-html-page-to-another-on-load), [HubSpot](https://blog.hubspot.com/website/html-redirect)|Learn how to make HTML page redirect to another page|
|[flexbox.help](https://flexbox.help/)|Visually understanding how flexbox for CSS works|
|[stackoverflow](https://stackoverflow.com/questions/15685666/changing-image-sizes-proportionally-using-css)|Changing image sizes proportionally using CSS|
|[stackoverflow](https://stackoverflow.com/questions/54151849/font-family-poppins-not-working-properly-on-my-website-when-it-loads)|Poppins family bold|
|[Josh W Comeau](https://www.joshwcomeau.com/css/designing-shadows/), [W3schools](https://www.w3schools.com/css/css3_shadows.asp), [MDN](https://developer.mozilla.org/en-US/docs/Web/CSS/filter-function/drop-shadow), [shadows.brumm.af](https://shadows.brumm.af/), [Josh W Comeau](https://www.joshwcomeau.com/shadow-palette/)|Learn how to make a shadow|
|[stackoverflow](https://stackoverflow.com/questions/2125509/how-do-i-set-the-size-of-an-html-text-box), [W3schools](https://www.w3schools.com/tags/att_input_size.asp), [stackoveflow](https://stackoverflow.com/questions/28127184/font-size-of-html-form-submit-button-cannot-be-changed)|Learn how to edit size of input text box|
|[W3Schools](https://www.w3schools.com/css/css_border.asp)|Learn how to make a border in css|
|[domain.com](https://www.domain.com/blog/what-is-a-redirect/#:~:text=There%20is%20a%20simple%20difference,that%20it%20is%20only%20temporary)|Learn what redirect code to use|
|[GeekPython](https://geekpython.in/render-images-from-flask)|Learn how to alter the folder structure to allow Flask to find images needed for front end|
|[DigitalOcean](https://www.digitalocean.com/community/tutorials/how-to-make-a-web-application-using-flask-in-python-3)|Learn about HTML blueprints and how to utilise them|
|[pymbook.readthedocs.io](https://pymbook.readthedocs.io/en/latest/flask.html#:~:text=Flask%20is%20a%20web%20framework,application%20or%20a%20commercial%20website.)|Understanding Flask and how it functions|

### Code Use

|Source|Code Used|
|---|---|
|[Javatpoint](https://www.javatpoint.com/how-to-make-a-navigation-bar-in-html)|Make a navigation bar using HTML and CSS|
|[stackoverflow](https://stackoverflow.com/questions/2906582/how-do-i-create-an-html-button-that-acts-like-a-link)|How to make a button that links to another page|
|[stackoverflow](https://stackoverflow.com/questions/17275707/how-do-i-evenly-add-space-between-a-label-and-the-input-field-regardless-of-leng)|Evenly add space between a label and the input field regardless of length of text|
|[stackoverflow](https://stackoverflow.com/questions/2125509/how-do-i-set-the-size-of-an-html-text-box)|Set the size of an HTML input text box|
|[W3schools](https://www.w3schools.com/howto/tryit.asp?font=Poppins)|Link for Poppins font|
|[stackoverflow](https://stackoverflow.com/questions/1775532/css-grid-system-for-forms-multi-column)|Making a grid of input boxes|
|[W3schools](https://www.w3schools.com/howto/howto_css_dividers.asp)|Creating a divider line using css and html|
|[stackoverflow](https://stackoverflow.com/questions/27891246/input-box-must-resize-when-div-gets-smaller)|Make input box get smaller when div gets smaller|
|[W3schools](https://www.w3schools.com/howto/howto_css_text_selection.asp)|Change text selection colour|
|[YouTube](https://youtu.be/dam0GPOAvVI?si=ndIpkOHmjgGOKBiR&t=2842)|Initializing flask app and utilising the blueprints|
|[testdriven.io](https://testdriven.io/blog/flask-sessions/)|Taking HTML form data and sending to back end|
|[stackoverflow](https://stackoverflow.com/questions/22259847/application-not-picking-up-css-file-flask-python)|Used to alter folder structure to allow Flask to find the CSS file|
|[SENTRY](https://sentry.io/answers/redirect-to-a-url-in-flask/#:~:text=Redirection%20in%20Flask%20can%20be,same%20application%20and%20external%20websites)|Allowing for redirection from question page to exit page|

### Other

- [Example Configuration Image: blueprint](https://blog.blueprintprep.com/mcat/free-mcat-practice-question-physics/)
