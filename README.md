# Live-Sports-Display

## Purpose
This project aims to display live scores on an LED Matrix Panel.

## Team Members
- Timothy Kosinski
- Najib Mohammad
- Jordan Grewe
- Ayman Elfayoumi
- Mitchel Brown
- Rory Jolliff

[Live Sports Display](https://livesportsdisplay-78ab65502a20.herokuapp.com/)

## How It Works
Our project has four main code sections:
- **Webserver Connection**
- **Optical Character Recognition (OCR)**
- **Sports API Data Collection**
- **Hardware**

These four sections work together to create our product:
- The webserver code connects the other portions, allowing for user input of images and output of relevant information to the hardware.
- The OCR code allows for images to be searched for both team and player names, sending them to the API code.
- The API code collects data on the teams and players and sends it to the hardware code.
- The hardware code takes the data it is given and displays it to the user on an LED Matrix Panel.
