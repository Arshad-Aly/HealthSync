# import requests
# from bs4 import BeautifulSoup
# import time
# import random
# from urllib.parse import urljoin

# class DoctorScraper:
#     def __init__(self, base_url):
#         self.base_url = base_url
#         self.session = requests.Session()
#         self.session.headers = {
#             'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
#             'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
#             'Accept-Language': 'en-US,en;q=0.9',
#             'Accept-Encoding': 'gzip, deflate, br',
#             'Connection': 'keep-alive',
#             'Referer': 'https://www.apollo247.com/',
#             'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
#             'sec-ch-ua-mobile': '?0',
#             'sec-ch-ua-platform': '"Windows"',
#             'Sec-Fetch-Dest': 'document',
#             'Sec-Fetch-Mode': 'navigate',
#             'Sec-Fetch-Site': 'same-origin',
#             'Sec-Fetch-User': '?1',
#             'Upgrade-Insecure-Requests': '1'
#         }

#     def get_page_content(self, url):
#         """Fetch webpage content with rate limiting and error handling"""
#         max_retries = 3
#         base_delay = 5  # Base delay between requests in seconds
        
#         for attempt in range(max_retries):
#             try:
#                 # Add random delay between requests
#                 delay = base_delay + random.uniform(1, 3)
#                 time.sleep(delay)
                
#                 print(f"Fetching page: {url}")
#                 response = self.session.get(url)
#                 response.raise_for_status()
                
#                 # If successful, return the content
#                 return response.text
                
#             except requests.exceptions.HTTPError as e:
#                 if e.response.status_code == 429:
#                     # If rate limited, wait longer before retry
#                     retry_after = int(e.response.headers.get('Retry-After', 60))
#                     wait_time = retry_after + random.uniform(1, 5)
#                     print(f"Rate limited. Waiting {wait_time:.2f} seconds before retry...")
#                     time.sleep(wait_time)
#                 else:
#                     print(f"HTTP Error: {e}")
                    
#             except requests.RequestException as e:
#                 print(f"Error fetching URL {url}: {e}")
#                 if attempt < max_retries - 1:
#                     wait_time = (attempt + 1) * base_delay
#                     print(f"Retrying in {wait_time} seconds...")
#                     time.sleep(wait_time)
#                 else:
#                     return None
        
#         return None

#     def extract_doctor_details(self, html_content):
#         """Extract doctor details from the HTML content"""
#         if not html_content:
#             return []

#         soup = BeautifulSoup(html_content, 'html.parser')
#         doctors_list = []
        
#         # Find all doctor cards
#         doctor_cards = soup.find_all('a', class_=lambda x: x and 'DoctorCard_doctorCard' in x)
        
#         for card in doctor_cards:
#             try:
#                 doctor = {}
                
#                 # Basic Details
#                 name_element = card.find('h2', class_=lambda x: x and 'displayName' in x)
#                 doctor['name'] = name_element.text.strip() if name_element else 'N/A'
                
#                 specialty_element = card.find('p', class_=lambda x: x and 'specialty' in x)
#                 doctor['specialty'] = specialty_element.text.strip() if specialty_element else 'N/A'
                
#                 # Experience and Qualifications
#                 exp_element = card.find('p', class_=lambda x: x and 'experience' in x)
#                 if exp_element:
#                     exp_text = exp_element.text.strip()
#                     exp_parts = exp_text.split('•')
#                     doctor['experience'] = exp_parts[0].strip()
#                     doctor['qualifications'] = exp_parts[1].strip() if len(exp_parts) > 1 else 'N/A'
                
#                 # Location
#                 location_elements = card.find_all('p', class_=lambda x: x and 'location' in x)
#                 doctor['city'] = location_elements[0].text.strip() if location_elements else 'N/A'
#                 doctor['clinic'] = location_elements[1].text.strip() if len(location_elements) > 1 else 'N/A'
                
#                 # Consultation Details
#                 buttons = card.find_all('div', class_=lambda x: x and 'buttonWrapper' in x)
#                 for button in buttons:
#                     type_element = button.find('span', class_=lambda x: x and 'button_title' in x)
#                     if not type_element:
#                         continue
                        
#                     consultation_type = type_element.text.strip()
                    
#                     price_element = button.find('p', class_=lambda x: x and 'fees' in x)
#                     price = price_element.text.strip() if price_element else 'N/A'
                    
#                     availability_element = button.find('span', class_=lambda x: x and 'availability' in x)
#                     availability = availability_element.text.strip() if availability_element else 'Not specified'
                    
