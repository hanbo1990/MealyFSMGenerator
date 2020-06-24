# MealyFSMGenerator ([Mealy](https://en.wikipedia.org/wiki/Mealy_machine))

> version: [0.2.0](https://github.com/hanbo1990/FSMGenerator/tree/master)

This mealy state machine generator will **generates c code together with its unit test** from [draw.io](https://www.draw.io) graph. The generator is written in a modular way, so it can easily extended to support other languages and other input sources.

Key words used in the state machine generator are **state**, **condition** and **transition function**. It can describe the mealy state machine behavior: In state A, condition occurs, state machine should call a transition function and go to state B. 

---

## How to use

### Step 1: Create the state machine graph.

State machine in draw.io can be created following the example given in below:

![Example](https://i.postimg.cc/SQVM4Tzx/example.png)

Patterns to follow:

> 1. States should start with unique number
> 2. Condition should start with unique number
> 3. Transition with single direction arrow should start from one state to another state. 
> 4. Each transition line should come with condition and transition function in a new line.
> 5. Condition and transition function must be created on the transition line (not creating a text and move to the line).

Once the graph is generated, use drawio build-in export function to export the graph in xml format by:

```bash
File->Export As->xml
```

**Ｍake sure don't select compressed.**

![DontUseCompress](https://i.postimg.cc/ht0j8hbP/Screenshot-from-2019-10-19-14-03-30.png)

### Step 2: Generate the code

By calling:

```bash
main.py -i <pathToXML> -n <StateMachineName>
```

After this step, you should be able to find the result in **Result** folder where you execute the main file.

### Step 3: Execute Unit Test

In Result/unit_test/ folder, execute following command:

```bash
ceedling
```

You should not see any reported error.

The Unit test is based on [ceedling](http://www.throwtheswitch.org/ceedling) which checks:

> 1. If the state number is same as the one in the graph. 
> 2. If the condition number is same as the one in the graph.
> 3. If the transition function is the same as the one in the graph.
> 4. Size of the Transition table is not changed.
> 5. The transition parameters (state, condition, next state, transition function) is same as the one in the graph. 

By enabling this unit_test, any manual change (exception is filling in the function slots) to the generated files will trigger a unit test failure.

---

## Result Folder

```bash
|
|--src                          # source folder
    |--fsmMgr                   # common code for all state machines
    |     |--MealyFSM.c         
    |     |--MealyFSM.h
    |--xxxSMFunc.c              # generated state machine code
    |--xxxSMFunc.h
    |--xxxSMTable.inc
|--unit_test                    # unit test folder
    |-- test                    # folder containing test files
         |-- test_xxx.c         # test file for the generated code
    |-- vendor                  # unit test plug-ins
```

---
##　License

Licensed under MIT.
