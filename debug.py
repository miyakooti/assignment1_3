
import boto3
from aws_credentials import get_session



session = get_session()

# AWSクライアントの作成
s3 = session.client('s3')

dynamodb = session.client("dynamodb")

response = dynamodb.list_tables()

print(response)

# 使用しているプロファイル名を取得
# profile_name = session.profile_name

# # プロファイルに紐づく認証情報ファイルのパスを取得
# credentials_path = session.get_credentials().path



# dyn_resource = boto3.resource("dynamodb")

# table_name = "hogehjkloge"
# params = {
#     "TableName": table_name,
#     "KeySchema": [
#         {"AttributeName": "title", "KeyType": "HASH"},
#         {"AttributeName": "artist", "KeyType": "RANGE"},
#     ],
#     "AttributeDefinitions": [
#         {"AttributeName": "title", "AttributeType": "S"},
#         {"AttributeName": "artist", "AttributeType": "S"},
#         # {"AttributeName": "year", "AttributeType": "N"},
#         # {"AttributeName": "web_url", "AttributeType": "S"},
#         # {"AttributeName": "image_url", "AttributeType": "S"},
#     ],
#     "ProvisionedThroughput": {"ReadCapacityUnits": 10, "WriteCapacityUnits": 10},
# }
# table = dyn_resource.create_table(**params)
# print(f"Creating {table_name}...")
# table.wait_until_exists()