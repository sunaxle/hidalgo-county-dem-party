import csv
import os

def curate_precinct_chairs(input_file, output_file):
    """
    Cleans up the raw HCDP_Precinct_Contacts.csv file.
    Filters out people without emails and standardizes the columns for the blaster.
    """
    curated_list = []
    
    try:
        with open(input_file, mode='r', encoding='utf-8') as infile:
            reader = csv.DictReader(infile)
            for row in reader:
                email = row.get('email', '').strip()
                # Skip if there is no email
                if not email:
                    continue
                    
                first_name = row.get('first', '').strip()
                last_name = row.get('last', '').strip()
                precinct = row.get('precinct', '').strip()
                
                # Standardize format for the email blaster
                curated_list.append({
                    'FirstName': first_name,
                    'LastName': last_name,
                    'Email': email,
                    'Tags': f'PrecinctChair, Precinct_{precinct}'
                })
                
        # Write the cleaned list
        with open(output_file, mode='w', encoding='utf-8', newline='') as outfile:
            fieldnames = ['FirstName', 'LastName', 'Email', 'Tags']
            writer = csv.DictWriter(outfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(curated_list)
            
        print(f"✅ Successfully curated {len(curated_list)} precinct chairs into {output_file}")
        
    except FileNotFoundError:
        print(f"❌ File not found: {input_file}")

if __name__ == "__main__":
    print("🧹 Running Data Curation Pipeline...")
    
    # 1. Curate the Precinct Chairs list that we already found in your folder
    curate_precinct_chairs(
        input_file='../HCDP_Precinct_Contacts.csv', 
        output_file='curated_precinct_chairs.csv'
    )
    
    # When you drop Kenna's undisclosed list or the Google Forms export, 
    # we will add more functions here to clean them up and merge them!
