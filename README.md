# MealyFSMGenerator ([Mealy](https://en.wikipedia.org/wiki/Mealy_machine))

> version: [0.3.0](https://github.com/hanbo1990/FSMGenerator/tree/master)

This mealy state machine generator will **generates c code together with its unit test** from:
* [draw.io](https://www.draw.io) graph if the user likes to draw the design in format of picture. Generating from png not supported in current version of drawio but will come soon. [Example here.](#Example-drawio)
* [graphviz](https://graphviz.org/) dot file if the user likes to draw graph in format of code. This allows more readable version tracking. [Example here.](#Example-graphviz)
 
The generator is written in a modular way, so it can easily extended to support other languages and other input sources.

Key words used in the state machine generator are **state**, **condition** and **transition function**. It can describe the mealy state machine behavior: In state A, condition occurs, state machine should call a transition function and go to state B. 

---

## How to use

```bash
'main.py -t <input type> -i <pathToInputFile> -n <StateMachineName>

    -t : input type, now 'dot' or 'drawio' supported. defaulted to  'drawio'.

    -i : path to the file, *.xml requried for drawio and *.dot required for dot

    -n : Name of generated state machine
```

For input type drawio, python dependencies lxml and bs4 are required.

---
### Example Drawio

#### Step 1: Create the state machine graph.

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

#### Step 2: Generate the code

By calling:

```bash
main.py -i <pathToXML> -n <StateMachineName>
```

After this step, you should be able to find the result in **Result** folder where you execute the main file.

#### Step 3: Execute Unit Test

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

### Example graphviz

graphviz is quite straight forward. Make sure at least you have states section and transitions section as below.

```bash
digraph G {
    splines=polyline
    node [style=filled];
    
    /* States */
    state_start [label="1START"]
    state_connecting [label="2CONNECTING"]
    state_connected [label="3CONNECTED"]
    
    /* transitions */
    state_start -> state_start[label="1NONE\nCheckIfTimeToConnect"]
    state_start -> state_connecting[label="2READY_TO_CONNECT\nConnect"]
    state_connecting -> state_start[label="3CONNECT_FAIL\nReset"]
    state_connecting -> state_start[label="4DISCONNECTED\nReset"]
    state_connecting -> state_connected[label="5CONNECT_SUCCESS\nNULL"]
    state_connected -> state_connected[label="1NONE\nSayHello"]
    state_connected -> state_start[label="4DISCONNECTED\nReset"]
}
```

Example and its preview looks like below.

![graphviz](https://i.postimg.cc/KvF57kHz/dot.png)

```bash
fsmgen.py -t dot -i Example/example.dot -n EXAMPLE
```

Will generate the expected results.

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

## License

Copyright <2020> <COPYRIGHT Bo Han (hanbo1990@gmail.com)>

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
