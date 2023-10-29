PC-DIY-Helper
===
A light helper for building my own PC.

# Usage
`python pc_diy_helper/pc_diy_helper_app.py`

This pops up a GUI:

<img width="2335" alt="Screenshot 2023-10-29 at 15 50 57" src="https://github.com/mhli971/PC-DIY-Helper/assets/50337211/cc779ed9-252e-4b80-974a-a1159dec5d6c">

allowing you to build you own PC.

# Features

## Conditional Selection

If you choose RTX 4090, you may want a CPU >= 13700, but if you choose RTX 4080, you may be okay with 13600 -- this app allows configurable dependency structure in `configs/dependents.json`.

## Specific Version Selection

After selecting models, you are able to select specifc versions of that model:

<img width="224" alt="Screenshot 2023-10-29 at 16 03 27" src="https://github.com/mhli971/PC-DIY-Helper/assets/50337211/5780585c-2cfc-446d-8f52-9a559cb41e48">

and hit `Build PC` button to show the total price and price decompositions:

<img width="725" alt="Screenshot 2023-10-29 at 16 03 46" src="https://github.com/mhli971/PC-DIY-Helper/assets/50337211/a1d3b69d-c054-484c-b1c6-a37d17a1fe76">

# TODO
* Implement buttons to watch prices from different sources

* Make this prettier
