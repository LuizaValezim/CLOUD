import os
import boto3
import json
import colorama
from colorama import Fore

global doc

colorama.init(autoreset=True)

dict_variables = {"virtual_machines" : {},  "sec_groups" : {}, "sec_group_instances": {}, "aws_region" : ""}
dict_users = {"aws_user_name" : []}
instances = []
username = ""
region = ""

def setup():
    global region
    global dict_variables
    global dict_users
    global instances
    global doc

    answer = input(Fore.LIGHTBLUE_EX + f"Great! Please, choose a region to start [1. us-east-1 // 2. us-west-1]:  ")

    while True:
        if answer == "1" or answer == "2":
            break
        else:
            answer = input(f"Invalid input. Please, choose a valid region to start [1. us-east-1 // 2. us-west-1]: ")

    if answer == "1":
        region = "us-east-1"
    elif answer == "2":
        region = "us-west-1"

    if region == "us-east-1":
        vpc_cidr_block = "10.0.0.0/16"
    else:
        vpc_cidr_block = "172.16.0.0/16" 

    doc = f'{region}/.auto-{region}.tfvars.json'

    if os.path.exists(doc):
        dict_variables = load_json()
        dict_users = load_json_users()
        instances = [instance for instance in {key for key in dict_variables["virtual_machines"]}]
    else:
        dict_variables = {"virtual_machines" : {},  "sec_groups" : {}, "sec_group_instances": {}, "aws_region" : "", "vpc_cidr_block":""}
        dict_users = {"aws_user_name" : []}
        instances = []


    dict_variables.update({str("aws_region") : str(region)})
    dict_variables.update({str("vpc_cidr_block") : str(vpc_cidr_block)})
    write(dict_variables)

def load_json():
    doc = f'{region}/.auto-{region}.tfvars.json'
    with open(doc, 'r') as json_file:
        dict_variables = json.load(json_file)
    return dict_variables

def load_json_users():
    file = 'users/.auto.tfvars.json'
    with open(file, 'r') as json_file:
        dict_users = json.load(json_file)
    return dict_users

def write(dict_variables):
    doc = f'{region}/.auto-{region}.tfvars.json'
    json_object = json.dumps(dict_variables, indent = 4)
    with open(doc, 'w') as outfile:
        outfile.write(json_object)

def write_user(dict_users):
    file = 'users/.auto.tfvars.json'
    json_object = json.dumps(dict_users, indent = 4)
    with open(file, 'w') as outfile:
        outfile.write(json_object)

def isValid(answer):
    if answer == "y" or answer == "Y" or answer == "n" or answer == "N":
        return False
    else:
        print(Fore.RED + f"Invalid input. Please, try again. " + "\n")
        return True

def isNumber(answer):
    if len(answer) == 1:
        if answer.isdigit():
            return False
    else:
        print(Fore.RED + f"Invalid input. Please type a valid number. " + "\n")
        return True

