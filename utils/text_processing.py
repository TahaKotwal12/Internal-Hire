import re

def extract_email(text):
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    emails = re.findall(email_pattern, text)
    return emails[0] if emails else None

def extract_linkedin(text):
    linkedin_pattern = r'https?://(?:www\.)?linkedin\.com/in/[\w\-]+/?'
    linkedin_profiles = re.findall(linkedin_pattern, text)
    return linkedin_profiles[0] if linkedin_profiles else None

def extract_github(text):
    github_pattern = r'https?://(?:www\.)?github\.com/[\w\-]+/?'
    github_profiles = re.findall(github_pattern, text)
    return github_profiles[0] if github_profiles else None

def extract_phone(text):
    phone_pattern = r'\b(?:\+\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b'
    phones = re.findall(phone_pattern, text)
    return phones[0] if phones else None

def extract_contact_info(text):
    return {
        'Email': extract_email(text),
        'Linkedin': extract_linkedin(text),
        'Github': extract_github(text),
        'Phone': extract_phone(text)
    }

# Alias for backwards compatibility
extract_key_details = extract_contact_info

def create_summary_with_details(summary, details):
    detail_str = " ".join([f"{k}: {v}\n" for k, v in details.items() if v])
    return f"{detail_str}\n\n{summary}"

def get_available_contact_methods(contact_info):
    return [method for method, value in contact_info.items() if value]