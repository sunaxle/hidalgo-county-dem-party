import json
import csv
import io

data = """Office	Last Name	First Name	Phone	Email	Residence	City	Zip	Mailing	City	Zip	DOB	Occupation
206th SDC	Zamora	Juan Roberto	956-420-4878	prisylla@etiksolutions.us	1313 Fullerton Avenue	McAllen	78504	1113 Nightingale Avenue	McAllen	78504	6/20/1977	Attorney
275th SDC	Cuéllar	Marla	956-207-7690	marla3esq@yahoo.com	1600 Palazzo	Mission	78572	Same			7/26/1969	Judge
370th SDC	González	Noe	956-457-9643	GNZ3@hotmail.com	6904 N. 4th Street	McAllen	78504	PO Box 1042	Edinburg	78540	7/30/1962	Judge
Probate 1	García	Jo Anne	956-624-8402	joanneforjudge@gmail.com	1209 W. Gardenia Avenue	McAllen	78501	5111 N. 10th Street # 229	McAllen	78504	12/29/1984	Judge
Probate 2	Garza	Aissa Ilianna	210-532-4773	aissa@aissalaw.com	2302 Fox Run	Mission	78574	Same			9/16/1986	Attorney
Probate 2	Esparza	Lawrence "Larry"	956-648-9186	esparz9@aol.com	208 Ben Hogan Avenue	McAllen	78503	Same			4/30/1962	Attorney
CCL 1	González	Rodolfo "Rudy"	956-358-6199	rudy.gonzale@co.hidalgo.tx.us	901 W. Ferguson	Pharr	78577	100 N. Closner	Edinburg	78539	2/19/1958	Judge
CCL 2	Palacios	Jaime Joel "Jay"	956-318-2380	jaime.palacios44@gmail.com	1303 S. Ebony	Pharr	78577	PO Box 623	Pharr	78577	11/15/1960	Judge
CCL 4	Garza, Jr.	Federico "Fred"	956-318-2390	fredgar0324@gmail.com	118511 N. Conway Avenue	Mission	78573	Same			12/19/1958	Judge
CCL 4	García Pérez	Katherine	956-381-1800	katherine@kplaw.net	1201 Fortress Drive	Edinburg	78539	1013 S. 10th Avenue	Edinburg	78539	7/15/1976	Attorney
CCL 5	Cantú, Jr.	Arnoldo	956-498-7885	arnoldocantujr@gmail.com								
CCL6	García	Alberto	956-460-7180	albertgarcia1113@gmail.com	1113 Ortega Circle	Alamo	78516	127 N. Alamo Road	Alamo	78516	3/24/1963	Judge
CCL 8	Maldonado	Enrique Omar	956-212-6040	Eomarmaldonado@gmail.com	1911 Mesa Drive	Edinburg	78539	100 N. Closner, 5th Floor	Edinburg	78539	2/8/1975	Judge
JP 1/2	González	Daniel Andrew	956-975-7651	drewgonzalez10@gmail.com	2004 Ashley Drive	Weslaco	78596	Same			9/20/1974	JP
JP 2/1	Gutiérrez	Cynthia A.	956-515-3502	drcynthia35@aol.com	400 W. 12th Street	San Juan	78589	Same			11/4/1971	Public health consultant
JP 2/1	Zambrano	Jorge Luis	956-378-3330	jorgezambranocampaign@gmail.com	1001 E. 13-1/2 Street	San Juan	78589	Same			10/25/1987	Realtor
JP 2/1	Sánchez	Lisa Marie	956-534-5990	lisamariesanchez1973@gmail.com	1309 S. Peking Street	McAllen	78501	Same			9/19/1973	Advocate
JP 2/2	Muñoz	Jaime Jerry	956-683-5596	jaimejmunoz@aol.com	1002 West Inspiration	Pharr	78577	Same			3/1/1970	Attorney
JP 3/2	Peña, Jr.	Juan José "J.J."	956-227-3215	pena.juan1@gmail.com	3017 N. Bensen Palm Drive	Mission	78574	Same			8/22/1979	Real estate broker
JP 3/2	Treviño	Sonia Melissa	956-867-2292	soniatrevino3232@gmail.com	1901 Royal Palm Drive	Mission	78572	Same			10/10/1967	Chiropractor
JP 4/2	Maldonado	Arnold André	956-607-9484	Andre@maldonadolawpllc.com	6918 Primos Circle	Edinburg	78542	1209 S. 10th Avenue	Edinburg	78539	10/28/1986	Attorney
JP 5/1	Peña, Jr.	Jason	956-375-8851	judgejasonpena@gmail.com	844 Sabal Avenue	Elsa	78543	PO Box 945	Elsa	78543	9/24/1985	JP
JP 5/1	Hernández	Victor Luis	956-472-3927	vich34@aol.com	1801 North Broadway	Elsa	78543	PO Box 2340	Elsa	78543	12/17/1978	Self-employed"""

out_data = []
lines = data.strip().split('\n')
for line in lines[1:]:
    cols = line.split('\t')
    if len(cols) < 13:
        cols.extend([''] * (13 - len(cols)))
    
    office = cols[0].strip()
    full_office = office
    if "SDC" in office:
        full_office = office.replace("SDC", "State District Court")
    elif "CCL" in office:
        full_office = office.replace("CCL", "County Court at Law No.").replace("No. ", "No. ")
        if office == "CCL6":
            full_office = "County Court at Law No. 6"
    elif "JP" in office:
        full_office = office.replace("JP", "Justice of the Peace, Precinct")

    record = {
        "office_shorthand": office,
        "office_full": full_office,
        "last_name": cols[1].strip(),
        "first_name": cols[2].strip(),
        "phone": cols[3].strip(),
        "email": cols[4].strip(),
        "residence_address": cols[5].strip(),
        "residence_city": cols[6].strip(),
        "residence_zip": cols[7].strip(),
        "mailing_address": cols[8].strip(),
        "mailing_city": cols[9].strip(),
        "mailing_zip": cols[10].strip(),
        "dob": cols[11].strip(),
        "occupation": cols[12].strip(),
    }
    out_data.append(record)

with open('data/judicial_candidates_and_officials.json', 'w', encoding='utf-8') as f:
    json.dump(out_data, f, indent=4, ensure_ascii=False)

print("JSON created at data/judicial_candidates_and_officials.json")