#                     if 'Digital' in consultation_type:
#                         doctor['digital_consult'] = {
#                             'price': price,
#                             'availability': availability
#                         }
#                     elif 'Clinic' in consultation_type:
#                         doctor['clinic_visit'] = {
#                             'price': price,
#                             'availability': availability
#                         }
                
#                 # Get doctor profile URL
#                 profile_url = card.get('href')
#                 if profile_url:
#                     doctor['profile_url'] = urljoin(self.base_url, profile_url)
                
#                 doctors_list.append(doctor)
                
#             except Exception as e:
#                 print(f"Error processing doctor card: {e}")
#                 continue
        
#         return doctors_list

#     def scrape_multiple_pages(self, specialty, max_pages=5):
#         """Scrape multiple pages for a given specialty"""
#         all_doctors = []
        
#         for page in range(1, max_pages + 1):
#             url = f"https://www.apollo247.com/specialties/{specialty}?page={page}&sortby=distance"
#             html_content = self.get_page_content(url)
            
#             if html_content:
#                 doctors = self.extract_doctor_details(html_content)
#                 if doctors:
#                     all_doctors.extend(doctors)
#                     print(f"Successfully scraped page {page} - Found {len(doctors)} doctors")
#                 else:
#                     print(f"No doctors found on page {page}. Stopping pagination.")
#                     break
#             else:
#                 print(f"Failed to fetch page {page}. Stopping pagination.")
#                 break
        
#         return all_doctors

# def save_to_file(doctors, filename="doctors_data.txt"):
#     """Save the scraped data to a file"""
#     with open(filename, 'w', encoding='utf-8') as f:
#         for i, doctor in enumerate(doctors, 1):
#             f.write(f"\nDoctor #{i}\n")
#             f.write("="*50 + "\n")
#             f.write(f"Name: {doctor['name']}\n")
#             f.write(f"Specialty: {doctor['specialty']}\n")
#             f.write(f"Experience: {doctor.get('experience', 'N/A')}\n")
#             f.write(f"Qualifications: {doctor.get('qualifications', 'N/A')}\n")
#             f.write(f"City: {doctor['city']}\n")
#             f.write(f"Clinic: {doctor['clinic']}\n")
            
#             if 'digital_consult' in doctor:
#                 f.write("\nDigital Consultation:\n")
#                 f.write(f"  Price: {doctor['digital_consult']['price']}\n")
#                 f.write(f"  Availability: {doctor['digital_consult']['availability']}\n")
                
#             if 'clinic_visit' in doctor:
#                 f.write("\nClinic Visit:\n")
#                 f.write(f"  Price: {doctor['clinic_visit']['price']}\n")
#                 f.write(f"  Availability: {doctor['clinic_visit']['availability']}\n")
            
#             f.write(f"Profile URL: {doctor.get('profile_url', 'N/A')}\n\n")

# def main():
#     base_url = "https://www.apollo247.com"
#     scraper = DoctorScraper(base_url)
    
#     # Specify the specialty you want to scrape
#     specialty = "neurosurgery"
    
#     # Scrape the data
#     print(f"Starting to scrape {specialty} doctors...")
#     doctors = scraper.scrape_multiple_pages(specialty, max_pages=3)
    
#     # Save the results
#     if doctors:
#         print(f"\nFound {len(doctors)} doctors")
#         save_to_file(doctors, f"{specialty}_doctors.txt")
#         print(f"Data saved to {specialty}_doctors.txt")
#     else:
#         print("No doctors found")

# if __name__ == "__main__":
#     main()


# import requests
# from bs4 import BeautifulSoup
# import time
# import random
# import json
# from datetime import datetime
# from urllib.parse import urljoin

# class DoctorScraper:
#     def __init__(self, base_url):
#         self.base_url = base_url
#         self.session = requests.Session()
#         self.session.headers = {
#             'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
#             'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
#             'Accept-Language': 'en-US,en;q=0.9',
#             'Accept-Encoding': 'gzip, deflate, br',
#             'Connection': 'keep-alive',
#             'Referer': 'https://www.apollo247.com/',
#             'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
#             'sec-ch-ua-mobile': '?0',
#             'sec-ch-ua-platform': '"Windows"',
#             'Sec-Fetch-Dest': 'document',
#             'Sec-Fetch-Mode': 'navigate',
#             'Sec-Fetch-Site': 'same-origin',
#             'Sec-Fetch-User': '?1',
#             'Upgrade-Insecure-Requests': '1'
#         }

#     def get_page_content(self, url):
#         """Fetch webpage content with rate limiting and error handling"""
#         max_retries = 3
#         base_delay = 5
        
