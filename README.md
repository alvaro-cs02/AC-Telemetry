# Assetto Corsa Telemetry

Welcome to the Assetto Corsa Telemetry Toolkit! This project is a versatile Python toolkit designed for Assetto Corsa enthusiasts, researchers, and anyone in between. It allows for highly customizable telemetry data extraction and analysis, suited for a variety of purposes beyond just racing. Whether you're analyzing lap times, investigating vehicle dynamics in simulated real-world scenarios, or conducting educational projects, this toolkit has got you covered.

## Features

- **Customizable Data Extraction**: Choose exactly what telemetry data you want to capture, from speed and acceleration to more intricate details like tire pressure and suspension travel. All of this can be customized through a simple configuration file.

- **Interactive Data Visualization**: Turn your raw telemetry data into insightful visual representations with our built-in visualization tool. Explore your data through interactive graphs and charts, making it easier to analyze and understand.

- **Versatile Application**: Whether you're a racer looking to improve your lap times, a researcher conducting studies, or an educator using Assetto Corsa for teaching physics concepts, this toolkit is designed to adapt to your needs.

## Getting Started

### Prerequisites

- Miniconda installed on your machine
- Assetto Corsa game installed
- Basic understanding of Python for setup and customization

### Installation

1. **Clone the Repository**

   Open a terminal (Command Prompt, PowerShell, or Git Bash) and run the following command:

   ```sh
   git clone https://github.com/alvaro-cs02/AC-Telemetry.git
   cd AC-Telemetry
   ```

2. **Install Miniconda**

   Download and install Miniconda from the [official website](https://docs.conda.io/en/latest/miniconda.html). During installation, make sure to check the option to **"Add Miniconda to my PATH environment variable"** (even though it is not recommended).

3. **Create a Conda Environment**

   Open a terminal and create a new Conda environment with Python 3.12:

   ```sh
   conda create -n ac_telemetry_env python=3.12
   ```

   **Note:** You can replace `ac_telemetry_env` with any name you prefer for your environment.

4. **Activate the Environment**

   Activate the newly created environment:

   ```sh
   conda activate ac_telemetry_env
   ```

5. **Install the Package**

   Inside the repository folder, run:

   ```sh
   pip install -e .
   ```

### Configuration

Navigate to `params_template.py` inside the `commons` directory and change the following line to reflect the path to your cloned repository:

```python
APP_DIR = Path("YOUR PATH TO THE REPO")
```

Then change the file name to `params.py`
### Running the App

To run the application, use:

```sh
python run.py
```

Then, open your browser and navigate to [http://127.0.0.1:8050/](http://127.0.0.1:8050/). Alternatively, you can click the link in the terminal.

### Alternative Installation

If you already have Python installed and don't want to use a Conda environment, you can simply run `pip install -e .` in the repository folder, and it should install dependencies in your global Python environment, provided the Python version is compatible.

## License

This project is licensed under the MIT License.

## Acknowledgments

- Thanks to the Assetto Corsa community for the invaluable resources and discussions that have helped shape this project.
