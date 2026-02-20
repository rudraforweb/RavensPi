# RavensPi 🌱

![mitbadge](https://github.com/user-attachments/assets/282e75e8-075f-4eac-84c9-b7bafc85c7e3)
![Static Badge](https://img.shields.io/badge/GPT-4o--mini-%23ffffff)
![Static Badge](https://img.shields.io/badge/Powered%20by-Raspberry%20Pi-%23ba0000)

## Introduction
Our robot is an intelligent, mobile robot that visually inspects plants using a Raspberry Pi, then uses OpenAI’s GPT-4o-mini Vision model to analyze plant health. If a plant appears dry or wilted, it automatically triggers watering. At the end of each session (once per day), the robot sends an email to the user's email address.

## Team Information
- Team Name: RavensPi
- Team ID: 3991-1
- Competition: Robofest Exhibition
- School: Sunlake Academy of Math and Science

## Project Overview

RavensPi is designed to automate plant care by combining computer vision, sensors, and autonomous navigation. The robot follows a predefined route, stops at each plant, captures an image, measures soil moisture, and decides whether watering is required. This system reduces human effort while ensuring plants receive consistent care.

The project was developed for Robofest Exhibition and emphasizes real-world reliability, modular design, and hardware–software integration.

## Key Features

* Uses a Raspberry Pi camera to capture high-resolution images of plants.
* OpenAI GPT-4o-mini Vision analyzes plant appearance along with soil moisture data.
* Activates a pump through a custom PCB for watering
* Uses a ToF distance sensor and controlled movement to approach plants.
*	Designed to empty and refill the water tank at the refill station.
*	Sends a detailed summary of each plant’s health status to the user.

## Hardware Components
### Main Robot
* Sphero RVR
* Raspberry Pi Zero 2 W
* ILI9341 (3.2in)
* Raspberry Pi Camera Module V2
* SparkFun Qwiic Button - Red LED
* Seeed Studio XIAO SAMD21
* Watering System Kit (pump and soil moisture sensor)
* PCA9685 Servo Interface Board
* Servos
* Custom 3D printed parts
* Custom PCB with MOSFET and 2200 µF decoupling capacitor to control pump

### Refill Station
* Arduino UNO R4 WIFI
* SparkFun Qwiic OLED Display (0.91 in)
* Watering System Kit (again)
* CQ Robot Liquid Water Sensor

## Software Stack
* Python 3
* Sphero RVR SDK
* Picamera2
* OpenAI GPT-4o-mini Vision
* Luma LCD display driver
* I²C & GPIO control
* SMTP (email notifications)
* C++ (refill station and XIAO)

The software is modular, with separate files for vision, movement, sensors, pumping, email, and display logic.

## How It Runs
1.	User starts the robot using a physical button
2.	Robot navigates to a plant
3.	Camera captures an image of the plant
4.	Soil moisture is measured
5.	AI analyzes plant health
6.	Robot waters the plant if needed
7.	Robot moves to the next plant
8.	Robot refills water tank at refill station
9.	At the end of the run, an email report is sent

## Possible Additional Features
*	Additional plant metrics (leaf color tracking over time)
*	Mobile app or web dashboard
*	Multi-day historical plant health analytics


(Icon.png sourced from pngtree.com)
