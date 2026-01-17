from ultralytics import YOLO
model = YOLO("ValBest_small.pt")
model.export(format="engine", imgsz=642, half=True, device=0,name="my_custom_engine" )

