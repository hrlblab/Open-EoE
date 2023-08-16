# Open-EoE
The official implementation of Open-EoE
<img src='doc/overview.png' align="center" height="500px">

## Abstract
Eosinophilic Esophagitis (EoE) is a chronic, immune/antigen-mediated esophageal disease, characterized by symptoms related to esophageal dysfunction and histological evidence of eosinophil-dominant inflammation. Owing to the intricate microscopic representation of EoE in imaging, current methodologies which depend on manual identification are not only labor-intensive but also prone to inaccuracies. In this study, we develop an open-source toolkit, named Open-EoE, to perform end-to-end whole slide image (WSI) level eosinophil (Eos) detection using one line of command via Docker. Specifically, the toolkit supports three state-of-the-art deep learning-based object detection models. Furthermore, Open-EoE further optimizes the performance by implementing an ensemble learning strategy, and enhancing the precision and reliability of our results. The experimental results demonstrated that the Open-EoE toolkit can efficiently detect Eos on a testing set with 289 WSIs. At the widely accepted threshold of ≥ 15 Eos per high power field (HPF) for diagnosing EoE, the Open-EoE achieved an accuracy of 91%, showing decent consistency with pathologist evaluations. This suggests a promising avenue for integrating machine learning methodologies into the diagnostic process for EoE.

## Installation
Please refer to [INSTALL.md](doc/INSTALL.md) for installation instructions of the detection phase.

## Model
The trained model can be found [here](https://drive.google.com/drive/folders/1_rKfvtnVKZWWacE3peFIzr3EQx2JQyF-?usp=drive_link)
Please put the folder into the floder <mmdetection/work_dirs>. If there is no folder in folder <mmdetection> please create one.

## Get Started
you can put your all WSIs in a folder.
1. Get the patch images
   
   ~~~
   python scn2patch.py <path/to/your/WSIfolder>
   ~~~
   
2. get the bounding box
      
   if you want to use faster-rcnn as the model:
   
   ~~~
   python gt_bbox.py faster
   ~~~
   
   if you want to use mask-rcnn as the model:
   
   ~~~   
   python gt_bbox.py mask
   ~~~
   if you want to use centernet as the model:
   
   ~~~   
   python gt_bbox.py center   
   ~~~
   if you want to use all of these three models:
   
   ~~~ 
   python gt_bbox.py all
   ~~~
3. get the ensemble result

   ~~~
   python gt_ensemble.py <path/to/your/WSIfolder>
   ~~~
4. get the maximum Eos count in HPF

   ~~~
   python gt_max.py <model_name>      model_name: faster; mask; centernet; ensemble
   ~~~

### Quick start

#### Get our docker image

```
sudo docker pull 
```
#### Run Open-EoE
First you need to put a folder include your data named ```WSIs``` in the container
```
#run the docker
sudo docker run open-eoe 
```
