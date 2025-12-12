# Home Maestro - 2T6

## Overview

This project implements a software system to monitor, control, and manage home automation devices and activities. It operates in contexts with multiple devices, including sensors, actuators and hubs.

## Team Composition

This project belongs to Team 6 from Class 2 of the curricular unit Software Architecture and Design of the Master in Software Engineering 2025-26 course.

The team is composed by:

- Afonso da Cruz Pimenta (202502507 / APimenta4)
- Guimarães Manuel Pascoal (202500544 / smithpapi2017)
- Gustavo Oliveira Martins (202502510 / gust0717)
- Leonor Teixeira Pinto (202511257 / leonor-p)

## Project Management

This project's management was centralized on the [Home Maestro Trello Board](https://trello.com/b/SKnU0Hi3/home-maestro).

## Installation

To install this project, follow these steps:

1. Ensure you have Python>=3.9 installed on your system.

   ```
   python --version
   ```

2. Clone the repository:
   ```
   git clone https://github.com/FEUP-MESW-ADS-2025/HomeMaestro-2T6
   ```
3. Install the required Python packages:
   ```bash
   pip install Flask flask-cors paho-mqtt

   # Alternatively, you can install all dependencies using the requirements.txt file:
   cd src/backend
   pip install -r requirements.txt
   ```
   The previous command installs Flask in your current python environment. If you aren't using any virtual environment, it will be installed on the global python version of your system.
   Learn more about virtual environments [here](https://www.w3schools.com/python/python_virtualenv.asp).
4. Install and run an MQTT broker (e.g., Mosquitto) on the `1883` port on your local machine (`localhost`). Our suggestion is to follow the instructions on the [Mosquitto website](https://mosquitto.org/download/) to install and run it on your operating system.
5. Run the backend:
   ```
   cd src/backend && python -m main
   ```
   A Flask server will start running at `http://localhost:5000`.
6. Run the frontend, by simply opening the `index.html` file located in the `src/frontend` directory in your preferred web browser.

## How to Contribute

On how to contribute to the project, see to our [How to Contribute](CONTRIBUTING.md).

## Final Report

This project's report for the curricular unit Software Architecture and Design can be in [Final Report](REPORT.md).
