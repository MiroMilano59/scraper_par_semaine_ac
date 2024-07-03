# Load environment variables from .env file
set -o allexport
source .env
set +o allexport

cd azure_function

# Créer un espace de noms pour les fonctions
az functionapp create \
    --resource-group $RESOURCE_GROUP \
    --consumption-plan-location $LOCATION \
    --name AllocineFunctionApp \
    --os-type Linux \
    --runtime python \
    --runtime-version 3.11 \
    --functions-version 4 \
    --storage-account $STORAGE_ACCOUNT 

# Déployer la fonction
func azure functionapp publish AllocineFunctionApp \
    --settings DB_HOST=$DB_HOST \
    --settings DB_USER=$DB_USER \
    --settings DB_PASSWORD=$DB_PASSWORD \
    --settings DB_DATABASE=$DB_DATABASE \

cd ..