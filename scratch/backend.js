/**
 * VAN Concierge Web App Backend
 * Securely looks up Email and Phone numbers based on the user's dropdown selection.
 */

// DO NOT SHARE THIS FILE - CONTAINS PRIVATE CONTACT INFO
var CHAIR_DATABASE = {
  "Precinct 2 - Cassandra S\u00e1nchez": {
    "email": "Cassie4589@gmail.com",
    "phone": "9563326219"
  },
  "Precinct 8 - Andr\u00e9s F Salinas": {
    "email": "afsalinas@att.net",
    "phone": "9562275759"
  },
  "Precinct 14 - Mary Alice Palacios": {
    "email": "mary.alice.palacios59@gmail.com",
    "phone": "9565601020"
  },
  "Precinct 16 - Daniel Angel Guzm\u00e1n": {
    "email": "dannyguzman65@yahoo.com",
    "phone": "9565510486"
  },
  "Precinct 16 - Selma Morales": {
    "email": "selmam1341@yahoo.com",
    "phone": "9562896131"
  },
  "Precinct 17 - Guadalupe Rangel": {
    "email": "guadalupe.rangel@co.hidalgo.tx.us",
    "phone": "9563328980"
  },
  "Precinct 22 - Jorge Ricardo Alvarado": {
    "email": "alvaradojorge1729@gmail.com",
    "phone": "9565384110"
  },
  "Precinct 23 - Raquel Mart\u00ednez": {
    "email": "raquel6037@yahoo.com",
    "phone": "9564637418"
  },
  "Precinct 25 - Daniela Renee \u00c1vila": {
    "email": "aviladaniela1@yahoo.com",
    "phone": "9563423479"
  },
  "Precinct 27 - Miguel Robledo": {
    "email": "mikerobledo1@yahoo.com",
    "phone": "9562893045"
  },
  "Precinct 30 - Aeryn Christian Ausborn": {
    "email": "aeryn389@outlook.com",
    "phone": "9568021454"
  },
  "Precinct 31 - Roel Garza-Morales": {
    "email": "roelgarzamorales@gmail.com",
    "phone": "9562155120"
  },
  "Precinct 33 - Concepci\u00f3n Villanueva": {
    "email": "convil1966@yahoo.com",
    "phone": "9563303835"
  },
  "Precinct 34 - Amanda Elise Salas": {
    "email": "amandaelisesalas@gmail.com",
    "phone": "9567399239"
  },
  "Precinct 39 - Imelda Castillo": {
    "email": "imeldacs76@yahoo.com",
    "phone": "9566850351"
  },
  "Precinct 40 - Robert Andrew Garc\u00eda": {
    "email": "Rgarcia547@gmail.com",
    "phone": "9562461338"
  },
  "Precinct 42 - Mario Cano": {
    "email": "1mariocano@gmail.com",
    "phone": "9565328987"
  },
  "Precinct 43 - Mar\u00eda Imelda Arteaga": {
    "email": "Imeldaa57@aol.com",
    "phone": "9564724805"
  },
  "Precinct 44 - Erik Torres": {
    "email": "etorres0622@gmail.com",
    "phone": "9565026150"
  },
  "Precinct 45 - Michael R. L\u00f3pez": {
    "email": "ayjale@gmail.com",
    "phone": "9566848491"
  },
  "Precinct 45 - \u00c1ngel Magallanes": {
    "email": "magallanesangel87@gmail.com",
    "phone": "9563937606"
  },
  "Precinct 48 - Jos\u00e9 B. Salda\u00f1a": {
    "email": "jb.saldana23@gmail.com",
    "phone": "9563316808"
  },
  "Precinct 49 - Manuel Garc\u00eda": {
    "email": "mangaric23@gmail.com",
    "phone": "5129778474"
  },
  "Precinct 50 - Ileana Cant\u00fa Gonz\u00e1lez": {
    "email": "ileana7982@gmail.com",
    "phone": "9568622628"
  },
  "Precinct 52 - Jason Daniel Vallejo": {
    "email": "jasondanielv@gmail.com",
    "phone": "9564545068"
  },
  "Precinct 54 - Regina Compi\u00e1n Richardson": {
    "email": "reginars43@regilaw.com",
    "phone": "9568004805"
  },
  "Precinct 55 - Domingo J. Rivas": {
    "email": "mingos735@yahoo.com",
    "phone": "9563439092"
  },
  "Precinct 59 - Oscar Santa Mar\u00eda": {
    "email": "santamariaoscar40@yahoo.com",
    "phone": "9562789367"
  },
  "Precinct 62 - Luule Moreno": {
    "email": "Luule6@hotmail.com",
    "phone": "9565669121"
  },
  "Precinct 63 - Noemi Ramos Garza": {
    "email": "jabgarza62@aol.com",
    "phone": "9562221051"
  },
  "Precinct 64 - Ang\u00e9lica Patricia Ramos": {
    "email": "gellysenpai@gmail.com",
    "phone": "9566808509"
  },
  "Precinct 87 - Robert Ricardo Maldonado": {
    "email": "robertmaldonado875@gmail.com",
    "phone": "9563521727"
  },
  "Precinct 72 - Mar\u00eda Elena Garc\u00eda": {
    "email": "marygarcia664@icloud.com",
    "phone": "9564530420"
  },
  "Precinct 79 - Abad Morales": {
    "email": "moralesconstruction72@gmail.com",
    "phone": "9566204533"
  },
  "Precinct 80 - Mar\u00eda Edith Lea\u00f1os Rodr\u00edguez": {
    "email": "leanosedith00@gmail.com",
    "phone": "9569468125"
  },
  "Precinct 81 - Chris Eduardo L\u00f3pez": {
    "email": "edsworld956@hotmail.com",
    "phone": "9567892228"
  },
  "Precinct 83 - David Braedon Aguirre": {
    "email": "davidbraedon2005@gmail.com",
    "phone": "9568886848"
  },
  "Precinct 84 - Alma Yadira Butcher": {
    "email": "alma_butcher@yahoo.com",
    "phone": "9568787362"
  },
  "Precinct 88 - Elizabeth Rodr\u00edguez M\u00e1rquez": {
    "email": "elizabethrodriguez.er956@gmail.com",
    "phone": "9565634164"
  },
  "Precinct 93 - Karen Louise Prewitt": {
    "email": "karen.prewitt.71@gmail.com",
    "phone": "9569578095"
  },
  "Precinct 94 - Rosa Mar\u00eda F\u00e9lix": {
    "email": "rosamfelix@yahoo.com",
    "phone": "2109055518"
  },
  "Precinct 95 - Everardo Salda\u00f1a": {
    "email": "sanhas4@yahoo.com",
    "phone": "9567153597"
  },
  "Precinct 96 - Irma Garc\u00eda": {
    "email": "irma.q.garcia@gmail.com",
    "phone": "9562390999"
  },
  "Precinct 99 - Jovanna Hern\u00e1ndez": {
    "email": "jovhdz0142@yahoo.com",
    "phone": "9562400214"
  },
  "Precinct 101 - Marta Garc\u00eda-Rodr\u00edguez": {
    "email": "maratarodz77@gmail.com",
    "phone": "9562225916"
  },
  "Precinct 102 - Mary Solum Hogan": {
    "email": "marysolumhogan@gmail.com",
    "phone": "9563692383"
  },
  "Precinct 105 - Lilia Elise Ram\u00edrez": {
    "email": "liliaeramirez401@gmail.com",
    "phone": "9565308434"
  },
  "Precinct 106 - Ann Varick Millard": {
    "email": "avmillard@gmail.com",
    "phone": "9566480541"
  },
  "Precinct 110 - Jes\u00fas Montalvo": {
    "email": "jessemontalvo8384@gmail.com",
    "phone": "9565326175"
  },
  "Precinct 112 - Betty P\u00e9rez": {
    "email": "bettyperez271@gmail.com",
    "phone": "9562723591"
  },
  "Precinct 113 - Jesse C\u00e1rdenas": {
    "email": "cfsr1990@gmail.com",
    "phone": "9564635907"
  },
  "Precinct 114 - Delma Cadena": {
    "email": "9562618652del@gmail.com",
    "phone": "9562618652"
  },
  "Precinct 116 - Asia Celestia Razo": {
    "email": "asiaamaya46@gmail.com",
    "phone": "9563136673"
  },
  "Precinct 124 - Paul M. Vazald\u00faa": {
    "email": "paulmv555@yahoo.com",
    "phone": "9564516775"
  },
  "Precinct 125 - Mar\u00eda Isabel Perales": {
    "email": "miperales50@yahoo.com",
    "phone": "9565690955"
  },
  "Precinct 126 - Juanita Solis": {
    "email": "jvsolis1@sbcglobal.net",
    "phone": "9567899301"
  },
  "Precinct 127 - Eleazar Escobedo": {
    "email": "eescobedosr54@yahoo.com",
    "phone": "9564387452"
  },
  "Precinct 132 - Nyssa Michelle Cruz": {
    "email": "hcdp132@mail.com",
    "phone": "9567337292"
  },
  "Precinct 136 - Valent\u00edn Victorino Guerra": {
    "email": "valentin.guerra@gmail.com",
    "phone": "4142931195"
  },
  "Precinct 142 - Mar\u00eda A. Recio": {
    "email": "reciomary922@icloud.com",
    "phone": "9566030952"
  },
  "Precinct 145 - Yolanda G. Trevi\u00f1o": {
    "email": "ytrevino4646@yahoo.com",
    "phone": "9564580990"
  },
  "Precinct 146 - Olga Ana Laura Cardoza": {
    "email": "olgalcardoza@gmail.com",
    "phone": "9566558344"
  },
  "Precinct 147 - Diana Laura Morales": {
    "email": "diana.morales91@gmail.com",
    "phone": "9564425357"
  },
  "Precinct 151 - Jos\u00e9 Frank P\u00e9rez": {
    "email": "perezfrank19610@gmail.com",
    "phone": "9564727401"
  },
  "Precinct 153 - Melissa Ch\u00e1vez": {
    "email": "jesmel1974@gmail.com",
    "phone": "9564571719"
  },
  "Precinct 154 - Juan P. Oliv\u00e1n": {
    "email": "jpolivan@sbcglobal.net",
    "phone": "9564577123"
  },
  "Precinct 155 - Norma Vento Reyes": {
    "email": "normavreyes@yahoo.com",
    "phone": "9566840657"
  },
  "Precinct 156 - Ana Paola Garc\u00eda": {
    "email": "aglight234@gmail.com",
    "phone": "9568782716"
  },
  "Precinct 160 - Kenna S Giffin": {
    "email": "ksg210@gmail.com",
    "phone": "9562834669"
  },
  "Precinct 161 - Joe David Garc\u00eda": {
    "email": "apex0378557@gmail.com",
    "phone": "9568008864"
  },
  "Precinct 162 - Prisylla Ann Jasso": {
    "email": "prisylla@etiksolutions.us",
    "phone": "9564676030"
  },
  "Precinct 167 - Clarissa Ram\u00edrez": {
    "email": "msclaramirez@gmail.com",
    "phone": "9565717778"
  },
  "Precinct 169 - Briana Villa": {
    "email": "bri241512@gmail.com",
    "phone": "9564514463"
  },
  "Precinct 174 - Abel Prado": {
    "email": "abeliprado@gmail.com",
    "phone": "9567320525"
  },
  "Precinct 176 - Alberto Rodr\u00edguez": {
    "email": "albert.rodrigueztx@gmail.com",
    "phone": "9563407534"
  },
  "Precinct 177 - Nellie Aide Medina": {
    "email": "nelliemedina0723@gmail.com",
    "phone": "9564604983"
  },
  "Precinct 180 - Gerardo Garc\u00eda": {
    "email": "Jergarcia19@gmail.com",
    "phone": "9566852685"
  },
  "Precinct 183 - Rolando Alvarado": {
    "email": "rolandotransports@gmail.com",
    "phone": "9564781357"
  },
  "Precinct 187 - Arturo Morales": {
    "email": "arturo90976@gmail.com",
    "phone": "3233710829"
  },
  "Precinct 192 - Melisa Zamorano Medina": {
    "email": "melzmed@yahoo.com",
    "phone": "9562791294"
  },
  "Precinct 193 - Michael Alexander Capps": {
    "email": "alexcappstx@gmail.com",
    "phone": "5129661815"
  },
  "Precinct 194 - Emily Jocelyn Rodr\u00edguez": {
    "email": "remily040@gmail.com",
    "phone": "9569004712"
  },
  "Precinct 195 - Kathryn Crystine Harvey": {
    "email": "kathryncharvey@aol.com",
    "phone": "8135233641"
  },
  "Precinct 201 - Jaime Eduardo Gonz\u00e1lez": {
    "email": "jimgonzalez64@yahoo.com",
    "phone": "9565663523"
  },
  "Precinct 207 - Rosendo Villagr\u00e1n": {
    "email": "gene12_2000@yahoo.com",
    "phone": "9565305516"
  },
  "Precinct 211 - Sonya N. Ramsey": {
    "email": "nicknathan@gmail.com",
    "phone": "6145073191"
  },
  "Precinct 216 - Madeleine Christina Croll": {
    "email": "madeleine.croll@gmail.com",
    "phone": "9567096118"
  },
  "Precinct 225 - Elberto Esiquiel Bravo": {
    "email": "elbertobravo3@gmail.com",
    "phone": "9565352822"
  },
  "Precinct 226 - Gustavo Padr\u00f3n Guerra": {
    "email": "gguerravv@gmail.com",
    "phone": "9568218433"
  },
  "Precinct 228 - Irma Cavazos Espinoza": {
    "email": "",
    "phone": "9562075177"
  },
  "Precinct 230 - Jos\u00e9 Robbie Ju\u00e1rez": {
    "email": "jdesign1920@gmail.com",
    "phone": "9563307809"
  },
  "Precinct 234 - Heriberto Rangel": {
    "email": "heriberto.rangel00@gmail.com",
    "phone": "9562491577"
  },
  "Precinct 235 - Angelo Billie Fonseca": {
    "email": "Bfonz33@gmail.com",
    "phone": "9566858920"
  },
  "Precinct 238 - Evelyn Izaguirre": {
    "email": "evelynizaguirre0228@gmail.com",
    "phone": "9563406820"
  },
  "Precinct 239 - Roel Alberto \u00c1vila": {
    "email": "roelavila@sbcglobal.net",
    "phone": "9564938418"
  },
  "Precinct 240 - Eleazar Guajardo": {
    "email": "mr_guajardo@yahoo.com",
    "phone": "9562215245"
  },
  "Precinct 244 - Betty J. (Alaniz) Ram\u00edrez": {
    "email": "bettyjramirezzz@gmail.com",
    "phone": "9563600602"
  },
  "Precinct 245 - Jos\u00e9 Santamar\u00eda": {
    "email": "jsanta_maria@hotmail.com",
    "phone": "9564605380"
  },
  "Precinct 249 - Rolando Max Garza": {
    "email": "rollie1717@yahoo.com",
    "phone": "9567893195"
  },
  "Precinct 250 - Sylvia Sue Handy": {
    "email": "sylviasuehandy@aol.com",
    "phone": "9569988543"
  },
  "Precinct 254 - Jessica Lizbeth S\u00e1nchez": {
    "email": "jessiica.sanchez3@gmail.com",
    "phone": "9563608760"
  },
  "Precinct 257 - Elva Arechiga": {
    "email": "lizzette_arechiga@yahoo.com",
    "phone": "9565800302"
  }
};

function doPost(e) {
  try {
    var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
    
    // Grab the data sent from the website
    var chair = e.parameter.precinct_chair;
    var listType = e.parameter.list_type;
    var timestamp = new Date();
    
    // Secure Lookup!
    var email = "";
    var phone = "";
    if (CHAIR_DATABASE[chair]) {
      email = CHAIR_DATABASE[chair].email;
      phone = CHAIR_DATABASE[chair].phone;
    }
    
    // Drop it into a new row!
    sheet.appendRow([timestamp, chair, email, phone, listType]);
    
    // Tell the website it was successful
    return ContentService.createTextOutput("Success").setMimeType(ContentService.MimeType.TEXT);
    
  } catch (error) {
    return ContentService.createTextOutput("Error: " + error.toString()).setMimeType(ContentService.MimeType.TEXT);
  }
}
