# Resistor Combination Calculator
# This program asks for a number of resistors and the value of each one.
# It then works out the total resistance in series and in parallel.
#
# MY OWN TWISTS (extra features):
#   1. Colour code reader - enter a resistor by its colour bands
#   2. Nearest standard value - suggests a real E12 resistor you can buy
#   3. Current and power - uses a supply voltage (Ohm's law)
#   4. History - calculate many circuits and see all the results at the end


# ---------------- Fixed lists (capital letters = they never change) ----------------
# Position in the list = digit value (black is 0, brown is 1, red is 2 ...)
COLOURS = ["black", "brown", "red", "orange", "yellow",
           "green", "blue", "violet", "grey", "white"]
TOLERANCE_COLOURS = ["gold", "silver"]
TOLERANCE_PERCENT = [5, 10]          # gold = 5%, silver = 10%
# Standard resistor values (E12 series). 100 is the start of the next range.
E12_VALUES = [10, 12, 15, 18, 22, 27, 33, 39, 47, 56, 68, 82, 100]


# ---------------- Functions ----------------
def get_number(message, whole_number=False, smallest=0.001, largest=1000000000):
    """Ask the user for a number between smallest and largest.
    Keep asking until the user types a valid one, then return it."""
    while True:
        text = input(message)
        try:
            # Convert the typed text into a number
            if whole_number:
                value = int(text)
            else:
                value = float(text)

            # Check the number is in the allowed range
            if smallest <= value <= largest:
                return value
            print("Sorry, the number must be from", smallest, "to", largest,
                  "- please try again.")
        except ValueError:
            # This runs when the text is not a number (for example "abc")
            if whole_number:
                print("Sorry, please type a whole number, like 3.")
            else:
                print("Sorry, please type a number, like 100 or 4.7.")


def get_colour(message, allowed):
    """Ask for a colour. Keep asking until it is in the allowed list."""
    while True:
        # strip() removes extra spaces, lower() makes it lowercase
        colour = input(message).strip().lower()
        if colour in allowed:
            return colour
        # join() puts the list items into one line, separated by commas
        print("Sorry, that colour is not allowed here. Choose from:",
              ", ".join(allowed))


def ask_yes_no(message):
    """Ask a yes/no question. Returns True for yes and False for no."""
    while True:
        answer = input(message).strip().lower()
        if answer == "yes" or answer == "y":
            return True
        elif answer == "no" or answer == "n":
            return False
        else:
            print("Sorry, please type yes or no.")


def colour_code_value():
    """Twist 1: read a 4-band resistor from its colours. Returns ohms."""
    # Tell the user how to read the bands
    print("  Hold the resistor so the gold or silver band is on the RIGHT,")
    print("  then read the colours from the LEFT. Type each colour in words.")
    print("  Colours: black, brown, red, orange, yellow, green, blue, violet,")
    print("           grey, white (band 3 can also be gold or silver)")

    # The first band cannot be black (a resistor value never starts with 0)
    first = get_colour("  Band 1 (first digit) colour: ", COLOURS[1:])
    second = get_colour("  Band 2 (second digit) colour: ", COLOURS)
    multiplier_colour = get_colour("  Band 3 (multiplier) colour: ",
                                   COLOURS + ["gold", "silver"])
    tolerance_colour = get_colour("  Band 4 (tolerance, gold or silver): ",
                                  TOLERANCE_COLOURS)

    # The first two bands make a two-digit number, e.g. brown(1) black(0) = 10
    digits = COLOURS.index(first) * 10 + COLOURS.index(second)

    # The third band is the multiplier
    if multiplier_colour == "gold":
        multiplier = 0.1
    elif multiplier_colour == "silver":
        multiplier = 0.01
    else:
        multiplier = 10 ** COLOURS.index(multiplier_colour)

    value = float(round(digits * multiplier, 3))
    tolerance = TOLERANCE_PERCENT[TOLERANCE_COLOURS.index(tolerance_colour)]
    print("  Colour code gives", value, "ohms, tolerance +/-", tolerance, "%")
    return value


def series_resistance(resistors):
    """Series: add all the resistor values together. Returns the total."""
    total = 0
    for r in resistors:
        total += r
    return total


