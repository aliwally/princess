# Princess Detection

This project explores deep-learning object detection for three animated princesses:
Aurora, Snow White, and Rapunzel. The models are trained to locate each character
and predict their class in an image.

## Dataset

Images were collected from Google image searches and the
[Kaggle Princess dataset](https://www.kaggle.com/datasets/sayehkargari/princess-dataset?resource=download).
They were manually reviewed to remove incorrect, duplicate, or overly unrelated
images. The remaining images vary in source, appearance, background, and quality.

Images were annotated with LabelImg using YOLO-format bounding boxes around each
princess's head and torso. The report describes a class-balanced split of
approximately 70% training, 15% validation, and 15% test:

| Class | Total | Train | Validation | Test |
|---|---:|---:|---:|---:|
| Aurora | 212 | 148 | 32 | 32 |
| Snow White | 223 | 156 | 33 | 34 |
| Rapunzel | 218 | 153 | 33 | 32 |
| **Total** | **653** | **457** | **98** | **98** |

The local `*_fin/selected/` folders contain curated images, but their contents
may differ from the 653-image split reported above. The notebook uses the YOLO
dataset configuration and annotations from the dataset repository linked
above; the local image folders alone are not a complete YOLO training set.

## Training

The notebook [Trainiing_princesses.ipynb](./Trainiing_princesses.ipynb) documents
the experiments:

1. A custom CNN for detection and classification, including experiments with
   loss functions and data augmentation.
2. Transfer-learning experiments.
3. Ultralytics YOLO26n, initialized with pretrained weights and trained for
   100 epochs at an input size of 64 × 64 pixels.

The notebook was run in Google Colab. Run its cells in order; the YOLO section
expects `princesses.yaml` and the annotated dataset cloned from
[`rabefanirakay/princess_guesser`](https://git.inpt.fr/rabefanirakay/princess_guesser).
It also uses Ultralytics and benefits from a GPU.

## Results

The project report compares the custom-model experiments with the final
Ultralytics detector:

| Experiment | Reported overall score |
|---|---:|
| Initial custom CNN | 26.0% |
| Custom CNN with the alternative loss setup | 35.8% |
| Custom CNN with data augmentation | 40.2% |
| Ultralytics YOLO26n | **72.4% mAP@0.50** |

For YOLO, the notebook uses mAP@0.50 as a proxy for the report's “overall
precision” figure. It is an object-detection metric, not classification
accuracy, and should not be compared directly with the custom models' reported
scores. On the held-out test split, the notebook also reports mAP@0.50:0.95 of
43.7%.

| Class | Precision | Recall | F1-score |
|---|---:|---:|---:|
| Aurora | 0.76 | 0.69 | 0.72 |
| Snow White | 0.74 | 0.66 | 0.69 |
| Rapunzel | 0.71 | 0.60 | 0.65 |

These results are a project baseline, not a guarantee of performance on new
images. The dataset is small, some images are similar, and bounding-box
annotations are not fully consistent. Low input resolution also makes small,
partially visible, or visually similar characters harder to detect.

## Project documents

- [Dataset and project report](./Projet_détection_objet_princesses.pdf)
- [Training and results report](./apprentissage_princesse_M.pdf)