#         for attempt in range(max_retries):
#             try:
#                 delay = base_delay + random.uniform(1, 3)
#                 time.sleep(delay)
                
#                 print(f"Fetching page: {url}")
#                 response = self.session.get(url)
#                 response.raise_for_status()
#                 return response.text
                
#             except requests.exceptions.HTTPError as e:
#                 if e.response.status_code == 429:
#                     retry_after = int(e.response.headers.get('Retry-After', 60))
#                     wait_time = retry_after + random.uniform(1, 5)
#                     print(f"Rate limited. Waiting {wait_time:.2f} seconds before retry...")
#                     time.sleep(wait_time)
#                 else:
#                     print(f"HTTP Error: {e}")
                    
#             except requests.RequestException as e:
#                 print(f"Error fetching URL {url}: {e}")
#                 if attempt < max_retries - 1:
#                     wait_time = (attempt + 1) * base_delay
#                     print(f"Retrying in {wait_time} seconds...")
#                     time.sleep(wait_time)
#                 else:
#                     return None
        
#         return None

#     lat = [17.411482, 17.438335, 17.399805, 17.342864, 18.456920, 16.870054, 18.035563]
#     lon = [78.403532, 78.504831, 78.479150, 78.506943, 79.135035, 79.562540, 79.629879]

#     def extract_doctor_details(self, html_content):
#         """Extract doctor details from the HTML content"""
#         if not html_content:
#             return []

#         soup = BeautifulSoup(html_content, 'html.parser')
#         doctors_list = []
        
#         doctor_cards = soup.find_all('a', class_=lambda x: x and 'DoctorCard_doctorCard' in x)
        
#         for card in doctor_cards:
#             try:
#                 doctor = {}
                
#                 # Extract doctor ID from href if available
#                 href = card.get('href', '')
#                 doctor['id'] = href.split('/')[-1] if href else 'N/A'
                
#                 # Basic Details
#                 name_element = card.find('h2', class_=lambda x: x and 'displayName' in x)
#                 doctor['name'] = name_element.text.strip() if name_element else 'N/A'
                
#                 specialty_element = card.find('p', class_=lambda x: x and 'specialty' in x)
#                 doctor['specialty'] = specialty_element.text.strip() if specialty_element else 'N/A'
                
#                 # Experience and Qualifications
#                 exp_element = card.find('p', class_=lambda x: x and 'experience' in x)
#                 if exp_element:
#                     exp_text = exp_element.text.strip()
#                     exp_parts = exp_text.split('•')
#                     doctor['experience'] = exp_parts[0].strip()
#                     doctor['qualifications'] = exp_parts[1].strip() if len(exp_parts) > 1 else 'N/A'
                
#                 # Location
#                 location_elements = card.find_all('p', class_=lambda x: x and 'location' in x)
#                 doctor['city'] = location_elements[0].text.strip() if location_elements else 'N/A'
#                 doctor['clinic'] = location_elements[1].text.strip() if len(location_elements) > 1 else 'N/A'
                
#                 # Ratings and Recommendations
#                 rec_div = card.find('div', class_=lambda x: x and 'doctorRecommendation' in x)
#                 if rec_div:
#                     rating = rec_div.find('p', class_=lambda x: x and 'rating' in x)
#                     recommendations = rec_div.find('p', class_=lambda x: x and 'count' in x)
#                     doctor['rating'] = rating.text.strip() if rating else 'N/A'
#                     doctor['recommendations'] = recommendations.text.strip() if recommendations else 'N/A'
                
#                 # Consultation Details
#                 doctor['consultations'] = {
#                     'digital': None,
#                     'clinic': None
#                 }
                
#                 buttons = card.find_all('div', class_=lambda x: x and 'buttonWrapper' in x)
#                 for button in buttons:
#                     type_element = button.find('span', class_=lambda x: x and 'button_title' in x)
#                     if not type_element:
#                         continue
                        
#                     consultation_type = type_element.text.strip()
                    
#                     price_element = button.find('p', class_=lambda x: x and 'fees' in x)
#                     price = price_element.text.strip() if price_element else 'N/A'
                    
#                     availability_element = button.find('span', class_=lambda x: x and 'availability' in x)
#                     availability = availability_element.text.strip() if availability_element else 'Not specified'
                    
#                     consult_data = {
#                         'price': price,
#                         'availability': availability
#                     }
                    
#                     if 'Digital' in consultation_type:
#                         doctor['consultations']['digital'] = consult_data
#                     elif 'Clinic' in consultation_type:
#                         doctor['consultations']['clinic'] = consult_data
                
#                 # Profile URL
#                 doctor['profile_url'] = urljoin(self.base_url, href) if href else 'N/A'
                
