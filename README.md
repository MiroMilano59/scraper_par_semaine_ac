
# Azure Resource Setup Guide

## 1. Create Azure Resources

1. **Log in to Azure**  
   ```sh
   az login
   ```

2. **Activate the Bash Script**  
   ```sh
   chmod +x create_azure_resources.sh
   ```

3. **Execute the Bash Script**  
   ```sh
   ./create_azure_resources.sh
   ```

## 2. Create Azure Function

1. **Install Azure Functions Core Tools**  
   Ensure you have installed `azure-functions-core-tools@4` on your computer.

2. **Set Up Python Environment**
   ```sh
   python3.11 -m venv env
   ```

3. **Activate Virtual Environment**
   ```sh
   source env/bin/activate
   ```

4. **Install Required Packages**
   ```sh
   pip install scrapy azure-functions SQLAlchemy psycopg2-binary python-dotenv
   pip freeze > requirements.txt
   ```

5. **Initialize Azure Function**
   ```sh
   func init AllocineFolder --worker-runtime python --model V2
   ```

6. **Create New Azure Function**
   ```sh
   cd AllocineFolder
   func new --template "Http Trigger" --name MyHttpTrigger --authlevel "anonymous"
   ```

7. **Test Azure Function**
   ```sh
   func start
   ```
8. **Publish on azure**
9. ```sh
   chmod +x publish_azure_function.sh
   ./publish_azure_function.sh
   ```

## 3. Create Data Factory Resource

1. **Rename and Update Properties File**
   Rename `fake_function_properties.json` to `real_function_properties.json` and update the necessary keys in this file.

2. **Execute Data Factory Pipeline Script**
   ```sh
   ./create_data_factory_pipeline.sh
   ```
