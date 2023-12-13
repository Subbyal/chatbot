import streamlit as st
from serpapi import GoogleSearch
import random
import time

# Set page configuration
st.set_page_config(
    page_title="Job Searching Chatbot",
    page_icon=":briefcase:",
    layout="wide",
)
st.title("Job Searching Chatbot")
# Add custom styles
st.markdown(
    """
    <style>
        body {
            color: #333;
            background-color: #f4f4f4;
            font-family: 'Arial', sans-serif;
        }
        .chat-container {
            width: 80%;
            margin: auto;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            background-color: #fff;
        }
        .user-message {
            background-color: #e6f7ff;
            border-radius: 10px;
            padding: 10px;
            margin-bottom: 10px;
        }
        .assistant-message {
            background-color: #000000;
            color: white;
            border-radius: 10px;
            padding: 10px;
            margin-bottom: 10px;
        }
        .chat-input {
            width: 80%;
            margin-top: 20px;
            padding: 10px;
            border: 1px solid #ccc;
            border-radius: 5px;
            outline: none;
        }
        .chat-btn {
            margin-top: 10px;
        }
        .expander-content {
            padding: 0 20px;
        }
        .custom-button {
            background-color: #4CAF50;
            color: white;
            padding: 10px 20px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            cursor: pointer;
            border-radius: 5px;
        }
    </style>
""",
    unsafe_allow_html=True,
)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Initialize job search results list
if "job_results" not in st.session_state:
    st.session_state.job_results = []
    

# Initialize user's job description variable
job_description = ""

# Display chat messages and job search results from history on app rerun
for item in st.session_state.messages + st.session_state.job_results:
    with st.chat_message(item["role"]):
        st.markdown(item["content"])

def clear_chat_history():
    st.session_state.messages = []
    st.session_state.job_results = []
    # Save chat history to a file
    with open("chathistory.txt", "w") as file:
        for item in st.session_state.messages + st.session_state.job_results:
            file.write(f"{item['role']}: {item['content']}\n")

st.sidebar.button('Clear Chat History', on_click=clear_chat_history)
st.sidebar.markdown("<div class='custom button'></div>", unsafe_allow_html=True)

# Function to perform SerpApi job search
def serpapi_search(query):
    search_params = {
        "q": query + " jobs",
        "api_key": "8cbdb735c72dfa150d5f30a66185186b804624920ffca82094ff91cd9bed8e5c"
    }
    search = GoogleSearch(search_params)
    result = search.get_dict()
    return result.get("organic_results", [])

# Function to display job search results in a collapsible section
def display_serpapi_jobs(serpapi_results):
    for index, result in enumerate(serpapi_results, start=1):
        title = result.get('title', '')
        company = result.get('snippet', '')
        link = result.get('link', '')

        # Create a collapsible section for each job result
        with st.expander(f"Job {index} - {title}"):
            # Add content inside the expander
            st.write(f"Company: {company}")
            st.write(f"Link: {link}")

# Accept user input
if prompt := st.chat_input("What is up?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        job_questions = [
            "job",
            "employment",
            "career",
            "position",
            "placement",
            "opportunity",
            "occupation",
            "Have you prepared a resume?",
            "Are you open to relocation?",
            "How do you handle employment interviews?",
            "Do you have any specific industries in mind?",
            "How do you handle job rejections?",
            "yes",
            "by",
        ]

        job_responses = [
            "Your Job Description",
            "Enter your employment description",
            "Put your career description here.",
            "Enter your position details",
            "Fill the information of your placement.",
            "Provide the specifics of your opportunity.",
            "Give your job details",
            "It's important to highlight your skills and experience on your resume.",
            "Consider specifying the type of job you are interested in to narrow down your search.",
            "Having a well-prepared resume is crucial for job applications.",
            "Being open to relocation can broaden your job opportunities.",
            "Prepare for job interviews by practicing common questions and researching the company.",
            "what?",
            "Good Bye",
            "Certain industries may have specific requirements; make sure to tailor your applications accordingly.",
        ]

        # Check if the user's input matches a job-related question
        matched_question = None
        for question in job_questions:
            if question.lower() in prompt.lower():
                matched_question = question
                break

        # If a match is found, respond with the corresponding answer
        if matched_question:
            index = job_questions.index(matched_question)
            assistant_response = job_responses[index]

            # Check if the assistant is asking for a job description
            if "Your Job Description" in assistant_response:
                # Store user's input in the job_description variable
                job_description = prompt

                # Now you can use the job_description variable for your API call
                # For example, you can pass it as a parameter to your API function
                serpapi_results = serpapi_search(job_description)

                # Simulate an API call by printing the results to the chat
                if serpapi_results:
                    st.write("")
                    display_serpapi_jobs(serpapi_results)
                    # Store job search results in a separate list
                    st.session_state.job_results.append({"role": "assistant", "content": serpapi_results})
                else:
                    st.write("No job listings found for the given criteria.")
        else:
            # If no match, provide a generic response
            assistant_response = random.choice(
                [
                    "Hello there! How can I assist you today?",
                    "Hi, human! Is there anything I can help you with?",
                    "Do you need help?",
                ]
            )

        # Simulate stream of response with milliseconds delay
        for chunk in assistant_response.split():
            full_response += chunk + " "
            time.sleep(0.05)
            # Add a blinking cursor to simulate typing
        message_placeholder.markdown(f"<div class='chat-container assistant-message'>{full_response}▌</div>", unsafe_allow_html=True)
        message_placeholder.markdown(f"<div class='chat-container assistant-message'>{full_response}</div>", unsafe_allow_html=True)

    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": full_response})
