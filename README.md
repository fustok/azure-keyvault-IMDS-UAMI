# azure-keyvault-IMDS-UAMI
Retrieve KeyVault secrets from container app in deployed in Microsoft Azure

In Azure portal, create a resource group hosting the below minimal artifacts:
<img width="334" height="143" alt="image" src="https://github.com/user-attachments/assets/14f0c8fe-d384-432b-9d89-788e2bab7cd5" />

Form your Terminal window run the command, assuming all is in the folder "_docker-images":
cd _docker-images
docker build --platform linux/amd64 --tag appsvc-keyvaultaccesstoken-custom-image .
docker tag appsvc-keyvaultaccesstoken-custom-image containerregistry.azurecr.io/appsvc-keyvaultaccesstoken-custom-image:latest
docker push containerregistry.azurecr.io/appsvc-keyvaultaccesstoken-custom-image:latest

Configure the UAMI over the container app to read the KeyVault secrets, and get the GUID.

Add additional deployment variables for the web app service container:
<img width="530" height="307" alt="image" src="https://github.com/user-attachments/assets/67ce5911-c364-4dcd-b0bd-4e7f660b4d6d" />

