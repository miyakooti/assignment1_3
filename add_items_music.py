import boto3
import json

def write_songs_to_dynamodb():


    table = "music"
    json_path = "a1.json"

    # DynamoDBクライアントの作成
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table(table)

    # JSONファイルの読み込み
    with open(json_path, 'r') as f:
        songs_data = json.load(f)

    # テーブルに書き込み
    with table.batch_writer() as batch:
        for song in songs_data['songs']:
            batch.put_item(
                Item={
                    'title': song['title'],
                    'artist': song['artist'],
                    'year': int(song['year']),  # DynamoDBは数値型をサポートするため、文字列から数値型に変換
                    'web_url': song['web_url'],
                    'image_url': song['img_url']  # JSONのキーがimg_urlですが、テーブルの属性名がimage_urlなので変換
                }
            )


if __name__ == "__main__":

    write_songs_to_dynamodb()
