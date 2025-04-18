import yaml
import re
from copy import deepcopy
import os


with open('docker-compose.yml', 'r') as file:
    config = yaml.safe_load(file)

# we define environment and services for each environment
supportedEnvs = {
    'full-infrastructure': {
        "services": [
            'dev-node',
            'operator-back',
            'operator-front',
            'operator-db',
            'explorer',
            'exchange-back',
            'exchange-front'
            'email-oracle',
            'file-sign-back',
            'file-sign-front',
        ]
    },
    'operator': {
        "services": [
            'operator-back',
            'operator-front',
            'operator-db',
        ]
    },
     'standard': {
        "services": [
            'dev-node'
            'operator-db',
            'operator-back',
            'operator-front',
        ]
    },
    'node': {
        "services": [
            'dev-node'
        ]
    }
}


envVarDocumentation = {
    'DEV_NODE_STORAGE_FOLDER': {
        'help': 'The folder used to store data for the development node',
        'default': './blockchain'
    },
    'EMAIL_ORACLE_KEYPAIR_FOLDER': {
        'help': 'The folder containing the keypair file for the email oracle',
        'default': './keys'
    },
    'EXCHANGE_ISSUER_KEYPAIR_FOLDER': {
        'help': 'The folder containing the keypair file for the issuer',
        'default': './keys'
    },
    'EMAIL_ORACLE_URL': {
        'help': 'The URL of the email oracle',
        'default': 'http://localhost:5012/verify/email',
    },
    'ENV_TAG': {
        'help': 'Used Carmentis environment (among "beta" and "alpha", default: "beta")',
        'default': "beta"
    },
    'EXPLORER_URL': {
        'help': 'The URL of the blockchain explorer',
        'default': 'http://localhost:5001',
    },
    'FILE_SIGN_API': {
        'help': 'The API URL used by the file-signature service front-end to interact with the back-end',
        'default': 'http://localhost:5010',
    },
    'FILE_SIGN_DEFAULT_APPLICATION_ID': {
        'help': 'The default application ID for the file-sign service'
    },
    'FILE_SIGN_DEFAULT_VERSION': {
        'help': 'The default version for the file-sign service'
    },
    'FILE_SIGN_JWT_SECRET': {
        'help': 'The JWT secret used for authentication within the file-sign service'
    },
    'FILE_SIGN_STORAGE_FOLDER': {
        'help': 'The folder used to store files and data for the file-sign back-end service',
        'default': './file-sign-data'
    },
    'NODE_URL': {
        'help': 'The blockchain node URL for connecting and interacting with the network',
        'default': 'http://localhost:5000',
    },
    'OPERATOR_DB_ENCRYPTION_KEY': {
        'help': 'The encryption key used by the operator to encrypt sensitive information on the database (can be generated via `openssl rand -hex 32`)'
    },
    'OPERATOR_JWT_SECRET': {
        'help': 'The JWT secret used for authentication purposes in operator services'
    },
    'OPERATOR_KEYPAIR_FOLDER': {
        'help': 'The folder containing the keypair file for the operator',
        'default': './keys'
    },
    'OPERATOR_POSTGRES_DB': {
        'help': 'The name of the PostgreSQL database used by the operator (Note: should be changed to fit your database)',
        'default': 'postgres'
    },
    'OPERATOR_POSTGRES_PASSWORD': {
        'help': 'The password for accessing the PostgreSQL database used by the operator',
    },
    'OPERATOR_POSTGRES_USER': {
        'help': 'The username for accessing the PostgreSQL database used by the operator (Note: should be changed to fit your database)',
        'default': 'postgres'
    },
    'OPERATOR_URL': {
        'help': 'The URL of the operator service',
        'default': 'http://localhost:5001',
    },
    'SMTP_HOST': {
        'help': 'The SMTP server URL used for sending emails'
    },
    'SMTP_PASS': {
        'help': 'The password for authenticating with the SMTP server'
    },
    'SMTP_PORT': {
        'help': 'The port of the SMTP server for communication'
    },
    'SMTP_USER': {
        'help': 'The username for authenticating with the SMTP server'
    },
}

# Function to transform an object into a YAML string
def objectToYaml(obj):
    return yaml.dump(obj)

# construct each env
for env in supportedEnvs.items():
    # parse the current env
    envName, envDescription = env

    # reduce the general config to include only needed services
    services = envDescription["services"]
    envServices = {serviceName: service for serviceName, service in config["services"].items()
                   if serviceName in services}
    envConfig = deepcopy(config)
    envConfig["services"] = envServices

    # Search all elements in the config variable using regex for the pattern `${vars}`
    elementsWithEnvTag = set(re.findall(r"\${[A-Z_]+}", str(envConfig)))
    elementsWithEnvTag = {el.strip("${}") for el in elementsWithEnvTag}
    elementsWithEnvTag = sorted(elementsWithEnvTag)



    # Create a directory with the environment's name if it doesn't exist
    if not os.path.exists(envName):
        print(f"Creating env {envName}")
        os.makedirs(envName)
    else:
        print(f"Env {envName} already exists")


    # Create .env.example file in the new directory
    envFilePath = os.path.join(envName, ".env.example")
    with open(envFilePath, "w") as envFile:
        for variable in elementsWithEnvTag:

            value = "..."
            doc = ""
            if variable in envVarDocumentation:
                varConfig = envVarDocumentation[variable]

                if 'help' in varConfig:
                    doc = f"# {varConfig['help']}\n"
                else:
                    print(f"WARNING: env var ${variable} not documented: Is this desired?")

                if 'default' in varConfig:
                    value = varConfig['default']

            else:
                print(f"WARNING: env var ${variable} not documented: Is this desired?")

            envFile.write(f"{doc}{variable}={value}\n")  # Write each variable key with an empty value

    # Create docker-compose.yml file in the new directory
    dockerComposeFilePath = os.path.join(envName, "docker-compose.yml")
    with open(dockerComposeFilePath, "w") as dockerComposeFile:
        dockerComposeFile.write(objectToYaml(envConfig))