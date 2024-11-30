"""
Author: Madhurima Rawat

This script is used to launch the CSVTU GPT app locally on Streamlit for interactive queries. 
The app facilitates finding relevant answers from CSV-based data sets, designed for academic subject information and other related content. 
It provides fuzzy matching, exact word matching, and syllabus search capabilities. 
The app can help users access subject-specific answers and resources efficiently.

Libraries used:
- Streamlit: To create the web-based application and handle user interface interactions.
- Pandas: For data reading, manipulation, and analysis.
- fuzzywuzzy: For matching user input with questions in data frames.
- OS: To navigate the file system and manage paths.

Functions overview:
- display_background_image: Sets the background image with opacity for a customized UI.
- load_data_from_directory: Loads CSV files containing data except for a specified university file.
- find_common_word_matches: Finds exact and partial matches between user input and question data.
- get_best_matches: Uses fuzzy matching to retrieve the most relevant questions and answers.
- check_for_syllabus: Identifies relevant syllabus files based on user input.
- display_response: Displays matched responses or relevant syllabus files based on user input.

The app offers an interactive experience for querying data related to various semesters and subjects.
"""

# Importing Required libraries
import pandas as pd
from fuzzywuzzy import process
import streamlit as st
import os

# Setting the page title
# This title will only be visible when running the app locally.
# In the deployed app, the title will be displayed as "Title - Streamlit," where "Title" is the one we provide.
# If we don't set the title, it will default to "Streamlit"
st.set_page_config(page_title="CSVTU GPT")

# Dictionary mapping Semesters to their corresponding full subject names
Semester_subject_names = {
    "Semester_1": [
        "Engineering Mathematics I",
        "Environmental Science",
        "Foundations of Electronics Engineering",
        "Fundamentals of Computational Biology",
        "Language and Writing Skills",
        "Learning Programming Concepts With C",
        "Professional Ethics and Life Skills",
    ],
    "Semester_2": [
        "Data Structure Using C",
        "Digital Logic and Design",
        "Engineering Mathematics II",
        "Entrepreneurship",
        "Object-Oriented Programming",
        "Python for Data Science",
    ],
    "Semester_3": [
        "Analysis and Design of Algorithm",
        "Computer Organization and Architecture",
        "Database Management System",
        "Discrete Structure",
        "Independent Project",
        "Probability and Statistics",
    ],
    "Semester_4": [
        "Artificial Intelligence Principles and Applications",
        "Computer Network",
        "Data Visualization",
        "Operating System",
        "R for Data Science",
        "Theory of Computation",
    ],
    "Semester_5": [
        "Computational Complexity",
        "Cryptography and Network Security",
        "Intelligent Data Analysis",
        "Natural Language Processing",
        "Pattern Recognition and Machine Learning",
        "Vocational Training",
    ],
    "Semester_7": [
        "Software Engineering",
        "Big Data Analytics",
        "Image Processing",
        "Data Wrangling",
    ],
}


