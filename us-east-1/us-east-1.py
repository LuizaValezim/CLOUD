import json
import os

print("")

dicionario = {"name":name}
jsonString = json.dumps(dicionario)
jsonFile = open("./region1/variables.json", "w")
jsonFile.write(jsonString)
jsonFile.close()

#os.system("terraform plan")
#os.system("terraform apply")