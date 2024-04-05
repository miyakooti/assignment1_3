import boto3
from boto3.dynamodb.conditions import Key, Attr



def write_data_to_dax_table(dyn_resource=None):

    if dyn_resource is None:
        dyn_resource = boto3.resource("dynamodb")

    table = dyn_resource.Table("login")
    
    for i in range(10):
        print(f"--- {i} ---")

        email = f"S4075688{i}@student.rmit.edu.au"

        name = f"kosuke arai {i}"

        password = f"{i}"

        for j in range(5):
            num = i + j + 1
            if num >= 10:
                num -= 10

            password += f"{num}"

        table.put_item(
            Item={
                "email": email,
                "user_name": name,
                "password": password,
            }
        )

        print(f"{i}succeeded")


if __name__ == "__main__":

    print("writing")
    write_data_to_dax_table()
