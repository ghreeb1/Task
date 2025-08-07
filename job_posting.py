import re
from datetime import datetime

def clean_text(text):
    """Remove emojis and clean up formatting"""
    # Remove emojis using regex
    emoji_pattern = re.compile("["
                              u"\U0001F600-\U0001F64F"  # emoticons
                              u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                              u"\U0001F680-\U0001F6FF"  # transport & map symbols
                              u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                              u"\U00002702-\U000027B0"
                              u"\U000024C2-\U0001F251"
                              "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', text)

def extract_job_info(text):
    """Extract key information from the job posting"""
    info = {}
    
    # Extract company name
    company_match = re.search(r'team at (\w+)', text)
    info['company'] = company_match.group(1) if company_match else "Unknown Company"
    
    # Extract email
    email_match = re.search(r'(\w+@\w+\.\w+)', text)
    info['email'] = email_match.group(1) if email_match else "No email found"
    
    # Extract deadline
    deadline_match = re.search(r'(\w+ \d+, \d+)', text)
    info['deadline'] = deadline_match.group(1) if deadline_match else "No deadline specified"
    
    # Extract requirements (lines starting with -)
    req_pattern = r'- (.+?)(?=\n-|\n\n|\Z)'
    requirements = re.findall(req_pattern, text, re.DOTALL)
    info['requirements'] = [req.strip() for req in requirements]
    
    # Extract testimonial
    testimonial_match = re.search(r'"([^"]+)"', text)
    info['testimonial'] = testimonial_match.group(1) if testimonial_match else None
    
    return info

def format_job_posting(info):
    """Format the extracted information into a clean job posting"""
    posting = f"""
JOB POSTING - GRAPHIC DESIGNER
{'=' * 40}

Company: {info['company']}
Position: Creative Graphic Designer
Work Type: Remote Available

REQUIREMENTS:
"""
    
    for i, req in enumerate(info['requirements'], 1):
        clean_req = clean_text(req).strip()
        posting += f"{i}. {clean_req}\n"
    
    posting += f"""
APPLICATION DETAILS:
- Email: {info['email']}
- Deadline: {info['deadline']}

"""
    
    if info['testimonial']:
        posting += f"TESTIMONIAL:\n\"{info['testimonial']}\"\n\n"
    
    posting += "Apply today - don't miss this opportunity!"
    
    return posting

def process_job_posting(text):
    """Main function to process the job posting"""
    print("Processing job posting...")
    print("-" * 50)
    
    # Extract information
    job_info = extract_job_info(text)
    
    # Display extracted data
    print("EXTRACTED INFORMATION:")
    print(f"Company: {job_info['company']}")
    print(f"Email: {job_info['email']}")
    print(f"Deadline: {job_info['deadline']}")
    print(f"Requirements found: {len(job_info['requirements'])}")
    print()
    
    # Generate formatted posting
    formatted_posting = format_job_posting(job_info)
    
    print("FORMATTED JOB POSTING:")
    print(formatted_posting)
    
    return job_info, formatted_posting

# Original text
text = '''📢 we're hiring! 📢

we're looking for a *creative* and motivated graphic designer 🎨 to join our amazing team at BrightStudio.

📝 requirements:
- 2+ years of experience in design (branding/web/social media)
- proficiency in Adobe Suite (esp. Illustrator, Photoshop)
- great communication skills 💬

📧 apply now: jobs@brightstudio.com  
💻 remote work available  
💰 salary: competitive (based on experience)

💡 "i applied last year and the process was super smooth" – @alex.design

interested? don't wait – applications close on Aug 10, 2025! 🗓️  
#hiring #graphicdesign #jobpost #remotejobs
'''

# Process the job posting
if __name__ == "__main__":
    job_data, clean_posting = process_job_posting(text)
    
    # Optional: Save to file
    with open('job_posting_clean.txt', 'w', encoding='utf-8') as f:
        f.write(clean_posting)
    print("\nClean posting saved to 'job_posting_clean.txt'")