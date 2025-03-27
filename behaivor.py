import time

motion_detected = False
cat_in_picture = False

def detect():
  # Wait for 5 minutes
  time.sleep(300)
  if (motion_detected):
    take_picture()
    if(cat_in_picture):
      play_with_cat()
  delete_photos()

def take_picture():
  print("Picture Taken")

def play_with_cat():
  print("Playing with Cat")

def delete_photos():
  print("Photos Delted")

