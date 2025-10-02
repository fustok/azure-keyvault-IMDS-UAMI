# Microsoft Azure KeyVault IMDS UAMI how to
Retrieve KeyVault secrets from container app in deployed in Microsoft Azure

In Azure portal, create a resource group hosting the below minimal artifacts:

<img width="334" height="143" alt="image" src="https://github.com/user-attachments/assets/14f0c8fe-d384-432b-9d89-788e2bab7cd5" />

Form your Terminal window run the command, assuming all is in the folder "_docker-images":
cd _docker-images
</br>
   docker build --platform linux/amd64 --tag appsvc-keyvaultaccesstoken-custom-image .
</br>
   docker tag appsvc-keyvaultaccesstoken-custom-image containerregistry.azurecr.io/appsvc-keyvaultaccesstoken-custom-image:latest
</br>
   docker push containerregistry.azurecr.io/appsvc-keyvaultaccesstoken-custom-image:latest
</br>

Configure the UAMI over the container app to read the KeyVault secrets, and get the GUID.

Add additional deployment variables for the web app service container:

<img width="530" height="299" alt="image" src="https://github.com/user-attachments/assets/d1f586be-372e-4c01-8fd0-dcecb2116cab" />

While running the py app, it will generate an html output showing this information:

<img width="532" height="296" alt="image" src="https://github.com/user-attachments/assets/c0713bf4-05d7-4540-969c-487281e56851" />


Step-by-Step:
AZURE
1 created key vault
2 created a secret
3 created managed identity, take the client_id (used in the py code running inside the web app service container)
4 added role of owner (reader is also fine) to the managed identity for key vault
5 created app container registry (hosting the repos. where to push the image from local)
6 created web app service container linux based / F1 plan (free)
7 added user assigned identity managed as poin #2 to the web app service container
 
LOCAL
8 created custom docker image based on flask / python code (client_id from above azure #3)
9 build then
10 tag then 
11 push in Azure container
 
 
RESULT
image is pulled by the web app service container
the py code running from inside the web app container just retrieves and display the keyvault access token and the value of the given secret 

General ref:
</br>
https://learn.microsoft.com/en-us/answers/questions/2076118/azure-app-with-managed-identity-enabled-cant-get-a
https://learn.microsoft.com/en-us/azure/app-service/tutorial-custom-container?pivots=container-linux&tabs=azure-portal#configure-app-service-to-deploy-the-image-from-the-registry
https://learn.microsoft.com/en-us/azure/app-service/quickstart-dotnetcore?tabs=net80&pivots=development-environment-vscode
https://learn.microsoft.com/en-us/azure/app-service/deploy-authentication-types

Queries to retrieve the configured identities:
root@xxxx:~# az login

root@xxxx:~# az webapp show --resource-group rg-1234 --name  app-service-docker --query "{name: name, objectId: identity.principalId, systemIdentityEnabled: identity.type == 'SystemAssigned' || identity.type == 'SystemAssigned, UserAssigned'}"

result:

{
  "name": "app-service-docker",
  "objectId": null,
  "systemIdentityEnabled": false
}


root@xxx:~# az webapp show --resource-group rg-1234 --name  app-service-docker --query "{name: name, systemIdentityEnabled: identity.type == 'SystemAssigned' || identity.type == 'SystemAssigned, UserAssigned', userAssignedIdentities: identity.userAssignedIdentities}"

result:

{
  "name": "app-service-docker",
  "systemIdentityEnabled": false,
  "userAssignedIdentities": 
  {
    "/subscriptions/<subscription guid>/resourcegroups/rg-1234/providers/Microsoft.ManagedIdentity/userAssignedIdentities/uami-1234": 
    {
      "clientId": "<guid>",
      "principalId": "<guid>"
    }
  }
}
