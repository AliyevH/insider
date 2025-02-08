# Selenium Kubernetes Test Deployment

This repository provides a Selenium Grid system deployed on Kubernetes, consisting of a **Selenium Hub** and **Chrome Node Pods**. The **Test Pod** runs the tests and communicates with the **Selenium Hub**, which delegates the tests to the **Node Pods**.

## How It Works

- **Test Pod** sends test requests to the **Selenium Hub** `selenium-hub` svc name and  via the `/wd/hub` endpoint.
- The **Selenium Hub** manages the **Node Pods** and delegates test execution to them.
- **Node Pods** are registered with the **Selenium Hub** and execute the tests using a headless browser.

## Deployment Steps

### 1. Install Kubernetes

Make sure you have Kubernetes installed locally (using Minikube, Docker Desktop, etc.) or on AWS EKS.

### 2. Run the Python Script to Deploy Resources

To deploy the resources, run the Python script that will download the YAML files from the repository and use `kubectl` to apply them to your Kubernetes cluster.

```bash
python3 installer.py
```

`insider_test.py` file contains test cases for `Home Page`, `Careers Page` and `QA job` filter.
We can execute this tests locally also with `pytest insider_test.py` command.




