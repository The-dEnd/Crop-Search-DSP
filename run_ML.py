import warnings
#since ML models tend to evolve very quickly, it is expected to have a large number of deprecation/future warnings, that will pollute shell interface; ence we clear them ahead of time
warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.simplefilter(action='ignore', category=UserWarning) 
import torch, joblib, sklearn, os, sys, pathlib, csv, cv2
from torchvision import models, transforms, ops
import numpy as np
from PIL import Image
from translator import tr, current_language

sys.path.append("models/yolov5/")
sys.path.append("models/")
from utils.general import non_max_suppression
import picCropper

with open("resources/data/confidence_threshold_ML.conf", "r") as f: #retrieve confidence threshold
    firstLine = True
    for line in f:
        if firstLine:
            line = line.strip()
            try:
                confidenceThres = float(line.split("#")[0].strip().replace('"',''))
            except:
                raise ValueError("resources/data/confidence_threshold_ML.conf could not be read properly; the confidence threshold for the ML could not be identified")
                sys.exit
            firstLine=False




def predict(path_to_pictures, callback=None):
    temp = pathlib.PosixPath

    YOLO_DIR = "models/yolov5/"
    weights_path = 'models/best.pt'
    global confidenceThres

    DEVICE = 'cpu' #we use CPU, in case there is no GPU available (e.g. on a laptop)

    # Load YOLOv5 model directly from weights with torch.load (no torch.hub), because torch.hub tries to connect to the Internet
    if os.name == 'nt':
        pathlib.PosixPath = pathlib.WindowsPath
    yolo_model = torch.load(weights_path, map_location=DEVICE, weights_only=False)['model'].float().fuse().eval()
    yolo_model.conf = confidenceThres  # set confidence threshold
    pathlib.PosixPath = temp

    # Load ResNet classifier + LabelEncoder
    LE = joblib.load('models/label_encoder.pkl')
    NUM_CLASSES = len(LE.classes_)

    resnet = models.resnet34(weights=None)
    resnet.fc = torch.nn.Linear(resnet.fc.in_features, NUM_CLASSES)
    resnet.load_state_dict(torch.load('models/best_resnet34_weights.pth', map_location=DEVICE))
    resnet = resnet.to(DEVICE).eval()

    resize_yolo = (512,512) #optimal size for each of the 2 algorithms
    resize_resnet = (224,224)
    
    yoloTransform = transforms.Compose([
        transforms.Resize(resize_yolo),
        transforms.ToTensor(),
    ])

    resnetTransform = transforms.Compose([
        transforms.Resize(resize_resnet),
        transforms.ToTensor(),
    ])

    rows = []

    ctPicProcessed = 0
    totalPics = len(path_to_pictures)
    for aPath in path_to_pictures:
        #YOLO DETECTION
    
    
        noDetection=True #boleean to see if there is a detection or not on the picture
        img = Image.open(aPath).convert("RGB")
        w,l=img.size
        if w!=l:
            cropArea = picCropper.cropToSquare(w,l)
            img = img.crop(cropArea)
        img_np = np.array(img)
        H, W, _ = img_np.shape
        img_tensor = yoloTransform(Image.fromarray(img_np)).unsqueeze(0).to(DEVICE)


        # Run inference on numpy image directly (yolo_model expects uint8 image)

        with torch.no_grad():
            results_tuple = yolo_model(img_tensor)
            results = results_tuple[0]

        pred = non_max_suppression(results, conf_thres=confidenceThres, iou_thres=0.45, agnostic=True)[0]

        detections = []
        if pred is not None and len(pred):
            for *xyxy, conf, cls_id in pred:
                x1, y1, x2, y2 = map(float, xyxy)
                scaleX =  W / resize_yolo[1]
                scaleY =  H / resize_yolo[0]
                x1 = x1 * scaleX
                x2 = x2 * scaleX
                y1 = y1 * scaleY
                y2 = y2 * scaleY
                cx = (x1 + x2) / 2 / W
                cy = (y1 + y2) / 2 / H
                bw = (x2 - x1) / W
                bh = (y2 - y1) / H
                detections.append([cx, cy, bw, bh, float(conf), int(cls_id)])

        detections = np.array(detections)


        #RESNET CLASSIFICATION

        for cx, cy, bw, bh, conf, cls_id in detections:
            noDetection = False
            cx, cy, bw, bh, conf = map(float, (cx, cy, bw, bh, conf))

            x1 = int((cx - bw / 2) * W)
            x2 = int((cx + bw / 2) * W)
            y1 = int((cy - bh / 2) * H)
            y2 = int((cy + bh / 2) * H)

            roi = img_np[max(y1, 0):max(y2, 0), max(x1, 0):max(x2, 0)]
            if roi.size == 0:
                continue

            tensor = resnetTransform(Image.fromarray(roi)).unsqueeze(0).to(DEVICE)
            with torch.no_grad():
                probs = torch.softmax(resnet(tensor), 1).squeeze(0)
                top5_prob, top5_idx = torch.topk(probs, k=5)

            top5_labels = LE.inverse_transform(top5_idx.cpu().numpy())
            top5_probs = top5_prob.cpu().numpy()

            line = ["", "", "", aPath]
            for lab, p in zip(top5_labels, top5_probs):
                if p < 0.001:
                    line += ["", "", ""]
                else:
                    line += [(str(lab) + "000")[0:4], pretty(str(lab)), round(float(p), 5)]

            
            line += [""] * 17

            # Add bounding box coordinatess (normalized)
            x1n, y1n, x2n, y2n = yolobbox2bbox(cx, cy, bw, bh)
            line += [int(W * x1n), int(H * y1n), int(W * x2n), int(H * y2n)]
            rows.append(line)
            
        if noDetection: #if nothing detected on apic, we display it anyway, in case of a false negative
            line = ["", "", "", aPath]
            line += [""] * 32
            line += [0,0,0,0]
            line[25] = tr("warnNoDetec")
            rows.append(line)
            
        ctPicProcessed += 1
        if callback:
            percentProgress = int(100 * ctPicProcessed / totalPics)
            callback(percentProgress)
    return rows


def yolobbox2bbox(x,y,w,h):
    x1, y1 = x-w/2, y-h/2
    x2, y2 = x+w/2, y+h/2
    return x1, y1, x2, y2

def pretty(npStr): #will clean a np.str, e.g. 1010 to a proper name, e.g. "wheel 10"
    if len(npStr)>1:
        main = tr("lMotifs")[int(npStr[0])]
        sub = int(npStr[1:])
        return(main+" "+str(sub))
    else:
        main = tr("lMotifs")[int(npStr[0])]
        return(main+" (?)")


def main(argv=None, callback=None):
    if argv is None:
        argv = sys.argv
    rows = predict(argv, callback)
    with open("output_ML.csv", "w", newline="") as outputML:
        outputMLWriter = csv.writer(outputML, delimiter=";")
        outputMLWriter.writerow("NumTesson;NumDecor;NumPhoto;NamePhoto;Choice1Id;Choice1Pretty;Proba1;Choice2Id;Choice2Pretty;Proba2;Choice3Id;Choice3Pretty;Proba3;Choice4Id;Choice4Pretty;Proba4;Choice5Id;Choice5Pretty;Proba5;Choice6Id;Choice6Pretty;Proba6;Choice7Id;Choice7Pretty;Proba7;Comment;Aux1;Aux2;Aux3;Aux4;Aux5;Aux6;Aux7;Aux8;Aux9;Aux10;xLeft;yBottom;xRight;yTop".split(";"))
        outputMLWriter.writerows(rows)

if __name__ == '__main__':
    main()
