import os
import json
import time

regions = ["us-east-1", "us-east-2"]
r1 = regions[0]
r2 = regions[1]

os.system('clear')

print("Olá, bem-vindo ao seu Dashboard")
time.sleep(0.8)

print("Para começarmos, selecione a região que deseja atuar")
time.sleep(0.8)

while True:

    print("")
    print("Regiões disponíveis:")
    print(r1)
    print(r2)
    print("")
    region = input("Digite a região escolhida: ")

    if region in regions:
        os.system("python3 ./" + region + "/" + region + ".py")
        print("")
        break

    else:
        print("Por favor, insira o nome corretamente")
        print("")