import os
import shutil

for file in os.listdir('kaggle_princess_dataset/arura'):
   file_img = os.path.join('kaggle_princess_dataset/arura/',file)
   shutil.copy2(file_img,os.path.join('aurora/','kaggle'+file))
    
for file in os.listdir('kaggle_princess_dataset/ruponzel'):
    file_img = os.path.join('kaggle_princess_dataset/ruponzel/',file)
    shutil.copy2(file_img,os.path.join('rapunzel/','kaggle'+file))
    
for file in os.listdir('kaggle_princess_dataset/Snow White'):
    file_img = os.path.join('kaggle_princess_dataset/Snow White/',file)
    shutil.copy2(file_img,os.path.join('snow_white/','kaggle'+file))
    