# Cló Gaelach converter
# Author: R0paire
# Date: 16 May 2026
# License: GNU General Public License v3.0
# URL: https://github.com/r0paire/clo-gaelach-converter
# Credit: gaeilge.ttf (Gaeilge 2) font by Padraig McCarthy, available
# in the public domain at https://fonts2u.com/gaeilge-2-normal.font

import tkinter as tk
from tkinter import font
import re

# Creates main application window
root = tk.Tk()
root.title("Cló Gaelach converter")
root.geometry("700x600")
root.configure(bg="#2e2e2e")

# Fonts
# Please install the "gaeilge.ttf" (Gaeilge 2) font included to use this application
input_font = font.Font(family="DejaVu Sans", size=16) # Regular font
custom_font = font.Font(family="Gaeilge 2", size=18) # Cló Gaelach font

# Mode selection
def set_mode():
    mode.get()

mode = tk.StringVar(value="classic")

radio_frame = tk.Frame(root, bg="#2e2e2e")
radio_frame.pack(pady=10)

# 'Classic' Cló Gaelach
tk.Radiobutton(
    radio_frame,
    text="Classic",
    variable=mode,
    value="classic",
    font=custom_font,
    command=set_mode,
    bg="#004d04",
    fg="#d8b800",
).pack(side=tk.LEFT, padx=10)

# 'Simplified' Cló Gaelach
tk.Radiobutton(
    radio_frame,
    text="Simplified",
    variable=mode,
    value="simplified",
    font=custom_font,
    command=set_mode,
    bg="#005239",
    fg="#ffffff",
).pack(side=tk.LEFT, padx=10)

# Modern Cló Rómhánach using the font of Cló Gaelach
tk.Radiobutton(
    radio_frame,
    text="Rómhánach",
    variable=mode,
    value="Romanach",
    font=input_font,
    command=set_mode,
    bg="#ffd900",
    fg="#ffffff",
).pack(side=tk.LEFT, padx=10)

# Build rules for diagraphs
def build_digraph_rules(*rule_sets):
    rules = {}

    for pairs in rule_sets:
        for k, v in pairs.items():
            if isinstance(v, tuple):
                upper, lower = v

                rules[k.lower()] = lower
                rules[k.upper()] = upper

                rules[k.capitalize()] = upper
                rules[k[0].lower() + k[1].upper()] = lower

    return rules

# Build rules for single characters
def build_single_rules(*rule_sets):
    rules = {}

    for pairs in rule_sets:
        for k, v in pairs.items():
            if isinstance(v, tuple):
                upper, lower = v

                rules[k.lower()] = lower
                rules[k.upper()] = upper

            else:
                rules[k.lower()] = v
                rules[k.upper()] = v

    return rules

# Build rules for special cases
def apply_special_rules(text, rules):
    for key, value in rules.items():
        pattern = rf"(?<!\w){re.escape(key)}(?!\w)"
        text = re.sub(pattern, value, text, flags=re.IGNORECASE)
    return text

# Gaelach mappings
# Séimhiú mappings (used in both Classic and Simplified; or where a séimhiú isn't used per grammar)
universalSeimhiu = {
    "bh": ("\u00A1", "\u00A2"),
    "ch": ("\u00A4", "\u00A5"),
    "dh": ("\u00A6", "\u00AB"),
    "fh": ("\u00B0", "\u00B1"),
    "gh": ("\u00B2", "\u00B3"),
    "mh": ("\u00B4", "\u00B5"),
    "ph": ("\u2219", "\u00B9"),
    "sh": ("\u00BB", "\u00BB"),
    "th": ("\u00D7", "\u00F7"),
}

# Letters that either don't exist in classical cló or have a different character
classicLetters = {
    "v": ("\u00A1", "\u00A2"),
    "r":("R", "\u2030"),
    "s":("S", "\u0160"),
}

# Classic (Cló Gaelach with séimhiú and old characters) mappings
# séimhiú (or where séimhiú isn't used per grammar)
classicSeimhiu = {
    "sh":("\u00BB", "\u0161"),
    "rh":("R", "\u2030"),
    "lh":("L", "l"),
    "nh":("N", "n"),
}

# Special cases for classic cló
specClassic = {
    "agus": "\u0026",
}
ClassicClo = build_digraph_rules(universalSeimhiu, classicSeimhiu)
ClassicSingle = build_single_rules(classicLetters)

# Simplified mappings, letter is made more distinguishable (and non-existent séimhiú is changed)
seimhiuSimplified  = {
    "sh": ("\u00BB", "\u00BF"),
    "rh": ("R", "r"),
    "lh":("L", "l"),
    "nh":("N", "n"),
}

# Letter doesn't exist in simplified cló, so substituted
substituteLetters = {
    "v": ("\u00A1", "\u00A2"),
}

SimplifiedClo = build_digraph_rules(universalSeimhiu, seimhiuSimplified)
SimplifiedSingle = build_single_rules(substituteLetters)

# Romanach mappings (Cló Romanach with Gaelach font)
# no mappings necessary since it uses modern latin letters

def apply_rules(text, rules):
    for key, value in sorted(rules.items(), key=lambda x: -len(x[0])):
        pattern = re.escape(key)
        text = re.sub(pattern, value, text)
    return text

# Conversion
def convert_to_gael():
    text_output.delete("1.0", tk.END)
    text = text_input.get("1.0", tk.END)
    mode_value = mode.get()

    if mode_value == "classic":
        text = apply_special_rules(text, specClassic)
        text = apply_rules(text, ClassicClo)
        text = apply_rules(text, ClassicSingle)

    elif mode_value == "simplified":
        text = apply_rules(text, SimplifiedSingle)
        text = apply_rules(text, SimplifiedClo)

    elif mode_value == "Romanach":
        pass

    text_output.config(state=tk.NORMAL)
    text_output.delete("1.0", tk.END)
    text_output.insert(tk.END, text)
    text_output.config(state=tk.DISABLED)

# Clears output
def clear_output():
    text_output.config(state=tk.NORMAL)
    text_output.delete("1.0", tk.END)
    text_output.config(state=tk.DISABLED)

# Create input text area
text_input = tk.Text(root, height=6, width=52, font=input_font)  # Use a monospaced font for better alignment
text_input.pack(pady=10)

# Create convert button
convert_button = tk.Button(root, text="Convert", font=input_font, command=convert_to_gael)
convert_button.pack(pady=5)

# Create output text area
text_output = tk.Text(root, height=6, width=30,font=custom_font, wrap="word")
text_output.pack(pady=(30, 10))
#text_input.pack(pady=10, fill="both", expand=True, padx=10)
text_output.config(state=tk.DISABLED)  # Make output read-only

# Create clear button
clear_button = tk.Button(root, text="Clear Output", font=input_font, command=clear_output, activebackground="#E09999", background="#BB6E6E", activeforeground="white")
clear_button.pack(pady=5)

root.mainloop()
