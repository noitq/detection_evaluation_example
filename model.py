import os
import torch
import torchvision
import torchvision.transforms as T
from PIL import Image
from dataset import COCO_NAMES

class MyModel():
    def __init__(self, device='cpu'):
        """Init model using torchvision models

        Args:
            device (str, optional): device to load. Defaults to 'cpu'.
        """
        self.device = device
        self.model = torchvision.models.detection.fasterrcnn_resnet50_fpn(pretrained=True)
        self.model.to(self.device)
        self.transform = T.Compose([T.ToTensor()])
        
    def detect(self, img_path, threshold=0.8):
        """Detect an image

        Args:
            img_path (str): path to image
            threshold (float, optional): confidence threshold. Defaults to 0.8.

        Returns:
            boxes, class: detection result
        """
        
        img = Image.open(img_path)
        img = self.transform(img)
        img = img.to(self.device)
        
        self.model.eval()
        pred = self.model([img])
        
        pred_class = [COCO_NAMES[i] for i in list(pred[0]['labels'].cpu().numpy())]
        pred_boxes = [[(i[0], i[1]), (i[2], i[3])] for i in list(pred[0]['boxes'].detach().cpu().numpy())]
        pred_score = list(pred[0]['scores'].detach().cpu().numpy())
        pred_t = [pred_score.index(x) for x in pred_score if x > threshold][-1]
        pred_boxes = pred_boxes[:pred_t + 1]
        pred_class = pred_class[:pred_t + 1]
        
        return pred_boxes, pred_class
    
    def predict(self, images):
        """predict a batch

        Args:
            images (tensor): batch images

        Returns:
            list[dict[tensor]]: prediction results 
            refer to torchvision.models.detection -> faster r-cnn output
        """
        
        self.model.eval()
        pred = self.model(images)
        
        return pred
