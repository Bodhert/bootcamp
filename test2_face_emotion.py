import botocore
import boto3
import json
from PIL import Image

if __name__ == "__main__":
    fileName = 'test2.jpg' # nombre en la nube de la imagen a modifica
    bucket = 'eafit-team2-input'
    client = boto3.client('rekognition', 'us-east-1')
    s3 = boto3.resource('s3')

    response = client.detect_faces(
        Image={'S3Object': {'Bucket': bucket, 'Name': fileName}}, Attributes=['ALL'])

    # print('Detected faces for ' + fileName)

    emocion_final = "_"
    confianza_final = -1.0
    Height = -1.0
    Left = -1.0
    Top = -1.0
    Width = -1.0
    # print (response)

    for faceDetail in response['FaceDetails']:
        print('The detected face is between ' + str(faceDetail['AgeRange']['Low'])
              + ' and ' + str(faceDetail['AgeRange']['High']) + ' years old')

        # print ('holaaaaa' + str(faceDetail['BoundingBox']['Height']))

        Height = float(str(faceDetail['BoundingBox']['Height']))
        Left = float(str(faceDetail['BoundingBox']['Left']))
        Top = float(str(faceDetail['BoundingBox']['Top']))
        Width = float(str(faceDetail['BoundingBox']['Width']))

        # print('The emotions are:' + str(faceDetail['Emotions']))
        for emotion in faceDetail['Emotions']:
            confianza = float(str(emotion["Confidence"]))
            emocion = str(emotion["Type"])
            # confianza_final = max(confianza_final, confianza)
            if confianza > confianza_final:
                emocion_final = emocion
                confianza_final = confianza

    # print (response)
    print(' Confianza: ' + str(confianza_final))
    print(' Emocion: ' + emocion_final)
    print('Top ' + str(Top))    
    print('Left ' + str(Left))
    print('Height": ' + str(Height))
    print('Width: ' + str(Width))

    # print('Here are the other attributes:')
    # print(json.dumps(faceDetail, indent=4, sort_keys=True))

    # traemos las imagen de s3

    try:
        s3.Bucket(bucket).download_file(fileName, 'local.jpg')
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            print("The object does not exist.")
        else:
            raise



    image_emotion_name = emocion_final + '.png'
    try:
        s3.Bucket(bucket).download_file(image_emotion_name,'emotion_local.png')
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            print("The object does not exist.")
        else:
            raise
    

    til = Image.open('local.jpg')
    image_width, image_height = til.size

    print("width_" + str(image_width) + "  height_: " + str(image_height))


    x1 = int(image_width * Left)
    y1 = int(image_height * Top)
    scale_x = int(image_width * Width )
    scale_y = int(image_height * Height)
    resize = scale_x,scale_y
    print(" x1: " + str(x1) + " y1: " + str(y1))
    # print(" x2: " + str(x2) + " y2: " + str(y2))
    # print("image_width" + str(image_width) + " Left: " + str(Left))
    
    
    # pos1 = width_ *

    icon = Image.open('emotion_local.png')
    icon.thumbnail(resize, Image.ANTIALIAS)
    icon.save("salida_.png")
    til.paste(icon, (x1,y1), icon)
    til.save("result.png")

    # til.paste()
