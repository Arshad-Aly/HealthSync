import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import logging
from typing import Dict, List
import time
import random

class DoctorWebScraper:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.setup_logging()
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
        })

    def setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('website_scraper.log'),
                logging.StreamHandler()
            ]
        )

    def fetch_page(self, url: str) -> BeautifulSoup:
        """Fetch and parse a webpage"""
        try:
            logging.info(f"Fetching page: {url}")
            response = self.session.get(url)
            response.raise_for_status()
            return BeautifulSoup(response.text, 'html.parser')
        except requests.RequestException as e:
            logging.error(f"Error fetching page: {e}")
            raise

    def extract_doctor_details(self, doctor_element: BeautifulSoup) -> Dict:
        """Extract details for a single doctor"""
        try:
            # Basic info
            name = doctor_element.find('p', class_='doc-name').text.strip()
            qualifications = doctor_element.find('p', class_='text-muted small').text.strip()
            designation = doctor_element.find('p', class_='doc-designation').text.strip()
            
            # Languages and other details
            languages = doctor_element.find('div', class_='know-lang').text.replace('language', '').strip()
            experience = doctor_element.find('i', class_='fa-briefcase').parent.text.strip()
            location = doctor_element.find('i', class_='fa-location-dot').parent.text.strip()
            
            # URLs
            profile_link = doctor_element.find('a', string='View Profile')
            profile_url = profile_link['href'] if profile_link else None
            image_url = doctor_element.find('img', class_='doc-thmb')['src']
            
            # Extract doctor ID and specialization from appointment button
            appointment_btn = doctor_element.find('div', class_='appointment_btn')
            doctor_id = appointment_btn['data-docid'] if appointment_btn else None
            specialization = appointment_btn['data-docspc'] if appointment_btn else None
            
            return {
                'name': name,
                'qualifications': qualifications,
                'designation': designation,
                'languages': languages,
                'experience': experience,
                'location': location,
                'profile_url': profile_url,
                'image_url': image_url,
                'doctor_id': doctor_id,
                'specialization': specialization,
                'scraped_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
        except Exception as e:
            logging.error(f"Error extracting doctor details: {e}")
            raise

    def extract_appointment_dates(self, doc_id: str, specialization: str) -> List[Dict]:
        """Extract available appointment dates for a doctor"""
        try:
            # Assuming there's an API or URL pattern for appointment dates
            # You'll need to adjust this based on the actual website structure
            appointment_url = f"{self.base_url}/appointments/{doc_id}/{specialization}"
            soup = self.fetch_page(appointment_url)
            
            dates = []
            date_elements = soup.find_all('div', class_='swiper-slide')
            
            for element in date_elements:
                # Skip disabled dates (Sundays)
                if element.find('button', disabled=True):
                    continue
                
                date_input = element.find('input', {'name': 'apptdate1'})
                if date_input:
                    dates.append({
                        'date': date_input['value'],
                        'day': element.text.strip(),
                        'is_available': 'active' in element.find('div', class_='demo-content').get('class', [])
                    })
            
            return dates
        except Exception as e:
            logging.error(f"Error extracting appointment dates: {e}")
            return []

    def save_to_json(self, data: Dict, filename: str = None):
        """Save the scraped data to a JSON file"""
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'doctors_data_{timestamp}.json'
            
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            logging.info(f"Successfully saved data to {filename}")
        except Exception as e:
            logging.error(f"Error saving to JSON: {e}")
            raise

def main():
    # Replace with actual website URL
    website_url = "https://www.yashodahospitals.com/find-doctor/"
    
    try:
        scraper = DoctorWebScraper(website_url)
        
        # Fetch main page
        soup = scraper.fetch_page(website_url)
        
        # Find all doctor elements
        doctor_elements = soup.find_all('div', class_='find-doc-list')
        
        all_doctors = []
        for doctor_element in doctor_elements:
            try:
                # Extract doctor details
                doctor_info = scraper.extract_doctor_details(doctor_element)
                
                # Add small delay between requests to be polite
                time.sleep(random.uniform(1, 3))
                
                # Extract appointment dates if available
                if doctor_info['doctor_id'] and doctor_info['specialization']:
                    appointments = scraper.extract_appointment_dates(
                        doctor_info['doctor_id'],
                        doctor_info['specialization']
                    )
                    doctor_info['available_appointments'] = appointments
                
                all_doctors.append(doctor_info)
                logging.info(f"Successfully scraped data for {doctor_info['name']}")
                
            except Exception as e:
                logging.error(f"Error processing doctor element: {e}")
                continue
        
        # Save all data
        complete_data = {
            'doctors': all_doctors,
            'total_doctors': len(all_doctors),
            'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        scraper.save_to_json(complete_data)
        print(f"Successfully scraped {len(all_doctors)} doctors")
        
    except Exception as e:
        logging.error(f"Scraping failed: {e}")
        print(f"Error occurred. Check website_scraper.log for details")

if __name__ == "__main__":
    main()