# Cloud Project

## Infos
Feito por: Luiza Valezim Augusto Pinto
Data: 2022.2

---

## Objectives
Desenvolver uma aplicação capaz de provisionar uma infraestrutura por meio de uma interface amigável(livre escolha) para gerenciar e administrá-la (construir, alterar e deletar recursos).

---

## Features
##### Criar
- VPC criação de uma VPC e sub-rede; instâncias: esta funcionalidade deverá permitir a escolha de pelo menos 2 tipos de configuração de hosts; ainda deverá ser possível aumentar e diminuir a quantidade de instâncias; security group: criação e a associação de grupos de segurança com instâncias; Usuário no IAM.
- Regras em security group; Instância em mais de uma região; Associar algum tipo de restrição de acesso a um usuário;
##### Deletar
- Instâncias, grupos de segurança e usuário.
- Regras de security group; recursos implantados na Região
#### Listar
- Aplicação deverá listar todas instâncias e suas regiões, usuários, grupos de segurança e suas regras.

--- 

## Tutorial
### 0. Pre-requirements
- Ubuntu
- Terraform
- AWS

### 1. Installation
- `pip install boto3`
- `pip install colorama`

### 2. AWS Credentials
Considerando que você já tem uma conta na AWS, vou te ajudar a achar as suas credenciais de acesso, elas serão necessárias para prosseguir com o projeto.

Primeiro, você tem que acessar o site da AWS e ir na "Security Credentials". Nessa página aparecerá as suas credenciais de segurança. Nela, você verá um botão "Criar chave de acesso". Salve o arquivo de suas informações, pois elas só poderão ser acessadas por você pela primeira vez quando são criadas.

### 3. AWS Configuration
Na root do seu computador, coloque o seguinte comando no seu terminal:

`nano .bashrc`

Ao final do arquivo, coloque as suas credenciais da AWS:

`export AWS_ACCESS_KEY_ID = <your_access_key>`

`export AWS_SECRET_ACCESS_KEY = <your_secret_access_key>`

Ainda na root, vá na pasta .aws e escreva o seguinte comando:

`touch credentials`

e 

`nano credentials`

Nesse arquivo você também vai precisar colar as suas credenciais no seguinte padrão:

`aws_access_key_id = <your_access_key>`

`aws_secret_access_key = <your_secret_access_key>`

De volta na pasta que está contida o main.py desse projeto, rode o seguinte comando:

`source ~/.bashrc`

Por fim, o último lugar que teremos que apresentar as nossas keys são para configurar a AWS do próprio computador. Dessa forma, use o código:

`aws configure --profile "your_username"`

Lá irá pedir suas keys, default region name e default output format.

### 4. Run main.py

Pronto! Agora o projeto está pronto para ser rodado usando:

`python main.py` ou `python3 main.py`