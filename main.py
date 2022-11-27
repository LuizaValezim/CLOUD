import colorama
from colorama import Fore
from functions import setup, write_user, create_user, create_instance, start_instance, stop_instance, change_region, destroy, list_all, commit
global doc

colorama.init(autoreset=True)

dict_variables = {"virtual_machines" : {},  "sec_groups" : {}, "sec_group_instances": {}, "aws_region" : ""}
dict_users = {"aws_user_name" : []}
instances = []
username = ""
region = ""

def main():

    global region
    global dict_users

    print(f"\nHello, welcome to your dashboard!")
    print(Fore.LIGHTBLUE_EX + "\n----------------------------------------------------------------------------\n")

    setup()    
    write_user(dict_users)

    print(Fore.LIGHTBLUE_EX + "\n----------------------------------------------------------------------------\n")

    programa_on = True
    while programa_on:
        answer = input(Fore.LIGHTYELLOW_EX + f"""What would you like to do?

    1. Create new instance and security group
    2. Create new user
    3. Execute instance
    4. Stop instance
    5. List all resources
    6. Destroy resource
    7. Change region
    8. Commit changes
        
Answer: """)

        print(Fore.LIGHTBLUE_EX + "\n----------------------------------------------------------------------------\n")

        if answer == "1":
            print(f"Create new instance and security group selected\n")
            create_instance()
        elif answer == "2":
            print(f"Create new user selected\n")
            create_user()
        elif answer == "3":
            print(f"Execute instance selected\n")
            region = input(f"What is the region you would like to execute [us-east-1 // us-weast-1]? ")
            start_instance(None, None, region)
        elif answer == "4":
            print(f"Stop instance selected\n")
            region = input(f"What is the region you would like to stop? ")
            stop_instance(None, None, region)
        elif answer == "5":
            print(f"List all resources selected\n" )
            list_all()
        elif answer == "6":
            print(f"Destroy resource selected\n")
            destroy()  
        elif answer == "7":
            print(f"Change region selected\n")
            change_region()      
        elif answer == "8":
            print(f"Commiting all your changes for the region {region}\n")
            commit()

        print(Fore.LIGHTBLUE_EX + "\n----------------------------------------------------------------------------\n")


main()