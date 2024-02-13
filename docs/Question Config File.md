# Question Config File

A question config file is a JSON file containing the configuration data for a set of questions. The default included `question.config` contains an empty array called `"questions"`. Each object in the array has a few key value pairs representing a question's data.

The `"question"` key is the case sensitive name for the type of question. For example, its value could be `"KinematicsQuestion"`.

The `"variableConfig"` key maps to a mapping containing the case-insensitive names for however many variables are necessary for the question. Each of the variables maps to an array where the first index is the minimum and second index is the maximum value the variable can take on, both floating point numbers. For example:
    ```
    "variableConfig": {
        "acceleration": [1.0, 2.0],
        "displacement": [2.0, 4.0],
        "initial_velocity": [0.0, 0.5],
        "time": [10.0, 100.0]
    }
    ```
Variable names are determined by the question type, and are case-insensitive. In the future, there will be specific documentation for the different question types, including their variable names and allowed values.

The `"solveVariable"` key maps to the name of the variable that the question is asking the student to solve for. It is also case insensitive. Ex: `"final_velocity"`.

The `"text"` key maps to text of the question displayed to the student.

The optional key `"correctRange"` maps to a float representing the allowed variance from the calculated answer for the students' submitted answers. It can be omitted.

Example of a question.config file:

```json
{
    "questions": [
        {
            "variableConfig": {
                "acceleration": [1.0, 2.0],
                "displacement": [2.0, 4.0],
                "initial_velocity": [0.0, 0.5],
                "time": [10.0, 100.0]
            },
            "solveVariable": "final_velocity",
            "text": "question text"
        }
    ]
}
```
