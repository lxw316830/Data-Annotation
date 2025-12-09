from ultralytics import YOLO
import os

# Load a model
model = YOLO("/root/autodl-tmp/best.pt")  # pretrained YOLO11n model
os.makedirs('./output_val', exist_ok=True)
for img in os.listdir('./yolo_data/images/val'):
    img_path = f"./yolo_data/images/val/{img}"
    results = model([img_path])  # return a list of Results objects

    # Process results list
    for result in results:
        boxes = result.boxes  # Boxes object for bounding box outputs
        masks = result.masks  # Masks object for segmentation masks outputs
        keypoints = result.keypoints  # Keypoints object for pose outputs
        probs = result.probs  # Probs object for classification outputs
        obb = result.obb  # Oriented boxes object for OBB outputs
        # result.show()  # display to screen
        result.save(filename=f"./output_val/{img}")  # save to disk