def create_restrictions():
    global dict_users

    list_describe = {
            "Action": [
            "ec2:Describe*",
            "ec2:Get*"
            ],
            "Effect": "Allow",
            "Resource": "*"
        }


    list_describe_create =  {
        "Action": [
            "ec2:Describe*",
            "ec2:Get*",
            "ec2:Create*",
            "ec2:UpdateSecurityGroupRuleDescriptionsEgress",
            "ec2:ModifySecurityGroupRules",
            "ec2:UpdateSecurityGroupRuleDescriptionsIngress",
            "ec2:AuthorizeSecurityGroupIngress", 
            "ec2:RevokeSecurityGroupIngress", 
            "ec2:AuthorizeSecurityGroupEgress", 
            "ec2:RevokeSecurityGroupEgress",
            "ec2:RunInstances"
        ],
        "Effect": "Allow",
        "Resource": "*"
        }

    list_describe_create_delete = {
        "Action": [
            "ec2:Describe*",
            "ec2:Get*",
            "ec2:Create*",
            "ec2:UpdateSecurityGroupRuleDescriptionsEgress",
            "ec2:ModifySecurityGroupRules",
            "ec2:UpdateSecurityGroupRuleDescriptionsIngress",
            "ec2:AuthorizeSecurityGroupIngress", 
            "ec2:RevokeSecurityGroupIngress", 
            "ec2:AuthorizeSecurityGroupEgress", 
            "ec2:RevokeSecurityGroupEgress",
            "ec2:RunInstances",
            "ec2:TerminateInstances",
            "ec2:Delete*"
        ],
        "Effect": "Allow",
        "Resource": "*"
        }

    options = input(Fore.YELLOW + f"""
    
    Please choose one of the following options for us to proceed with your resources:

        1. Describe and list;
        2. Describe, list and create;
        3. Describe, list, create and destroy;

    Digite o número da opção que você deseja: """)   

    while isNumber(options):
        options = input(f"What would you like to do? ")

    if options == "1":
        dict_users["aws_user_name"].append({"username" : username, "policy_name": "ReadOnlyAccess_" + username, "policy_description": "Descrever e listar recursos", 
            "policy_action": list_describe["Action"], "policy_resource": list_describe["Resource"], "policy_effect": list_describe["Effect"]})
        write_user(dict_users)
    elif options == "2":
        dict_users["aws_user_name"].append({"username" : username, "policy_name": "ReadWriteAccess_" + username, "policy_description": "Descrever, listar e criar recursos", 
            "policy_action": list_describe_create["Action"], "policy_resource": list_describe_create["Resource"], "policy_effect": list_describe_create["Effect"] })
        write_user(dict_users)
    elif options == "3":
        dict_users["aws_user_name"].append({"username" : username, "policy_name": "ReadWriteDeleteAccess_" + username, "policy_description": "Descrever, listar, criar e destroy recursos", 
            "policy_action": list_describe_create_delete["Action"], "policy_resource": list_describe_create_delete["Resource"], "policy_effect": list_describe_create_delete["Effect"] })
        write_user(dict_users)

def create_user():
    global username
    global dict_users

    print(f"Lets start by creating a user for you! " + "\n")
    username = input(f"What will be the its name? ")
    print(f"""
    The user starts by having the following permissions: 
        - Change password;
        - Create and stop instances;
    """)

    create_politics = input(f"Would you like to create some restrictions for this user? If not, the default permissions will be applied (y/n): ")

    while isValid(create_politics):
        create_politics = input(f"Would you like to create some restrictions for this user? If not, the default permissions will be applied (y/n): ")

    if create_politics == "y" or create_politics == "Y":
        create_restrictions()
    elif create_politics == "n" or create_politics == "N":
        dict_users["aws_user_name"].append({"username": username, "policy_name": "FullAccess_" + username, "policy_description": "All access conceed to the user", "policy_action": ["*"], "policy_resource": "*", "policy_effect": "Allow"})
        write_user(dict_users)

    print(Fore.LIGHTGREEN_EX + "\nUser creation was a success!")

def create_secgroup():
    null = None

    print(f"Creating security groups..." + "\n")
    n_secgroup = input(f"How many security groups would you like to create? " + "\n")

    for i in range(int(n_secgroup)):
        lista_group_name = []

        security_group_name = input(f"How it is going to be named the security group n°{i}: ")
        print("\n")

        n_rules = input(f"How many rules do you want to create for this security group? " + "\n")

        dict_standard_rule = {"ingress" : {"description" : "Allow inbound traffic", \
                            "from_port" : 0, \
                            "to_port" : 0, \
                            "protocol" : -1, \
                            "ipv6_cidr_blocks" : null, \
                            "prefix_list_ids" : null, \
                            "self" : null , \
                            "security_groups" : null , \
                            "cidr_blocks" : ["0.0.0.0/0"]}}

        list_rules = [dict_standard_rule]

        for i in range(int(n_rules)):
            description_security_group = input(f"Description: ")
            print("\n")
            aws_from_port = input(f"Start port:")
            print("\n")
            aws_to_port = input(f"End port:")
            print("\n")
            aws_protocol = input(f"Protocol:")
            print("\n")
            aws_cidr_blocks = input(f"CIDR Block: ")
            print("\n")

            dict_rules = {"ingress" : {"description" : str(description_security_group), \
                                        "from_port" : str(aws_from_port), 
                                        "to_port" : str(aws_to_port), \
                                        "protocol" : str(aws_protocol), 
                                        "ipv6_cidr_blocks" : null,  \
                                        "prefix_list_ids" : null,  \
                                        "self" : null,  \
                                        "security_groups" : null,  \
                                        "cidr_blocks" : [str(aws_cidr_blocks)]}}
            
            list_rules.append(dict_rules)

            dict_variables["sec_groups"].update({str(security_group_name) : {"name" : security_group_name, "ingress": list_rules}})
            write(dict_variables)

        flag = True
        while flag:
            nome_inst_sec = input(f"Which instances will be linked to this security group?  Answer:")

            instancias = list(set(nome_inst_sec.split(",")))

            for i in range(len(instancias)):
                if instancias[i] not in instances:
                    print(f"Invalid input. Type a valid name. " + "\n")
                else:
                    if i == len(instancias)-1:
                        flag = False

        for nome_inst_sec_group in instancias:
            if nome_inst_sec_group in dict_variables["sec_group_instances"]:
                lista_group_name = dict_variables["sec_group_instances"][nome_inst_sec_group]["sec_names"]
                lista_group_name.append(security_group_name)
                dict_variables["sec_group_instances"].update({nome_inst_sec_group : {"sec_names" : lista_group_name}})
            else:
                dict_variables["sec_group_instances"].update({str(nome_inst_sec_group) : {"sec_names" : [str(security_group_name)]}})

        write(dict_variables)

