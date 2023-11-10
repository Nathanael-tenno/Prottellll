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
    
    # Preprocessing gambar untuk prediksi model
    processed_image = image / 255.0
    processed_image = cv2.resize(processed_image, (224, 224))
    processed_image = np.expand_dims(processed_image, axis=0)
    
    # Prediksi dari model tanpa progress bar
    predictions = model.predict(processed_image, verbose=0)
    predicted_class_index = np.argmax(predictions)
    predicted_class = label_classes[predicted_class_index]
    predicted_probability = predictions[0][predicted_class_index]

    # Menghitung persentase kesegaran
    freshness_percentage = predicted_probability * 100

    # Mengembalikan hasil prediksi dan persentase kesegaran
    return {
        "freshness": predicted_class,
        "confidence_percentage": freshness_percentage
    }

if __name__ == "__main__":
    import sys
    try:
        if len(sys.argv) < 2:
            print("Usage: python app.py [image_url]")
            sys.exit(1)

        # Menerima URL gambar sebagai argumen command-line
        image_url = sys.argv[1]
        prediction_result = predict(image_url)
        print(prediction_result)
    except Exception as e:
        print(f"Error: {e}")
