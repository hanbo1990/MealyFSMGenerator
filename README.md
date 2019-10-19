# MealyFSMGenerator ([Mealy](https://en.wikipedia.org/wiki/Mealy_machine))
> version: [0.1.0](null)

This mealy state machine generator will **generates c code together with its unit test** from [draw.io](https://www.draw.io) graph. The generator is written in a modular way, so it can easily extended to support other languages and other input sources.

Key words used in the state machine generator are **state**, **condition** and **transition function**. It can describe the mealy state machine behavior: In state A, condition occurs, state machine should call a transition function and go to state B. 

---
## How to use:

### Step 1: Create the state machine graph. 

State machine in draw.io can be created following the example given in below:

![Example](https://lh3.googleusercontent.com/79LyHz-hOjSZwUUlIiSxy1J5TxUlIdGJIOCbkVzu-FUri0TW8bbVvqsrm3hdIXoCoXgOrxVzccZa9Ft8Zr39s2xX88Ml-Xli7OBuHwXfcRzr6C01ZO2YwWX9WY2Czy4AgN4GW4FrDPttZsPhOQ4yuNbvsgVrUErjEpKHaCrM7NfUUo2CHxucLP0T2Js3LeH4K2VG9miufp70T02wrPKVeLCuCSHfmNJ-yvFGf1jg_97jBRxqpwQO854FhQuvYqoOC37m33cAODDTiSlkinFn-9cuIB1ivvGuBvezkNJ2sK1PsT52Z21O-JxEXTEactNy1qEn_ghgHWYi7yT8GfOzsbuXEnEM_32GncdGy5vS-oV_tSlU2nTcJOdDbArKzVIpTuGSiJR_TTqSpV2BpeeMiybHUH9wYRM1ZmmOeHapJQvf2hOtDiBefVUngkac_vpGe6E7aH-xp57BXvJFlY-8oOJuhE9_9eXF9UO3vfSlwUTWRcl6w-VV7kRXnZj8e5WiuDAe8KNhyih6KtzbrnuXjthwfoMriYDTYHlHNyvoFPcX6ZBmoP3CJmnq-iqYnCzOrnUui-3Vt09uf01miW7v1OfgSXcyesgt__IgqNoiHz1YvRWeRj6fqz67XNhzRPHunl8J9wSU0nRzohsVJ2FzDyROlCocLgQRues4g-HFSH7KKoey2ee4bvA=w352-h469-no)

Patterns to follow:
> 1. States should start with unique number
> 2. Condition should start with unique number
> 3. Transition with single direction arrow should start from one state to another state. 
> 4. Each transition line should come with condition and transition function in a new line.
> 5. Condition and transition function must be created on the transition line (not creating a text and move to the line).

Once the graph is generated, use drawio build-in export function to export the graph in xml format by:

```
File->Export As->xml
```
**Ｍake sure don't select compressed.**
![DontUseCompress](https://lh3.googleusercontent.com/1eYsjHon_iV1OkaWqMvx0XCgtRhiI7EJ9CsDWyNTY6oObz8CZnwS2Fu6f-kNQvoYhspR72kL0hZbaimqQre8szUF3EdnZFIRlv6VqYPdgL32nuiyvyZRhZ_uWI6jSPhztDNyLXn14TVItdrmfLCDxsgqTVLboMGfAfax0OQi26Ep6FuM_bTNcq58mtIQe2bCJoD0NVjTN3fJiKVnXRToMrYRAisF4qb9T0PkPzJ2774uqORPNzLahavcY2wBtem6NImc47a8GrEqZxwXxkDF6ouFq7cfgpnTQi5CeJ7yTh2J5fLXTOj2D2KNY-jGqLF5Jg_Sbo2Nqhc-yz16A9t1ffDThnjk692iXDGEy-lkK_0n4vJ5_psa2DPVXxoq6n0zyVs7PD5ywKKuzPaUchbeBrBhinbhQMvLmI8FnsCL2ViNJoFJznnKyDfRP9BHVKP4etIiOn1O8Wzm43j7OBcCw6432-J1JOC4P02WApH29AzKFAq03uIT87G7zyyuGJDUkkJ3JsgZjrcTNM8TMepNcfBRJGczvejK8dJE02DJ8KdufjWhaGMyTiHNJPEMV8CQhcEoAy1nDEkBeZsiLFFXJx80z0XvGDoJCpKOSklXpRB8dyjYc3la31DJujea9MXjFY75kisYRx8ZcDYcwrgg9pxLfLgbh0R0rGP9Z1hXJIpcbKwdBiJRMi8=w369-h246-no)

### Step 2: Generate the code

By calling:
```
main.py -i <pathToXML> -n <StateMachineName>
```

After this step, you should be able to find the result in **Result** folder where you execute the main file.

### Step 3: Execute Unit Test

In Result/unit_test/ folder, execute following command:
```
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

```
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
