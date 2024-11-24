"""
# -*- coding: utf-8 -*-
verdora.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1iIVTiBYmz7T9XEUyPoT1HajGpSaMdDEq


# %pip install huggingface_hub
# %pip install -U yolov5
# %pip install gradio

from PIL import Image
import numpy as np
import io
import yolov5
import keras

import cv2
from pathlib import Path
import os
from pprint import pprint
from typing import Iterable
import tempfile

# import gradio as gr

from huggingface_hub import from_pretrained_fastai
from huggingface_hub import from_pretrained_keras

from huggingface_hub import hf_hub_download, list_repo_files
from google.colab import userdata

from ultralytics import YOLO


### Experimenting with random recycling classification model

from huggingface_hub import from_pretrained_keras

model = from_pretrained_keras("viola77data/recycling")

model.summary()

# Commented out IPython magic to ensure Python compatibility.
# %ls

with open("food_scraps.png", "rb") as image:
  image_data = image.read()
  image = Image.open(io.BytesIO(image_data)).convert("RGB")
  image = image.resize((224, 224))  # expected input size
  input_array = np.array(image) / 255.0  # normalize pixel values
  input_array = np.expand_dims(input_array, axis=0)  # add batch dimension

  # Perform prediction
  predictions = model.predict(input_array)

print(predictions)


Not worth looking into for now.


### Experimenting with YOLOv5 Object Detection


def inference(file_path, model, visualize = True):

  with open(file_path, "rb") as image:
    image_data = image.read()
    image = Image.open(io.BytesIO(image_data)).convert("RGB")
    img_array = np.array(image)

  # perform inference
  # results = model(img_array, size=640)
  results = model(img_array, augment=True)

  # parse results
  predictions = results.pred[0]
  boxes = predictions[:, :4] # x1, y1, x2, y2
  scores = predictions[:, 4]
  categories = predictions[:, 5]

  outputs = []

  for box, score, category in zip(boxes, scores, categories):
    x1, y1, x2, y2 = map(int, box)  # Convert box coordinates to integers
    label = f'{model.names[int(category)]}: {score:.2f}'

    outputs.append({"label": model.names[int(category)], "confidence": float(score), "bbox": [x1, y1, x2, y2]})

    # For visualization only
    if visualize:
      cv2.rectangle(img_array, (x2, y1), (x1, y2), (0, 255, 0), 2)  # Bounding box
      cv2.putText(img_array, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2) # Text

  if visualize:
    img_array = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
    cv2_imshow(img_array)

  return outputs


#### YOLOv5s

# load model
small_model = yolov5.load('keremberke/yolov5s-garbage')

# set model parameters
small_model.conf = 0.53  # NMS confidence threshold
small_model.iou = 0.40  # NMS IoU threshold
small_model.agnostic = True  # NMS class-agnostic
small_model.multi_label = False
small_model.max_det = 10

print(small_model.names)

current_dir = Path(os.getcwd())

# Loop through all files in the directory
for file in current_dir.iterdir():
    # Only process image files (you can customize this by checking extensions)
    if file.is_file() and file.suffix.lower() in ['.jfif','.jpg', '.jpeg', '.png', '.webp']:
        output = inference(file, small_model)
        pprint(output)


#### YOLOv5m

# load model
medium_model = yolov5.load('keremberke/yolov5m-garbage')

# set model parameters
medium_model.conf = 0.53  # NMS confidence threshold
medium_model.iou = 0.40  # NMS IoU threshold
medium_model.agnostic = False  # NMS class-agnostic
medium_model.multi_label = False
medium_model.max_det = 15

print(medium_model.names)

current_dir = Path(os.getcwd())

# Loop through all files in the directory
for file in current_dir.iterdir():
    # Only process image files (you can customize this by checking extensions)
    if file.is_file() and file.suffix.lower() in ['.jfif','.jpg', '.jpeg', '.png', '.webp']:
        output = inference(file, medium_model)
        pprint(output)


### Experiments with Pre-trained Keras Classifier

keras_model = from_pretrained_keras('chaninder/trashtacks-model-final')

# !pip install gradio

labels = ['compost', 'e-waste', 'recycle', 'trash']

def classify_image(file_path):
    with open(file_path, "rb") as image:
      image_data = image.read()
      image = Image.open(io.BytesIO(image_data)).convert("RGB")

    img_array = np.array(image)

    display_img = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
    cv2_imshow(display_img)

    img_array = np.expand_dims(img_array, axis=0)

    # img_array = keras.applications.mobilenet_v2.preprocess_input(img_array)
    prediction = keras_model.predict(img_array).flatten()
    confidences = {labels[i]: float(prediction[i]) for i in range(4)}

    return confidences

current_dir = Path(os.getcwd())

# Loop through all files in the directory
for file in current_dir.iterdir():
    # Only process image files (you can customize this by checking extensions)
    if file.is_file() and file.suffix.lower() in ['.jfif','.jpg', '.jpeg', '.png', '.webp']:
        output = classify_image(file)
        print(output)


Very subpar model.


### Experimenting with Specific Recycling Classification Models


materials_model = from_pretrained_fastai("pyesonekyaw/recycletree_materials")
paper_model = from_pretrained_fastai("pyesonekyaw/recycletree_paper")
plastic_model = from_pretrained_fastai("pyesonekyaw/recycletree_plastic")
metal_model = from_pretrained_fastai("pyesonekyaw/recycletree_metal")
others_model = from_pretrained_fastai("pyesonekyaw/recycletree_others")
glass_model = from_pretrained_fastai("pyesonekyaw/recycletree_glass")

recycling_models = {"materials": materials_model, "paper": paper_model, "plastic": plastic_model, "metal": metal_model, "others": others_model, "glass": glass_model }


#### Constants

material_names = ['Glass', 'Metal', 'Others', 'Paper', 'Plastic']
plastic_names = ['CD Disk', 'Straw', 'Plastic Bag', 'Clothes Hanger', 'Plastic Container or Bottle',
                 'Disposable Cutlery', 'Plastic Packaging', 'Plastic Packaging With Foil', 'Styrofoam']
paper_names = ['Beverage Carton', 'Cardboard', 'Chopsticks', 'Disposables', 'Paper Bag', 'Paper Packaging',
               'Paper Product', 'Receipt', 'Paper Roll', 'Paper Sheet', 'Tissue Box', 'Tissue Paper']
glass_names = ['Ceramic', 'Glassware', 'Lightbulb']
other_names = ['Battery', 'Electronic Waste', 'Stationery']
metal_names = ['Aerosol Can', 'Aluminium Foil or Tray', 'Metal Can or Container']

material_num_name_dict = {
  "metal": "Metal",
  "glass": "Glass",
  "paper": "Paper",
  "plastic": "Plastic",
  "others": "Others",
}

plastic_item_num_dict = {
  "CD Disk": ["yes", "N/A"],
  "Straw": ["no","N/A"],
  "Plastic Bag": ["yes", "when there is any remaining food contents or other residue, or when they are biodegradable bags"],
  "Clothes Hanger": ["yes", "when they are made up of more than one type of plastic. If unsure, dispose as normal waste."],
  "Plastic Container or Bottle": ["yes", "when there is any remaining food contents or other residue "],
  "Disposable Cutlery": ["no", "N/A"],
  "Plastic Packaging": ["yes", "when contaminated with food contents, like when directly enclosing food"],
  "Plastic Packaging With Foil": ["no","N/A"],
  "Styrofoam": ["no","N/A"]
}
glass_item_num_dict = {
  "Ceramic": ["no", "it could be reusable, depending on the condition"],
  "Glassware": ["yes","when there is any remaining food contents or other residue"],
  "Lightbulb": ["no", "N/A"]
}
metal_item_num_dict = {
  "Aerosol Can": ["yes","If there are any remaining contents in the can"],
  "Aluminium Foil or Tray": ["yes","when there is any remaining food contents or other residue"],
  "Metal Can or Container": ["yes","when there is any remaining food contents or other residue"]
}
others_item_num_dict = {
  "Battery": ["no","can be recycled through specific collection points (e-waste collection)"],
  "Electronic Waste": ["no","can be recycled through specific collection points (e-waste collection)"],
  "Stationery": ["no", "it could be reusable, depending on the condition"]
}
paper_item_num_dict = {
  "Beverage Carton": ["yes","as long as they are rinsed and flattened"],
  "Cardboard": ["yes", "when there are remains of other materials such as tape, or they are contaminated with other waste"],
  "Chopsticks": ["no", "N/A"],
  "Disposables": ["no", "N/A"],
  "Paper Bag": ["yes","when there is any remaining food contents or other residue"],
  "Paper Packaging": ["yes", "unless made up of more than one material or contaminated with food waste"],
  "Paper Product": ["yes", "unless contaminated with other waste"],
  "Receipt": ["yes", "unless contaminated with other waste"],
  "Paper Roll": ["yes", "unless contaminated with other waste"],
  "Paper Sheet": ["yes", "unless contaminated with other waste "],
  "Tissue Box": ["yes", "if plastic lining is not removed or it is contaminated with other waste"],
  "Tissue Paper": ["no", "N/A"]
}


#### Function

def 
classify_for_recycling(file_name, recycling_models, visualize = True):
    
    
    Performs inference for a given input image and returns the prediction and CAM image.
    
    materials_model = recycling_models['materials']
    paper_model = recycling_models['paper']
    plastic_model = recycling_models['plastic']
    metal_model = recycling_models['metal']
    glass_model = recycling_models['glass']
    other_model = recycling_models['others']

    with open(file_name, "rb") as image:
        image_data = image.read()
        image = Image.open(io.BytesIO(image_data)).convert("RGB")
        img_array = np.array(image)

        # Only for visualization
        if visualize:
          cv2_imshow(cv2.cvtColor(img_array, cv2.COLOR_BGR2RGB))

    material_label, material_label_idx, material_probs = materials_model.predict(img_array)
    material_preds = {name: prob for name, prob in zip(material_names, material_probs.tolist())}

    if material_label == 'paper':
        specific_label, specific_label_idx, specific_probs = paper_model.predict(img_array)
        specific_preds = {name: prob for name, prob in zip(paper_names, specific_probs.tolist())}
        specific_label = paper_names[int(specific_label_idx)]
        recyclable_qn = paper_item_num_dict[specific_label][0]
        recyclable_advice = paper_item_num_dict[specific_label][1]

    elif material_label == 'plastic':
        specific_label, specific_label_idx, specific_probs = plastic_model.predict(img_array)
        specific_preds = {name: prob for name, prob in zip(plastic_names, specific_probs.tolist())}
        specific_label = plastic_names[int(specific_label_idx)]
        recyclable_qn = plastic_item_num_dict[specific_label][0]
        recyclable_advice = plastic_item_num_dict[specific_label][1]

    elif material_label == 'glass':
        specific_label, specific_label_idx, specific_probs = glass_model.predict(img_array)
        specific_preds = {name: prob for name, prob in zip(glass_names, specific_probs.tolist())}
        specific_label = glass_names[int(specific_label_idx)]
        recyclable_qn = glass_item_num_dict[specific_label][0]
        recyclable_advice = glass_item_num_dict[specific_label][1]

    elif material_label == 'metal':
        specific_label, specific_label_idx, specific_probs = metal_model.predict(img_array)
        specific_preds = {name: prob for name, prob in zip(metal_names, specific_probs.tolist())}
        specific_label = metal_names[int(specific_label_idx)]
        recyclable_qn = metal_item_num_dict[specific_label][0]
        recyclable_advice = metal_item_num_dict[specific_label][1]

    elif material_label == 'others':
        specific_label, specific_label_idx, specific_probs = others_model.predict(img_array)
        specific_preds = {name: prob for name, prob in zip(other_names, specific_probs.tolist())}
        specific_label = other_names[int(specific_label_idx)]
        recyclable_qn = others_item_num_dict[specific_label][0]
        recyclable_advice = others_item_num_dict[specific_label][1]

    return material_preds, material_label, specific_preds, specific_label, recyclable_qn, recyclable_advice


#### Test runs

current_dir = Path(os.getcwd())

# Loop through all files in the directory
for file in current_dir.iterdir():
    if file.is_file() and file.suffix.lower() in ['.jfif','.jpg', '.jpeg', '.png', '.webp']:
      outputs = classify_for_recycling(file, recycling_models)
      pprint(outputs)


Seems to be reliable enough for plastics, glass, paper, and sometimes metal. If biodegradable, do NOT use this.


### Experimenting with Clothes Detection


hf_model_id = 'kesimeg/yolov8n-clothing-detection'
hf_token = userdata.get('HF_TOKEN')

repo_files = list_repo_files(repo_id=hf_model_id, repo_type="model", token=hf_token)

# download config file for triggering download counter
config_file = "config.json"
if config_file in repo_files:
    _ = hf_hub_download(
        repo_id=hf_model_id,
        filename=config_file,
        repo_type="model",
        token=hf_token,
    )

# download model file
model_file = [f for f in repo_files if f.endswith(".pt")][0]
file = hf_hub_download(
    repo_id=hf_model_id,
    filename=model_file,
    repo_type="model",
    token=hf_token,
)

clothing_model = YOLO(file)

def find_clothes(file_name, clothing_model, visualize = True):

  with open(file_name, "rb") as image:
    image_data = image.read()
    image = Image.open(io.BytesIO(image_data)).convert("RGB")
    img_array = np.array(image)

  labels = ["accessories", "bags", "clothing", "shoes"]
  results = clothing_model.predict(file_name)
  boxes = results[0].boxes

  xyxy = boxes.xyxy.cpu().numpy()  # Bounding box coordinates
  conf = boxes.conf.cpu().numpy()  # Confidence scores
  cls = boxes.cls.cpu().numpy()    # Class indices

  outputs = []
  for i in range(len(xyxy)):
    x1, y1, x2, y2 = map(int, xyxy[i])
    confidence = conf[i]
    class_idx = int(cls[i])
    label = labels[class_idx]

    outputs.append({"label": label, "bbox": [x1,y1,x2,y2], "confidence":float(confidence)})

    # Only for visualization:
    if visualize:
      color = (0, 255, 0)  # Green
      text = f"{label} {confidence:.2f}"

      cv2.rectangle(img_array, (x1, y1), (x2, y2), color, 2)
      font = cv2.FONT_HERSHEY_SIMPLEX
      text_size = cv2.getTextSize(text, font, 0.5, 2)[0]
      text_x, text_y = x1, y1 - 10 if y1 - 10 > 10 else y1 + 10
      cv2.rectangle(
          img_array,
          (text_x, text_y - text_size[1] - 5),
          (text_x + text_size[0] + 5, text_y + 5),
          color,
          -1,
      )
      cv2.putText(img_array, text, (text_x, text_y), font, 0.5, (0, 0, 0), 1)
  if visualize:
    image_bgr = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
    cv2_imshow(image_bgr)

  return outputs

print(find_clothes("tshirt_jeans.jpg", clothing_model))


## Combining Models


### Combining Clothing and Waste Detection Models


main_annotations = inference("plastic_bottle.jpg", medium_model)
clothing_annotations = find_clothes("plastic_bottle.jpg", clothing_model)

print(main_annotations + clothing_annotations)


The clothing model very confidently guesses that there are clothes in this picture. To fix this, we can
 calculate the IOU of the two regions (ratio of overlap to total area), and if it's high then disregard the clothing model's results.

def compare_bounding_box_formats(file, main_bbox, clothing_bbox):

  with open(file, "rb") as image:
    image_data = image.read()
    image = Image.open(io.BytesIO(image_data)).convert("RGB")
    img_array = np.array(image)

  mx1, my1, mx2, my2 = main_bbox
  main_point1_color = (255,0,0) # Red
  main_point2_color = (0,0,255) # Blue

  cx1, cy1, cx2, cy2 = clothing_bbox
  clothing_point1_color = (255,0,255) # Purple
  clothing_point2_color = (0,255,255) # Cyan

  cv2.circle(img_array, (mx2,my1), 2, main_point1_color, 2)   # ] - Found that we had to switch the order of these
  cv2.circle(img_array, (mx1,my2), 2, main_point2_color, 5)   # ]
  cv2.rectangle(img_array, (mx2,my1), (mx1,my2), (0,255,0), 1)

  cv2.circle(img_array, (cx1,cy1), 2, clothing_point1_color, 2)
  cv2.circle(img_array, (cx2,cy2), 2, clothing_point2_color, 5)
  cv2.rectangle(img_array, (cx1,cy1), (cx2,cy2), (0,255,0), 1)

  img_array = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
  cv2_imshow(img_array)

compare_bounding_box_formats("plastic_bottle.jpg",  [196, 50, 314, 491], [194, 66, 314, 489])


Initially, the bounding box formats were inconsistent (the
y were stored as sets, and were also in the wrong order). Now that we fixed this, we can combat the issue of VERY wrong outputs.

# Returns a value between 0-1
def calculate_iou(rect1, rect2):
    ax1, ay1, ax2, ay2 = rect1
    bx1, by1, bx2, by2 = rect2

    # Check that the x1,y1 co-ordinates are top left
    assert bx1 < bx2
    assert by1 < by2
    assert ax1 < ax2
    assert ay1 < ay2

    # determine the coordinates of the intersection rectangle
    x_left = max(ax1, bx1)
    y_top = max(ay1, by1)
    x_right = min(ax2, bx2)
    y_bottom = min(ay2, by2)

    if x_right < x_left or y_bottom < y_top:
        return 0.0

    # The intersection of two axis-aligned bounding boxes is always an
    # axis-aligned bounding box
    intersection_area = (x_right - x_left) * (y_bottom - y_top)

    # compute the area of both AABBs
    bb1_area = (ax2 - ax1) * (ay2 - ay1)
    bb2_area = (bx2 - bx1) * (by2 - by1)

    # compute the intersection over union by taking the intersection
    # area and dividing it by the sum of prediction +
    # ground-truth areas - the interesection area
    iou = intersection_area / float(bb1_area + bb2_area - intersection_area)
    assert iou >= 0.0
    assert iou <= 1.0
    return iou

def get_corrected_clothing_annotations(main_annotations, clothing_annotations):

  for main_annotation in main_annotations:
    for clothing_annotation in clothing_annotations:
      main_bbox = main_annotation["bbox"]
      cloth_bbox = clothing_annotation["bbox"]
      iou = calculate_iou(main_bbox, cloth_bbox)
      print(iou)
      if iou >= 0.50:
        clothing_annotations.remove(clothing_annotation)

  return clothing_annotations

main_annotations = inference("plastic_bottle.jpg", medium_model, visualize = False)
clothing_annotations = find_clothes("plastic_bottle.jpg",clothing_model, visualize = False)

print(get_corrected_clothing_annotations(medium_model, clothing_model))


### Combining Waste Detection Output with Recycling Classification Pipeline


#### Flagging E-waste


def 
flag_ewaste(file_name, models, visualize=True):
    
    Processes an image file, divides it into 3x3 blocks, saves each block as a temporary file,
    and performs classification on each block, as well as the whole image.

    Then analyzes the list of 5 dictionaries with recycling classification results.

    Args:
        file_name (str): Path to the image file.
        models (dict): Dictionary containing material and specific classification models.
        visualize (bool): Whether to visualize the image and blocks.

    Returns:
    
        results (bool, float): Whether it contains e-waste, and what the confidence is.
    

    results = []
    material_preds, material_label, specific_preds, specific_label, recyclable_qn, recyclable_advice = classify_for_recycling(
                file_name, models, visualize = visualize)

    results.append({
        "block_index": 0,
        "material_preds": material_preds,
        "material_label": material_label,
        "specific_preds": specific_preds,
        "specific_label": specific_label,
        "recyclable_qn": recyclable_qn,
        "recyclable_advice": recyclable_advice
    })

    with open(file_name, "rb") as image:
        image_data = image.read()
        image = Image.open(io.BytesIO(image_data)).convert("RGB")
        img_array = np.array(image)

    # Divide the image into 2x2 blocks
    h = img_array.shape[0]
    w = img_array.shape[1]
    M = h//2
    N = w//2
    tiles = [img_array[x:x+M,y:y+N] for x in range(0,h,M) for y in range(0,w,N)]

    # Perform classification on each block
    for idx, block in enumerate(tiles):
        # Save block as a temporary file
        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as temp_file:
            block_path = temp_file.name
            block_img = Image.fromarray(block)
            block_img.save(block_path)

        try:
            material_preds, material_label, specific_preds, specific_label, recyclable_qn, recyclable_advice = classify_for_recycling(
                block_path, models, visualize = visualize)

            results.append({
                "block_index": idx+1,
                "material_preds": material_preds,
                "material_label": material_label,
                "specific_preds": specific_preds,
                "specific_label": specific_label,
                "recyclable_qn": recyclable_qn,
                "recyclable_advice": recyclable_advice
            })
        finally:
            # Clean up the temporary file
            os.remove(block_path)

    ewaste_flag = False
    confidence = 0
    for result in results:
      if result['material_preds']['Others'] > 0.5 and result['material_preds']['Others'] > 0.5:
        ewaste_flag = True
        confidence = result['material_preds']['Others'] * result['material_preds']['Others']
        break

    return (ewaste_flag, round(float(confidence),2))

flag_ewaste("broken_phone.jpg", recycling_models)

flag_ewaste("plastic_bottle.jpg", recycling_models, visualize = False)


#### Adding Recycling Info to Object Detection Output

OD_anntns = inference("plastic_bottle.jpg", medium_model, visualize = False)

print(OD_anntns)

def 
classify_and_update_annotations(file_name, annotations, recycling_models, visualize_crops = False, visualize=True):
    
    Processes an image based on bounding box annotations, performs classification, and updates annotations.

    Args:
        file_name (str): Path to the image file.
        annotations (list): List of bounding box annotations with format:
                            [{'label': str, 'confidence': float, 'bbox': [x_min, y_min, x_max, y_max]}]
        recycling_models (dict): Dictionary containing material and specific classification models.
        visualize (bool): Whether to visualize the bounding boxes and cropped regions.

    Returns:
    
        updated_annotations (list): List of updated annotations with recycling information.
    
    # Load the image
    image = Image.open(file_name).convert("RGB")
    img_array = np.array(image)

    # Create a copy of annotations to update
    updated_annotations = []

    for idx, annotation in enumerate(annotations):
        label = annotation['label']
        bbox = annotation['bbox']
        conf = annotation['confidence']

        # Expand the bounding box slightly (e.g., by 10%)
        x_min, y_min, x_max, y_max = bbox
        h, w, _ = img_array.shape
        pad_x = int((x_max - x_min) * 0.1)
        pad_y = int((y_max - y_min) * 0.1)

        x_min = max(0, x_min - pad_x)
        y_min = max(0, y_min - pad_y)
        x_max = min(w, x_max + pad_x)
        y_max = min(h, y_max + pad_y)

        # Crop the image around the bounding box
        cropped_img = img_array[y_min:y_max, x_min:x_max]

        # Save the cropped image as a temporary file
        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as temp_file:
            cropped_path = temp_file.name
            cropped_img_pil = Image.fromarray(cropped_img)
            cropped_img_pil.save(cropped_path)

        if visualize_crops:
            # Draw bounding box on the image for visualization
            img_with_box = img_array.copy()
            cv2.rectangle(
                img_with_box,
                (x_min, y_min),
                (x_max, y_max),
                color=(0, 255, 0),
                thickness=2
            )
            print(f"Annotation {idx + 1}")
            cv2_imshow(cv2.cvtColor(img_with_box, cv2.COLOR_RGB2BGR))

        # Classify the cropped image
        material_preds, material_label, specific_preds, specific_label, recyclable_qn, recyclable_advice = classify_for_recycling(
            cropped_path,
            recycling_models,
            visualize=visualize
        )

        # print(f"Main label: {label}, material label: {material_label}")
        # print(f"Main label: {conf}, material label: {material_preds}")

        # Remove the temporary file
        os.remove(cropped_path)

        # Update annotation based on label and classification
        if label in {'plastic', 'metal', 'glass', 'paper'}:
            # Check if the material label matches with confidence > 0.5
            if material_preds.get(label.capitalize(), 0) > 0.5:
                annotation['recycling'] = {
                    'possible_type': specific_label,
                    'should_recycle': recyclable_qn,
                    'caution': recyclable_advice
                }
            else:
                annotation['recycling'] = {
                    'possible_type': "the model is uncertain",
                    'should_recycle': "yes",
                    'caution': "double check whether it can be recycled, given its condition and material composition!"
                }
        elif label in {'cardboard'}:
            # Check if the specific label matches with confidence > 0.5
            if specific_label.get(label.capitalize(), 0) > 0.5:
                annotation['recycling'] = {
                    'possible_type': specific_label,
                    'should_recycle': recyclable_qn,
                    'caution': recyclable_advice
                }
            else:
                annotation['recycling'] = {
                    'possible_type': "the model is uncertain",
                    'should_recycle': "yes",
                    'caution': "if there are plastic or other contaminants"
                }
        elif label in {'clothing', 'biodegradable'}:
            annotation['recycling'] = None
        else:
            annotation['recycling'] = None

        updated_annotations.append(annotation)

    return updated_annotations

bottle_annts = inference("plastic_bottle.jpg", medium_model, visualize = False)
updated_anntns = classify_and_update_annotations("plastic_bottle.jpg", bottle_annts, recycling_models, visualize_crops = True)

pprint(updated_anntns)

can_anntns = inference("crumpled_cans.webp", medium_model, visualize = False)
updated_anntns = classify_and_update_annotations("crumpled_cans.webp", can_anntns, recycling_models)

pprint(updated_anntns)

cloth_anntns = inference("tshirt_jeans.jpg", medium_model, visualize = False)
updated_anntns = classify_and_update_annotations("tshirt_jeans.jpg", cloth_anntns, recycling_models)

print(updated_anntns)

cloth_anntns = inference("clothes_pile.webp", medium_model, visualize = False)
updated_anntns = classify_and_update_annotations("clothes_pile.webp", cloth_anntns, recycling_models, visualize = False)

updated_anntns

def get_corrected_main_annotations(main_annotations, clothing_annotations):
  if len(clothing_annotations) == 0:
    return main_annotations

  for clothing_annotation in clothing_annotations:
    for main_annotation in main_annotations:

      uncertainty = main_annotation['recycling']['possible_type']
      label = main_annotation['label']
      main_bbox = main_annotation["bbox"]
      cloth_bbox = clothing_annotation["bbox"]

      iou = calculate_iou(main_bbox, cloth_bbox)

      if iou >= 0.30 and uncertainty == 'the model is uncertain':
        main_annotations.remove(main_annotation)

  return main_annotations

clothes_annotations = find_clothes("tshirt_jeans.jpg", clothing_model, visualize = False)

corrected_updated_anntns = get_corrected_main_annotations(updated_anntns, clothes_annotations)

print(corrected_updated_anntns)


## Complete Pipeline for /classify Endpoint

def classify(file_name, main_model, clothing_model, recycling_models):

  main_annotations = inference(file_name, main_model, visualize = False)
  clothing_annotations = find_clothes(file_name, clothing_model, visualize = False)

  corrected_clothing_annotations = get_corrected_clothing_annotations(main_annotations, clothing_annotations)

  main_annotations = main_annotations + corrected_clothing_annotations

  main_annotations_with_recycling = classify_and_update_annotations(file_name, main_annotations, recycling_models, visualize = False)
  corrected_recycling_annotations = get_corrected_main_annotations(main_annotations_with_recycling, corrected_clothing_annotations)

  return corrected_recycling_annotations

print(classify("random.jpg", medium_model, clothing_model, recycling_models))

print(flag_ewaste("random.jpg", recycling_models, visualize = False))


### Checking base64 encoded images

import base64
def 
encode_image_to_base64(file_name):
    
    Encodes an image file into a base64 string.

    Args:
        file_name (str): Path to the image file.

    Returns:
    
        str: The base64 encoded string of the image.
    
    with open(file_name, "rb") as image_file:
        # Read the image file
        image_data = image_file.read()
        # Encode the image data in base64
        base64_encoded = base64.b64encode(image_data).decode("utf-8")

    return base64_encoded

enc = encode_image_to_base64("broken_phone.jpg")

def 
save_base64_to_temp_file(base64_string):
    
    Decodes a base64 string and saves it as a temporary file.

    Args:
        base64_string (str): The base64 encoded image string.

    Returns:
    
        str: The file path of the saved temporary file.
    
    # Decode the base64 string to binary data
    image_data = base64.b64decode(base64_string)

    # Create a temporary file to store the decoded image
    with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as temp_file:
        # Write the decoded image data to the temporary file
        temp_file.write(image_data)
        temp_file_path = temp_file.name  # Get the file path

    return temp_file_path

def classify_base64(encoding, model, clothing_model, recycling_models):
  file_name = save_base64_to_temp_file(encoding)
  return classify(file_name, model, clothing_model, recycling_models)

classify_base64(enc, medium_model, clothing_model, recycling_models)

"""