#                 doctors_list.append(doctor)
                
#             except Exception as e:
#                 print(f"Error processing doctor card: {e}")
#                 continue
        
#         return doctors_list

#     def scrape_multiple_pages(self, specialty, max_pages=5):
#         """Scrape multiple pages for a given specialty"""
#         all_doctors = []
        
#         for page in range(1, max_pages + 1):
#             url = f"https://www.apollo247.com/specialties/{specialty}?page={page}&sortby=distance"
#             html_content = self.get_page_content(url)
            
#             if html_content:
#                 doctors = self.extract_doctor_details(html_content)
#                 if doctors:
#                     all_doctors.extend(doctors)
#                     print(f"Successfully scraped page {page} - Found {len(doctors)} doctors")
#                 else:
#                     print(f"No doctors found on page {page}. Stopping pagination.")
#                     break
#             else:
#                 print(f"Failed to fetch page {page}. Stopping pagination.")
#                 break
        
#         return all_doctors

# def save_to_json(doctors, specialty):
#     """Save the scraped data to a JSON file with timestamp"""
#     timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
#     filename = f"{specialty}_doctors_{timestamp}.json"
    
#     data = {
#         'metadata': {
#             'specialty': specialty,
#             'total_doctors': len(doctors),
#             'scrape_timestamp': datetime.now().isoformat(),
#         },
#         'doctors': doctors
#     }
    
#     with open(filename, 'w', encoding='utf-8') as f:
#         json.dump(data, f, indent=2, ensure_ascii=False)
    
#     return filename

# def main():
#     base_url = "https://www.apollo247.com"
#     scraper = DoctorScraper(base_url)
    
#     # Specify the specialty you want to scrape
#     specialty = "neurosurgery"
    
#     # Scrape the data
#     print(f"Starting to scrape {specialty} doctors...")
#     doctors = scraper.scrape_multiple_pages(specialty, max_pages=3)
    
#     # Save the results
#     if doctors:
#         print(f"\nFound {len(doctors)} doctors")
#         filename = save_to_json(doctors, specialty)
#         print(f"Data saved to {filename}")
#     else:
#         print("No doctors found")

# if __name__ == "__main__":
#     main()


import requests
from bs4 import BeautifulSoup
import time
import random
import json
from datetime import datetime
from urllib.parse import urljoin