def create_default_secgroup(name_instance):

    list_rules = []
    null = None
    dict_rules = {"ingress" : {"description" : "Allow inbound traffic", \
                                "from_port" : 0, \
                                "to_port" : 0, \
                                "protocol" : -1, \
                                "ipv6_cidr_blocks" : null, \
                                "prefix_list_ids" : null, \
                                "self" : null , \
                                "security_groups" : null , \
                                "cidr_blocks" : ["0.0.0.0/0"]}}
            
    list_rules.append(dict_rules)
    dict_variables["sec_groups"].update({"standard" : {"name" : "standard", "ingress": list_rules}})
    write(dict_variables)

    for i in range(len(instances)):
        if instances[i] == name_instance:
            dict_variables["sec_group_instances"].update({str(instances[i]) : {"sec_names" : ["standard"]}})
            write(dict_variables)

def create_instance():
    global region
    n_instances = input(f"How many instances would you like to create? ")

    while isNumber(n_instances):
        n_instances = input(f"\nInvalid input. How many instances would you like to create? ")

    for i in range(int(n_instances)):
        name_instance = input(f"""What is the name of your instance? """)
        instances.append(name_instance)
        image_id_answer = input(f""" 
    Which image? 
        1. Ubuntu Server 20.04 LTS 
        2. Ubuntu Server 22.04 LTS 
    Answer: """)

        if image_id_answer == "1" and region == "us-east-1":
            image_id = "ami-0149b2da6ceec4bb0"
        elif image_id_answer == "2" and region == "us-east-1":
            image_id = "ami-08c40ec9ead489470"
        elif image_id_answer == "1" and region == "us-west-1":
            image_id = "ami-03f6d497fceb40069"
        elif image_id_answer == "2" and region == "us-west-1":
            image_id = "ami-02ea247e531eb3ce6"
        
        
        while True:
            instance_type_choice = input(f"""

    Which type?
        1. t2.micro;
        2. t2.small;
        3. t2.medium;
        4. t2.large      
    Answer: """)

            if instance_type_choice == "1" or instance_type_choice == "2" or instance_type_choice == "3" or instance_type_choice == "4":
                break
            else:
                print(f"Input not valid. Try again " + "\n")
        if instance_type_choice == "1":
            instance_type = "t2.micro"
        elif instance_type_choice == "2":
            instance_type = "t2.small"
        elif instance_type_choice == "3":
            instance_type = "t2.medium"
        elif instance_type_choice == "4":
            instance_type = "t2.large"

        dict_variables["virtual_machines"].update({str(name_instance) : {"image_id" : str(image_id), "instance_type" : str(instance_type)}})
        write(dict_variables)   

    sec_group = input(f"\nWould you like to create a security group with rules? (y/n) ")

    while isValid(sec_group):
        sec_group = input(f"Invalid input. Will you like to create a security group with rules (y/n)  \n")
    if sec_group == "y" or sec_group == "Y":
        create_secgroup()
    elif sec_group == "n" or sec_group == "N":
        print(f"Selecting the default option.")
        create_default_secgroup(name_instance)

