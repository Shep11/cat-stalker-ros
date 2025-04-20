import fiftyone as fo
import fiftyone.zoo as foz

# ONE TIME USE ONLY. Do not execute if there are images already in the data directory!

# If there are too many images and you need to download them yourself, replace the file paths in the code below.
# To maintain consistency, ensure that /data/cats and /data/notcats are still present.

# USE THE FULL FOLDER PATH! 

def load_cats():

    fo.config.dataset_zoo_dir = "C:/Users/Leila/Documents/GitHub/cat-stalker/cat_model/image_downloader/fiftyone/cats"

    dataset_cattrain = foz.load_zoo_dataset(
    "open-images-v7",
    split="train",
    dataset_name="cat_train",
    label_types=["detections", "classifications"],
    classes=["Cat"],
    max_samples=10, # 20000
    )

def load_notcats():

    fo.config.dataset_zoo_dir = "C:/Users/Leila/Documents/GitHub/cat-stalker/cat_model/image_downloader/fiftyone/notcats"

    dataset_not = foz.load_zoo_dataset(
    "open-images-v7",
    split="train",
    label_types=["detections", "classifications"],
    classes=["Furniture", "Person", "Building", "Toy", "Clothing"],
    max_samples=20, # 20000
    seed=51,
    shuffle=True,
    )
    #filtered_view = dataset.filter_labels(F("label").is_in(exclude_classes, invert=True))





if __name__ == "__main__":
    # Ensures that the App processes are safely launched on Windows

    # note that you may have to comment out one or the other just in case of a network timeout.
    load_cats()
    load_notcats()



