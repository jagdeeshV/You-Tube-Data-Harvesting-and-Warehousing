<h1 align="center">
YouTube Data Harvesting and Warehousing
</h1>

### Project Objective
This project is to provide users with the ability to access, store and analyse data from any YouTube channels with their Channel Id. 

The primary objective of this project was to develop a Streamlit application that enables users to:

+	Access from multiple YouTube channels.
+	Store the data in a MySQL database for structured querying.
+	Analyze data by performing searches and execute queries on the stored data with predefined queries.

The project’s goal was to create a tool that could provide meaningful insights from YouTube data, such as identifying the top-performing videos, understanding viewer engagement, and analyzing content trends.

#### Data Harvesting and Warehousing

**Data Harvesting** refers to the process of extraction of data from various sources for analysis, research, or use. The data gathered from websites, social media platforms, and (literally) from any possible digital source using techniques like web scraping, APIs, and automated tools. While data harvesting provides insights for effective decision-making, it also raises concerns about privacy and security.

**Data warehousing** is the process of storing the collected data into a centralized repository, typically for analysis and reporting purposes. A data Warehouse is based on analytical processing.  Data Warehousing can be applied anywhere where we have a huge amount of data and we want to see statistical results that help in decision making. 

### Technologies used and Pre-requisites
1.	**Python:** The programming language used for building the application and scripting tasks.

    Visit the URL  [Download Python | Python.org](https://www.python.org/downloads/)    to download and install python in the PC

    **Install necessary Python packages / Libraries:** Install the necessary packages / libraries using pip or conda package manager. Required libraries include DateTime, Regex, Streamlit, Pandas, mysql-connector-python and google-api-python-client

2.	**Streamlit:** Streamlit is an open-source Python framework designed to create and share web applications. It is specifically built for Python, making it easy for data scientists and machine learning engineers to deploy their models and visualize data without needing extensive knowledge of web development
	
        A web-based user interface is developed using Streamlit where users can enter a YouTube channel ID to fetch and store channel details and to view results based on predefined queries.

3.	**YouTube API  key:** To search or integrate YouTube with external applications, one needs an authentication key called a YouTube API key.  This API ensures error-free, reliable data exchanges and let use YouTube outside of the Google app
	
     Visit the URL [YouTube Data API Overview  |  Google for Developers](https://developers.google.com/youtube/v3/getting-started) to get the key.
  	
     YouTube API was used to Connect to the YouTube and retrieve channel and video data from you tube.
  	
4.	**MySql DB:**  is an open-source relational database management system (RDBMS) that uses Structured Query Language (SQL) to manage and manipulate databases.

     Search web for MYSQL database installation and install the same in the PC.

     MySQL database is used to store the retrieved data for more structured querying.
  	
5.	**SQL queries:** (Structured Query Language) is a programming language designed for managing and manipulating relational databases. SQL queries are commands used to interact with databases to retrieve, insert, update, or delete data. They are essential for data management and analysis tasks
	
     SQL queries are used to analyse data and extract meaningful insights for the predefined options in this project.

### Executing the Application 

To run the YouTube Data Harvesting and Warehousing project, follow these steps:

1.	Install Python and required packages / libraries as given above
2.	Create your YouTube API and have it handy.
3.	Install MySQL and have its login credentials for storing the data.
4.	Download the Application Script Jag_You_Tube_proj.py from Git hub. 
5.	Launch the Application through Streamlit in the command-line interface.  
     **Streamlit run \<path>\Jag_You_Tube_proj.py**

### Features

The YouTube Data Harvesting and Warehousing application offers the following features:
+	Retrieval of channel, video and comments (first 100) data from YouTube using the YouTube API for the given channel id.
+	Storage of data confirmed by user to a MySQL database for efficient querying and analysis.
+	Search and retrieval of data from the SQL database using SQL queries for a ten different pre-defined search options.
+	Data analysis and visualization through charts and graphs using Streamlit's data visualization capabilities.

### Conclusion

This project was a deep dive into the world of data harvesting and warehousing using real-world YouTube data. By combining tools like Streamlit,  MySQL DB and SQL Queries, I was able to create a application that provides valuable insights into YouTube channels and videos. This project showcases the potential of using modern data tools to analyze and understand social media content.

### References

> •	Streamlit Documentation: [https://docs.streamlit.io/](https://docs.streamlit.io/)  
> •	YouTube API Documentation: [https://developers.google.com/youtube](https://developers.google.com/youtube)  
> •	Python Documentation: [https://docs.python.org/](https://docs.python.org/)

#### My Contact
📧 Email: jagdeeshv@hotmail.com  
🌐 LinkedIn: https://www.linkedin.com/in/jagadeesh-v-a09a681b7

For any further questions or inquiries, feel free to reach out. I am happy to assist you with any queries.

