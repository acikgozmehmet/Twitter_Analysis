# Twitter Data Analysis 

## Table of contents
* [General info](#general-info)
* [Technologies](#technologies)
* [Setup](#setup)

## General info
In this project, an application performing and visualizing some sophisticated
analytic queries on twitter data is designed, developed and deployed.

Please feel free to check out **Twitter_Analysis_Poster.pdf** for more details about the project

The project contains 3 main parts.
* Data Collection / Data Storage:

  Twitter data is collected with the "tweepy_streamer.py" program in data_conllection folder. 
  Please note that 
  1. You need to store your own Twitter credentials in "twitter_credentials.py" in the same folder.
  2. After storing the twitter data in the file (ie: file_YYYYMMDDHHMMSS.txt), you will need to rename "twitter_data.json" 
     and move it to "data" folder with the following command:
     
     ```
     $ mv file_YYYYMMDDHHMMSS.txt ../data/twitter_data.json
     ```
        
 
   Twitter data is stored in the "data" folder with the name "twitter_data.json".
   This is a **data-driven application.** When you run the application within the container, 
   please make sure to put the input data in "data" folder where you invoke the container.
   
* Running the program:

  The main code for the analysis can be found in **"twitter_analysis.py"**
  
  When the program is ran within the Docker container. it generates 2 output folders, "outs" and "plots" respectively. 
  A figure for each query is stored in the "plots" folder while the result of each query is stored in another folder in "outs" folder.
  You can still access the files with the folders or you can use the extra visualization provided within the "www" folder.
  
  Please check out the set-up part for details about installing and running the program.
    

* Presenting the results on the webpage:

  Please note that the web pages can be accessed by the index.html in "www' folder.
  The webpages are designed on **Responsive Design** and all pages have liquid layout.


## Technologies
Project is created with:
* Python 
* PySpark
* Hadoop
* Numpy
* Pandas
* Matplotlib
* Docker
* HTML5 & CSS
	
## Setup/Availability
To install it locally using git:

```
$ git clone https://github.com/acikgozmehmet/Twitter_Analysis.git
```


To build the Docker image:

```
$ docker build -t twitter_analysis .

```

To create and run the container

```
$ docker run --rm -p 8888:8888 -v $(pwd):/app --name my_twitter_analysis twitter_analysis
```


