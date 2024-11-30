# CSVTU-GPT

This repository hosts the **CSVTU GPT app**, a Streamlit-based interactive application designed to provide efficient access to subject-specific academic information and resources. It supports functionalities like fuzzy matching, exact word matching, and syllabus search capabilities, enabling users to query data conveniently.

<a href = "https://csvtu-gpt-question-answer.streamlit.app/"><img src = "https://github.com/user-attachments/assets/7c87746b-7b67-4acb-979f-f881d3843ea7" title ="Website Image 1" alt ="Website Image 1"></a>

<a href = "https://csvtu-gpt-question-answer.streamlit.app/"><img src = "https://github.com/user-attachments/assets/02377dd9-a5f4-4e2a-af2e-a53240e82a56" title ="Website Image 2" alt ="Website Image 2"></a>

---

## Features
- **Interactive Query Resolution**: Use fuzzy matching and exact word matching to find the most relevant academic answers from the dataset.
- **Syllabus Search**: Identify and access specific syllabus files quickly.
- **Customizable UI**: A polished and user-friendly interface with background images for better usability.

---

## Libraries Used
- **Streamlit**: For building the web application and handling user interface interactions.
- **Pandas**: To handle data reading, manipulation, and analysis.
- **fuzzywuzzy**: For matching user input with questions in the dataset.
- **OS**: To navigate the file system and manage file paths.

---

## App Links

Explore the web scraping functionalities at: [CSVTU GPT App](https://web-scrapper-functions-h6phqofpkjtaylwyn9uvzf.streamlit.app/)

Discover CSVTU-specific question-answering features here: [CSVTU GPT](https://csvtu-gpt-question-answer.streamlit.app/)

---

## Functions Overview

### `display_background_image`
Sets the background image with opacity to create a visually appealing and customized user interface.

### `load_data_from_directory`
Loads CSV files containing datasets, excluding a specified university file.

### `find_common_word_matches`
Finds exact and partial matches between user input and question data.

### `get_best_matches`
Uses fuzzy matching to retrieve the most relevant questions and their corresponding answers.

### `check_for_syllabus`
Identifies relevant syllabus files based on user input.

### `display_response`
Displays matched responses or relevant syllabus files in an interactive manner.

---

## Directory Structure
```
|-- Codes
|   |-- Dataset
|       |-- Website_Data
|       |-- Preprocessed_Dataset
|       |-- Syllabus_Data
|       |-- Syllabus_Data_PDF
|-- Resources
|-- LICENSE
|-- README.md
```
- **Codes**: Contains the code files for the application.
  - **Dataset**: Holds academic data and preprocessed files.
  - **Syllabus_Data**: Stores syllabus-related information and PDFs.
- **Resources**: Includes additional resources to aid development.
- **LICENSE**: License information for the repository.
- **README.md**: Documentation for the project.

---

## Thanks for Visiting 😄

- Drop a 🌟 if you find this repository useful.<br><br>
- If you have any doubts or suggestions, feel free to reach me.<br><br>
  📩 **How to reach me:** &nbsp; [![Linkedin Badge](https://img.shields.io/badge/-madhurima-blue?style=flat&logo=Linkedin&logoColor=white)](https://www.linkedin.com/in/madhurima-rawat/) &nbsp; &nbsp;
  <a href ="mailto:rawatmadhurima@gmail.com"><img src="https://github.com/madhurimarawat/Machine-Learning-Using-Python/assets/105432776/b6a0873a-e961-42c0-8fbf-ab65828c961a" height=35 width=30 title="Mail Illustration" alt="Mail Illustration📩" > </a><br><br>
- **Contribute and Discuss:** Feel free to open [issues 🐛](https://github.com/madhurimarawat/CSVTU-GPT/issues), submit [pull requests 🛠️](https://github.com/madhurimarawat/CSVTU-GPT/pulls), or start [discussions 💬](https://github.com/madhurimarawat/CSVTU-GPT/discussions) to help improve this repository!

Check out the project repository: [CSVTU GPT on GitHub](https://github.com/madhurimarawat/CSVTU-GPT)
