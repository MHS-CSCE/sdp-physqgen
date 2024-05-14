# Question Types

All question types assume SI standard units.

There is currently a single available type of question, a constant-acceleration Kinematics question.

## KinematicsQuestion

In order to use this type of question in a configuration, include the following line in a question block:

- `"questionType": "KinematicsQuestion"`

In the `variableConfigs` for this block, include three of the following as keys:

- `"acceleration"`
  - An acceleration of 0 may have unintended affects, so it is dissallowed.
- `"initial_velocity"`
  - A value for initial velocity that is equal to final velocity will result in an acceleration of 0, causing the same effects as above. To avoid this, the ranges supplied to initial and final velocity, if they are both defined, must not overlap.
- `"final_velocity"`
- `"displacement"`
- `"time"`
  - A time of 0 may have unintended affects, so it is dissallowed.

Include one of the same set in the question block with the key `"answerVariableName"`, and do not include it in `"variableConfigs"`. It will be solved for automatically.

When solving for time using displacement, acceleration, and initial or final velocity, the positive result of the square root is kept. Make sure to check that all values in the configured ranges, given the question text, will have this result, or the calculated answer may be the logically incorrect one.

A similar situation is true when solving for initial or final velocity using acceleration, displacement, and their counterpart.
