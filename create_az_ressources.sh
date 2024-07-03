# Load environment variables from .env file
set -o allexport
source .env
set +o allexport

# Create a new resource group
az group create --name $RESOURCE_GROUP --location $LOCATION

echo "Resource group created"

# Create a new db
az postgres flexible-server create \
    --resource-group $RESOURCE_GROUP \
    --name $DB_SERVER_NAME \
    --location $LOCATION \
    --admin-user $DB_USER \
    --admin-password $DB_PASSWORD \
    --public all\
    --sku-name Standard_B1ms \
    --tier Burstable \
    --storage-size 32 \
    --version 13 \
    --database-name $DB_DATABASE 

echo "Database created"

# Créer un Storage Account
az storage account create \
    --name $STORAGE_ACCOUNT \
    --resource-group $RESOURCE_GROUP \
    --location $LOCATION \
    --access-tier Cool \
    --sku Standard_LRS

echo "Storage account created" 


# Récupérer la clé de stockage
STORAGE_KEY=$(az storage account keys list --resource-group $RESOURCE_GROUP \
                --account-name $STORAGE_ACCOUNT \
                --query '[0].value' \
                --output tsv \
                )

# Créer un conteneur
az storage container create \
    --name $CONTAINER_NAME \
    --account-name $STORAGE_ACCOUNT \
    --account-key $STORAGE_KEY

# Vérifier si la variable d'environnement STORAGE_KEY existe
if [ -z "${STORAGE_KEY}" ]; then
    # Si la variable n'existe pas, ajoute la ligne dans le fichier .env
    echo -e "\nSTORAGE_KEY='${STORAGE_KEY}'" >> .env
fi
