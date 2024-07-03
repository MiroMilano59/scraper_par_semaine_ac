# Load environment variables from .env file
set -o allexport
source .env
set +o allexport

# 1. Créer le service Data Factory
az datafactory create --resource-group $RESOURCE_GROUP --factory-name $DATAFACTORYNAME --location $LOCATION



# 2. Création du Function linked service

FunctionLinkedServiceName="FunctionLinkedService"
Functionjsonpath="json/real_function_properties.json"

# Attention jq doit être installé sur votre machine
FunctionServiceContent=$(cat $Functionjsonpath | jq -c '.')

# Créer le linked service
az datafactory linked-service create \
    --factory-name $DATAFACTORYNAME \
    --properties "$FunctionServiceContent" \
    --name $FunctionLinkedServiceName \
    --resource-group $RESOURCE_GROUP


# 3. Création du Pipeline

PipelineName="PythonPipeline"
Pipelinejsonpath="json/pipeline_properties.json"

# Attention jq doit être installé sur votre machine
PipelineContent=$(cat $Pipelinejsonpath | jq -c '.')

# Créer le linked service
az datafactory pipeline create \
    --factory-name $DATAFACTORYNAME \
    --pipeline "$PipelineContent" \
    --name $PipelineName \
    --resource-group $RESOURCE_GROUP

# 4. Création du Trigger

TriggerName="TriggerPythonPipeline"
Triggerjsonpath="json/trigger_properties.json"

# Attention jq doit être installé sur votre machine
TriggerContent=$(cat $Triggerjsonpath | jq -c '.')

# Créer le Trigger
az datafactory trigger create \
    --factory-name $DATAFACTORYNAME \
    --properties "$TriggerContent" \
    --name $TriggerName \
    --resource-group $RESOURCE_GROUP

# 5. Start the trigger
az datafactory trigger start \
    --resource-group $RESOURCE_GROUP \
    --factory-name $DATAFACTORYNAME \
    --name $TriggerName