import streamlit as st
from serpapi import GoogleSearch

def serpapi_search(query):
    search_params = {
        "q": query+"jobs",
        "api_key": "2571163e947b2a303758f118289932369c6a27eeb1700b900832492ce6b23b43"
    }
    search = GoogleSearch(search_params)
    result = search.get_dict()
    return result.get("organic_results", [])

def display_serpapi_jobs(serpapi_results):
    for index, result in enumerate(serpapi_results, start=1):
        title = result.get('title', '')
        company = result.get('snippet', '')
        link = result.get('link', '')
        st.write(f"Job {index}:\n|Title: {title}|\nCompany: {company}|\nLink: {link}\n")

def main():
    st.title("Job Searching Platform")

    job_title = st.text_input("Enter the job Description:","software engineer job")


    if st.button("Search Jobs"):
        
        serpapi_results = serpapi_search(job_title)
    
        if serpapi_results:
            st.write("Job Search Results:")
            display_serpapi_jobs(serpapi_results)
        else:
            st.write("No job listings found using SerpApi for the given criteria.")

if __name__ == "__main__":
    main()

