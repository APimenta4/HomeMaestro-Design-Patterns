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

This project's management is centralized on the [Home Maestro Trello Board](https://trello.com/b/SKnU0Hi3/home-maestro).

## Diagrams

[Domain Model (draw.io)](https://app.diagrams.net/#G1Dm2RSYODV8ipJ_am0yr1ROCWjzooqt7y)

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
3. In case you don't have it yet, install `Flask` via pip:
   ```
   pip install Flask
   ```
   The previous command installs Flask in your current python environment. If you aren't using any virtual environment, it will be installed on the global python version of your system.
4. Running the backend:
   ```
   cd src/backend && python -m main
   ```
   A Flask server will start running at `http://localhost:5000`.
5. To run the frontend, simply open the `index.html` file located in the `src/frontend` directory in your preferred web browser.

## How to Contribute

On how to contribute to the project, see to our [How to Contribute](CONTRIBUTING.md).

## Final Report

This project's final report for the curricular unit Software Architecture and Design can be in [Final Report](REPORT.md).
