# Grocery-Expiry-Tracker
Automating grocery management with AI-powered expiry tracking

![Badges](https://img.shields.io/badge/TensorFlow-2.x-orange)
![Badges](https://img.shields.io/badge/Python-3.x-blue)
![Badges](https://img.shields.io/badge/Code%20Size-406%20lines-yellow)

## 📌 Overview
The Grocery-Expiry-Tracker is a TensorFlow-based project designed to track the expiry dates of groceries using image recognition. The real-world purpose of this project is to help reduce food waste by alerting users when their groceries are near expiry. The methodology involves training a deep learning model to recognize expiry dates on product packaging. The key outcome is a system that can accurately predict the expiry dates of various grocery products. This project utilizes a dataset of images of product packaging to train the model. The Grocery-Expiry-Tracker has the potential to be integrated into smart refrigerators or mobile apps to provide users with a convenient and automated way to manage their groceries.

## ✨ Features
* Utilizes TensorFlow for building and training the expiry date recognition model
* Employs a convolutional neural network (CNN) architecture for image recognition
* Achieves high accuracy in recognizing expiry dates on product packaging
* Supports recognition of various types of product packaging, including cans, bottles, and cartons
* Uses transfer learning to leverage pre-trained models and improve training efficiency
* Includes data preprocessing techniques, such as image resizing and normalization, to improve model performance
* Supports batch processing of images to enable efficient tracking of multiple products
* Provides a user-friendly interface for uploading images and retrieving expiry date predictions
* Includes a database to store product information and expiry dates for easy tracking

## 🛠️ Tech Stack
| Library | Version | Purpose |
| --- | --- | --- |
| TensorFlow | 2.x | Building and training the expiry date recognition model |
| Python | 3.x | Developing the project and integrating with TensorFlow |
| OpenCV | - | Image processing and computer vision tasks |

## 📁 Project Structure
```markdown
Grocery-Expiry-Tracker/
├── temp_images/
│   ├── image1.jpg
│   ├── image2.jpg
│   └── ...
├── templates/
│   ├── index.html
│   ├── style.css
│   └── ...
├── src/
│   ├── model.py
│   ├── data.py
│   ├── utils.py
│   └── ...
├── requirements.txt
├── README.md
└── ...
```

## ⚙️ Installation
1. Clone the repository using `git clone https://github.com/username/Grocery-Expiry-Tracker.git`
2. Navigate to the project directory using `cd Grocery-Expiry-Tracker`
3. Install the required dependencies using `pip install -r requirements.txt`
4. Download the required dataset and place it in the `temp_images` folder

## 🚀 Usage
To use the Grocery-Expiry-Tracker, simply run the `python src/model.py` command and follow the prompts to upload an image of the product packaging. The model will then predict the expiry date and display it on the screen.

## 📊 Dataset
The dataset used for this project consists of images of product packaging with expiry dates. The dataset is not publicly available and must be collected manually. To use the project, place the dataset in the `temp_images` folder.

## 📈 Results
The Grocery-Expiry-Tracker achieves high accuracy in recognizing expiry dates on product packaging. The model is evaluated using metrics such as precision, recall, and F1-score. A confusion matrix is also used to evaluate the model's performance. The expected output is the predicted expiry date, which is displayed on the screen.

## 🤝 Contributing
To contribute to the Grocery-Expiry-Tracker, fork the repository and submit a pull request with your changes. Please ensure that your code is well-documented and follows the existing coding style.

## 📄 License
The Grocery-Expiry-Tracker is licensed under the MIT License.