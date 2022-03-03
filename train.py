import face_recognition
import os
import pickle

image_folder = "images"
jitter = 100

known_face_encodings = []
known_face_names = []


for subfolder in os.listdir(image_folder):
    # processing each file in the subfolder
    print("Processing folder: " + subfolder)
    for filename in os.listdir(os.path.join(image_folder, subfolder)):
        print("\tProcessing file: " + filename)
        image = face_recognition.load_image_file(os.path.join(image_folder, subfolder, filename))
        face_encoding = face_recognition.face_encodings(image, num_jitters=jitter)[0]
        known_face_encodings.append(face_encoding)
        known_face_names.append(subfolder)


data = {"encodings": known_face_encodings, "names": known_face_names}
# save data
with open("data.pickle", "wb") as f:
    pickle.dump(data, f)
