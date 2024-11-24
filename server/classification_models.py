from PIL import Image
import numpy as np
import io
import yolov5
import base64 

import keras

import torch

import cv2
from pathlib import Path
import pathlib

temp = pathlib.PosixPath
pathlib.PosixPath = pathlib.WindowsPath

import os
from pprint import pprint
from typing import Iterable
import tempfile

# import gradio as gr

from huggingface_hub import from_pretrained_fastai
from huggingface_hub import hf_hub_download, list_repo_files

from dotenv import load_dotenv

from ultralytics import YOLO

load_dotenv()

# Initialize models

# 1) Object Detection of Trash
model = yolov5.load('keremberke/yolov5m-garbage', device='cpu')

# set model parameters
model.conf = 0.53  # NMS confidence threshold
model.iou = 0.40  # NMS IoU threshold
model.agnostic = False  # NMS class-agnostic
model.multi_label = False
model.max_det = 15

# 2) RecycleNet - Further classification of recyclable materials
materials_model = from_pretrained_fastai("pyesonekyaw/recycletree_materials")
paper_model = from_pretrained_fastai("pyesonekyaw/recycletree_paper")
plastic_model = from_pretrained_fastai("pyesonekyaw/recycletree_plastic")
metal_model = from_pretrained_fastai("pyesonekyaw/recycletree_metal")
others_model = from_pretrained_fastai("pyesonekyaw/recycletree_others")
glass_model = from_pretrained_fastai("pyesonekyaw/recycletree_glass")

recycling_models = {"materials": materials_model, "paper": paper_model, "plastic": plastic_model, "metal": metal_model, "others": others_model, "glass": glass_model }

# 3) Object detection of clothing
hf_model_id = 'kesimeg/yolov8n-clothing-detection'
hf_token = os.getenv('HF_TOKEN')

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

def inference(file_path, model):
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
    # label = f'{model.names[int(category)]}: {score:.2f}'

    outputs.append({"label": model.names[int(category)], "confidence": float(score), "bbox": [x1, y1, x2, y2]})

  return outputs

def classify_for_recycling(file_name, recycling_models):
    """
    Performs inference for a given input image and returns the prediction and CAM image.
    """
    materials_model = recycling_models['materials']
    paper_model = recycling_models['paper']
    plastic_model = recycling_models['plastic']
    metal_model = recycling_models['metal']
    glass_model = recycling_models['glass']
    other_model = recycling_models['others']

    # Subclass names for recycling classifier and some pre-defined rules based on research and common knowledge
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

    with open(file_name, "rb") as image:
        image_data = image.read()
        image = Image.open(io.BytesIO(image_data)).convert("RGB")
        img_array = np.array(image)

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

def find_clothes(file_name, clothing_model):

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

  return outputs

# Helper functions
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

def flag_ewaste(file_name, models):
    """
    Processes an image file, divides it into 3x3 blocks, saves each block as a temporary file, 
    and performs classification on each block, as well as the whole image. 
    
    Then analyzes the list of 5 dictionaries with recycling classification results.

    Args:
        file_name (str): Path to the image file.
        models (dict): Dictionary containing material and specific classification models.
        visualize (bool): Whether to visualize the image and blocks.

    Returns:
        results (bool, float): Whether it contains e-waste, and what the confidence is. 
    """

    results = []
    material_preds, material_label, specific_preds, specific_label, recyclable_qn, recyclable_advice = classify_for_recycling(
                file_name, models)
    
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
                block_path, models)

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

def classify_and_update_annotations(file_name, annotations, recycling_models):
    """
    Processes an image based on bounding box annotations, performs classification, and updates annotations.

    Args:
        file_name (str): Path to the image file.
        annotations (list): List of bounding box annotations with format:
                            [{'label': str, 'confidence': float, 'bbox': [x_min, y_min, x_max, y_max]}]
        recycling_models (dict): Dictionary containing material and specific classification models.
        visualize (bool): Whether to visualize the bounding boxes and cropped regions.

    Returns:
        updated_annotations (list): List of updated annotations with recycling information.
    """
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

        # Classify the cropped image
        material_preds, material_label, specific_preds, specific_label, recyclable_qn, recyclable_advice = classify_for_recycling(
            cropped_path,
            recycling_models
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

def classify(file_name, main_model, clothing_model, recycling_models):
  
  main_annotations = inference(file_name, main_model)
  clothing_annotations = find_clothes(file_name, clothing_model)
  
  corrected_clothing_annotations = get_corrected_clothing_annotations(main_annotations, clothing_annotations)

  main_annotations = main_annotations + corrected_clothing_annotations

  main_annotations_with_recycling = classify_and_update_annotations(file_name, main_annotations, recycling_models)
  corrected_recycling_annotations = get_corrected_main_annotations(main_annotations_with_recycling, corrected_clothing_annotations)

  return corrected_recycling_annotations

def save_base64_to_temp_file(base64_string):
    """
    Decodes a base64 string and saves it as a temporary file.

    Args:
        base64_string (str): The base64 encoded image string.

    Returns:
        str: The file path of the saved temporary file.
    """
    # Decode the base64 string to binary data
    image_data = base64.b64decode(base64_string)

    # Create a temporary file to store the decoded image
    with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as temp_file:
        # Write the decoded image data to the temporary file
        temp_file.write(image_data)
        temp_file_path = temp_file.name  # Get the file path

    return temp_file_path

def classify_base64(encoding):
  file_name = save_base64_to_temp_file(encoding)
  return classify(file_name, model, clothing_model, recycling_models)

def flag_ewaste_base64(encoding):
  file_name = save_base64_to_temp_file(encoding)
  return flag_ewaste(file_name, recycling_models)

print(classify("sample_images/random.jpg", model, clothing_model, recycling_models))
print(flag_ewaste("sample_images/random.jpg", recycling_models))
