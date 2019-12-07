import json
import boto3

def lambda_handler(event, context):

    client = boto3.client('textract')
    
    # Analyze the image with Textract
    response = client.analyze_document( \
        Document={'S3Object': {'Bucket': "learn-textract", 'Name': "sample-image.png"}}, FeatureTypes= ['TABLES','FORMS'])
        
    # Scan through all the blocks, to identify the Word blocks. 
    # Put them all in a map, so that we can pick a word from its key
    words = {}
    for x in response["Blocks"]:
        if x['BlockType'] == 'WORD':
            words[x["Id"]] = x 
    
    # Scan through all the blocks, to identify the Value blocks. 
    # Put them all in a map, so that we can pick a Value from its key
    values = {}
    for x in response["Blocks"]:
        if (x['BlockType'] == 'KEY_VALUE_SET' and x["EntityTypes"][0]=='VALUE'):
            values[x["Id"]] = x
    
    # With things in place, we now loop through all the Key blocks in the JSON
    # For each Key, we dig down, to identify the corresponding Value Block
    # We then identify the Word Blocks corresponding to the Keys and Values
    # We can then pick up these words, and join them into a sentence to be printed.
    for k in [x for x in response["Blocks"] if x['BlockType'] == 'KEY_VALUE_SET' and x["EntityTypes"][0]=='KEY']:
        print("Key: " + " ".join([[words[id]["Text"] for id in r["Ids"]] for r in k["Relationships"] if r["Type"]=="CHILD"][0]))
        print("Value: " + " ".join([[[words[id]["Text"] for id in values[vId]["Relationships"][0]["Ids"]] for vId in r["Ids"]] for r in k["Relationships"] if r["Type"]=="VALUE"][0][0]))
        print("")

    return {
        'statusCode': 200,
        'body': json.dumps("Success")
    }
