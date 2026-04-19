import json

data = """Office	First Name	Last Name	Email	Phone
U.S. Senator	James	Talarico		
U.S. Senator	Colin	Allred		
CD 15	Bobby	Pulido		
CD 28	Henry	Cuéllar		
Governor	Gina	Hinojosa		
Lieutenant Governor	Vicki	Goodwin		
Attorney General	Joe 	Jaworski		
Attorney General	Nathan	Johnson		
Comptroller				
GLO Commissioner				
Ag Commissioner	Clayton	Tucker		
RR Commissioner				
SCJ Place 3				
SCJ Place 5				
SCJ Place 9				
CCAJ Place 5				
CCAJ Place 6				
SBOE District 2	Thomas	García		
SBOE District 3				
State Senator District 27				
State Rep District 35	Oscar	Longoria		
State Rep District 36	Sergio	Muñoz, Jr.	sergio@sergiomunozjr.com	956-381-5555
State Rep District 39	Armando "Mando" 	Martínez	andoconmando@yahoo.com	956-493-7600
State Rep District 40	Terry	Canales	Tcanales@rgvattorney.com	956-578-9568
State Rep District 41	Eric	Holguín	Eric@ericfortexas.com	956-489-2889
State Rep District 41	Seby	Haddad	sebyhaddad@gmail.com	956-605-7762
State Rep District 41	Julio	Salinas		
13th COAJ Place 3				
206th JD	Juan J.	Zamora	prisylla@etiksolutions.us	956-420-4878
206th JD	Lucia	Regalado		
275th JD	Marla	Cuéllar	marla3esq@yahoo.com	956-207-7690
370th JD	Noe	González	GNZ3@hotmail.com	956-457-9643
Criminal District Attorney	Terry	Palacios	toribiopalacios@att.net	956-330-0788
County Judge	Ricardo "Richard" F. 	Cortez	rfcortezcpa@gmail.com	956-648-5941
District Clerk	Laura	Hinojosa	lauraleehinojosa@gmail.com	956-605-1010
County Clerk	Arturo	Guajardo, Jr.	arturo.guajardo@co.hidalgo.tx.us	956-279-6037
County Treasurer	Lita L.	Leo	lrain21@gmail.com	956-279-8451
County Treasurer	Alejandro	Cantú	alemx16@hotmail.com	956-867-3650
County Comm Pct 2	Eddie	Cantú, Jr.	eddiecantu@me.com	956-454-7247
County Comm Pct 4	Ellie	Torres	jdredbail@yahoo.com	956-279-4874
Constable Pct 5	Daniel	Marichalar	Danman182142@icloud.com	956-756-0438
Constable Pct 5	Jorge Luis	Arce	jorge.arce62@gmail.com	956-379-0792
CCL 1	Rodolfo "Rudy" 	González	rudy.gonzale@co.hidalgo.tx.us	956-358-6199
CCL 2	Jaime "Jay"	Palacios	Jaime.Palacios44@gmail.com	956-318-2380
CCL 4	Federico "Fred"	Garza, Jr.	zambranodallas@gmail.com/ fredgar0324@gmail.com	956-330-1649
CCL 4	Katherine	García Pérez	katherine@kperezlaw.net	956-381-1800
CCL 5	Arnoldo	Cantú, Jr.	arnoldocantujr@gmail.com	956-498-7885
CCL 6	Albert	García	albertgarcia1113@yahoo.com	956-460-7180
CCL 8	Omar	Maldonado	Eomarmaldonado@gmail.com	956-212-6040
Probate Court 1	JoAnne	García	joannefojudge@gmail.com	956-624-8402
Probate Court 2	Aissa	Garza	aissa@aissalaw.com	210-552-9773
JP 1, Place 2	Andrew	González	drewgonzalez10@gmail.com	956-975-7651
JP 2, Place 1	Cynthia	Gutiérrez	drcynthia35@aol.com	956-515-3502
JP 2, Place 1	Jorge Luis	Zambrano	jorgezambranocampaign2026@gmail.com	956-800-3623
JP 2, Place 1	Lisa Marie	Sánchez	lisamariesanchez1973@gmail.com	956-534-5990
JP 2, Place 2	Jaime Jerry	Muñoz	jaimejmunoz@aol.com	956-683-5596
JP 3, Place 2	Juan José	Peña	pena.juan1@gmail.com	956-227-3215
JP 3, Place 2	Sonia Melissa	Treviño	soniatrevino3232@gmail.com	956-519-3111 
JP 4, Place 2	André	Maldonado	Andre@maldonadolawpllc.com	956-607-9484
JP 5/1	Jason	Peña	judgejasonpena@gmail.com	956-375-8851
JP 5/1	Hernández	Victor Luis	vich34@aol.com	956-472-3927"""

officials = []
lines = data.strip().split('\n')
for line in lines[1:]:
    cols = line.split('\t')
    record = {
        "office": cols[0].strip(),
        "first_name": cols[1].strip() if len(cols) > 1 else "",
        "last_name": cols[2].strip() if len(cols) > 2 else "",
        "email": cols[3].strip() if len(cols) > 3 else "",
        "phone": cols[4].strip() if len(cols) > 4 else ""
    }
    # Only keep those who actually have a name listed
    if record["first_name"] or record["last_name"]:
        officials.append(record)

with open('data/master_candidates_2026.json', 'w', encoding='utf-8') as f:
    json.dump(officials, f, indent=4, ensure_ascii=False)

print("Created data/master_candidates_2026.json with", len(officials), "records.")