def start_instance(event, context, region):
    instances = [input(f"Instance id you want to execute: ")]
    ec2 = boto3.client('ec2', region_name=region)
    ec2.start_instances(InstanceIds=instances)
    print('Started your instances: ' + str(instances))

def stop_instance(event, context, region):
    instances = [input("Instance id you want to stop: ")]
    ec2 = boto3.client('ec2', region_name=region)
    ec2.stop_instances(InstanceIds=instances)
    print('Stopped your instances: ' + str(instances))

def change_region():
    global region 
    global dict_variables
    global dict_users
    global instances
    global doc

    answer = input(f"To what region would you like to change to? [1. us-east-1 // 2. us-west-1]? ")
    print("\n")

    while True:
        if answer == "1" or answer == "2":
            break
        else:
            answer = input(f"To what region would you like to change to? [1. us-east-1 // 2. us-west-1]? ")

    print(f"Success on updating your region! ")

    if answer == "1":
        region = "us-east-1"
    elif answer == "2":
        region = "us-west-1"

    if region == "us-east-1":
        vpc_cidr_block = "10.0.0.0/16"
    else:
        vpc_cidr_block = "172.16.0.0/16" 

    doc = f'{region}/.auto-{region}.tfvars.json'

    if os.path.exists(doc):
        dict_variables = load_json()
        dict_users = load_json_users()
    else:
        dict_variables = {"virtual_machines" : {},  "sec_groups" : {}, "sec_group_instances": {}, "aws_region" : []}
        dict_users = {"aws_user_name" : []}
        instances = []


    dict_variables.update({str("aws_region") : str(region)})
    dict_variables.update({str("vpc_cidr_block") : str(vpc_cidr_block)})
    write(dict_variables)

def destroy():

    dict_variables = load_json()

    destroy = input(f"""
Which resource would you like to destroy?

    1. Instance;
    2. Security Group;
    3. Security Group Rule;
    4. User;
    
    Answer: """)

    if destroy == "1":
        instance_destroy = input(f"""
Destroy instance selected...
    \nWhat is the name of the instance you would like to destroy? """)
        print("\n")

        instance_chosen = dict_variables["virtual_machines"][instance_destroy]
        goingToDestroy = input(Fore.RED + f'Are you sure you want to destroy this instance {instance_destroy}: {instance_chosen}? (y/n) ')

        while isValid(goingToDestroy):
            goingToDestroy = input(f"Are you sure you want to destroy this instance? (y/n) \n ")

        if goingToDestroy == "y" or goingToDestroy == "Y":
            print("\n")
            print(f"Destroying instance...  " + "\n")
            dict_variables["virtual_machines"].pop(str(instance_destroy))
            for chave in dict_variables["sec_group_instances"].copy():
                if instance_destroy == chave:
                    del dict_variables["sec_group_instances"][str(instance_destroy)]
            write(dict_variables)

        elif goingToDestroy == "n" or goingToDestroy == "N":
            print("\n")
            print(f"Aborting destruction..." + "\n")

    elif destroy == "2":
        sec_group_destroy = input(f"""
Destroy security group selected...
    \nWhat is the name of the security group you would like to destroy? """)

        goingToDestroy = input(f"Are you sure you want to destroy this security_group (y/n). Answer: ")

        while isValid(goingToDestroy):
            goingToDestroy = input(f"Are you sure you want to destroy this security_group (y/n). Answer: ")

        if goingToDestroy == "y" or goingToDestroy == "Y":
            print("\n")
            print(f"Destroying security group... " + "\n")
            
            size = len(dict_variables["sec_groups"][str(sec_group_destroy)]["ingress"])
            while size > 1:
                if dict_variables["sec_groups"][str(sec_group_destroy)]["ingress"][size-1]["ingress"]["description"] != "Allow inbound traffic":
                    dict_variables["sec_groups"][str(sec_group_destroy)]["ingress"].pop()
                    size = size - 1
                    write(dict_variables)

        elif goingToDestroy == "n" or goingToDestroy == "N":
            print("\n")
            print(f"Aborting destruction..." + "\n")

    elif destroy == "3":
        sec_group_destroy_regra = input(f"""
Destroy rule of security group selected... 
    \nWhat is the name of the security group that contains the rule you want to destroy? """)

        print(Fore.RED + f'The security group {sec_group_destroy_regra} contains the following rules:  \n')

        for i in range(len(dict_variables["sec_groups"][str(sec_group_destroy_regra)]["ingress"])):
            topico = dict_variables["sec_groups"][str(sec_group_destroy_regra)]["ingress"][i]["ingress"]
            print(f'{i} - {topico["description"]}, {topico["protocol"]}, {topico["from_port"]}, {topico["to_port"]}, {topico["cidr_blocks"]} ')

        print("\n")
        destroy_rule = input(f'What is the number of the rule you want to destroy? Answer: \n ')
        goingToDestroy = input(f"""

Are you sure you want to destroy the following rule: {destroy_rule}? (y/n) """)

        while isValid(goingToDestroy):
            goingToDestroy = input(f"Are you sure you want to destroy the following rule? {destroy_rule} (y/n) ")

        if goingToDestroy == "y" or goingToDestroy == "Y":
            print("\n")
            print(f"Destroying rule... " + "\n")
            dict_variables["sec_groups"][str(sec_group_destroy_regra)]["ingress"].pop(int(destroy_rule))
            write(dict_variables)
        elif goingToDestroy == "n" or goingToDestroy == "N":
            print("\n")
            print(f"Aborting destruction..." + "\n")

    elif destroy == "4":
        destroy_user = input(f""" 
Destroy user selected... 
    \nWhat is the name of the user you would like to destroy? """)

        goingToDestroy = input(Fore.RED + f'Are you sure you want to destroy the user {destroy_user}? (y/n) \n Answer: ')

        while isValid(goingToDestroy):
            goingToDestroy = input(f"Are you sure you want to destroy the user {destroy_user}? (y/n) \n Answer: ")

        if goingToDestroy == "y" or goingToDestroy == "Y":
            print("\n")
            print(f"Destroying user... " + "\n")
            size = len(dict_users["aws_user_name"])
            for i in range(size):
                if dict_users["aws_user_name"][i]["username"] == destroy_user:
                    dict_users["aws_user_name"].pop(i)
                    size = size - 1
                    write_user(dict_users)
                    break

        elif goingToDestroy == "n" or goingToDestroy == "N":
            print("\n")
            print(f"Aborting destruction..." + "\n")