class DoctorScraper:
    def __init__(self, base_url):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Referer': 'https://www.apollo247.com/',
            'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1'
        }
        # Define coordinates lists as class attributes
        self.coordinates = list(zip(
            [17.411482, 17.438335, 17.399805, 17.342864, 18.456920, 16.870054, 18.035563],
            [78.403532, 78.504831, 78.479150, 78.506943, 79.135035, 79.562540, 79.629879]
        ))

    def get_random_coordinates(self):
        """Get a random pair of coordinates while maintaining lat/lon pairing"""
        return random.choice(self.coordinates)

    def get_page_content(self, url):
        """Fetch webpage content with rate limiting and error handling"""
        max_retries = 3
        base_delay = 5
        
        for attempt in range(max_retries):
            try:
                delay = base_delay + random.uniform(1, 3)
                time.sleep(delay)
                
                print(f"Fetching page: {url}")
                response = self.session.get(url)
                response.raise_for_status()
                return response.text
                
            except requests.exceptions.HTTPError as e:
                if e.response.status_code == 429:
                    retry_after = int(e.response.headers.get('Retry-After', 60))
                    wait_time = retry_after + random.uniform(1, 5)
                    print(f"Rate limited. Waiting {wait_time:.2f} seconds before retry...")
                    time.sleep(wait_time)
                else:
                    print(f"HTTP Error: {e}")
                    
            except requests.RequestException as e:
                print(f"Error fetching URL {url}: {e}")
                if attempt < max_retries - 1:
                    wait_time = (attempt + 1) * base_delay
                    print(f"Retrying in {wait_time} seconds...")
                    time.sleep(wait_time)
                else:
                    return None
        
        return None

    def extract_doctor_details(self, html_content):
        """Extract doctor details from the HTML content"""
        if not html_content:
            return []

        soup = BeautifulSoup(html_content, 'html.parser')
        doctors_list = []
        
        doctor_cards = soup.find_all('a', class_=lambda x: x and 'DoctorCard_doctorCard' in x)
        
        for card in doctor_cards:
            try:
                doctor = {}
                
                # Add random coordinates to each doctor
                lat, lon = self.get_random_coordinates()
                doctor['latitude'] = lat
                doctor['longitude'] = lon
                
                # Extract doctor ID from href if available
                href = card.get('href', '')
                doctor['id'] = href.split('/')[-1] if href else 'N/A'
                
                # Basic Details
                name_element = card.find('h2', class_=lambda x: x and 'displayName' in x)
                doctor['name'] = name_element.text.strip() if name_element else 'N/A'
                
                specialty_element = card.find('p', class_=lambda x: x and 'specialty' in x)
                doctor['specialty'] = specialty_element.text.strip() if specialty_element else 'N/A'
                
                # Experience and Qualifications
                exp_element = card.find('p', class_=lambda x: x and 'experience' in x)
                if exp_element:
                    exp_text = exp_element.text.strip()
                    exp_parts = exp_text.split('•')
                    doctor['experience'] = exp_parts[0].strip()
                    doctor['qualifications'] = exp_parts[1].strip() if len(exp_parts) > 1 else 'N/A'
                
                # Location
                location_elements = card.find_all('p', class_=lambda x: x and 'location' in x)
                doctor['city'] = location_elements[0].text.strip() if location_elements else 'N/A'
                doctor['clinic'] = location_elements[1].text.strip() if len(location_elements) > 1 else 'N/A'
                
                # Ratings and Recommendations
                rec_div = card.find('div', class_=lambda x: x and 'doctorRecommendation' in x)
                if rec_div:
                    rating = rec_div.find('p', class_=lambda x: x and 'rating' in x)
                    recommendations = rec_div.find('p', class_=lambda x: x and 'count' in x)
                    doctor['rating'] = rating.text.strip() if rating else 'N/A'
                    doctor['recommendations'] = recommendations.text.strip() if recommendations else 'N/A'
                
                # Consultation Details
                doctor['consultations'] = {
                    'digital': None,
                    'clinic': None
                }
                
                buttons = card.find_all('div', class_=lambda x: x and 'buttonWrapper' in x)
                for button in buttons:
                    type_element = button.find('span', class_=lambda x: x and 'button_title' in x)
                    if not type_element:
                        continue
                        
                    consultation_type = type_element.text.strip()
                    
                    price_element = button.find('p', class_=lambda x: x and 'fees' in x)
                    price = price_element.text.strip() if price_element else 'N/A'
                    
                    availability_element = button.find('span', class_=lambda x: x and 'availability' in x)
                    availability = availability_element.text.strip() if availability_element else 'Not specified'
                    
                    consult_data = {
                        'price': price,
                        'availability': availability
                    }
                    
                    if 'Digital' in consultation_type:
                        doctor['consultations']['digital'] = consult_data
                    elif 'Clinic' in consultation_type:
                        doctor['consultations']['clinic'] = consult_data
                
                # Profile URL
                doctor['profile_url'] = urljoin(self.base_url, href) if href else 'N/A'
                
                doctors_list.append(doctor)
                
            except Exception as e:
                print(f"Error processing doctor card: {e}")
                continue
        
        return doctors_list

    def scrape_multiple_pages(self, specialty, max_pages=5):
        """Scrape multiple pages for a given specialty"""
        all_doctors = []
        
        for page in range(1, max_pages + 1):
            url = f"https://www.apollo247.com/specialties/{specialty}?page={page}&sortby=distance"
            html_content = self.get_page_content(url)
            
            if html_content:
                doctors = self.extract_doctor_details(html_content)
                if doctors:
                    all_doctors.extend(doctors)
                    print(f"Successfully scraped page {page} - Found {len(doctors)} doctors")
                else:
                    print(f"No doctors found on page {page}. Stopping pagination.")
                    break
            else:
                print(f"Failed to fetch page {page}. Stopping pagination.")
                break
        
        return all_doctors
    
def save_to_json(doctors, specialty):
    """Save the scraped data to a JSON file with timestamp"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"{specialty}_doctors_{timestamp}.json"
    
    data = {
        'metadata': {
            'specialty': specialty,
            'total_doctors': len(doctors),
            'scrape_timestamp': datetime.now().isoformat(),
        },
        'doctors': doctors
    }
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    return filename

def main():
    base_url = "https://www.apollo247.com"
    scraper = DoctorScraper(base_url)
    
    # Specify the specialty you want to scrape
    specialty = "neurosurgery"
    
    # Scrape the data
    print(f"Starting to scrape {specialty} doctors...")
    doctors = scraper.scrape_multiple_pages(specialty, max_pages=3)
    
    # Save the results
    if doctors:
        print(f"\nFound {len(doctors)} doctors")
        filename = save_to_json(doctors, specialty)
        print(f"Data saved to {filename}")
    else:
        print("No doctors found")

if __name__ == "__main__":
    main()