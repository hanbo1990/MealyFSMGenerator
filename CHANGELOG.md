# Change Log

## 0.4.0

- Change
  - Generate from png file for drawio, generated from xml not exposed.
  - Add default condition None so state machine always have a idle condition

## 0.2.0

- Fix
  - Transition for each state are sorted by condition number. Before the transition will be appended to the state randomly.
- Change
  - Introduce beautiful soup with lxml to do xml parsing to improve drawio xml parsing and readbility.

## 0.1.0

- First Release
