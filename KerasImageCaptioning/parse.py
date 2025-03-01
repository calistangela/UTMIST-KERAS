import os

# Parce the Flicker8k_Dataset

def parse_flicker():
    accumulator = ""
    with open("Datasets/token.txt", "r") as readfile:
        accumulator = readfile.read()

    imagesFolder = "Flicker8k_Dataset"
    with open("Datasets/Flickr8k.token.txt", "r") as readfile, open("Datasets/token.txt", "w") as writefile:
        lines = readfile.readlines()
        for i, line in enumerate(lines):
            imageName, info = line[:line.index("#")], line[line.index("#"):]
            imageName = os.path.join(imagesFolder, imageName).replace("\\", "/")
            accumulator += imageName + info

        writefile.write(accumulator)

parse_flicker()


import ijson
# https://medium.com/@lakshmi_priya_ramisetty/handling-large-json-files-without-fully-loading-them-into-memory-ce3d020a3f82
def process_large_json(file_path, imagesFolder):
    # Open the large JSON file
    accumulator = ""
    with open("Datasets/token.txt", "r") as readfile:
        accumulator = readfile.read()


    with open(file_path, 'rb') as readfile, open("Datasets/token.txt", "w") as writefile:
        # Use ijson to parse the file incrementally
        images_data = ijson.items(readfile, "annotations.item")
        caption_count = {}
        # Iterate over the parsing events

        for item in images_data:
            image_id, caption = item["image_id"], item["caption"]
            caption_count[image_id] = caption_count.get(image_id, 0)
            imageName = "{:012d}".format(image_id) + ".jpg"
            imagePath = os.path.join(imagesFolder, imageName).replace("\\", "/")
            entry = imagePath + "#" + str(caption_count[image_id]) + "\t" + caption
            entry = entry.strip("\n")
            accumulator += entry + "\n"
            caption_count[image_id] += 1 # Next caption will be incremented by one

        writefile.write(accumulator)

process_large_json("annotations_trainval2017/annotations/captions_val2017.json", "val2017")
#process_large_json("annotations_trainval2017/annotations/captions_train2017.json", "train2017")

