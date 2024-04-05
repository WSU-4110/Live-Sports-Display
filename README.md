# Live-Sports-Display

![alt text](https://github.com/WSU-4110/Live-Sports-Display/blob/main/Logo/MMM_Logo.png)


## Our Website
Our website can be accessed here:
https://livesportsdisplay-78ab65502a20.herokuapp.com/

## Our Purpose:
This project aims to display live Scores on an LED Matrix Panel.

## Our Team members:

- Timothy Kosinski 
- Najib Mohammad
- Jordan Grewe
- Ayman Elfayoumi
- Mitchel Brown
- Rory Jolliff

## How it works:
Our project has four main code sections:
- The Webserver connection
- Optical Character Recognition (OCR)
- Sports API data collection (API)
- Hardware

These four section work together to create our product:
- The webserver code connects the other portions, allowing for user input of images - and output of relevant information to the hardware
- The OCR code allows for images to be searched for both team and player names - sending them to the API code
- The API code allows for the collection of the data on the teams and players - sending it to the Hardware code
- The Hardware code takes the data it is given, and displays it to the user on an LED Matrix Panel
