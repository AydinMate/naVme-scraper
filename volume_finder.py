import re
import json

class VolumeFinder:
    def __init__(self, jobs):
        if isinstance(jobs, dict):
            self.jobs = [jobs]
        else:
            self.jobs = jobs
        
        filtered_jobs = []

        for job in self.jobs:
            order_items = job['order_items']

            # Check if any SKU contains "DELSOS"
            if any("DELSOS" in item.get("SKU", "") for item in order_items):
                print(f"Skipping job {job['order_number']} due to SKU containing 'DELSOS'")
            else:
                filtered_jobs.append(job)

        # Replace the original jobs list with the filtered one
            self.jobs = filtered_jobs

            

            for item in order_items:
                
                sku = item["SKU"].strip().upper()
                uom = item["UOM"].strip().upper()
                description = item["Description"].lower()

                if uom == "LM":
                    
                    numbers = [int(num) for num in re.findall(r'\d+', description)]
                    numbers.sort(reverse=True)

                    if len(numbers) > 2:
                        numbers = numbers[:2]

                    elif sku.startswith(("BPWB")):
                        numbers = [numbers[0], 19]
                    
                    if len(numbers) == 2:
                        width = self.mm_to_m(numbers[0])
                        height = self.mm_to_m(numbers[1])
                        lineal_meters_str = item["Qty Ordered"]
                        lineal_meters_str = lineal_meters_str.replace(",", "")
                        lineal_meters = float(lineal_meters_str)

                        volume = width * height * lineal_meters
                        
                        item["width"] = width
                        item["height"] = height
                        item["lineal_meters"] = lineal_meters
                        item["volume"] = volume
                    else:
                        print(item)
                        print("has an error")
                        print(numbers)
                        item["volume"] = 0

                elif (uom == "EA" or uom == "EACH") and not (sku[0].isdigit() and len(sku) > 6) and not sku.startswith(("DEL", "FAP", "FRIN", "HIT", "WTAPE", "SB", "UN", "AB", "SSZP", "HB", "SJHB", "MN", "FS", "THOR", "EPA", "ANAS", "SEL")):
                    numbers = [int(num) for num in re.findall(r'\d+', description) if int(num) <= 10000]
                    

                                   
                    if len(numbers) >= 6:
                        numbers = [numbers[3], numbers[2], numbers[3]]
                        
                    elif len(numbers) == 5 and "jamb" in description:
                        numbers = [next(num for num in numbers if 100 < num < 200), max(numbers), next(num for num in numbers if 10 < num < 25)*3]

                    elif len(numbers) == 5 and not "jamb" in description:
                        print(f"This product: {description}, has 5 numbers but is unfiltered. The volume is set to 0 - {numbers}")
                        numbers = [0, 0, 0]
                        
                
                    elif len(numbers) == 4:
                        if "packer" in description or "hardi" in description:
                            numbers = [numbers[1], numbers[0], float(str(numbers[2]) + "." + str(numbers[3]))]
                            
                            
                        elif "sleeper" in description:
                            numbers = [numbers[0], int(float(str(numbers[2]) + "." + str(numbers[3])) * 1000), numbers[1]]

                        elif ("flooring" and "tongue") in description:
                            numbers = [numbers[2], int(float(str(numbers[0]) + "." + str(numbers[1])) * 1000), numbers[3]]
                            
                        elif ("plywood" and "flooring") in description or "cavity" in description:
                            numbers = [numbers[2], numbers[1], numbers [3]]

                        elif ("axon") in description or ("ply") in description:
                            numbers = [numbers[1], numbers[0], numbers[2]]
                        else:
                            print(f"This product: {description}, has 4 numbers but is unfiltered. The volume is set to 0 - {numbers}")
                            numbers = [0, 0, 0]

                    elif "aluminium" in description:
                        numbers = [1, max(numbers), 1]

                    
                        
                    if len(numbers) == 3:
                        width = self.mm_to_m(numbers[0])
                        length = self.mm_to_m(numbers[1])
                        height = self.mm_to_m(numbers[2])
                        quantity = float(item["Qty Ordered"])
                        volume = width * length * height * quantity

                        item["width"] = width
                        item["length"] = length
                        item["height"] = height
                        item["volume"] = volume

                    else:
                        print(item)
                        print("has an error")
                        print(numbers)
                        item["volume"] = 0
                else:
                    item["volume"] = 0


    def get_updated_jobs(self):
        return self.jobs
    
    def mm_to_m(self, mm):
        return mm / 1000

    def save_to_file(self, output_filename="updated_jobs.json"):
        with open(output_filename, "w") as outfile:
            json.dump(self.jobs, outfile, indent=4)
        print(f"Updated jobs saved to {output_filename}")


# Formatted Date: 2023-8-23