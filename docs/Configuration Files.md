# Configuration

A question config file is a JSON file containing the configuration data for a set of questions. As all configurations must, the default included `kinematics.json` configuration file contains an empty array called `"questions"`. Each object in the array has a few key value pairs representing a question's data.

The `"questionType"` key is the case sensitive name for the type of question. (Ex: `"KinematicsQuestion"`. See the [question type docs](https://github.com/MHS-CSCE/sdp-physqgen/blob/main/docs/Question%20Types.md) for more.)

The `"variableConfig"` key (the name of the section) contains another section. This section contains key-value pairs for each variable that should be randomized for the question. The valid keys will be different depending on the above `questionType`, see the question type docs. The value in those pairs is also a structure, with a few keys.

- `"range"` contains the minimum and maximum value the variable can take on, both numbers (whether with decimals or not).
- `"units"` are appended to the end of the displayed value for the variable.
- `"displayName"` is the name the value will be paired with when displayed. This is meant to help it match the text you included for the question. See the default kinematics configuration for an example.
- `"decimalPlaces"` is the numbe of decimal places to include when displaying the value of each variable to a student. Can be omitted, in which case the default is 3.

For example:

```json
    ...
    "variableConfig": {
        "acceleration": {
            "range": [1, 9.81],
            "units": "m/s^2",
            "displayName": "g"
        },
        "initial_velocity": {
            "range": [0.1, 97.3],
            "units": "m/s",
            "displayName": "s",
            "decimalPlaces": 1
        },
        "time": {
            "range": [1.3, 1.3],
            "units": "s",
            "displayName": "t",
            "decimalPlaces": 1
        }
    }
    ...
```

Variable names are determined by the question type.

The `"answerVariableName"` key maps to the name of the variable that the question is asking the student to solve for. It is also case insensitive. (Ex: `"final_velocity"`)

The `"text"` key maps to text of the question displayed to the student.

The `"imageFilename"` key must be the name of an image file in the image folder in the configs folder. You can add your own images there, and reference them here, and they will show up on the site. These images are stored permanently in `src/physqgen/app/static/images`, so if you want to reuse a name, you'll have to go to that folder and delete the previously copied image.

The optional key `"correctLeeway"` maps to a float representing the allowed variance from the calculated answer for the students' submitted answers. It can be omitted, in which case the default value is 10%, or 0.1.

## Example

```json
{
    "questions": [
        {
            "questionType": "KinematicsQuestion",
            "variableConfig": {
                ... // See above for an example
            },
            "answerVariableName": "final_velocity",
            "text": "question text, reference variables with display names",
            "imageFilename": "kinematics.png"
        }
    ]
}
```
