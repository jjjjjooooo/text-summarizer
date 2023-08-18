name: Azure Deployment

on:
  push:
    branches:
      - main
    paths-ignore:
      - "README.md"

jobs:
  build-and-deploy:
    name: Build and Deploy
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Code
        uses: actions/checkout@v2

      - name: Login to Azure
        uses: azure/login@v1
        with:
          creds: ${{ secrets.AZURE_CREDENTIALS }}

      - name: Build Docker Image
        run: |
          docker build -t myapp-image .
          docker login myacr.azurecr.io -u ${{ secrets.ACR_USERNAME }} -p ${{ secrets.ACR_PASSWORD }}
          docker tag myapp-image myacr.azurecr.io/myapp-image:latest
          docker push myacr.azurecr.io/myapp-image:latest

      - name: Deploy to AKS
        uses: azure/aks-set-context@v1
        with:
          creds: ${{ secrets.AZURE_CREDENTIALS }}
          cluster-name: myakscluster
          resource-group: myresourcegroup

      - name: Kubectl apply
        run: |
          kubectl apply -f deployment.yaml