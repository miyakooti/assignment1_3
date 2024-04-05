
import boto3

# AWS認証情報の設定
session = boto3.Session(
    aws_access_key_id='ASIAQ3EGVH4JRBUGXUCY',
    aws_secret_access_key='ks2cwzMttFQzG2mLCZLWH6kyIzsQCQTkXDweSMnI',
    aws_session_token='IQoJb3JpZ2luX2VjEHMaCXVzLXdlc3QtMiJGMEQCIFenjpnD4AHcmQ3YQI9SCo7wIPhJbF5LgrGDNTRrhkHRAiBYTaJWA5ZxT3UUlkH+6a6Wd7lrefwwZ65WUAsfEOKzZCq/Agic//////////8BEAAaDDA1ODI2NDQ2OTI2NyIM9hk+VOGkCBQHCHyVKpMCXjnDx9M8pin7LoIiq9GqCKxhDEeP7rLdosGvnSrJh1ZVLQCyGhiYqWNWs5xFkcty7sMXrxoyYT6jrEtfF80Q/WghoTdz0SZWbMKvnSiWcNjfOPaq+49rBOr56RhbUtkgigj+/7Pho6H2PJNpcrqgXmmOjm0Z4pn1IFFsxt7n3BKvNNrJxVxSSu7D7Jb404y+U42ZSuLp6pNFP0z9TjOEtJPpVci9crugb0gt4hYG8Sf/VmXWBTLHZOKC2ncQXYapZRbhTzfsoN3lBX9H3EHuYjMG06Z9c4BEBcQ06PqNoBXFY46r/f3jFklocXtoXY3BkIJZil+mvlf9WaMY7hDWO+dJv1i0ApQrPN5+/22idPIO5dowv829sAY6ngHY4WdMI5k28A4yWwy4fWBM+1ikhdMLyPFMvxG4bd0GstbDyMixh6QUziT+TaC6VAPLvMCyHy/Oxoi5kk+5n7wUiVIJcZ5VmP+kgLqQVq5VPweiaEVwtFaJPoysUfLo3LFYzl+8+rq0Y2kGx7T0lGzPWVd36FKgdumjEpcFv8ZEh3+NU5sGdQYuJ/sGCSdNxe7o+qoKwtYGIS1/9W4N8g==',  # オプション（一般的には必要ありません）
    region_name='us-east-1'
)

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