def parallel_resistance(resistors):
    """Parallel: 1/total = 1/R1 + 1/R2 + ... Returns the total."""
    inverse_total = 0
    for r in resistors:
        inverse_total += 1 / r
    return 1 / inverse_total


def nearest_standard(value):
    """Twist 2: find the closest standard E12 resistor value."""
    # Step 1: scale the value so it sits between 10 and 100
    scale = 1
    while value / scale >= 100:
        scale = scale * 10
    while value / scale < 10:
        scale = scale / 10
    scaled = value / scale

    # Step 2: find which standard value is closest
    best = E12_VALUES[0]
    for standard in E12_VALUES:
        if abs(standard - scaled) < abs(best - scaled):
            best = standard

    # Step 3: scale back to the real size
    return float(round(best * scale, 3))


def calculate_circuit():
    """Run one full calculation. Returns a short summary for the history."""
    # Step 1: how many resistors?
    print()
    print("=" * 50)
    print("NEW CIRCUIT")
    print("=" * 50)
    count = get_number("How many resistors do you have? (type 1 to 20): ",
                       True, 1, 20)

    # Step 2: store every resistor value in a list
    resistors = []
    for i in range(count):
        print()
        print("--- Resistor", i + 1, "of", count, "---")
        print("How do you want to enter this resistor?")
        print("  1 = type its value in ohms")
        print("  2 = enter its colour bands")
        choice = get_number("Type 1 or 2, then press Enter: ", True, 1, 2)
        if choice == 1:
            value = get_number("  Value in ohms (example: 100 or 4.7): ")
        else:
            value = colour_code_value()
        resistors.append(value)

    # Step 3: total resistance for both connections
    series_total = series_resistance(resistors)
    parallel_total = parallel_resistance(resistors)

    print()
    print("=" * 50)
    print("RESULTS")
    print("=" * 50)
    print("Resistors entered (ohms):", resistors)
    print("Total resistance in series:  ", round(series_total, 2), "ohms")
    print("Total resistance in parallel:", round(parallel_total, 2), "ohms")

    # Step 4: nearest standard values you can actually buy
    print()
    print("Nearest standard (E12) value for series:  ",
          nearest_standard(series_total), "ohms")
    print("Nearest standard (E12) value for parallel:",
          nearest_standard(parallel_total), "ohms")

    # Step 5: current and power for a supply voltage
    print()
    voltage = get_number("Enter the supply voltage in volts (example: 12): ")

    series_current = voltage / series_total        # Ohm's law: I = V / R
    parallel_current = voltage / parallel_total
    series_power = voltage * series_current        # Power: P = V x I
    parallel_power = voltage * parallel_current

    print()
    print("--- Results at", voltage, "volts ---")
    print("Series:   current =", round(series_current, 3), "A, power =",
          round(series_power, 3), "W")
    print("Parallel: current =", round(parallel_current, 3), "A, power =",
          round(parallel_power, 3), "W")

    # Step 6: a warning based on the highest power (parallel draws the most)
    if parallel_power > 100:
        print("Warning: very high power. Use high-wattage resistors.")
    elif parallel_power > 10:
        print("Moderate power. Check the wattage rating of your resistors.")
    else:
        print("Low power. This is a safe level for small circuits.")

    # Build the summary line that goes into the history
    summary = (str(count) + " resistor(s) at " + str(voltage) + " V: series "
               + str(round(series_total, 2)) + " ohms, parallel "
               + str(round(parallel_total, 2)) + " ohms")
    return summary


# ---------------- Main program ----------------
print("=" * 50)
print("      RESISTOR COMBINATION CALCULATOR")
print("=" * 50)
print("HOW TO USE:")
print("  - Read each question, type your answer, then press Enter.")
print("  - Type numbers like 100 or 4.7 (no units, no letters).")
print("  - Colours are typed in words, like brown or red.")
print("  - If you type something wrong, it will ask again.")

history = []        # Twist 4: a list that remembers every calculation
again = True

while again:
    summary = calculate_circuit()
    history.append(summary)
    print()
    again = ask_yes_no("Do you want to calculate another circuit? Type yes or no: ")

# Show the history when the user is finished
print()
print("=== History of this session ===")
number = 1
for entry in history:
    print(str(number) + ". " + entry)
    number += 1
print("Goodbye!")
