from kagglehub import enum
import pandas as pd
import os
import kagglehub
from face import skin
from complexion import analyze

# Download latest version
path = kagglehub.dataset_download("jangedoo/utkface-new")
print("Path to dataset files:", path)

image_files = []

for root, dirs, files in os.walk(path):
    for file in files:
        if file.lower().endswith((".jpg", ".jpeg", ".png")):
            image_files.append(os.path.join(root, file))

image_files=image_files[:1000]
print("Number of images :", len(image_files))
rows=[]

for i, img in enumerate(image_files):

    print(f"Processing {(i+1)/len(image_files)} : {img}")

    try:

        image_path = os.path.join(path, img)
        hex_color,rgb,lab = skin(image_path)
        complexion, undertone, _ = analyze(hex_color)

        row = {
            "image": img,
            "RGB" : rgb,
            "LAB" : lab,
            "hex": hex_color,
            "complexion": complexion,
            "undertone": undertone
        }

        rows.append(row)

    except Exception as e:

        print(f"Failed: {img}")
        print("Reason:", e)

    df= pd.DataFrame(rows)

output_path = os.path.join(os.getcwd(),"test_results.csv")
df.to_csv(output_path, index=False)
print("\nCSV saved to:", output_path)
print("Successful images:", len(df))