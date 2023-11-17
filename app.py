import streamlit as st
from bs4 import BeautifulSoup
import requests
import random

def generate_text(ngram_freq, seed, length=3):
    for _ in range(length):
        if seed not in ngram_freq:
            break
        seed += (random.choices(list(ngram_freq[seed]), weights=ngram_freq[seed]))[0],
    return ' '.join(seed)

def scrape_jobs(job_title, qualification):
    base_url = f'https://scrapeops.io/python-web-scraping-playbook/python-indeed-scraper/?job_title={job_title}&qualification={qualification}'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.61.0 Safari/537.36'
    }

    job_listings = []

    page = 1
    while True:
        query_url = f'{base_url}&page={page}'
        response = requests.get(query_url, headers=headers)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            job_listings_on_page = soup.find_all('div', class_='job-listing')
            if not job_listings_on_page:
                break
            job_listings.extend(job_listings_on_page)
            page += 1
        else:
            break

    return job_listings

def display_jobs(job_listings):
    for index, job in enumerate(job_listings, start=1):
        title = job.find('h2', class_='job-title').text
        company = job.find('span', class_='company-name').text
        qualification = job.find('div', class_='qualification').text
        link = job.find('a', href=True)['href']
        st.write(f"Job {index}:\nTitle: {title}\nCompany: {company}\nQualification: {qualification}\nLink: {link}\n")

def main():
    st.title("Job Search Chatbot")

    job_title = st.text_input("Enter the job title:")
    qualification = st.text_input("Enter the qualification:")

    if st.button("Search Jobs"):
        ngram_freq = {
            ('software', 'engineer'): ['position', 'job', 'opportunity'],
            ('data', 'scientist'): ['position', 'job', 'opportunity'],
            ('web', 'developer'): ['position', 'job', 'opportunity']
        }

        seed = tuple(job_title.lower().split()) + tuple(qualification.lower().split())
        suggestion = generate_text(ngram_freq, seed, length=3)
        st.write(f"Suggested job description: {suggestion}")

        job_listings = scrape_jobs(job_title, qualification)

        if job_listings:
            display_jobs(job_listings)
        else:
            st.write("No job listings found for the given criteria.")

if __name__ == "__main__":
    main()
