import tensorflow as tf
from tensorflow.keras.preprocessing import image
import numpy as np
# import matplotlib.pyplot as plt

def run_model(model, imgpath):

    img = image.load_img(imgpath, target_size=(224, 224))  # Resize

    # convert to array
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = img_array / 255.0  # Normalize to [0, 1]

    #plt.imshow(img)
    #plt.axis('off')
    #plt.show()

    # RUN IMAGE THROUGH MODEL
    prediction = model.predict(img_array)

    # Debug
    print(f"Prediction shape: {prediction.shape}")
    print(f"Prediction: {prediction}")
    print(f"Prediction value: {prediction[0][0]:.4f}")
    print(f"Image: {imgpath}")

    # the prediction value is stored here. The lower the value, the higher the likelihood that there's a cat.
    if prediction[0][0] < 0.5:
        print("It's a cat!")

        # INSERT STUFF HERE

    else:
        print("It's not a cat.")

        # DO OTHER THINGS HERE


def main():
    # Load the saved model
    # Ignore the compilation warning--don't have to bother with it ATM
    model = tf.keras.models.load_model("cat_detector.h5")

    # image paths
    img1p = "test_images/cookie.jpg"
    img2p = "test_images/noortree.jpg"
    img3p = "test_images/noorbag.jpg"
    img4p = "test_images/dude.jpg"

    run_model(model, img1p)
    run_model(model, img2p)
    run_model(model, img3p)
    run_model(model, img4p)



if __name__ == '__main__':
    main()


