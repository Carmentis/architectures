import yaml
import re
from copy import deepcopy
import os


with open('docker-compose.yml', 'r') as file:
    config = yaml.safe_load(file)

with open('architectures-config.yaml', 'r') as file:
    archs = yaml.safe_load(file)


# Function to transform an object into a YAML string
def objectToYaml(obj):
    return yaml.dump(obj)


architectures = archs['architectures']
variables = archs['variables']

# construct each env
for env in architectures.items():
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
            if variable in variables:
                varConfig = variables[variable]

                if 'help' in varConfig:
                    doc = f"# {varConfig['help']}\n"
                else:
                    print(f"WARNING: env var ${variable} not documented: Is this desired?")

                if 'value' in varConfig:
                    values = varConfig['value']
                    defaultValue = values['default'] if 'default' in values else None
                    envValue = values[envName] if envName in values else None
                    if defaultValue is None and envValue is None:
                        print(f"WARNING: env var ${variable} does not have have value but a 'value:' is specified: leaving unspecified")
                    elif envValue is not None:
                        value = envValue
                    else:
                        value = defaultValue

            else:
                print(f"WARNING: env var ${variable} not documented: Is this desired?")

            envFile.write(f"{doc}{variable}={value}\n")  # Write each variable key with an empty value

    # Create docker-compose.yml file in the new directory
    dockerComposeFilePath = os.path.join(envName, "docker-compose.yml")
    with open(dockerComposeFilePath, "w") as dockerComposeFile:
        dockerComposeFile.write(objectToYaml(envConfig))