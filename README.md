# Physics Question Generator

This program is intended to allow a teacher to easily host a website to students on the same wifi network. This website gives the students a series of questions, which can be configured directly by the teacher, with different randomized values for each variable. This is intended to allow students to focus more on the question solving process than on the specific answers they get.

The installation and running process is relatively simple. Configuration of questions is currently done by creating and editing `.json` format files, with a document below explaining the process.

Information about what and how students complete questions is stored, and can be viewed easily using the Admin app.

## Installation

1. Install [Git](https://git-scm.com/downloads) and [Python 3.12.x](https://www.python.org/downloads/).
2. Choose a folder to store the program in. The following steps will create a subfolder in this folder, where everything related to the software will go.
3. Open a terminal in the selected folder. On Windows, this can be done by clicking in the blank region next to the path in a file explorer window, replacing the text with `cmd`, and hitting \<Enter>.
    - Use this terminal to enter all of the following commands.
4. In the terminal, enter the following: `git clone https://github.com/MHS-CSCE/sdp-physqgen.git`, and hit enter.
5. Enter the command `cd sdp-physqgen` to move into the newly created project folder.
6. Create a python virtual environment in the folder. This can be done with the following command: `python -m venv .venv`
7. Initialize the virtual environment with: `.venv\\Scripts\\activate`.
    - IMPORTANT: This also has to be done whenever you run the server or admin app.
8. Install the project dependencies with: `pip install -e .`. The virtual environment should still be active.

## Running and Accessing the Website and Admin app

In order to run the following commands, you will need to have a terminal open with the Python virtual environment enabled.

On Windows, this can be done by clicking on the blank space next to the file path (it should highlight the whole path like text), replacing it with `cmd`, then hitting enter. This should open a command prompt in the correct location to run the following commands. To enable the virtual enviornment, run `.venv\\Scripts\\activate`.

### Website

- Run `python main.py` in order to start the server.
- This will output two urls into the terminal, which will be mostly composed of digits, as well as some information lines. Students should enter the url that is NOT `http://127.0.0.1:8080` into the search bar of their browsers, which will allow them to access the site as long as they are on the same wifi network. The url can be copied with `ctrl+shift+c` and posted somewhere the students can access it.
- This will monopolize the command prompt, you cannot use the same window to run the admin app.
- The additional information includes a warning that can be ignored, as well as the shortcut for closing the server, `ctrl+c`.
- Students will only be able to access the site if they are on the same wifi network.

### Admin App

- Run `python admin.py` in order to launch the app used to view information about student question submission and completion.
- Beware, closing the command prompt will close this window.
- This command prompt is also monopolized by the app, you cannot use this same prompt to run the server.
- The app can be closed using the "x" button.

### Configuration

See the [configuration file docs](https://github.com/MHS-CSCE/sdp-physqgen/blob/main/docs/Configuration%20Files.md) for information on the structure of the configuration files. See the [question type docs](https://github.com/MHS-CSCE/sdp-physqgen/blob/main/docs/Question%20Types.md) for more information on available question(s).

## Development

See [`PhysQGen Development Setup.md`](https://github.com/MHS-CSCE/sdp-physqgen/blob/main/docs/PhysQGen%20Development%20Setup.md) for info on setting up to contribute.

This program only contains a very limited selection of question types as of right now, which is an avenue for improvement.

## Sources

The following soures are split into different categories depending on what they were used for.

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
|[Josh W Comeau](https://www.joshwcomeau.com/css/designing-shadows/), [W3schools](https://www.w3schools.com/css/css3_shadows.asp), [MDN](https://developer.mozilla.org/en-US/docs/Web/CSS/filter-function/drop-shadow), [shadows.brumm.af](https://shadows.brumm.af/), [Josh W Comeau](https://www.joshwcomeau.com/shadow-palette/)|Learn how to make a shadow|
|[stackoverflow](https://stackoverflow.com/questions/2125509/how-do-i-set-the-size-of-an-html-text-box), [W3schools](https://www.w3schools.com/tags/att_input_size.asp), [stackoverflow](https://stackoverflow.com/questions/28127184/font-size-of-html-form-submit-button-cannot-be-changed)|Learn how to edit size of input text box|
|[W3Schools](https://www.w3schools.com/css/css_border.asp)|Learn how to make a border in css|
|[domain.com](https://www.domain.com/blog/what-is-a-redirect/#:~:text=There%20is%20a%20simple%20difference,that%20it%20is%20only%20temporary)|Learn what redirect code to use|
|[GeekPython](https://geekpython.in/render-images-from-flask)|Learn how to alter the folder structure to allow Flask to find images needed for front end|
|[DigitalOcean](https://www.digitalocean.com/community/tutorials/how-to-make-a-web-application-using-flask-in-python-3)|Learn about HTML blueprints and how to utilise them|
|[pymbook.readthedocs.io](https://pymbook.readthedocs.io/en/latest/flask.html#:~:text=Flask%20is%20a%20web%20framework,application%20or%20a%20commercial%20website.)|Understanding Flask and how it functions|
|[DEV](https://dev.to/sachingeek/session-in-flask-store-user-specific-data-on-server-28ap)|Learn about Flask sessions|
|[Calculator Online](https://calculator-online.net/kinematics-calculator/)|Verifying formula derivations|

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
|[stackoverflow](https://stackoverflow.com/questions/11903037/copy-all-jpg-file-in-a-directory-to-another-directory-in-python)|Learn of shutil module|
|[launch_code education](https://education.launchcode.org/lchs/chapters/more-flask/template-conditionals.html)|Jinja3 template if blocks|
|[stackoverflow](https://stackoverflow.com/questions/54151849/font-family-poppins-not-working-properly-on-my-website-when-it-loads)|Poppins family bold|

### Other

- [Example Configuration Image: blueprint](https://blog.blueprintprep.com/mcat/free-mcat-practice-question-physics/)
- Fonts are sourced from `fonts.googleapis.com`

## Contact Information

These emails will not exist after July of 2024.

| Email | Name |
|---|---|
| `asing1@ocdsb.ca` | Amelia |
| `inich3@ocdsb.ca` | Isabelle |
| `sjone12@ocdsb.ca` | Stuart |
