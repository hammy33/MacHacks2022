# MammoHelp: MacHacks2022 Submission

## Installation Requirements
Navigate to the main directory and create/activate a virtual environment: <code>sourve /path_to_venv/Scripts/activate</code>
Ensure that the necessary libraries are installed: <code>pip install flask, torch, torchvision</code>.
Navigate to the Flask directory and run the application: <code>flask run</code>.

## Inspiration

2.3 million women were diagnosed with breast cancer in 2020 globally. It is vital that patients who receive a mammogram test are provided with accurate and fast results, however, the current nature of medicine provides patients with far too much uncertainty due to long wait times for scan analysis and booking appointments. 

## What it does

A doctor is provided with their own user credentials to create and store patient records. Four scans at different views (Left/Right + Caudal-Cranial/Mediolateral Oblique) are to be uploaded to the website. Within a matter of seconds, the backend machine learning code will provide the doctor with a diagnosis of what BI-RAD number the scans are most likely to be representative of. From here, the doctor is provided with the next steps including suggestions and future follow-up details.

## How we built it

PyTorch was used to build the machine learning software that makes up the backend of the software. Flask was used to host the website alongside an SQLAlchemy Database to store user credentials and patient scans. HTML, CSS and Javascript were used to build and style the front end of the website.

## Machine Learning Backend
Using the BI-RAD classification for breast cancer screening, a quantitivate way of analyzing CT scans immediately was determined using pytorch's neural network and machine learning capabilities. The following open-source project (https://github.com/nyukat/BIRADS_classifier) allows users to obtain such BI-RAD predictions by applying the pretrained CNN model on standard screening mammogram exam with four views. 

## Challenges we ran into

The parsed arguments that were required for the function to calculate the bi-rad values proved to be very difficult to sync together. Additionally, creating an effective database of the patient records and information that the doctor is able to view at a time proved to be challenging as a result of the time constraint.

## Accomplishments that we're proud of

Having built an entire website with a functional backend supported by Machine Learning in a small period of time is a significant accomplishment, especially for our first time working directly with AI!

## What we learned

We got extensive experience working with machine learning technologies, and became increasingly comfortable with data processing and neural networks. Additionally, we learnt the importance of software quality and the delegation of tasks in order to meet the deadline for this project.

## What's next for MammoHelp

The future holds increased accuracy for the technology through efficient precision measures. The website can also be grown to accept abdomen and head scans in the future in order to be accessible for a wider range of patients.
