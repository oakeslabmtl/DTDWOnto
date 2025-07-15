# DTDW Ontology and Sample Notebooks

This repository is for the paper titled **Constructing Digital Twin Services: Applying an Ontologically-Based Workflow Approach in Practice**.

It includes the Digital Twin Deployment Workflow (DTDW) Ontology in OML, and two cases described in the paper. These contain Jupyter notebooks, Modelica models executed via OpenModelica, and a RabbitMQ server used for inter-process communication.

## Table of Contents

- [DTDW Ontology](#dtdw-ontology)
    - [Table of Contents](#table-of-contents)
    - [Cases](#cases)
    - [Requirements](#requirements)
    - [Installation](#installation)
    - [Running the Experiments](#running-the-experiments)
    - [Troubleshooting](#troubleshooting)
    - [License](#license)

## Cases

There are two cases in this reproducibility package.

1. The wind turbine case, first described in **Towards Ontological Service-Driven Engineering of Digital Twins**. This case has Jupyter notebooks to follow and execute.
2. The concrete mixing case described in the paper. As this case is industrially-sensitive, only the Jupyter notebook skeleton and empty files are provided.

## Requirements

Ensure you have the following installed:

- Python 3.8+
- [Jupyter Notebook](https://jupyter.org/)
- [OpenModelica](https://openmodelica.org/) (Tested with version v1.20 on Windows)
- Docker + Docker Compose
- `git`

For the ontological loading/querying/etc., please see the README in the `dtdw_ontology` folder.

For the instructions below, please run them in the `wind_turbine_case` folder.

Python packages (listed in `requirements.txt`):

```bash
pip install -r requirements.txt
````

## Installation

1. **Clone the repository**:

    ```bash
    git clone <repository-url>
    cd <repository-name>
    ```

2. **Set up the RabbitMQ Docker container**: Navigate to rabbit_server and run:

    ```bash
    docker compose up -d
    ```

    This will launch RabbitMQ and expose it on the default ports.

3. **Verify that RabbitMQ is running**:

   * Management UI: [http://localhost:15672](http://localhost:15672) (username: `incubator`, password: `incubator`)
   * AMQP URL: `amqp://localhost:5672`

4. **Install OpenModelica and check that OpenModelica (`omc`) is in your PATH**:

[https://openmodelica.org/](https://openmodelica.org/)

    ```bash
    omc --version
    ```

    If not, add it to your PATH environment variable.

## Running the Experiments

1. **Start Jupyter Notebook**:

    ```bash
    jupyter notebook
    ```

2. **Navigate to the current directory** and open the notebooks. They need to be run in order: first the [modelling_workflow](service_deployment_workflow.ipynb) and then the [service_deployment_workflow](modelling_workflow.ipynb).

3. The notebooks will:

   * Compile and simulate Modelica models using `omc`.
   * Interact with RabbitMQ for communication or data collection.
   * Save results in `results/`.
   * Illustrate the methodology discussed in the paper. 

## Troubleshooting

* If RabbitMQ is not reachable, ensure the Docker container is running:

  ```bash
  docker ps
  ```

* If `omc` is not found:

  * Make sure OpenModelica is installed.
  * Ensure your system PATH includes the directory containing `omc`.

* Ports in use? Stop other services using ports `5672` or `15672`.

## Citation

Cite this work as follows, or download the BibTeX entry [here](/assets/bibtex.bib):

```
Pambo, C., Andersen, M., Gomes, C., Kamburjan, E. and Oakes, B. (2025). 
Constructing Digital Twin Services: Applying an Ontologically-Based Workflow Approach in Practice. 

```

## License

This project is licensed under the 
[Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License](https://creativecommons.org/licenses/by-nc-sa/4.0/).