# Function to include background image and opacity
def display_background_image(url, opacity):
    """
    Displays a background image with a specified opacity on the web app using CSS.

    Args:
    - url (str): URL of the background image.
    - opacity (float): Opacity level of the background image.
    """
    st.markdown(
        f"""
        <style>
            body {{
                background: url('{url}') no-repeat center center fixed;
                background-size: cover;
                opacity: {opacity};
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )


# Function to load data from CSV files in the specified directory
@st.cache_data  # Cache data to optimize loading
def load_data_from_directory(directory_path):
    """
    Loads data from all CSV files in the specified directory except the university file.

    Args:
    - directory_path (str): Path to the directory containing CSV files.

    Returns:
    - dataframes (dict): Dictionary of dataframes with file names as keys.
    - university_file (str): Name of the university-specific data file.
    """
    dataframes = {}
    university_file = "University_Website_Data_Question_Answer.csv"

    for file_name in os.listdir(directory_path):
        if file_name.endswith(".csv") and file_name != university_file:
            file_path = os.path.join(directory_path, file_name)
            try:
                df = pd.read_csv(file_path)
                dataframes[file_name] = df
            except Exception as e:
                st.write(f"Failed to read {file_name}: {e}")

    return dataframes, university_file


# Function to find common word matches
def find_common_word_matches(user_input, data):
    """
    Finds matches where user input has common words with questions or answers in the data.

    Args:
    - user_input (str): The user query.
    - data (dict): Dictionary of dataframes with questions and answers.

    Returns:
    - matches (list): List of tuples containing file name, question, score, and answer.
    """
    matches = []
    user_words = set(user_input.lower().split())

    for file_name, df in data.items():
        if {"Question", "Answer"}.issubset(df.columns):
            for _, row in df.iterrows():
                question_words = (
                    set(row["Question"].lower().split())
                    if pd.notna(row["Question"])
                    else set()
                )
                answer_words = (
                    set(row["Answer"].lower().split())
                    if pd.notna(row["Answer"])
                    else set()
                )

                if user_words.issubset(question_words | answer_words):
                    matches.append((file_name, row["Question"], 100, row["Answer"]))
                else:
                    common_words = user_words & (question_words | answer_words)
                    if common_words:
                        matches.append((file_name, row["Question"], 70, row["Answer"]))

    return matches


# Function to get best fuzzy matches
def get_best_matches(user_input, data, top_n=3):
    """
    Finds the best fuzzy matches for the user input.

    Args:
    - user_input (str): The user query.
    - data (dict): Dictionary of dataframes with questions and answers.
    - top_n (int): Number of top matches to return.

    Returns:
    - matches (list): List of tuples containing file name, question, score, and answer.
    """
    matches = []

    for file_name, df in data.items():
        if {"Question", "Answer"}.issubset(df.columns):
            df["Question"] = df["Question"].astype(str)
            df["Answer"] = df["Answer"].astype(str)
            for question in df["Question"]:
                score = process.extractOne(user_input, [question])[1]
                matches.append(
                    (
                        file_name,
                        question,
                        score,
                        df[df["Question"] == question]["Answer"].values[0],
                    )
                )

    matches = sorted(matches, key=lambda x: x[2], reverse=True)
    return matches[:top_n]


# Function to check for relevant syllabus based on user input
def check_for_syllabus(user_input):
    """
    Checks if the user input mentions any semester subjects and returns the relevant syllabus file(s).

    Args:
    - user_input (str): The user query.

    Returns:
    - syllabus_files (list): List of filenames for the relevant syllabus files.
    """
    syllabus_files = []
    user_words = set(user_input.lower().split())

    for semester, subjects in Semester_subject_names.items():
        if user_words.intersection(subjects):
            syllabus_files.append(
                f"Preprocessed_{semester}_Syllabus_Question_Answer.csv"
            )

    # If the word 'syllabus' appears by itself, return files for the first semester or all semesters
    if "syllabus" in user_words:
        if len(syllabus_files) == 1:
            syllabus_files = [syllabus_files[0]]
        else:
            syllabus_files = [
                f"Preprocessed_Semester_{i}_Syllabus_Question_Answer.csv"
                for i in range(1, 8)
                if f"Preprocessed_Semester_{i}_Syllabus_Question_Answer.csv"
                in syllabus_files
            ]

    return syllabus_files


# Function to display the response based on user input and data
def display_response(user_input, data, university_file_path):
    """
    Displays relevant responses based on user input and data, including syllabus files if needed.

    Args:
    - user_input (str): The user query.
    - data (dict): Dictionary of dataframes with questions and answers.
    - university_file_path (str): Path to the university-specific data file.
    """
    syllabus_files = check_for_syllabus(user_input)

    if syllabus_files:
        st.write("### Relevant Syllabus Files")
        for syllabus_file in syllabus_files:
            st.write(f"- {syllabus_file}")
        return

    if user_input:
        filtered_data = {k: v for k, v in data.items() if k != university_file_path}

        # Try finding exact/common word matches
        common_word_matches = find_common_word_matches(user_input, filtered_data)
        if common_word_matches:
            matches = common_word_matches[:3]
            st.write("### Exact Matches")
            for _, question, _, answer in matches:
                st.success(f"**Question:** {question}\n\n**Answer:** {answer}")
            return

        # If no exact matches, fallback to fuzzy matching
        st.write("### Fuzzy Matches")
        matches = get_best_matches(user_input, filtered_data)

        if matches:
            for _, question, score, answer in matches:
                if score >= 90:
                    st.success(f"**Question:** {question}\n\n**Answer:** {answer}")
                elif score >= 80:
                    st.warning(f"**Question:** {question}\n\n**Answer:** {answer}")
                elif score >= 70:
                    st.error(f"**Question:** {question}\n\n**Answer:** {answer}")
                else:
                    st.info(f"**Question:** {question}\n\n**Answer:** {answer}")
            return

        # If no matches found, search in the university file
        university_data = pd.read_csv(university_file_path)
        if {"Question", "Answer"}.issubset(university_data.columns):
            university_data["Question"] = university_data["Question"].astype(str)
            university_data["Answer"] = university_data["Answer"].astype(str)
            matches = get_best_matches(user_input, {"University": university_data})

            if matches:
                for _, question, score, answer in matches:
                    if score >= 90:
                        st.success(f"**Question:** {question}\n\n**Answer:** {answer}")
                    elif score >= 80:
                        st.warning(f"**Question:** {question}\n\n**Answer:** {answer}")
                    elif score >= 70:
                        st.error(f"**Question:** {question}\n\n**Answer:** {answer}")
                    else:
                        st.info(f"**Question:** {question}\n\n**Answer:** {answer}")
            else:
                st.warning("Sorry, no relevant answers found.")


# Main code to initialize Streamlit
if __name__ == "__main__":
    # Display background
    display_background_image(
        "https://th.bing.com/th/id/OIP.gEB384k5m-GvLbulHyIzMwHaEO?w=1344&h=768&rs=1&pid=ImgDetMain",
        0.8,
    )

    # Display a brief "About Me" section with links to your profile and portfolio with icons
    st.sidebar.markdown(
        """
        <p style="text-align: center;">
        <h3> About Me</h3>
        Hello! I'm <strong>Madhurima Rawat</strong>, a developer passionate about creating impactful applications. 
        Feel free to check out my GitHub and portfolio for more insights into my work.
        This is a simple chatbot that I have trained on a question-answer dataset sourced from the scraped data 
        of my university, CSVTU's website. I first scraped the data and then converted it into a question-answer 
        format. Additionally, the syllabus for the B.Tech (Hons) Data Science program for the semester is included.
        </p>
        """,
        unsafe_allow_html=True,
    )

    # Using Font Awesome icons for links
    st.sidebar.markdown(
        """
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
        <a href="https://github.com/madhurimarawat" target="_blank"><i class="fab fa-github"> &nbsp;</i> GitHub</a> &nbsp;
        <a href="https://madhurimarawat.github.io/Portfolio-Website/" target="_blank"><i class="fas fa-globe"></i> &nbsp; Portfolio</a>&nbsp;
        <a href="https://www.linkedin.com/in/madhurima-rawat/" target="_blank"><i class="fab fa-linkedin"></i> &nbsp; LinkedIn</a>
        """,
        unsafe_allow_html=True,
    )

    # Upload and display data from CSV files
    # Load the data
    data_directory = "Dataset/Preprocessed_Dataset"
    data, university_file = load_data_from_directory(data_directory)

    # User input section
    st.title("Welcome to CSVTU GPT")
    user_input = st.text_input("Ask your question here:")
    if user_input:
        display_response(
            user_input, data, os.path.join(data_directory, university_file)
        )
