import os
import requests
import subprocess
import tempfile

def download_and_apply_yaml(url):
    # Download the YAML file
    response = requests.get(url)
    
    # Check for successful response
    if response.status_code == 200:
        # Create a temporary file to save the YAML content
        with tempfile.NamedTemporaryFile(delete=False, mode='w', suffix='.yaml') as temp_file:
            temp_file.write(response.text)
            temp_file.close()  # Ensure the file is saved before applying

            # Apply the YAML file using kubectl
            print(f"Applying {temp_file.name} to Kubernetes...")
            subprocess.run(["kubectl", "apply", "-f", temp_file.name], check=True)

            # Optionally, remove the temporary file after applying
            os.remove(temp_file.name)
    else:
        print(f"Failed to download {url}. Status code: {response.status_code}")

def create_and_apply_selenium_node_yaml(node_count):
    # URL of the base selenium-node.yaml (modify with actual path)
    base_url = "https://raw.githubusercontent.com/AliyevH/insider/main/selenium-node.yaml"

    # Download the base selenium-node.yaml
    response = requests.get(base_url)
    
    if response.status_code == 200:
        # Modify the YAML content to set the replicas based on node_count
        selenium_node_yaml = response.text.replace("replicas: 1", f"replicas: {node_count}")
        
        # Write modified YAML to a temp file
        with tempfile.NamedTemporaryFile(delete=False, mode='w', suffix='.yaml') as temp_file:
            temp_file.write(selenium_node_yaml)
            temp_file.close()  # Ensure the file is saved before applying

            # Apply the modified YAML file using kubectl
            print(f"Applying {temp_file.name} to Kubernetes...")
            subprocess.run(["kubectl", "apply", "-f", temp_file.name], check=True)

            # Optionally, remove the temporary file after applying
            os.remove(temp_file.name)
    else:
        print(f"Failed to download base selenium-node.yaml. Status code: {response.status_code}")

def deploy_kubernetes_resources(node_count):
    # URLs of the YAML files (replace with the actual GitHub raw URLs)
    github_url = "https://raw.githubusercontent.com/AliyevH/insider/main/"

    # Apply the selenium hub (static)
    download_and_apply_yaml(github_url + "selenium-hub.yaml")
    
    # Apply the selenium tester pod (static)
    download_and_apply_yaml(github_url + "selenium-tester-pod.yaml")
    
    # Deploy the chrome node pods based on the node_count
    create_and_apply_selenium_node_yaml(node_count)

if __name__ == "__main__":
    node_count = 2  # Specify the number of Chrome nodes for testing (can be 1 to 5)
    deploy_kubernetes_resources(node_count)
