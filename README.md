<!-- GETTING STARTED -->
## Getting Started

This project contains scripts and a guiding structure for running torchserve inference using multiple models and outputting whether there is consensus across models on the top class prediction on a single image input.

### Prerequisites

* Python 3.8

    Recommended to try Pyenv
    Link below has more guidance
    https://medium.com/macoclock/how-to-install-and-manage-multiple-python-versions-on-macos-ca01a5e398d4

* Java
  ```sh
  https://download.oracle.com/java/19/latest/jdk-19_macos-aarch64_bin.dmg
  ```

* Miniconda for Mac Apple M1
  https://docs.conda.io/en/latest/miniconda.html


### Installation

These installation instructions are specifically for an M1 Mac using conda for further installation guides see torchserve repo

1) Create and activate a conda enviroment
    ```sh   
    conda create -n torchserver python==3.8
    conda activate torchserver
    ```
2) Clone this project repo
    ```sh
   git clone https://github.com/abpfern/custom_serve.git
   ```
3) Install requirements
    ```sh
    pip install -r requirements.txt
    ```
4) In this project(custom_serve) create a model_store for your model files
    ```sh
    mkdir model_store
    ```
5) In root of this project(custom_serve) clone the torchserve repo
    ```sh
    git clone https://github.com/pytorch/serve.git
    ```

6) Install torchserve dependencies
    ```sh
    cd serve
    python3 ./ts_scripts/install_dependencies.py
    ```
7) Install model archiver tool to create model files for inference
    ```sh
    cd model-archiver
    pip install .
    ```

8) Create a model definitions folder in the serve repo
    ```sh
    mkdir model_defs
    ```
9) Move relevant model files to model_defs folder.

   The model_defs folder will contain: 
   
    a) model training file (model-file, .py file)
    
    b) the weights (serialized-file, .pth file)
    
    c) the mapping of indexes to classes(extra-files, .json)
    
    d) the handler file (runs inference pipeline including pre-processing tranformation steps, .py). 

    Example command for pulling pretrained weights from pytorch
    
    ```sh
    curl -O https://download.pytorch.org/models/densenet161-8d451a50.pth
    ```

    See custom_image_classifer.py in the root of this project as an example custom handler which has added transformations for padding and color jitter.

10) Create a .mar file for your custom model
    ```sh
    torch-model-archiver --model-name densenet161_custom \           
    --version 1.0 \            
    --model-file serve/model_defs/densenet161/model.py \
     --serialized-file serve/model_defs/densenet161-8d451a50.pth \
     --export-path model_store \
     --extra-files serve/model_defs/index_to_name.json \
     --handler serve/model_defs/custom_image_classifier.py

    ```
11) Rerun step 9 and 10 and add files from a different model to model_defs and  arguments to match new model files in model_defs. Example commands 
    ```sh
    curl -O https://download.pytorch.org/models/resnet18-f37072fd.pth
    ```
    ```sh
    torch-model-archiver --model-name resnet18-f37072fd_custom \           
    --version 1.0 \            
    --model-file serve/model_defs/resnet18/model.py \
     --serialized-file serve/model_defs/resnet18-f37072fd.pth \
     --export-path model_store \
     --extra-files serve/model_defs/index_to_name.json \
     --handler serve/model_defs/custom_image_classifier.py

    ```
12) Pull example image if required for running inference as input else ensure image location is known.
```sh
    cp ./serve/docs/images/kitten_small.jpg . 
```
13) Start the torchserve server
```sh
    torchserve --start --ncs --model-store model_store --models densenet161_custom.mar
```

14) In a separate terminal in root of project (custom-serve) run inference script with arguments for models used for inference and comparison and image input.
```sh
    python3 serve/inference_executor.py -m "densenet161_custom" "resnet18-f37072fd_custom" -i “kitten_small.jpg”
```

Results and metrics from running this inference in result_files folder

In terminal True or False is reported as to whether the models had the same top prediction for the image. 

A unique id for the inference request is also reported in terminal when running this script.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

This project can be used to compare model predictions on a single image and also test inference latencies.

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Project Link: [https://github.com/abpfern/custom_serve](https://github.com/abpfern/custom_serve)


<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/abpfern/custom_serve.svg?style=for-the-badge
[contributors-url]: https://github.com/abpfern/custom_serve/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/abpfern/custom_serve.svg?style=for-the-badge
[forks-url]: https://github.com/abpfern/custom_serve/network/members
[stars-shield]: https://img.shields.io/github/stars/abpfern/custom_serve.svg?style=for-the-badge
[stars-url]: https://github.com/abpfern/custom_serve/stargazers
[issues-shield]: https://img.shields.io/github/issues/abpfern/custom_serve.svg?style=for-the-badge
[issues-url]: https://github.com/abpfern/custom_serve/issues
[license-shield]: https://img.shields.io/github/license/abpfern/custom_serve.svg?style=for-the-badge
[license-url]: https://github.com/abpfern/custom_serve/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/nushfernando
