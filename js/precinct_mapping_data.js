const precinctDistricts = [
  {
    "PRECINCT": "0001",
    "CC": "1",
    "HD": "039",
    "SD": "027",
    "CITY": "Mercedes",
    "CD": "15"
  },
  {
    "PRECINCT": "0002",
    "CC": "1",
    "HD": "039",
    "SD": "027",
    "CITY": "Weslaco",
    "CD": "15"
  },
  {
    "PRECINCT": "0003",
    "CC": "1",
    "HD": "039",
    "SD": "027",
    "CITY": "Donna",
    "CD": "15"
  },
  {
    "PRECINCT": "0004",
    "CC": "2",
    "HD": "040",
    "SD": "027",
    "CITY": "San Juan",
    "CD": "15"
  },
  {
    "PRECINCT": "0005",
    "CC": "2",
    "HD": "036",
    "SD": "020",
    "CITY": "Pharr",
    "CD": "15"
  },
  {
    "PRECINCT": "0006",
    "CC": "2",
    "HD": "041",
    "SD": "020",
    "CITY": "Pharr",
    "CD": "15"
  },
  {
    "PRECINCT": "0007",
    "CC": "2",
    "HD": "041",
    "SD": "020",
    "CITY": "San Juan",
    "CD": "28"
  },
  {
    "PRECINCT": "0008",
    "CC": "2",
    "HD": "041",
    "SD": "020",
    "CITY": "Pharr",
    "CD": "15"
  },
  {
    "PRECINCT": "0009",
    "CC": "3",
    "HD": "036",
    "SD": "020",
    "CITY": "Mission",
    "CD": "28"
  },
  {
    "PRECINCT": "0010",
    "CC": "3",
    "HD": "036",
    "SD": "020",
    "CITY": "Mission",
    "CD": "28"
  },
  {
    "PRECINCT": "0011",
    "CC": "3",
    "HD": "035",
    "SD": "020",
    "CITY": "La Joya",
    "CD": "28"
  },
  {
    "PRECINCT": "0012",
    "CC": "3",
    "HD": "036",
    "SD": "020",
    "CITY": "Mission",
    "CD": "15"
  },
  {
    "PRECINCT": "0013",
    "CC": "4",
    "HD": "041",
    "SD": "020",
    "CITY": "Edinburg",
    "CD": "15"
  },
  {
    "PRECINCT": "0014",
    "CC": "4",
    "HD": "040",
    "SD": "020",
    "CITY": "Edinburg",
    "CD": "15"
  },
  {
    "PRECINCT": "0015",
    "CC": "1",
    "HD": "040",
    "SD": "027",
    "CITY": "Monte Alto",
    "CD": "15"
  },
  {
    "PRECINCT": "0016",
    "CC": "1",
    "HD": "035",
    "SD": "027",
    "CITY": "Edcouch",
    "CD": "15"
  },
  {
    "PRECINCT": "0017",
    "CC": "1",
    "HD": "035",
    "SD": "027",
    "CITY": "La Villa",
    "CD": "15"
  },
  {
    "PRECINCT": "0018",
    "CC": "1",
    "HD": "035",
    "SD": "027",
    "CITY": "Hargill",
    "CD": "15"
  },
  {
    "PRECINCT": "0019",
    "CC": "4",
    "HD": "035",
    "SD": "020",
    "CITY": "Linn",
    "CD": "15"
  },
  {
    "PRECINCT": "0020",
    "CC": "2",
    "HD": "036",
    "SD": "020",
    "CITY": "McAllen",
    "CD": "15"
  },
  {
    "PRECINCT": "0021",
    "CC": "1",
    "HD": "039",
    "SD": "027",
    "CITY": "Weslaco",
    "CD": "15"
  },
  {
    "PRECINCT": "0022",
    "CC": "1",
    "HD": "039",
    "SD": "027",
    "CITY": "Weslaco",
    "CD": "15"
  },
  {
    "PRECINCT": "0023",
    "CC": "1",
    "HD": "039",
    "SD": "027",
    "CITY": "Donna",
    "CD": "15"
  },
  {
    "PRECINCT": "0024",
    "CC": "3",
    "HD": "035",
    "SD": "020",
    "CITY": "Linn",
    "CD": "15"
  },
  {
    "PRECINCT": "0025",
    "CC": "2",
    "HD": "036",
    "SD": "020",
    "CITY": "Pharr",
    "CD": "15"
  },
  {
    "PRECINCT": "0026",
    "CC": "2",
    "HD": "041",
    "SD": "020",
    "CITY": "McAllen",
    "CD": "28"
  },
  {
    "PRECINCT": "0027",
    "CC": "2",
    "HD": "041",
    "SD": "020",
    "CITY": "McAllen",
    "CD": "28"
  },
  {
    "PRECINCT": "0028",
    "CC": "3",
    "HD": "036",
    "SD": "020",
    "CITY": "Mission",
    "CD": "28"
  },
  {
    "PRECINCT": "0029",
    "CC": "3",
    "HD": "036",
    "SD": "020",
    "CITY": "Palmview",
    "CD": "28"
  },
  {
    "PRECINCT": "0030",
    "CC": "4",
    "HD": "040",
    "SD": "020",
    "CITY": "Edinburg",
    "CD": "15"
  },
  {
    "PRECINCT": "0031",
    "CC": "4",
    "HD": "040",
    "SD": "020",
    "CITY": "Edinburg",
    "CD": "15"
  },
  {
    "PRECINCT": "0032",
    "CC": "1",
    "HD": "039",
    "SD": "027",
    "CITY": "Mercedes",
    "CD": "15"
  },
  {
    "PRECINCT": "0033",
    "CC": "1",
    "HD": "035",
    "SD": "027",
    "CITY": "Monte Alto",
    "CD": "15"
  },
  {
    "PRECINCT": "0034",
    "CC": "2",
    "HD": "041",
    "SD": "020",
    "CITY": "McAllen",
    "CD": "28"
  },
  {
    "PRECINCT": "0035",
    "CC": "2",
    "HD": "040",
    "SD": "020",
    "CITY": "Pharr",
    "CD": "28"
  },
  {
    "PRECINCT": "0036",
    "CC": "2",
    "HD": "036",
    "SD": "020",
    "CITY": "Pharr",
    "CD": "28"
  },
  {
    "PRECINCT": "0037",
    "CC": "2",
    "HD": "041",
    "SD": "020",
    "CITY": "McAllen",
    "CD": "28"
  },
  {
    "PRECINCT": "0038",
    "CC": "3",
    "HD": "041",
    "SD": "020",
    "CITY": "Mission",
    "CD": "28"
  },
  {
    "PRECINCT": "0039",
    "CC": "2",
    "HD": "039",
    "SD": "027",
    "CITY": "San Juan",
    "CD": "15"
  },
  {
    "PRECINCT": "0040",
    "CC": "1",
    "HD": "039",
    "SD": "027",
    "CITY": "Weslaco",
    "CD": "15"
  },
  {
    "PRECINCT": "0041",
    "CC": "1",
    "HD": "039",
    "SD": "027",
    "CITY": "Weslaco",
    "CD": "15"
  },
  {
    "PRECINCT": "0042",
    "CC": "1",
    "HD": "039",
    "SD": "027",
    "CITY": "Weslaco",
    "CD": "15"
  },
  {
    "PRECINCT": "0043",
    "CC": "4",
    "HD": "040",
    "SD": "027",
    "CITY": "Edinburg",
    "CD": "15"
  },
  {
    "PRECINCT": "0044",
    "CC": "1",
    "HD": "039",
    "SD": "027",
    "CITY": "Edinburg",
    "CD": "15"
  },
  {
    "PRECINCT": "0045",
    "CC": "1",
    "HD": "039",
    "SD": "027",
    "CITY": "Donna",
    "CD": "15"
  },
  {
    "PRECINCT": "0046",
    "CC": "1",
    "HD": "039",
    "SD": "027",
    "CITY": "Weslaco",
    "CD": "15"
  },
  {
    "PRECINCT": "0047",
    "CC": "2",
    "HD": "041",
    "SD": "020",
    "CITY": "McAllen",
    "CD": "28"
  },
  {
    "PRECINCT": "0048",
    "CC": "2",
    "HD": "036",
    "SD": "020",
    "CITY": "McAllen",
    "CD": "28"
  },
  {
    "PRECINCT": "0049",
    "CC": "2",
    "HD": "041",
    "SD": "020",
    "CITY": "McAllen",
    "CD": "28"
  },
  {
    "PRECINCT": "0050",
    "CC": "3",
    "HD": "035",
    "SD": "020",
    "CITY": "Penitas",
    "CD": "28"
  },
  {
    "PRECINCT": "0051",
    "CC": "3",
    "HD": "035",
    "SD": "020",
    "CITY": "Sullivan City",
    "CD": "28"
  },
  {
    "PRECINCT": "0052",
    "CC": "4",
    "HD": "040",
    "SD": "020",
    "CITY": "Edinburg",
    "CD": "15"
  },
  {
    "PRECINCT": "0053",
    "CC": "4",
    "HD": "040",
    "SD": "020",
    "CITY": "Edinburg",
    "CD": "15"
  },
  {
    "PRECINCT": "0054",
    "CC": "4",
    "HD": "041",
    "SD": "020",
    "CITY": "McAllen",
    "CD": "15"
  },
  {
    "PRECINCT": "0055",
    "CC": "1",
    "HD": "039",
    "SD": "027",
    "CITY": "Donna",
    "CD": "15"
  },
  {
    "PRECINCT": "0056",
    "CC": "1",
    "HD": "039",
    "SD": "027",
    "CITY": "Mercedes",
    "CD": "15"
  },
  {
    "PRECINCT": "0057",
    "CC": "1",
    "HD": "039",
    "SD": "027",
    "CITY": "Weslaco",
    "CD": "15"
  },
  {
    "PRECINCT": "0058",
    "CC": "1",
    "HD": "039",
    "SD": "027",
    "CITY": "Weslaco",
    "CD": "15"
  },
  {
    "PRECINCT": "0059",
    "CC": "2",
    "HD": "040",
    "SD": "027",
    "CITY": "San Juan",
    "CD": "15"
  },
  {
    "PRECINCT": "0060",
    "CC": "2",
    "HD": "041",
    "SD": "020",
    "CITY": "Pharr",
    "CD": "15"
  },
  {
    "PRECINCT": "0061",
    "CC": "2",
    "HD": "040",
    "SD": "020",
    "CITY": "Pharr",
    "CD": "28"
  },
  {
    "PRECINCT": "0062",
    "CC": "4",
    "HD": "041",
    "SD": "020",
    "CITY": "McAllen",
    "CD": "15"
  },
  {
    "PRECINCT": "0063",
    "CC": "3",
    "HD": "036",
    "SD": "020",
    "CITY": "Mission",
    "CD": "28"
  },
  {
    "PRECINCT": "0064",
    "CC": "3",
    "HD": "035",
    "SD": "020",
    "CITY": "Mission",
    "CD": "28"
  },
  {
    "PRECINCT": "0065",
    "CC": "4",
    "HD": "041",
    "SD": "020",
    "CITY": "McAllen",
    "CD": "15"
  },
  {
    "PRECINCT": "0066",
    "CC": "2",
    "HD": "041",
    "SD": "020",
    "CITY": "McAllen",
    "CD": "28"
  },
  {
    "PRECINCT": "0067",
    "CC": "4",
    "HD": "041",
    "SD": "020",
    "CITY": "McAllen",
    "CD": "28"
  },
  {
    "PRECINCT": "0068",
    "CC": "4",
    "HD": "040",
    "SD": "020",
    "CITY": "Edinburg",
    "CD": "15"
  },
  {
    "PRECINCT": "0069",
    "CC": "4",
    "HD": "040",
    "SD": "020",
    "CITY": "Edinburg",
    "CD": "15"
  },
  {
    "PRECINCT": "0070",
    "CC": "1",
    "HD": "035",
    "SD": "027",
    "CITY": "Weslaco",
    "CD": "15"
  },
  {
    "PRECINCT": "0071",
    "CC": "1",
    "HD": "039",
    "SD": "027",
    "CITY": "Weslaco",
    "CD": "15"
  },
  {
    "PRECINCT": "0072",
    "CC": "4",
    "HD": "041",
    "SD": "020",
    "CITY": "McAllen",
    "CD": "15"
  },
  {
    "PRECINCT": "0073",
    "CC": "4",
    "HD": "041",
    "SD": "020",
    "CITY": "McAllen",
    "CD": "15"
  },
  {
    "PRECINCT": "0074",
    "CC": "4",
    "HD": "041",
    "SD": "020",
    "CITY": "McAllen",
    "CD": "15"
  },
  {
    "PRECINCT": "0075",
    "CC": "3",
    "HD": "035",
    "SD": "020",
    "CITY": "Edinburg",
    "CD": "15"
  },
  {
    "PRECINCT": "0076",
    "CC": "3",
    "HD": "035",
    "SD": "020",
    "CITY": "Edinburg",
    "CD": "34"
  },
  {
    "PRECINCT": "0077",
    "CC": "1",
    "HD": "039",
    "SD": "027",
    "CITY": "Alamo",
    "CD": "15"
  },
  {
    "PRECINCT": "0078",
    "CC": "3",
    "HD": "036",
    "SD": "020",
    "CITY": "Palmview",
    "CD": "28"
  },
  {
    "PRECINCT": "0079",
    "CC": "1",
    "HD": "035",
    "SD": "027",
    "CITY": "Weslaco",
    "CD": "15"
  },
  {
    "PRECINCT": "0080",
    "CC": "3",
    "HD": "035",
    "SD": "020",
    "CITY": "Sullivan City",
    "CD": "28"
  },
  {
    "PRECINCT": "0081",
    "CC": "4",
    "HD": "041",
    "SD": "020",
    "CITY": "McAllen",
    "CD": "15"
  },
  {
    "PRECINCT": "0082",
    "CC": "3",
    "HD": "036",
    "SD": "020",
    "CITY": "Mission",
    "CD": "28"
  },
  {
    "PRECINCT": "0083",
    "CC": "3",
    "HD": "041",
    "SD": "020",
    "CITY": "Mission",
    "CD": "28"
  },
  {
    "PRECINCT": "0084",
    "CC": "4",
    "HD": "041",
    "SD": "020",
    "CITY": "McAllen",
    "CD": "28"
  },
  {
    "PRECINCT": "0085",
    "CC": "1",
    "HD": "039",
    "SD": "027",
    "CITY": "Mercedes",
    "CD": "15"
  },
  {
    "PRECINCT": "0086",
    "CC": "3",
    "HD": "036",
    "SD": "020",
    "CITY": "Palmhurst",
    "CD": "28"
  },
  {
    "PRECINCT": "0087",
    "CC": "1",
    "HD": "035",
    "SD": "027",
    "CITY": "Edinburg",
    "CD": "15"
  },
  {
    "PRECINCT": "0088",
    "CC": "3",
    "HD": "036",
    "SD": "020",
    "CITY": "San Juan",
    "CD": "28"
  },
  {
    "PRECINCT": "0089",
    "CC": "3",
    "HD": "040",
    "SD": "020",
    "CITY": "Mission",
    "CD": "28"
  },
  {
    "PRECINCT": "0090",
    "CC": "1",
    "HD": "040",
    "SD": "027",
    "CITY": "Elsa",
    "CD": "15"
  },
  {
    "PRECINCT": "0091",
    "CC": "1",
    "HD": "039",
    "SD": "027",
    "CITY": "Alamo",
    "CD": "15"
  },
  {
    "PRECINCT": "0092",
    "CC": "4",
    "HD": "035",
    "SD": "027",
    "CITY": "Monte Alto",
    "CD": "15"
  },
  {
    "PRECINCT": "0093",
    "CC": "3",
    "HD": "036",
    "SD": "020",
    "CITY": "Mission",
    "CD": "28"
  },
  {
    "PRECINCT": "0094",
    "CC": "3",
    "HD": "036",
    "SD": "020",
    "CITY": "Mission",
    "CD": "28"
  },
  {
    "PRECINCT": "0095",
    "CC": "2",
    "HD": "036",
    "SD": "020",
    "CITY": "McAllen",
    "CD": "28"
  },
  {
    "PRECINCT": "0096",
    "CC": "4",
    "HD": "041",
    "SD": "020",
    "CITY": "McAllen",
    "CD": "15"
  },
  {
    "PRECINCT": "0097",
    "CC": "2",
    "HD": "041",
    "SD": "020",
    "CITY": "McAllen",
    "CD": "28"
  },
  {
    "PRECINCT": "0098",
    "CC": "3",
    "HD": "036",
    "SD": "020",
    "CITY": "Palmview",
    "CD": "28"
  },
  {
    "PRECINCT": "0099",
    "CC": "3",
    "HD": "036",
    "SD": "020",
    "CITY": "Mission",
    "CD": "28"
  },
  {
    "PRECINCT": "0100",
    "CC": "3",
    "HD": "036",
    "SD": "020",
    "CITY": "Palmview",
    "CD": "28"
  },
  {
    "PRECINCT": "0101",
    "CC": "3",
    "HD": "035",
    "SD": "020",
    "CITY": "Palmhurst",
    "CD": "28"
  },
  {
    "PRECINCT": "0102",
    "CC": "3",
    "HD": "036",
    "SD": "020",
    "CITY": "Mission",
    "CD": "28"
  },
  {
    "PRECINCT": "0103",
    "CC": "3",
    "HD": "036",
    "SD": "020",
    "CITY": "Mission",
    "CD": "28"
  },
  {
    "PRECINCT": "0104",
    "CC": "4",
    "HD": "040",
    "SD": "027",
    "CITY": "Monte Alto",
    "CD": "15"
  },
  {
    "PRECINCT": "0105",
    "CC": "4",
    "HD": "041",
    "SD": "020",
    "CITY": "McAllen",
    "CD": "15"
  },
  {
    "PRECINCT": "0106",
    "CC": "4",
    "HD": "040",
    "SD": "020",
    "CITY": "Edinburg",
    "CD": "15"
  },
  {
    "PRECINCT": "0107",
    "CC": "4",
    "HD": "041",
    "SD": "020",
    "CITY": "Edinburg",
    "CD": "15"
  },
  {
    "PRECINCT": "0108",
    "CC": "4",
    "HD": "040",
    "SD": "020",
    "CITY": "Edinburg",
    "CD": "15"
  },
  {
    "PRECINCT": "0109",
    "CC": "4",
    "HD": "040",
    "SD": "020",
    "CITY": "Edinburg",
    "CD": "15"
  },
  {
    "PRECINCT": "0110",
    "CC": "1",
    "HD": "039",
    "SD": "027",
    "CITY": "Weslaco",
    "CD": "15"
  },
  {
    "PRECINCT": "0111",
    "CC": "1",
    "HD": "039",
    "SD": "027",
    "CITY": "Weslaco",
    "CD": "15"
  },
  {
    "PRECINCT": "0112",
    "CC": "1",
    "HD": "039",
    "SD": "027",
    "CITY": "Weslaco",
    "CD": "15"
  },
  {
    "PRECINCT": "0113",
    "CC": "1",
    "HD": "039",
    "SD": "027",
    "CITY": "Weslaco",
    "CD": "15"
  },
  {
    "PRECINCT": "0114",
    "CC": "1",
    "HD": "039",
    "SD": "027",
    "CITY": "Weslaco",
    "CD": "15"
  },
  {
    "PRECINCT": "0115",
    "CC": "2",
    "HD": "040",
    "SD": "020",
    "CITY": "Pharr",
    "CD": "28"
  },
  {
    "PRECINCT": "0116",
    "CC": "2",
    "HD": "041",
    "SD": "020",
    "CITY": "Pharr",
    "CD": "15"
  },
  {
    "PRECINCT": "0117",
    "CC": "2",
    "HD": "039",
    "SD": "027",
    "CITY": "San Juan",
    "CD": "15"
  },
  {
    "PRECINCT": "0118",
    "CC": "2",
    "HD": "039",
    "SD": "027",
    "CITY": "San Juan",
    "CD": "15"
  },
  {
    "PRECINCT": "0119",
    "CC": "1",
    "HD": "040",
    "SD": "027",
    "CITY": "Weslaco",
    "CD": "15"
  },
  {
    "PRECINCT": "0120",
    "CC": "1",
    "HD": "039",
    "SD": "027",
    "CITY": "Donna",
    "CD": "15"
  },
  {
    "PRECINCT": "0121",
    "CC": "1",
    "HD": "039",
    "SD": "027",
    "CITY": "Weslaco",
    "CD": "15"
  },
  {
    "PRECINCT": "0122",
    "CC": "2",
    "HD": "036",
    "SD": "020",
    "CITY": "Pharr",
    "CD": "15"
  },
  {
    "PRECINCT": "0123",
    "CC": "1",
    "HD": "039",
    "SD": "027",
    "CITY": "Alamo",
    "CD": "15"
  },
  {
    "PRECINCT": "0124",
    "CC": "4",
    "HD": "041",
    "SD": "020",
    "CITY": "McAllen",
    "CD": "28"
  },
  {
    "PRECINCT": "0125",
    "CC": "3",
    "HD": "035",
    "SD": "020",
    "CITY": "Mission",
    "CD": "28"
  },
  {
    "PRECINCT": "0126",
    "CC": "1",
    "HD": "039",
    "SD": "027",
    "CITY": "Alamo",
    "CD": "15"
  },
  {
    "PRECINCT": "0127",
    "CC": "1",
    "HD": "039",
    "SD": "027",
    "CITY": "Alamo",
    "CD": "15"
  },
  {
    "PRECINCT": "0128",
    "CC": "3",
    "HD": "036",
    "SD": "020",
    "CITY": "Palmview",
    "CD": "28"
  },
  {
    "PRECINCT": "0129",
    "CC": "4",
    "HD": "041",
    "SD": "020",
    "CITY": "McAllen",
    "CD": "15"
  },
  {
    "PRECINCT": "0130",
    "CC": "2",
    "HD": "039",
    "SD": "027",
    "CITY": "Alamo",
    "CD": "15"
  },
  {
    "PRECINCT": "0131",
    "CC": "3",
    "HD": "035",
    "SD": "020",
    "CITY": "Sullivan City",
    "CD": "28"
  },
  {
    "PRECINCT": "0132",
    "CC": "1",
    "HD": "039",
    "SD": "027",
    "CITY": "Weslaco",
    "CD": "15"
  },
  {
    "PRECINCT": "0133",
    "CC": "3",
    "HD": "035",
    "SD": "020",
    "CITY": "Mission",
    "CD": "28"
  },
  {
    "PRECINCT": "0134",
    "CC": "4",
    "HD": "041",
    "SD": "020",
    "CITY": "McAllen",
    "CD": "15"
  },
  {
    "PRECINCT": "0135",
    "CC": "2",
    "HD": "041",
    "SD": "020",
    "CITY": "McAllen",
    "CD": "28"
  },
  {
    "PRECINCT": "0136",
    "CC": "2",
    "HD": "041",
    "SD": "020",
    "CITY": "McAllen",
    "CD": "28"
  },
  {
    "PRECINCT": "0137",
    "CC": "2",
    "HD": "039",
    "SD": "027",
    "CITY": "San Juan",
    "CD": "15"
  },
  {
    "PRECINCT": "0138",
    "CC": "2",
    "HD": "041",
    "SD": "020",
    "CITY": "McAllen",
    "CD": "28"
  },
  {
    "PRECINCT": "0139",
    "CC": "2",
    "HD": "041",
    "SD": "020",
    "CITY": "McAllen",
    "CD": "28"
  },
  {
    "PRECINCT": "0140",
    "CC": "2",
    "HD": "041",
    "SD": "020",
    "CITY": "McAllen",
    "CD": "15"
  },
  {
    "PRECINCT": "0141",
    "CC": "2",
    "HD": "041",
    "SD": "020",
    "CITY": "McAllen",
    "CD": "28"
  },
  {
    "PRECINCT": "0142",
    "CC": "4",
    "HD": "040",
    "SD": "027",
    "CITY": "La Blanca",
    "CD": "15"
  },
  {
    "PRECINCT": "0143",
    "CC": "4",
    "HD": "040",
    "SD": "020",
    "CITY": "Edinburg",
    "CD": "15"
  },
  {
    "PRECINCT": "0144",
    "CC": "2",
    "HD": "041",
    "SD": "027",
    "CITY": "Pharr",
    "CD": "15"
  },
  {
    "PRECINCT": "0145",
    "CC": "3",
    "HD": "035",
    "SD": "020",
    "CITY": "Palmview",
    "CD": "28"
  },
  {
    "PRECINCT": "0146",
    "CC": "2",
    "HD": "036",
    "SD": "020",
    "CITY": "Pharr",
    "CD": "15"
  },
  {
    "PRECINCT": "0147",
    "CC": "2",
    "HD": "036",
    "SD": "020",
    "CITY": "Pharr",
    "CD": "15"
  },
  {
    "PRECINCT": "0148",
    "CC": "2",
    "HD": "041",
    "SD": "020",
    "CITY": "McAllen",
    "CD": "28"
  },
  {
    "PRECINCT": "0149",
    "CC": "2",
    "HD": "036",
    "SD": "020",
    "CITY": "McAllen",
    "CD": "28"
  },
  {
    "PRECINCT": "0150",
    "CC": "2",
    "HD": "041",
    "SD": "020",
    "CITY": "McAllen",
    "CD": "15"
  },
  {
    "PRECINCT": "0151",
    "CC": "4",
    "HD": "040",
    "SD": "020",
    "CITY": "Edinburg",
    "CD": "15"
  },
  {
    "PRECINCT": "0152",
    "CC": "4",
    "HD": "040",
    "SD": "020",
    "CITY": "Edinburg",
    "CD": "15"
  },
  {
    "PRECINCT": "0153",
    "CC": "1",
    "HD": "040",
    "SD": "027",
    "CITY": "Monte Alto",
    "CD": "15"
  },
  {
    "PRECINCT": "0154",
    "CC": "4",
    "HD": "040",
    "SD": "020",
    "CITY": "Edinburg",
    "CD": "15"
  },
  {
    "PRECINCT": "0155",
    "CC": "1",
    "HD": "039",
    "SD": "027",
    "CITY": "Mercedes",
    "CD": "15"
  },
  {
    "PRECINCT": "0156",
    "CC": "2",
    "HD": "040",
    "SD": "027",
    "CITY": "San Juan",
    "CD": "15"
  },
  {
    "PRECINCT": "0157",
    "CC": "1",
    "HD": "039",
    "SD": "027",
    "CITY": "Weslaco",
    "CD": "15"
  },
  {
    "PRECINCT": "0158",
    "CC": "4",
    "HD": "040",
    "SD": "020",
    "CITY": "San Juan",
    "CD": "15"
  },
  {
    "PRECINCT": "0159",
    "CC": "2",
    "HD": "040",
    "SD": "020",
    "CITY": "San Juan",
    "CD": "15"
  },
  {
    "PRECINCT": "0160",
    "CC": "2",
    "HD": "041",
    "SD": "020",
    "CITY": "McAllen",
    "CD": "15"
  },
  {
    "PRECINCT": "0161",
    "CC": "4",
    "HD": "041",
    "SD": "020",
    "CITY": "McAllen",
    "CD": "28"
  },
  {
    "PRECINCT": "0162",
    "CC": "4",
    "HD": "041",
    "SD": "020",
    "CITY": "McAllen",
    "CD": "15"
  },
  {
    "PRECINCT": "0163",
    "CC": "1",
    "HD": "035",
    "SD": "027",
    "CITY": "Donna",
    "CD": "15"
  },
  {
    "PRECINCT": "0164",
    "CC": "2",
    "HD": "041",
    "SD": "020",
    "CITY": "McAllen",
    "CD": "28"
  },
  {
    "PRECINCT": "0165",
    "CC": "3",
    "HD": "035",
    "SD": "020",
    "CITY": "Mission",
    "CD": "28"
  },
  {
    "PRECINCT": "0166",
    "CC": "4",
    "HD": "041",
    "SD": "020",
    "CITY": "McAllen",
    "CD": "15"
  },
  {
    "PRECINCT": "0167",
    "CC": "4",
    "HD": "041",
    "SD": "020",
    "CITY": "McAllen",
    "CD": "15"
  },
  {
    "PRECINCT": "0168",
    "CC": "2",
    "HD": "040",
    "SD": "020",
    "CITY": "Pharr",
    "CD": "28"
  },
  {
    "PRECINCT": "0169",
    "CC": "1",
    "HD": "035",
    "SD": "027",
    "CITY": "Mercedes",
    "CD": "15"
  },
  {
    "PRECINCT": "0170",
    "CC": "3",
    "HD": "036",
    "SD": "020",
    "CITY": "Palmview",
    "CD": "28"
  },
  {
    "PRECINCT": "0171",
    "CC": "1",
    "HD": "039",
    "SD": "027",
    "CITY": "Donna",
    "CD": "28"
  },
  {
    "PRECINCT": "0172",
    "CC": "2",
    "HD": "039",
    "SD": "027",
    "CITY": "Donna",
    "CD": "15"
  },
  {
    "PRECINCT": "0173",
    "CC": "1",
    "HD": "039",
    "SD": "027",
    "CITY": "Donna",
    "CD": "15"
  },
  {
    "PRECINCT": "0174",
    "CC": "1",
    "HD": "039",
    "SD": "027",
    "CITY": "Donna",
    "CD": "15"
  },
  {
    "PRECINCT": "0175",
    "CC": "1",
    "HD": "039",
    "SD": "027",
    "CITY": "Donna",
    "CD": "15"
  },
  {
    "PRECINCT": "0176",
    "CC": "1",
    "HD": "039",
    "SD": "027",
    "CITY": "Alamo",
    "CD": "15"
  },
  {
    "PRECINCT": "0177",
    "CC": "2",
    "HD": "039",
    "SD": "027",
    "CITY": "San Juan",
    "CD": "15"
  },
  {
    "PRECINCT": "0178",
    "CC": "2",
    "HD": "039",
    "SD": "027",
    "CITY": "San Juan",
    "CD": "28"
  },
  {
    "PRECINCT": "0179",
    "CC": "1",
    "HD": "035",
    "SD": "027",
    "CITY": "Weslaco",
    "CD": "15"
  },
  {
    "PRECINCT": "0180",
    "CC": "1",
    "HD": "035",
    "SD": "027",
    "CITY": "Monte Alto",
    "CD": "15"
  },
  {
    "PRECINCT": "0181",
    "CC": "1",
    "HD": "039",
    "SD": "027",
    "CITY": "Alamo",
    "CD": "15"
  },
  {
    "PRECINCT": "0182",
    "CC": "3",
    "HD": "035",
    "SD": "020",
    "CITY": "Penitas",
    "CD": "28"
  },
  {
    "PRECINCT": "0183",
    "CC": "3",
    "HD": "036",
    "SD": "020",
    "CITY": "Palmhurst",
    "CD": "28"
  },
  {
    "PRECINCT": "0184",
    "CC": "1",
    "HD": "035",
    "SD": "027",
    "CITY": "Monte Alto",
    "CD": "15"
  },
  {
    "PRECINCT": "0186",
    "CC": "1",
    "HD": "039",
    "SD": "027",
    "CITY": "Weslaco",
    "CD": "15"
  },
  {
    "PRECINCT": "0187",
    "CC": "3",
    "HD": "036",
    "SD": "020",
    "CITY": "Palmview",
    "CD": "28"
  },
  {
    "PRECINCT": "0188",
    "CC": "3",
    "HD": "041",
    "SD": "020",
    "CITY": "Mission",
    "CD": "28"
  },
  {
    "PRECINCT": "0189",
    "CC": "4",
    "HD": "039",
    "SD": "027",
    "CITY": "Edinburg",
    "CD": "15"
  },
  {
    "PRECINCT": "0190",
    "CC": "1",
    "HD": "039",
    "SD": "027",
    "CITY": "Weslaco",
    "CD": "15"
  },
  {
    "PRECINCT": "0191",
    "CC": "1",
    "HD": "039",
    "SD": "027",
    "CITY": "Weslaco",
    "CD": "15"
  },
  {
    "PRECINCT": "0192",
    "CC": "1",
    "HD": "039",
    "SD": "027",
    "CITY": "Alamo",
    "CD": "15"
  },
  {
    "PRECINCT": "0193",
    "CC": "2",
    "HD": "036",
    "SD": "020",
    "CITY": "McAllen",
    "CD": "28"
  },
  {
    "PRECINCT": "0194",
    "CC": "3",
    "HD": "036",
    "SD": "020",
    "CITY": "Palmview",
    "CD": "28"
  },
  {
    "PRECINCT": "0195",
    "CC": "3",
    "HD": "035",
    "SD": "020",
    "CITY": "Penitas",
    "CD": "28"
  },
  {
    "PRECINCT": "0196",
    "CC": "1",
    "HD": "039",
    "SD": "027",
    "CITY": "Weslaco",
    "CD": "15"
  },
  {
    "PRECINCT": "0197",
    "CC": "3",
    "HD": "035",
    "SD": "020",
    "CITY": "Penitas",
    "CD": "28"
  },
  {
    "PRECINCT": "0198",
    "CC": "3",
    "HD": "035",
    "SD": "020",
    "CITY": "La Joya",
    "CD": "28"
  },
  {
    "PRECINCT": "0199",
    "CC": "4",
    "HD": "041",
    "SD": "020",
    "CITY": "McAllen",
    "CD": "15"
  },
  {
    "PRECINCT": "0200",
    "CC": "4",
    "HD": "041",
    "SD": "020",
    "CITY": "McAllen",
    "CD": "15"
  },
  {
    "PRECINCT": "0201",
    "CC": "4",
    "HD": "041",
    "SD": "020",
    "CITY": "Edinburg",
    "CD": "15"
  },
  {
    "PRECINCT": "0202",
    "CC": "1",
    "HD": "039",
    "SD": "027",
    "CITY": "Mercedes",
    "CD": "15"
  },
  {
    "PRECINCT": "0203",
    "CC": "3",
    "HD": "036",
    "SD": "020",
    "CITY": "Mission",
    "CD": "28"
  },
  {
    "PRECINCT": "0204",
    "CC": "3",
    "HD": "036",
    "SD": "020",
    "CITY": "Mission",
    "CD": "28"
  },
  {
    "PRECINCT": "0205",
    "CC": "3",
    "HD": "036",
    "SD": "020",
    "CITY": "Palmhurst",
    "CD": "28"
  },
  {
    "PRECINCT": "0206",
    "CC": "4",
    "HD": "041",
    "SD": "020",
    "CITY": "McAllen",
    "CD": "15"
  },
  {
    "PRECINCT": "0207",
    "CC": "4",
    "HD": "041",
    "SD": "020",
    "CITY": "McAllen",
    "CD": "15"
  },
  {
    "PRECINCT": "0208",
    "CC": "2",
    "HD": "036",
    "SD": "020",
    "CITY": "Pharr",
    "CD": "28"
  },
  {
    "PRECINCT": "0209",
    "CC": "3",
    "HD": "035",
    "SD": "020",
    "CITY": "Palmview",
    "CD": "28"
  },
  {
    "PRECINCT": "0210",
    "CC": "3",
    "HD": "036",
    "SD": "020",
    "CITY": "Palmview",
    "CD": "28"
  },
  {
    "PRECINCT": "0211",
    "CC": "3",
    "HD": "041",
    "SD": "020",
    "CITY": "Mission",
    "CD": "28"
  },
  {
    "PRECINCT": "0212",
    "CC": "3",
    "HD": "035",
    "SD": "020",
    "CITY": "Mission",
    "CD": "28"
  },
  {
    "PRECINCT": "0213",
    "CC": "1",
    "HD": "039",
    "SD": "027",
    "CITY": "Mercedes",
    "CD": "15"
  },
  {
    "PRECINCT": "0214",
    "CC": "2",
    "HD": "040",
    "SD": "027",
    "CITY": "San Juan",
    "CD": "15"
  },
  {
    "PRECINCT": "0215",
    "CC": "2",
    "HD": "036",
    "SD": "020",
    "CITY": "Mission",
    "CD": "28"
  },
  {
    "PRECINCT": "0216",
    "CC": "2",
    "HD": "041",
    "SD": "020",
    "CITY": "McAllen",
    "CD": "28"
  },
  {
    "PRECINCT": "0217",
    "CC": "3",
    "HD": "035",
    "SD": "020",
    "CITY": "Mission",
    "CD": "28"
  },
  {
    "PRECINCT": "0218",
    "CC": "3",
    "HD": "036",
    "SD": "020",
    "CITY": "Palmhurst",
    "CD": "28"
  },
  {
    "PRECINCT": "0219",
    "CC": "3",
    "HD": "036",
    "SD": "020",
    "CITY": "Mission",
    "CD": "28"
  },
  {
    "PRECINCT": "0220",
    "CC": "3",
    "HD": "036",
    "SD": "020",
    "CITY": "Palmhurst",
    "CD": "28"
  },
  {
    "PRECINCT": "0221",
    "CC": "4",
    "HD": "041",
    "SD": "020",
    "CITY": "McAllen",
    "CD": "15"
  },
  {
    "PRECINCT": "0222",
    "CC": "4",
    "HD": "041",
    "SD": "020",
    "CITY": "McAllen",
    "CD": "15"
  },
  {
    "PRECINCT": "0223",
    "CC": "4",
    "HD": "041",
    "SD": "020",
    "CITY": "McAllen",
    "CD": "15"
  },
  {
    "PRECINCT": "0224",
    "CC": "4",
    "HD": "041",
    "SD": "020",
    "CITY": "Edinburg",
    "CD": "15"
  },
  {
    "PRECINCT": "0225",
    "CC": "1",
    "HD": "040",
    "SD": "027",
    "CITY": "Weslaco",
    "CD": "15"
  },
  {
    "PRECINCT": "0226",
    "CC": "2",
    "HD": "036",
    "SD": "020",
    "CITY": "Pharr",
    "CD": "15"
  },
  {
    "PRECINCT": "0227",
    "CC": "2",
    "HD": "036",
    "SD": "020",
    "CITY": "Pharr",
    "CD": "15"
  },
  {
    "PRECINCT": "0228",
    "CC": "2",
    "HD": "039",
    "SD": "027",
    "CITY": "San Juan",
    "CD": "15"
  },
  {
    "PRECINCT": "0229",
    "CC": "2",
    "HD": "039",
    "SD": "027",
    "CITY": "Alamo",
    "CD": "15"
  },
  {
    "PRECINCT": "0230",
    "CC": "4",
    "HD": "040",
    "SD": "020",
    "CITY": "Mission",
    "CD": "15"
  },
  {
    "PRECINCT": "0231",
    "CC": "2",
    "HD": "041",
    "SD": "020",
    "CITY": "McAllen",
    "CD": "28"
  },
  {
    "PRECINCT": "0232",
    "CC": "1",
    "HD": "039",
    "SD": "027",
    "CITY": "Weslaco",
    "CD": "15"
  },
  {
    "PRECINCT": "0233",
    "CC": "2",
    "HD": "036",
    "SD": "020",
    "CITY": "McAllen",
    "CD": "28"
  },
  {
    "PRECINCT": "0234",
    "CC": "2",
    "HD": "036",
    "SD": "020",
    "CITY": "McAllen",
    "CD": "15"
  },
  {
    "PRECINCT": "0235",
    "CC": "1",
    "HD": "039",
    "SD": "027",
    "CITY": "Weslaco",
    "CD": "15"
  },
  {
    "PRECINCT": "0236",
    "CC": "3",
    "HD": "035",
    "SD": "020",
    "CITY": "Palmhurst",
    "CD": "28"
  },
  {
    "PRECINCT": "0237",
    "CC": "1",
    "HD": "040",
    "SD": "027",
    "CITY": "Elsa",
    "CD": "15"
  },
  {
    "PRECINCT": "0238",
    "CC": "1",
    "HD": "039",
    "SD": "027",
    "CITY": "Weslaco",
    "CD": "15"
  },
  {
    "PRECINCT": "0239",
    "CC": "4",
    "HD": "040",
    "SD": "020",
    "CITY": "Linn",
    "CD": "15"
  },
  {
    "PRECINCT": "0240",
    "CC": "2",
    "HD": "041",
    "SD": "020",
    "CITY": "Pharr",
    "CD": "15"
  },
  {
    "PRECINCT": "0241",
    "CC": "3",
    "HD": "035",
    "SD": "020",
    "CITY": "Edinburg",
    "CD": "28"
  },
  {
    "PRECINCT": "0242",
    "CC": "1",
    "HD": "039",
    "SD": "027",
    "CITY": "Alamo",
    "CD": "15"
  },
  {
    "PRECINCT": "0243",
    "CC": "3",
    "HD": "036",
    "SD": "020",
    "CITY": "Palmhurst",
    "CD": "28"
  },
  {
    "PRECINCT": "0244",
    "CC": "3",
    "HD": "035",
    "SD": "020",
    "CITY": "Mission",
    "CD": "28"
  },
  {
    "PRECINCT": "0245",
    "CC": "2",
    "HD": "039",
    "SD": "027",
    "CITY": "San Juan",
    "CD": "15"
  },
  {
    "PRECINCT": "0246",
    "CC": "2",
    "HD": "041",
    "SD": "020",
    "CITY": "McAllen",
    "CD": "28"
  },
  {
    "PRECINCT": "0247",
    "CC": "3",
    "HD": "036",
    "SD": "020",
    "CITY": "Palmhurst",
    "CD": "28"
  },
  {
    "PRECINCT": "0248",
    "CC": "3",
    "HD": "036",
    "SD": "020",
    "CITY": "Palmhurst",
    "CD": "28"
  },
  {
    "PRECINCT": "0249",
    "CC": "1",
    "HD": "039",
    "SD": "027",
    "CITY": "Mercedes",
    "CD": "15"
  },
  {
    "PRECINCT": "0250",
    "CC": "1",
    "HD": "039",
    "SD": "027",
    "CITY": "Weslaco",
    "CD": "15"
  },
  {
    "PRECINCT": "0251",
    "CC": "1",
    "HD": "039",
    "SD": "027",
    "CITY": "Alamo",
    "CD": "15"
  },
  {
    "PRECINCT": "0252",
    "CC": "2",
    "HD": "041",
    "SD": "020",
    "CITY": "McAllen",
    "CD": "15"
  },
  {
    "PRECINCT": "0253",
    "CC": "1",
    "HD": "039",
    "SD": "027",
    "CITY": "Alamo",
    "CD": "15"
  },
  {
    "PRECINCT": "0254",
    "CC": "3",
    "HD": "035",
    "SD": "020",
    "CITY": "Palmview",
    "CD": "28"
  },
  {
    "PRECINCT": "0255",
    "CC": "1",
    "HD": "039",
    "SD": "027",
    "CITY": "Alamo",
    "CD": "15"
  },
  {
    "PRECINCT": "0256",
    "CC": "3",
    "HD": "041",
    "SD": "020",
    "CITY": "Palmhurst",
    "CD": "28"
  },
  {
    "PRECINCT": "0257",
    "CC": "3",
    "HD": "035",
    "SD": "020",
    "CITY": "Penitas",
    "CD": "28"
  },
  {
    "PRECINCT": "0258",
    "CC": "2",
    "HD": "036",
    "SD": "020",
    "CITY": "Pharr",
    "CD": "28"
  },
  {
    "PRECINCT": "0259",
    "CC": "1",
    "HD": "040",
    "SD": "027",
    "CITY": "Edinburg",
    "CD": "15"
  },
  {
    "PRECINCT": "Total People",
    "CC": "Total People",
    "HD": "Total People",
    "SD": "Total People",
    "CD": "Unknown"
  }
];
