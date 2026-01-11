# Home Maestro - 2T6

## Overview

This project implements a software system to monitor, control, and manage home automation devices and activities. It operates in contexts with multiple devices, including sensors, actuators and hubs.

The purpose of this project was to use design patterns, justifying our motivations and analyzing the results. For that reason, a minimal set of libraries were used.

## Final Report

This project's report for the curricular unit Software Architecture and Design can be in [Final Report](REPORT.md).

## Team Composition

This project belongs to the curricular unit Software Architecture and Design of the Master in Software Engineering 2025-26 course.

The team was composed by:

- [Afonso Pimenta](https://github.com/APimenta4)
- [Guimarães Manuel Pascoal](https://github.com/smithpapi2017)
- [Gustavo Oliveira Martins](https://github.com/gust0717)
- [Leonor Teixeira Pinto](https://github.com/leonor-p)

## Installation

To install and run this project locally, please follow the following steps. Optionally, you can use Docker to run the backend through the `docker-compose up -d` command.

> Install Docker/Docker Desktop if you don't have it yet by following the instructions on the [official docs](https://docs.docker.com/desktop/).

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
   cd src/backend && pip install -r requirements.txt
   ```
   The previous command installs the dependencies in your current python environment. If you aren't using any virtual environment, it will be installed on the global python version of your system.
   Learn more about virtual environments [here](https://www.w3schools.com/python/python_virtualenv.asp).
4. Install and run an MQTT broker (e.g., Mosquitto) on the `1883` port on your local machine (`localhost`). Our suggestion is to follow the instructions on the [Mosquitto website](https://mosquitto.org/download/) to install and run it on your operating system.
5. Run the backend:
   ```
   cd src/backend && python -m main
   ```
   A Flask server will start running at `http://localhost:5000`.
6. Run the frontend, by simply opening the `index.html` file located in the `src/frontend` directory in your preferred web browser.

