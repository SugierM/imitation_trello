from faker import Faker
import requests


# USER

# ['email',
# 'first_name',
# 'last_name',
# 'bio',
# 'phone',
# 'nickname',
# 'password'
# ]


def api_call(url, args:list[str]):
    """
    API calls for django. Based on [2:] sys.args
    """ 
    print(args)

    faker = Faker()
    api = "/".join([item for item in args[0:] if not (item.startswith('-') or item.startswith("random"))]) + "/"
    endpoint = f"{url}{api}"
    print(f"endpoint - {endpoint}")
    method = "get" if "-g" in args else "post"
    if method == "get":
        response = requests.get(endpoint, verify=False)
        print("\n\n\n\nResponse:\n")
        print("List of Users:")
        print(response.text)
        return


    if args[0].startswith("create"):
        """
        Create user.
        """
        def random_user():
            """
            Creates random user with password = 123
            """


            email, _ = faker.email().split("@")
            nickname, _ = faker.name().split()
            password = 123
            return [email, password, nickname]
    

        def normal_user():
            """
            Creates user with custom email, password, nickname
            """

            
            email = input("Email: ")
            password = input("Password: ") + ""
            nickname = input("Nickname: ") + ""
            return [email, password, nickname]


        print(endpoint)
        
        first_name, last_name = faker.name().split()
        email, password, nickname = normal_user() if args[-1] != "random" else random_user()

        json = {
            "first_name": first_name,
            "last_name": last_name,
            "email": email + "@test.pl",
            "password": password,
            "nickname": nickname,
        }

        print("User:")
        print(json) 
        response = requests.post(endpoint, json=json, verify=False)
        print("\n\n\n\nResponse:\n")
        print(response.text)


    else:
        """
        Echos random bullshit
        """
        test_data = {'query': 'Some query',
                    'data': 'Some personal data',}

        test_params = {'abc': 123,
                    'None_of': 'Your business',}

        params = {'json': test_data} if '-d' in args else {}
        params.update({'params': test_params} if '-p' in args else {})
        response = requests.get(endpoint, verify=False, **params)


    if 199 < response.status_code < 300 :
        print("^^^^^^^^^^^ THATS LAME WARNING ^^^^^^^^^^^")
        print("\n\n\n\n\n\n")
        print("Success:")
        print(response.json())      
        print("\n")
    else:
        print(f"Failed with status code: {response.status_code}")
    