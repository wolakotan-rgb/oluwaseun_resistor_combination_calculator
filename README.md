# oluwaseun_resistor_combination_calculator
# Resistor Combination Calculator

## What it does
This Python program calculates the total resistance of a group of
resistors connected in series and in parallel. You enter how many
resistors you have and the value of each one, either in ohms or by
typing its colour bands.

## How to run it
Install Python 3, then run: python resistor_calculator.py

## Sample output
```
Resistors entered (ohms): [100.0, 1000.0, 220.0]
Total resistance in series:   1320.0 ohms
Total resistance in parallel: 64.33 ohms

Nearest standard (E12) value for series:   1200.0 ohms
Nearest standard (E12) value for parallel: 68.0 ohms

--- Results at 12.0 volts ---
Series:   current = 0.009 A, power = 0.109 W
Parallel: current = 0.187 A, power = 2.239 W
Low power. This is a safe level for small circuits.
```

## My own twist
I added four extra features:
1. **Colour code reader:** enter a resistor by its 4 colour bands.
2. **Nearest standard value:** suggests the closest real E12 resistor.
3. **Current and power:** uses a supply voltage to calculate both.
4. **History:** calculate many circuits and see all results at the end.

## What I learned
While creating this project, I learned that a resistor’s color bands are really a number, and that a list’s positions can store that code. This meant I could convert colors into ohms with one line instead of writing a separate if for every color. Another thing was, Before this project I wasn’t sure how the totals compared to the individual resistors. Coding it showed me that series simply adds the values, so the total is bigger than any one resistor, while parallel adds 1/R and flips the answer, so the total is smaller than the smallest resistor. And lastly, I learned to test with odd inputs and not only good ones, by typing letters, zero, negative numbers and wrong colors on purpose. This showed me that a resistor of 0 ohms would crash the parallel calculation (you can’t divide by zero), so I made the program reject it and ask again. All of these shaped me into building this project with grit and determination.

## Author
Olakotan Oluwaseun Williams, ND2 Mechatronics Engineering, YabaTech.
