import os
import requests
import subprocess
import tempfile


def download_and_apply_yaml(url):
    response = requests.get(url)

    if response.status_code == 200:

        with tempfile.NamedTemporaryFile(delete=False, mode='w', suffix='.yaml') as temp_file:
            temp_file.write(response.text)
            temp_file.close()

            print(f"Applying {temp_file.name} to Kubernetes...")
            subprocess.run(["kubectl", "apply", "-f", temp_file.name], check=True)

            os.remove(temp_file.name)
    else:
        print(f"Failed to download {url}. Status code: {response.status_code}")


def create_and_apply_selenium_node_yaml(node_count):
    base_url = "https://raw.githubusercontent.com/AliyevH/insider/main/selenium-node.yaml"

    response = requests.get(base_url)

    if response.status_code == 200:
        selenium_node_yaml = response.text.replace("replicas: 1", f"replicas: {node_count}")

        with tempfile.NamedTemporaryFile(delete=False, mode='w', suffix='.yaml') as temp_file:
            temp_file.write(selenium_node_yaml)
            temp_file.close()

            print(f"Applying {temp_file.name} to Kubernetes...")
            subprocess.run(["kubectl", "apply", "-f", temp_file.name], check=True)

            os.remove(temp_file.name)
    else:
        print(f"Failed to download base selenium-node.yaml. Status code: {response.status_code}")


def deploy_kubernetes_resources(node_count):
    github_url = "https://raw.githubusercontent.com/AliyevH/insider/main/"

    download_and_apply_yaml(github_url + "selenium-hub.yaml")

    download_and_apply_yaml(github_url + "selenium-tester-pod.yaml")

    create_and_apply_selenium_node_yaml(node_count)


if __name__ == "__main__":
    node_count = 1
    deploy_kubernetes_resources(node_count)
