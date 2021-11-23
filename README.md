<div id="top"></div>

<!--
*** This is the readme docurment for the project, Manage Your Security Evaluations.
-->


<!-- PROJECT SHIELDS -->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]


<!-- ABOUT THE PROJECT -->
## About The Project
**Manage Your Security Evaluations** is one of 2021/22 engineering projects of the Department of System and Computer Engineering.<br />
This project aims to develop a platform that developers can use to store and manage the security evidence 
generated during the entire system development lifecycle for future security assessments.

### Team Members
This project is supervised and directed by [**Dr. Jason Jaskolka**](https://carleton.ca/jaskolka/), Ph.D., P.Eng, the director of CyberSEA Research Lab.<br />
Team Members includes:<br />
**&emsp;&emsp;<a href="https://www.linkedin.com/in/zijun-hu/">Zijun Hu</a><br />
&emsp;&emsp;<a href="https://www.linkedin.com/in/tiantian-lin-0595291a2/?originalSubdomain=ca">Tiantian Lin</a><br />
&emsp;&emsp;<a href="https://www.linkedin.com/in/jiawei-ma-19841715b/">Jiawei Ma</a><br />
&emsp;&emsp;<a href="https://www.linkedin.com/in/ruixuan-ni-a4bb5b19b/">Ruixuan Ni</a><br />**

### Build With
* [**Python**](https://www.python.org/)
* [**Flask**](https://flask.palletsprojects.com/en/2.0.x/)

<p align="right">(<a href="#top">back to top</a>)</p>


## Getting Started
This is an example of how to run the project.

### Prerequest:
* [**Python**](https://www.python.org/): Recommend using the latest version of Python.
* [**Flask**](https://flask.palletsprojects.com/en/2.0.x/): Use the following command to install Flask.<br />
		&emsp;&emsp;```sh $ pip install Flask ```<br />
* [**Git**](https://git-scm.com/): Required when clone the project. Recommend using the latest version.

### Run the project
Below is an example of how to run the project.

1. Clone the project to your local environment.
	```sh
	git clone https://github.com/Security-Evaluations-Management/ManageYourSecurityEvaluations.git
	```
2. Change to project directory
	```sh
	cd ./ManageYourSecurityEvaluations
	```
3. Exporting the FLASK_APP environment variable depends on the OS you're using.<br />
	**Bash**
	```sh 
	$ export FLASK_APP=__init__.py
	```

	**CMD**
	```sh 
	> set FLASK_APP=__init__.py
	```

	**Powershell**
	```sh 
	> $env:FLASK_APP = "__init__.py"
	```
4. Run Flask
	```sh
	flask run
	```
	**Note:** Flask default runs on Host: 127.0.0.1, Port:5000. <br />
	To change the Host and port, replace the **Step 4** command with
	```sh
	flask run --host=x.x.x.x --port=xxxx
	```

<p align="right">(<a href="#top">back to top</a>)</p>


## Usage
This project can be used can use to store and manage the security evidence 
generated during the entire system development lifecycle for future security assessments.

For more example, please refer to the [Documentation Section](https://github.com/Security-Evaluations-Management/myse-documentation)

<p align="right">(<a href="#top">back to top</a>)</p>


## Roadmap


## Contributing
To make contributions to our project, please follow the steps:
1. Fork the Project
2. Create your Feature Branch 
	```sh
	git checkout -b feature/AmazingFeature`)
	```
3. Commit your Changes 
	```sh
	git commit -m 'Add some AmazingFeature'
	```
4. Push to the Branch 
	```sh
	git push origin feature/AmazingFeature
	```
5. Open a Pull Request

<p align="right">(<a href="#top">back to top</a>)</p>


## License



## Contact



## Acknowledgments



<!-- MARKDOWN LINKS & IMAGES -->
<!-- ref: https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/Security-Evaluations-Management/ManageYourSecurityEvaluations
[contributors-url]: https://github.com/Security-Evaluations-Management/ManageYourSecurityEvaluations/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/Security-Evaluations-Management/ManageYourSecurityEvaluations
[forks-url]: https://github.com/Security-Evaluations-Management/ManageYourSecurityEvaluations/network/members
[stars-shield]: https://img.shields.io/github/stars/Security-Evaluations-Management/ManageYourSecurityEvaluations
[stars-url]: https://github.com/Security-Evaluations-Management/ManageYourSecurityEvaluations/stargazers
[issues-shield]: https://img.shields.io/github/issues/Security-Evaluations-Management/ManageYourSecurityEvaluations
[issues-url]: https://github.com/Security-Evaluations-Management/ManageYourSecurityEvaluations/issues
