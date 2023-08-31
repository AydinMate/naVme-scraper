import json
import googlemaps

class AddressFinder:
    def __init__(self, api_key):
        self.api_key = api_key
        self.gmaps = googlemaps.Client(key=self.api_key)

        self.starting_state = 'Victoria'

    def get_suburb(self, geocode_result):
        for component in geocode_result['address_components']:
            if 'locality' in component['types']:
                return component['long_name']
        return None

    def format_job_details(self, jobs):
        formatted_job_details = []

        for job in jobs:
            original_address = job['address']
            address = original_address

            if '/' in original_address:
                address = original_address.split('/', 1)[1].strip()

            geocode_result = self.gmaps.geocode(address, components={'country': 'AU', 'administrative_area': self.starting_state})


            if not geocode_result or not any(address_type in geocode_result[0]['types'] for address_type in ['street_address', 'route', 'premise']):

                formatted_job_details.append({
                    "customer_name": job['customer_name'],
                    "order_number": job['order_number'],
                    "address": original_address,
                    "coordinates": None,
                    "address_found": False,
                    "suburb": "Address not found",
                    "delivery_time": "Anytime",
                    "delivery_size": "Small",
                    "delivery_type": "Any",
                    "order_items": job["order_items"],
                    'status': job["status"]
                    
                })
            else:
                formatted_address = geocode_result[0]['formatted_address']
                suburb = self.get_suburb(geocode_result[0])
                formatted_job_details.append({
                    "customer_name": job['customer_name'],
                    "order_number": job['order_number'],
                    "address": formatted_address,
                    "coordinates": geocode_result[0]["geometry"]["location"],
                    "address_found": True,
                    "suburb": suburb,
                    "delivery_time": "Anytime",
                    "delivery_size": "Small",
                    "delivery_type": "Any",
                    "order_items": job["order_items"],
                    'status': job["status"]
                    
                })

        output_filename = "formatted_jobs.json"

        with open(output_filename, "w") as outfile:
            json.dump(formatted_job_details, outfile, indent=4)

        return formatted_job_details
