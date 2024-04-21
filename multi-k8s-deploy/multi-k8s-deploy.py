"AOIC-24"
"This script applies or deletes Kubernetes manifests found in the specified directory and its subdirectories."

import os
import shlex
import subprocess
import yaml

def is_kubernetes_manifest(file_path):
    "Check if a file is a valid Kubernetes manifest."
    try:
        with open(file_path, 'r') as file:
            documents = yaml.safe_load_all(file)
            for doc in documents:
                if isinstance(doc, dict) and 'apiVersion' in doc and 'kind' in doc:
                    return True
            return False
    except yaml.YAMLError:
        return False

def apply_or_delete_kubernetes_manifests(path, operation):
    "Apply or delete Kubernetes manifests found in the specified directory and its subdirectories."
    for root, dirs, files in os.walk(path):
        for file in files:
            file_path = os.path.join(root, file)
            if file.endswith(".yaml") and is_kubernetes_manifest(file_path):
                command = f'kubectl {operation} -f "{file_path}"'
                try:
                    subprocess.run(shlex.split(command), check=True, stderr=subprocess.PIPE)
                    print(f"{operation.capitalize()}: {file_path}")
                except subprocess.CalledProcessError as e:
                    # Handle the error gracefully
                    if "NotFound" in str(e.stderr):
                        print(f"Service not found: {file_path}")
                    else:
                        # If it's not a service not found error, raise the exception
                        continue

if __name__ == "__main__":
    manifests_path = r"D:\FedML-AWS" # Path to the project containing the Kubernetes manifests
    # Use "apply" or "delete" as the operation
    #operation = "apply"  
    operation = "delete"
    apply_or_delete_kubernetes_manifests(manifests_path, operation)