# How to use the image downloader

ONE TIME USE ONLY. Do not execute `fetch_images.py` if there are images already in the data directory or if the model has already been trained!
#### read the code comments!

Running it is as simple as navigating to `image_downloader/fiftyone` and running `fetch_images.py`.

Be sure to change the filepaths inside or else strange things will happen. It's better not to run it at all actually because of the sheer volume of images that will be downloaded. 

For this repository, I've maintained the file structure that results from running `fetch_images.py`. You can see them in `/fiftyone` under `/cats/` and `/noncats`. The `data` folders originally contained all the images that were downloaded, but in this case, I've removed them and instead placed dummy text files just so the folders actually show up. The reason I did this is because the sheer number of images would've made this repository too large to manage. The metadata was retained, however.

---

#### Due to how files are managed in Fiftyone, it may be necessary to rename directories or move folders around.


Outside of `/image_downloader`, create a folder called `raws` and inside it create a folder `images`.

After running the image downloader, you'll notice that several directories have been created:

`fiftyone / cats / open-images-v7 / train`

For the folder named `data` inside the `train` directory, rename it to `cats`. Move `cats` into the `images` folder you created. Do the same thing for `notcats`.

`images` should have two folders within: `cats` and `noncats`.

Next, create a folder called `dataset` inside `cat_model`. 

Run `datasplit.py` from the `cat_model` directory.


------

# Running the model

See `run_model.py` as an example and read the code comments. `run_model.py` is a sample pipeline.

REQUIREMENTS:

`tensorflow 2.19.0`

`keras 3.9.2`




