import cv2
import numpy as np
import tensorflow as tf
import tensorflow_hub as hub
import requests
import urllib

# model loading
model = tf.keras.models.load_model(
    'model/model.h5', 
    custom_objects={'KerasLayer': hub.KerasLayer}
)

# list of class
label_classes = [
    "FreshApple",
    "FreshBanana",
    "FreshBellpepper",
    "FreshCarrot",
    "FreshCucumber",
    "FreshMango",
    "FreshOrange",
    "FreshPotato",
    "FreshStrawberry",
    "FreshTomato",
    "RottenApple",
    "RottenBanana",
    "RottenBellpepper",
    "RottenCarrot",
    "RottenCucumber",
    "RottenMango",
    "RottenOrange",
    "RottenPotato",
    "RottenStrawberry",
    "RottenTomato"
]


# get image from url
def url_to_image(url):
    resp = urllib.request.urlopen(url)
    image = np.asarray(bytearray(resp.read()), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    return image

def predict(url):
    image = url_to_image(url)
    
    load = image/255.0
    load = cv2.resize(load, (224,224))
    z = tf.keras.utils.img_to_array(load)
    z = np.expand_dims(z, axis=0)
    images = np.vstack([z])
    classes = model.predict(images, verbose=0)
    index = np.argmax(classes) 
    freshness_level = label_classes[index]

    return ({"freshness": freshness_level})   

if __name__ == "__main__":
    import sys
    try:  
        if len(sys.argv) < 2:
            print("input url image : python app.py [image_url]")
            sys.exit(1)
        
        url = sys.argv[1]
        output = predict(url)
    except Exception as err:
        print(err)
    else:
        print(output)