def list_all():
    global region

    session = boto3.Session(profile_name='default', region_name=region)
    ec2iam = session.client('iam')
    ec2re = session.resource('ec2')
    escolha_listar = input(f""" 

    Do you want to list which of the following resources?
        1. Instances;
        2. Security group & Rules;
        3. User;
    
    Answer: """)

    while isNumber(escolha_listar):
        escolha_listar = input(f""" 
    Do you want to list which of the following resources?
        1. Instances;
        2. Security group & Rules;
        3. User;
    
    Answer: """)

    if escolha_listar == "1":
        print("\n")
        print(f"Instances: " + "\n")

        for each in ec2re.instances.all():
            print(f"Id: " + each.id + " " + "| Name: " + each.tags[0]["Value"] + " " + "| State: " + each.state["Name"] + " " +
            "| Type: " + each.instance_type +  "| Region: "+  each.placement['AvailabilityZone'] + "\n " + f"")


    elif escolha_listar == "2":
        print("\n")
        print(f"Security group: & Rules: " )
        for each in ec2re.security_groups.all():
            print(f"Name: " + each.group_name + "\n")
            for rule in each.ip_permissions:
                print(f"Rule: " + str(rule) + "\n")


    elif escolha_listar == "3":
        print("\n")
        print(f"Users: " )
        for user in ec2iam.list_users()['Users']:
            print("User: {0}\Id: {1}\nARN: {2}\Create on: {3}\n".format(
                user['UserName'],
                user['UserId'],
                user['Arn'],
                user['CreateDate']
                )
            )
            print(f"")

def commit():
    global doc
    doc = f'.auto-{region}.tfvars.json'
    os.system("source ~/.bashrc")
    os.system(f'cd users && terraform init && terraform  plan && terraform apply')
    os.system(f'cd {region} && terraform init && terraform  plan -var-file={doc} && terraform apply -var-file={doc}')