import pytest
import pathlib
import sys
import pandas as pd
import json

ROOT_PATH = pathlib.Path(__file__).parents[1]
code_directory = ROOT_PATH/'deployment'/'code'

if str(code_directory) not in sys.path:
    sys.path.append(str(code_directory))

from predictor import app

@pytest.fixture
def inputValidation1():
    input1 = {
        "trucker": {
            "person_uuid": "b614401f-7928-11ec-a361-02fb9b06c548",
            "document": "97179841072",
            "name": "Douglas Portela Fontella",
            "process": [
                {
                    "Number": "04283166520118217000",
                    "CourtType": "criminal",
                    "MainSubject": "trafico de drogas e condutas afins",
                    "PublicationDate": "2021-10-01T00:00:00",
                    "NoticeDate": "2011-09-09T00:00:00",
                    "RedistributionDate": "0001-01-01T00:00:00",
                    "LawsuitAge": 147,
                    "ResponseDecisions": [
                        {
                            "DecisionContent": "Decisão condenatória",
                            "DecisionDate": "2022-05-20T00:00:00"
                        }
                    ],
                    "ResponseParties": [
                        {
                            "Doc": "97179841072",
                            "IsPartyActive": "true",
                            "Name": "douglas portela fontella",
                            "Polarity": "passive",
                            "Type": "defendant",
                            "LastCaptureDate": "2021-10-02T23:51:18",
                            "PartyDetails": {
                                "SpecificType": "correu"
                            }
                        }
                    ]
                },
                {
                    "Number": "01658943820118217000",
                    "CourtType": "criminal",
                    "MainSubject": "trafico de drogas e condutas afins",
                    "PublicationDate": "2021-10-01T00:00:00",
                    "NoticeDate": "2011-04-19T00:00:00",
                    "RedistributionDate": "0001-01-01T00:00:00",
                    "LawsuitAge": 143,
                    "ResponseDecisions": [
                        {
                            "DecisionContent": "Decisão condenatória",
                            "DecisionDate": "2022-05-20T00:00:00"
                        }
                    ],
                    "ResponseParties": [
                        {
                            "Doc": "97179841072",
                            "IsPartyActive": "true",
                            "Name": "douglas portela fontella",
                            "Polarity": "passive",
                            "Type": "defendant",
                            "LastCaptureDate": "2021-10-02T23:49:09",
                            "PartyDetails": {
                                "SpecificType": "correu"
                            }
                        }
                    ]
                },
                {
                    "Number": "01482748120098217000",
                    "CourtType": "criminal",
                    "MainSubject": "trafico de drogas e condutas afins",
                    "PublicationDate": "2021-10-01T00:00:00",
                    "NoticeDate": "2009-10-19T00:00:00",
                    "RedistributionDate": "0001-01-01T00:00:00",
                    "LawsuitAge": 547,
                    "ResponseDecisions": [
                        {
                            "DecisionContent": "Decisão condenatória",
                            "DecisionDate": "2022-05-20T00:00:00"
                        }
                    ],
                    "ResponseParties": [
                        {
                            "Doc": "97179841072",
                            "IsPartyActive": "true",
                            "Name": "douglas portela fontella",
                            "Polarity": "passive",
                            "Type": "defendant",
                            "LastCaptureDate": "2021-10-02T23:45:53",
                            "PartyDetails": {
                                "SpecificType": "correu"
                            }
                        }
                    ]
                },
                {
                    "Number": "70027949056",
                    "CourtType": "criminal",
                    "MainSubject": "trafico de drogas e condutas afins",
                    "PublicationDate": "2021-10-01T00:00:00",
                    "NoticeDate": "2008-12-15T00:00:00",
                    "RedistributionDate": "0001-01-01T00:00:00",
                    "LawsuitAge": 121,
                    "ResponseDecisions": [
                        {
                            "DecisionContent": "Decisão condenatória",
                            "DecisionDate": "2022-05-20T00:00:00"
                        }
                    ],
                    "ResponseParties": [
                        {
                            "Doc": "97179841072",
                            "IsPartyActive": "true",
                            "Name": "douglas portela fontella",
                            "Polarity": "passive",
                            "Type": "defendant",
                            "LastCaptureDate": "2021-10-02T23:42:23",
                            "PartyDetails": {
                                "SpecificType": "correu"
                            }
                        }
                    ]
                }
            ]
        },
        "vehicle_owners": [
            {
                "person_uuid": "9619f6df-ca42-4979-b031-c8df9cb0cf82",
                "document": "97179841072",
                "name": "Maria Oliveira",
                "process": [
                    {
                        "Number": "456",
                        "CourtType": "Criminal",
                        "MainSubject": "Ameaca",
                        "PublicationDate": "2022-03-01T00:00:00",
                        "NoticeDate": "2022-03-10T00:00:00",
                        "RedistributionDate": "2022-03-12T00:00:00",
                        "LawsuitAge": 60,
                        "ResponseDecisions": [
                            {
                                "DecisionContent": "culpado",
                                "DecisionDate": "2022-03-12T00:00:00"
                            }
                        ],
                        "ResponseParties": [
                            {
                                "Doc": "97179841072",
                                "IsPartyActive": "true",
                                "Name": "Maria Oliveira",
                                "Polarity": "passive",
                                "Type": "defendant",
                                "LastCaptureDate": "2021-10-02T23:42:23",
                                "PartyDetails": {
                                    "SpecificType": "reu"
                                }
                            }
                        ]
                    }
                ]
            }
        ],
        "rntrc_owners": [
            {
                "person_uuid": "9619f6df-ca42-4979-b031-c8df9cb0cf82",
                "document": "97179841072",
                "name": "Maria Oliveira",
                "process": [
                    {
                        "Number": "456",
                        "CourtType": "Criminal",
                        "MainSubject": "Ameaca",
                        "PublicationDate": "2022-03-01T00:00:00",
                        "NoticeDate": "2022-03-10T00:00:00",
                        "RedistributionDate": "2022-03-12T00:00:00",
                        "LawsuitAge": 60,
                        "ResponseDecisions": [
                            {
                                "DecisionContent": "culpado",
                                "DecisionDate": "2022-03-12T00:00:00"
                            }
                        ],
                        "ResponseParties": [
                            {
                                "Doc": "97179841072",
                                "IsPartyActive": "true",
                                "Name": "Maria Oliveira",
                                "Polarity": "passive",
                                "Type": "defendant",
                                "LastCaptureDate": "2021-10-02T23:42:23",
                                "PartyDetails": {
                                    "SpecificType": "reu"
                                }
                            }
                        ]
                    }
                ]
            }
        ]
    }

    return input1

@pytest.fixture
def outputValidation1():
    
    d = {"person_uuid": ["b614401f-7928-11ec-a361-02fb9b06c548",
                        "b614401f-7928-11ec-a361-02fb9b06c548",
                        "b614401f-7928-11ec-a361-02fb9b06c548",
                        "b614401f-7928-11ec-a361-02fb9b06c548"],
         "document": ["97179841072",
                 "97179841072",
                 "97179841072",
                 "97179841072"],        
         "name": ["douglas portela fontella",
                  "douglas portela fontella",
                  "douglas portela fontella",
                  "douglas portela fontella"],
         "Number": ["04283166520118217000",
                    "01658943820118217000", 
                    "01482748120098217000", 
                    "70027949056"],      
         "CourtType": ["criminal",
                       "criminal", 
                       "criminal", 
                       "criminal"],
         "MainSubject": ["trafico de drogas e condutas afins",
                         "trafico de drogas e condutas afins",
                         "trafico de drogas e condutas afins",
                         "trafico de drogas e condutas afins"],             
         "PublicationDate": ["2021-10-01t00:00:00",
                             "2021-10-01t00:00:00", 
                             "2021-10-01t00:00:00",
                             "2021-10-01t00:00:00"],
         "NoticeDate": ["2011-09-09t00:00:00",
                        "2011-04-19t00:00:00",
                        "2009-10-19t00:00:00",
                        "2008-12-15t00:00:00"],
         "RedistributionDate": ["0001-01-01t00:00:00",
                                "0001-01-01t00:00:00",
                                "0001-01-01t00:00:00",
                                "0001-01-01t00:00:00"],
         "LawsuitAge": [147,143,547,121],
         "Doc": ["97179841072","97179841072","97179841072","97179841072"],
         "IsPartyActive": ["true","true","true","true"],
         "Name": ["douglas portela fontella",
                  "douglas portela fontella",
                  "douglas portela fontella",
                  "douglas portela fontella"],
         "Polarity": ["passive","passive","passive","passive"],
         "Type": ["defendant","defendant","defendant","defendant"],
         "SpecificType": ["correu","correu","correu","correu"],
         "LastCaptureDate": ["2021-10-02t23:51:18",
                             "2021-10-02t23:49:09",
                             "2021-10-02t23:45:53",
                             "2021-10-02t23:42:23"]}
    
    output1 = pd.DataFrame(data=d)
    
    return output1

@pytest.fixture
def inputValidation2():
    input2 = {
        "trucker": {
            "person_uuid": "b614401f-7928-11ec-a361-02fb9b06c548",
            "document": "97179841072",
            "name": "Douglas Portela Fontella",
            "process": [
                {
                    "Number": "04283166520118217000",
                    "CourtType": "criminal",
                    "MainSubject": "trafico de drogas e condutas afins",
                    "PublicationDate": "2021-10-01T00:00:00",
                    "NoticeDate": "2011-09-09T00:00:00",
                    "RedistributionDate": "0001-01-01T00:00:00",
                    "LawsuitAge": 147,
                    "ResponseDecisions": [
                        {
                            "DecisionContent": "Decisão condenatória",
                            "DecisionDate": "2022-05-20T00:00:00"
                        }
                    ],
                    "ResponseParties": [
                        {
                            "Doc": "97179841072",
                            "IsPartyActive": "true",
                            "Name": "douglas portela fontella",
                            "Polarity": "passive",
                            "Type": "defendant",
                            "LastCaptureDate": "2021-10-02T23:51:18",
                            "PartyDetails": {
                                "SpecificType": "correu"
                            }
                        }
                    ]
                },
                {
                    "Number": "01658943820118217000",
                    "CourtType": "criminal",
                    "MainSubject": "trafico de drogas e condutas afins",
                    "PublicationDate": "2021-10-01T00:00:00",
                    "NoticeDate": "2011-04-19T00:00:00",
                    "RedistributionDate": "0001-01-01T00:00:00",
                    "LawsuitAge": 143,
                    "ResponseDecisions": [
                        {
                            "DecisionContent": "Decisão condenatória",
                            "DecisionDate": "2022-05-20T00:00:00"
                        }
                    ],
                    "ResponseParties": [
                        {
                            "Doc": "97179841072",
                            "IsPartyActive": "true",
                            "Name": "douglas portela fontella",
                            "Polarity": "passive",
                            "Type": "defendant",
                            "LastCaptureDate": "2021-10-02T23:49:09",
                            "PartyDetails": {
                                "SpecificType": "correu"
                            }
                        }
                    ]
                },
                {
                    "Number": "01482748120098217000",
                    "CourtType": "criminal",
                    "MainSubject": "trafico de drogas e condutas afins",
                    "PublicationDate": "2021-10-01T00:00:00",
                    "NoticeDate": "2009-10-19T00:00:00",
                    "RedistributionDate": "0001-01-01T00:00:00",
                    "LawsuitAge": 547,
                    "ResponseDecisions": [
                        {
                            "DecisionContent": "Decisão condenatória",
                            "DecisionDate": "2022-05-20T00:00:00"
                        }
                    ],
                    "ResponseParties": [
                        {
                            "Doc": "97179841072",
                            "IsPartyActive": "true",
                            "Name": "douglas portela fontella",
                            "Polarity": "passive",
                            "Type": "defendant",
                            "LastCaptureDate": "2021-10-02T23:45:53",
                            "PartyDetails": {
                                "SpecificType": "correu"
                            }
                        }
                    ]
                },
                {
                    "Number": "70027949056",
                    "CourtType": "criminal",
                    "MainSubject": "trafico de drogas e condutas afins",
                    "PublicationDate": "2021-10-01T00:00:00",
                    "NoticeDate": "2008-12-15T00:00:00",
                    "RedistributionDate": "0001-01-01T00:00:00",
                    "LawsuitAge": 121,
                    "ResponseDecisions": [
                        {
                            "DecisionContent": "Decisão condenatória",
                            "DecisionDate": "2022-05-20T00:00:00"
                        }
                    ],
                    "ResponseParties": [
                        {
                            "Doc": "97179841072",
                            "IsPartyActive": "true",
                            "Name": "douglas portela fontella",
                            "Polarity": "passive",
                            "Type": "defendant",
                            "LastCaptureDate": "2021-10-02T23:42:23",
                            "PartyDetails": {
                                "SpecificType": "correu"
                            }
                        }
                    ]
                }
            ]
        },
        "vehicle_owners": [
            {
                "person_uuid": None,
                "document": "97179841072",
                "name": "Maria Oliveira",
                "process": [
                    {
                        "Number": "456",
                        "CourtType": "Criminal",
                        "MainSubject": "Ameaca",
                        "PublicationDate": "2022-03-01T00:00:00",
                        "NoticeDate": "2022-03-10T00:00:00",
                        "RedistributionDate": "2022-03-12T00:00:00",
                        "LawsuitAge": 60,
                        "ResponseDecisions": [
                            {
                                "DecisionContent": "culpado",
                                "DecisionDate": "2022-03-12T00:00:00"
                            }
                        ],
                        "ResponseParties": [
                            {
                                "Doc": "97179841072",
                                "IsPartyActive": "true",
                                "Name": "Maria Oliveira",
                                "Polarity": "passive",
                                "Type": "defendant",
                                "LastCaptureDate": "2021-10-02T23:42:23",
                                "PartyDetails": {
                                    "SpecificType": "reu"
                                }
                            }
                        ]
                    }
                ]
            }
        ],
        "rntrc_owners": [
            {
                "person_uuid": None,
                "document": "97179841072",
                "name": "Maria Oliveira",
                "process": [
                    {
                        "Number": "456",
                        "CourtType": "Criminal",
                        "MainSubject": "Ameaca",
                        "PublicationDate": "2022-03-01T00:00:00",
                        "NoticeDate": "2022-03-10T00:00:00",
                        "RedistributionDate": "2022-03-12T00:00:00",
                        "LawsuitAge": 60,
                        "ResponseDecisions": [
                            {
                                "DecisionContent": "culpado",
                                "DecisionDate": "2022-03-12T00:00:00"
                            }
                        ],
                        "ResponseParties": [
                            {
                                "Doc": "97179841072",
                                "IsPartyActive": "true",
                                "Name": "Maria Oliveira",
                                "Polarity": "passive",
                                "Type": "defendant",
                                "LastCaptureDate": "2021-10-02T23:42:23",
                                "PartyDetails": {
                                    "SpecificType": "reu"
                                }
                            }
                        ]
                    }
                ]
            }
        ]
    }
    
    return input2

@pytest.fixture
def outputValidation2():
    d = {"person_uuid": ["b614401f-7928-11ec-a361-02fb9b06c548",
                        "b614401f-7928-11ec-a361-02fb9b06c548",
                        "b614401f-7928-11ec-a361-02fb9b06c548",
                        "b614401f-7928-11ec-a361-02fb9b06c548"],
         "document": ["97179841072",
                 "97179841072",
                 "97179841072",
                 "97179841072"],        
         "name": ["douglas portela fontella",
                  "douglas portela fontella",
                  "douglas portela fontella",
                  "douglas portela fontella"],
         "Number": ["04283166520118217000",
                    "01658943820118217000", 
                    "01482748120098217000", 
                    "70027949056"],      
         "CourtType": ["criminal",
                       "criminal", 
                       "criminal", 
                       "criminal"],
         "MainSubject": ["trafico de drogas e condutas afins",
                         "trafico de drogas e condutas afins",
                         "trafico de drogas e condutas afins",
                         "trafico de drogas e condutas afins"],             
         "PublicationDate": ["2021-10-01t00:00:00",
                             "2021-10-01t00:00:00", 
                             "2021-10-01t00:00:00",
                             "2021-10-01t00:00:00"],
         "NoticeDate": ["2011-09-09t00:00:00",
                        "2011-04-19t00:00:00",
                        "2009-10-19t00:00:00",
                        "2008-12-15t00:00:00"],
         "RedistributionDate": ["0001-01-01t00:00:00",
                                "0001-01-01t00:00:00",
                                "0001-01-01t00:00:00",
                                "0001-01-01t00:00:00"],
         "LawsuitAge": [147,143,547,121],
         "Doc": ["97179841072","97179841072","97179841072","97179841072"],
         "IsPartyActive": ["true","true","true","true"],
         "Name": ["douglas portela fontella",
                  "douglas portela fontella",
                  "douglas portela fontella",
                  "douglas portela fontella"],
         "Polarity": ["passive","passive","passive","passive"],
         "Type": ["defendant","defendant","defendant","defendant"],
         "SpecificType": ["correu","correu","correu","correu"],
         "LastCaptureDate": ["2021-10-02t23:51:18",
                             "2021-10-02t23:49:09",
                             "2021-10-02t23:45:53",
                             "2021-10-02t23:42:23"]}
    
    output2 = pd.DataFrame(data=d)
    
    return output2

@pytest.fixture
def inputValidation3():
    input3 = {
        "trucker": {
            "person_uuid": "9619f6df-ca42-4979-b031-c8df9cb0cf82",
            "document": "97179841072",
            "name": "Douglas Portela Fontella",
            "process": [
                {
                    "Number": "04283166520118217000",
                    "CourtType": "criminal",
                    "MainSubject": "trafico de drogas e condutas afins",
                    "PublicationDate": "2021-10-01T00:00:00",
                    "NoticeDate": "2011-09-09T00:00:00",
                    "RedistributionDate": "0001-01-01T00:00:00",
                    "LawsuitAge": 147,
                    "ResponseDecisions": [
                        {
                            "DecisionContent": "Decisão condenatória",
                            "DecisionDate": "2022-05-20T00:00:00"
                        }
                    ],
                    "ResponseParties": [
                        {
                            "Doc": "97179841072",
                            "IsPartyActive": "true",
                            "Name": "douglas portela fontella",
                            "Polarity": "passive",
                            "Type": "defendant",
                            "LastCaptureDate": "2021-10-02T23:51:18",
                            "PartyDetails": {
                                "SpecificType": "correu"
                            }
                        }
                    ]
                },
                {
                    "Number": "01658943820118217000",
                    "CourtType": "criminal",
                    "MainSubject": "trafico de drogas e condutas afins",
                    "PublicationDate": "2021-10-01T00:00:00",
                    "NoticeDate": "2011-04-19T00:00:00",
                    "RedistributionDate": "0001-01-01T00:00:00",
                    "LawsuitAge": 143,
                    "ResponseDecisions": [
                        {
                            "DecisionContent": "Decisão condenatória",
                            "DecisionDate": "2022-05-20T00:00:00"
                        }
                    ],
                    "ResponseParties": [
                        {
                            "Doc": "97179841072",
                            "IsPartyActive": "true",
                            "Name": "douglas portela fontella",
                            "Polarity": "passive",
                            "Type": "defendant",
                            "LastCaptureDate": "2021-10-02T23:49:09",
                            "PartyDetails": {
                                "SpecificType": "correu"
                            }
                        }
                    ]
                },
                {
                    "Number": "01482748120098217000",
                    "CourtType": "criminal",
                    "MainSubject": "trafico de drogas e condutas afins",
                    "PublicationDate": "2021-10-01T00:00:00",
                    "NoticeDate": "2009-10-19T00:00:00",
                    "RedistributionDate": "0001-01-01T00:00:00",
                    "LawsuitAge": 547,
                    "ResponseDecisions": [
                        {
                            "DecisionContent": "Decisão condenatória",
                            "DecisionDate": "2022-05-20T00:00:00"
                        }
                    ],
                    "ResponseParties": [
                        {
                            "Doc": "97179841072",
                            "IsPartyActive": "true",
                            "Name": "douglas portela fontella",
                            "Polarity": "passive",
                            "Type": "defendant",
                            "LastCaptureDate": "2021-10-02T23:45:53",
                            "PartyDetails": {
                                "SpecificType": "correu"
                            }
                        }
                    ]
                },
                {
                    "Number": "70027949056",
                    "CourtType": "criminal",
                    "MainSubject": "trafico de drogas e condutas afins",
                    "PublicationDate": "2021-10-01T00:00:00",
                    "NoticeDate": "2008-12-15T00:00:00",
                    "RedistributionDate": "0001-01-01T00:00:00",
                    "LawsuitAge": 121,
                    "ResponseDecisions": [
                        {
                            "DecisionContent": "Decisão condenatória",
                            "DecisionDate": "2022-05-20T00:00:00"
                        }
                    ],
                    "ResponseParties": [
                        {
                            "Doc": "97179841072",
                            "IsPartyActive": "true",
                            "Name": "douglas portela fontella",
                            "Polarity": "passive",
                            "Type": "defendant",
                            "LastCaptureDate": "2021-10-02T23:42:23",
                            "PartyDetails": {
                                "SpecificType": "correu"
                            }
                        }
                    ]
                }
            ]
        },
        "vehicle_owners": [
            {
                "person_uuid": "9619f6df-ca42-4979-b031-c8df9cb0cf82",
                "document": "97179841072",
                "name": "Maria Oliveira",
                "process": [
                    {
                        "Number": "456",
                        "CourtType": "Criminal",
                        "MainSubject": "Ameaca",
                        "PublicationDate": "2022-03-01T00:00:00",
                        "NoticeDate": "2022-03-10T00:00:00",
                        "RedistributionDate": "2022-03-12T00:00:00",
                        "LawsuitAge": 60,
                        "ResponseDecisions": [
                            {
                                "DecisionContent": "culpado",
                                "DecisionDate": "2022-03-12T00:00:00"
                            }
                        ],
                        "ResponseParties": [
                            {
                                "Doc": "97179841072",
                                "IsPartyActive": "true",
                                "Name": "Maria Oliveira",
                                "Polarity": "passive",
                                "Type": "defendant",
                                "LastCaptureDate": "2021-10-02T23:42:23",
                                "PartyDetails": {
                                    "SpecificType": "reu"
                                }
                            }
                        ]
                    }
                ]
            }
        ]
    }
        
    return input3


@pytest.fixture
def inputValidation3backup():
    input3 = [{
        "trucker_id": "9619f6df-ca42-4979-b031-c8df9cb0cf82",
        "cpf": "01590738128",
        "name": "Denilson Ramos Junior",
        "process": [
            {
                "Number": "00040272120168120013",
                "CourtType": "criminal",
                "MainSubject": "ameaca",
                "PublicationDate": "2018-08-14T00:00:00",
                "NoticeDate": "2016-12-08T00:00:00",
                "RedistributionDate": "0001-01-01T00:00:00",
                "LawsuitAge": 2102,
                "ResponseParties": {
                    "Doc": "01590738128",
                    "IsPartyActive": "true",
                    "Name": "DENILSON RAMOS JUNIOR",
                    "Polarity": "PASSIVE",
                    "Type": "DEFENDANT",
                    "LastCaptureDate": "2018-08-15T03:26:54",
                    "PartyDetails": {
                        "SpecificType": "REU"
                    }
                }
            },
            {
                "Number": "00008822020178120013",
                "CourtType": "criminal",
                "MainSubject": "ameaca",
                "PublicationDate": "2021-02-12T00:00:00",
                "NoticeDate": "2017-03-23T00:00:00",
                "RedistributionDate": "0001-01-01T00:00:00",
                "LawsuitAge": 1997,
                "ResponseParties": {
                    "Doc": "01590738128",
                    "IsPartyActive": "true",
                    "Name": "DENILSON RAMOS JUNIOR",
                    "Polarity": "PASSIVE",
                    "Type": "DEFENDANT",
                    "LastCaptureDate": "2021-02-13T14:03:26",
                    "PartyDetails": {
                        "SpecificType": "REU"
                    }
                }
            },
            {
                "Number": "00013433120138120013",
                "CourtType": "criminal",
                "MainSubject": "furto",
                "PublicationDate": "2020-07-08T00:00:00",
                "NoticeDate": "2010-10-22T00:00:00",
                "RedistributionDate": "0001-01-01T00:00:00",
                "LawsuitAge": 4341,
                "ResponseParties": {
                    "Doc": "01590738128",
                    "IsPartyActive": "true",
                    "Name": "DENILSON RAMOS JUNIOR",
                    "Polarity": "PASSIVE",
                    "Type": "DEFENDANT",
                    "LastCaptureDate": "2020-07-09T15:29:10",
                    "PartyDetails": {
                        "SpecificType": "REU"
                    }
                }
            },
            {
                "Number": "00022876720128120013",
                "CourtType": "criminal",
                "MainSubject": "extorsao mediante sequestro",
                "PublicationDate": "2020-08-12T00:00:00",
                "NoticeDate": "2010-12-13T00:00:00",
                "RedistributionDate": "0001-01-01T00:00:00",
                "LawsuitAge": 4289,
                "ResponseParties": {
                    "Doc": "01590738128",
                    "IsPartyActive": "true",
                    "Name": "DENILSON RAMOS JUNIOR",
                    "Polarity": "PASSIVE",
                    "Type": "DEFENDANT",
                    "LastCaptureDate": "2020-08-13T18:59:21",
                    "PartyDetails": {
                        "SpecificType": "REU"
                    }
                }
            },
            {
                "Number": "00037991220178120013",
                "CourtType": "criminal",
                "MainSubject": "ameaca",
                "PublicationDate": "2021-12-03T00:00:00",
                "NoticeDate": "2017-12-12T00:00:00",
                "RedistributionDate": "0001-01-01T00:00:00",
                "LawsuitAge": 1733,
                "ResponseParties": {
                    "Doc": "01590738128",
                    "IsPartyActive": "true",
                    "Name": "DENILSON RAMOS JUNIOR",
                    "Polarity": "PASSIVE",
                    "Type": "DEFENDANT",
                    "LastCaptureDate": "2021-12-05T13:40:37",
                    "PartyDetails": {
                        "SpecificType": "REU"
                    }
                }
            }
        ]
    }]
    return input3

@pytest.fixture
def inputValidation4():
    input4 = {
        "trucker": {
            "person_uuid": "9619f6df-ca42-4979-b031-c8df9cb0cf82",
            "document": "97179841072",
            "name": "Douglas Portela Fontella",
            "process": [
                {
                    "Number": "04283166520118217000",
                    "CourtType": "criminal",
                    "MainSubject": "trafico de drogas e condutas afins",
                    "PublicationDate": "2021-10-01T00:00:00",
                    "NoticeDate": "2011-09-09T00:00:00",
                    "RedistributionDate": "0001-01-01T00:00:00",
                    "LawsuitAge": 147,
                    "ResponseDecisions": [
                        {
                            "DecisionContent": "Decisão condenatória",
                            "DecisionDate": "2022-05-20T00:00:00"
                        }
                    ],
                    "ResponseParties": [
                        {
                            "Doc": "97179841072",
                            "IsPartyActive": "true",
                            "Name": "douglas portela fontella",
                            "Polarity": "passive",
                            "Type": "defendant",
                            "LastCaptureDate": "2021-10-02T23:51:18",
                            "PartyDetails": {
                                "SpecificType": "correu"
                            }
                        }
                    ]
                },
                {
                    "Number": "01658943820118217000",
                    "CourtType": "criminal",
                    "MainSubject": "trafico de drogas e condutas afins",
                    "PublicationDate": "2021-10-01T00:00:00",
                    "NoticeDate": "2011-04-19T00:00:00",
                    "RedistributionDate": "0001-01-01T00:00:00",
                    "LawsuitAge": 143,
                    "ResponseDecisions": [
                        {
                            "DecisionContent": "Decisão condenatória",
                            "DecisionDate": "2022-05-20T00:00:00"
                        }
                    ],
                    "ResponseParties": [
                        {
                            "Doc": "97179841072",
                            "IsPartyActive": "true",
                            "Name": "douglas portela fontella",
                            "Polarity": "passive",
                            "Type": "defendant",
                            "LastCaptureDate": "2021-10-02T23:49:09",
                            "PartyDetails": {
                                "SpecificType": "correu"
                            }
                        }
                    ]
                },
                {
                    "Number": "01482748120098217000",
                    "CourtType": "criminal",
                    "MainSubject": "trafico de drogas e condutas afins",
                    "PublicationDate": "2021-10-01T00:00:00",
                    "NoticeDate": "2009-10-19T00:00:00",
                    "RedistributionDate": "0001-01-01T00:00:00",
                    "LawsuitAge": 547,
                    "ResponseDecisions": [
                        {
                            "DecisionContent": "Decisão condenatória",
                            "DecisionDate": "2022-05-20T00:00:00"
                        }
                    ],
                    "ResponseParties": [
                        {
                            "Doc": "97179841072",
                            "IsPartyActive": "true",
                            "Name": "douglas portela fontella",
                            "Polarity": "passive",
                            "Type": "defendant",
                            "LastCaptureDate": "2021-10-02T23:45:53",
                            "PartyDetails": {
                                "SpecificType": "correu"
                            }
                        }
                    ]
                },
                {
                    "Number": "70027949056",
                    "CourtType": "criminal",
                    "MainSubject": "trafico de drogas e condutas afins",
                    "PublicationDate": "2021-10-01T00:00:00",
                    "NoticeDate": "2008-12-15T00:00:00",
                    "RedistributionDate": "0001-01-01T00:00:00",
                    "LawsuitAge": 121,
                    "ResponseDecisions": [
                        {
                            "DecisionContent": "Decisão condenatória",
                            "DecisionDate": "2022-05-20T00:00:00"
                        }
                    ],
                    "ResponseParties": [
                        {
                            "Doc": "97179841072",
                            "IsPartyActive": "true",
                            "Name": "douglas portela fontella",
                            "Polarity": "passive",
                            "Type": "defendant",
                            "LastCaptureDate": "2021-10-02T23:42:23",
                            "PartyDetails": {
                                "SpecificType": "correu"
                            }
                        }
                    ]
                }
            ]
        },
        "vehicle_owners": [
            {
               
            }
        ],
        "rntrc_owners": [
            {
                "person_uuid": None,
                "document": "97179841072",
                "name": "Maria Oliveira",
                "process": [
                    {
                        "Number": "456",
                        "CourtType": "Criminal",
                        "MainSubject": "Ameaca",
                        "PublicationDate": "2022-03-01T00:00:00",
                        "NoticeDate": "2022-03-10T00:00:00",
                        "RedistributionDate": "2022-03-12T00:00:00",
                        "LawsuitAge": 60,
                        "ResponseDecisions": [
                            {
                                "DecisionContent": "culpado",
                                "DecisionDate": "2022-03-12T00:00:00"
                            }
                        ],
                        "ResponseParties": [
                            {
                                "Doc": "97179841072",
                                "IsPartyActive": "true",
                                "Name": "Maria Oliveira",
                                "Polarity": "passive",
                                "Type": "defendant",
                                "LastCaptureDate": "2021-10-02T23:42:23",
                                "PartyDetails": {
                                    "SpecificType": "reu"
                                }
                            }
                        ]
                    }
                ]
            }
        ]
    }
    
    return input4
    

@pytest.fixture
def outputValidation4():
    output4 = {
        "trucker_id": "95a3a6f5-9896-4119-a862-26643902b314", 
        "isGoodsRange": 0, 
        "isServiced": 0,
        "isSizeCompany": 0
    }
    return output4


@pytest.fixture
def inputValidation5():
    input5 = {
        "trucker": {
            "person_uuid": "b614401f-7928-11ec-a361-02fb9b06c548",
            "document": "97179841072",
            "name": "Douglas Portela Fontella",
            "process": [
                {
                    "Number": "70027949056",
                    "CourtType": "criminal",
                    "MainSubject": "trafico de drogas e condutas afins",
                    "PublicationDate": "2021-10-01T00:00:00",
                    "NoticeDate": "2008-12-15T00:00:00",
                    "RedistributionDate": "0001-01-01T00:00:00",
                    "LawsuitAge": 121,
                    "ResponseDecisions": [
                        {
                            "DecisionContent": "Decisão condenatória",
                            "DecisionDate": "2022-05-20T00:00:00"
                        }
                    ],
                    "ResponseParties": [
                        {
                            "Doc": "97179841072",
                            "IsPartyActive": "true",
                            "Name": "douglas portela fontella",
                            "Polarity": "passive",
                            "Type": "defendant",
                            "LastCaptureDate": "2021-10-02T23:42:23",
                            "PartyDetails": {
                                "SpecificType": "correu"
                            }
                        }
                    ]
                }
            ]
        },
        "vehicle_owners": [
            {
                "person_uuid": "9619f6df-ca42-4979-b031-c8df9cb0cf82",
                "document": "97179841072",
                "name": "Maria Oliveira",
                "process": [
                    {
                        "Number": "456",
                        "CourtType": "Criminal",
                        "MainSubject": "Ameaca",
                        "PublicationDate": "2022-03-01T00:00:00",
                        "NoticeDate": "2022-03-10T00:00:00",
                        "RedistributionDate": "2022-03-12T00:00:00",
                        "LawsuitAge": 60,
                        "ResponseDecisions": [
                            {
                                "DecisionContent": "culpado",
                                "DecisionDate": "2022-03-12T00:00:00"
                            }
                        ],
                        "ResponseParties": [
                            {
                                "Doc": "97179841072",
                                "IsPartyActive": "true",
                                "Name": "Maria Oliveira",
                                "Polarity": "passive",
                                "Type": "defendant",
                                "LastCaptureDate": "2021-10-02T23:42:23",
                                "PartyDetails": {
                                    "SpecificType": "reu"
                                }
                            }
                        ]
                    }
                ]
            }
        ],
        "rntrc_owners": [
            {
                "person_uuid": "9619f6df-ca42-4979-b031-c8df9cb0cf82",
                "document": "97179841072",
                "name": "Maria Oliveira",
                "process": [
                    {
                        "Number": "456",
                        "CourtType": "Criminal",
                        "MainSubject": "Ameaca",
                        "PublicationDate": "2022-03-01T00:00:00",
                        "NoticeDate": "2022-03-10T00:00:00",
                        "RedistributionDate": "2022-03-12T00:00:00",
                        "LawsuitAge": 60,
                        "ResponseDecisions": [
                            {
                                "DecisionContent": "culpado",
                                "DecisionDate": "2022-03-12T00:00:00"
                            }
                        ],
                        "ResponseParties": [
                            {
                                "Doc": "97179841072",
                                "IsPartyActive": "true",
                                "Name": "Maria Oliveira",
                                "Polarity": "passive",
                                "Type": "defendant",
                                "LastCaptureDate": "2021-10-02T23:42:23",
                                "PartyDetails": {
                                    "SpecificType": "reu"
                                }
                            }
                        ]
                    }
                ]
            }
        ]
    }
    return input5
    
@pytest.fixture
def outputValidation5():
    d = {"person_uuid": ["b614401f-7928-11ec-a361-02fb9b06c548"],
         "document": ["97179841072"],        
         "name": ["douglas portela fontella"],
         "Number": ["70027949056"],      
         "CourtType": ["criminal"],
         "MainSubject": ["trafico de drogas e condutas afins"],             
         "PublicationDate": ["2021-10-01t00:00:00"],
         "NoticeDate": ["2008-12-15t00:00:00"],
         "RedistributionDate": ["0001-01-01t00:00:00"],
         "LawsuitAge": [121],
         "Doc": ["97179841072"],
         "IsPartyActive": ["true"],
         "Name": ["douglas portela fontella"],
         "Polarity": ["passive"],
         "Type": ["defendant"],
         "LastCaptureDate": ["2021-10-02t23:42:23"],
         "SpecificType": ["correu"]}
    
    output5 = pd.DataFrame(data=d)
    
    return output5
    
@pytest.fixture
def inputValidation6():
    input6 = {
        "trucker": {
            "person_uuid": "9619f6df-ca42-4979-b031-c8df9cb0cf82",
            "document": "01590738128",
            "name": "denilson ramos junior",
            "process": [
                {
                    "Number": "00040272120168120013",
                    "CourtType": "criminal",
                    "MainSubject": "ameaca",
                    "PublicationDate": "2018-08-14T00:00:00",
                    "NoticeDate": "2016-12-08T00:00:00",
                    "RedistributionDate": "0001-01-01T00:00:00",
                    "LawsuitAge": 2102,
                    "ResponseParties": [
                        {
                            "Doc": "01590738128",
                            "IsPartyActive": "true",
                            "Name": "denilson ramos junior",
                            "Polarity": "passive",
                            "Type": "defendant",
                            "LastCaptureDate": "2018-08-15T03:26:54",
                            "PartyDetails": {
                                "SpecificType": "reu"
                            }
                        }
                    ]
                },
                {
                    "Number": "00008822020178120013",
                    "CourtType": "trabalhista",
                    "MainSubject": "xxx",
                    "PublicationDate": "2021-02-12T00:00:00",
                    "NoticeDate": "2017-03-23T00:00:00",
                    "RedistributionDate": "0001-01-01T00:00:00",
                    "LawsuitAge": 1997,
                    "ResponseParties": [
                        {
                            "Doc": "01590738128",
                            "IsPartyActive": "true",
                            "Name": "denilson ramos junior",
                            "Polarity": "passive",
                            "Type": "defendant",
                            "LastCaptureDate": "2021-02-13T14:03:26",
                            "PartyDetails": {
                                "SpecificType": "reu"
                            }
                        }
                    ]
                },
                {
                    "Number": "00022876720128120013",
                    "CourtType": "civel",
                    "MainSubject": "cnh",
                    "PublicationDate": "2020-08-12T00:00:00",
                    "NoticeDate": "2010-12-13T00:00:00",
                    "RedistributionDate": "0001-01-01T00:00:00",
                    "LawsuitAge": 4289,
                    "ResponseParties": [
                        {
                            "Doc": "01590738128",
                            "IsPartyActive": "true",
                            "Name": "denilson ramos junior",
                            "Polarity": "passive",
                            "Type": "defendant",
                            "LastCaptureDate": "2020-08-13T18:59:21",
                            "PartyDetails": {
                                "SpecificType": "reu"
                            }
                        }
                    ]
                }
            ]
        },
        "vehicle_owners": [
            {
                "person_uuid": "9619f6df-ca42-4979-b031-c8df9cb0cf82",
                "document": "97179841072",
                "name": "Maria Oliveira",
                "process": [
                    {
                        "Number": "456",
                        "CourtType": "Criminal",
                        "MainSubject": "Ameaca",
                        "PublicationDate": "2022-03-01T00:00:00",
                        "NoticeDate": "2022-03-10T00:00:00",
                        "RedistributionDate": "2022-03-12T00:00:00",
                        "LawsuitAge": 60,
                        "ResponseDecisions": [
                            {
                                "DecisionContent": "culpado",
                                "DecisionDate": "2022-03-12T00:00:00"
                            }
                        ],
                        "ResponseParties": [
                            {
                                "Doc": "97179841072",
                                "IsPartyActive": "true",
                                "Name": "Maria Oliveira",
                                "Polarity": "passive",
                                "Type": "defendant",
                                "LastCaptureDate": "2021-10-02T23:42:23",
                                "PartyDetails": {
                                    "SpecificType": "reu"
                                }
                            }
                        ]
                    }
                ]
            }
        ],
        "rntrc_owners": [
            {
                "person_uuid": "9619f6df-ca42-4979-b031-c8df9cb0cf82",
                "document": "97179841072",
                "name": "Maria Oliveira",
                "process": [
                    {
                        "Number": "456",
                        "CourtType": "Criminal",
                        "MainSubject": "Ameaca",
                        "PublicationDate": "2022-03-01T00:00:00",
                        "NoticeDate": "2022-03-10T00:00:00",
                        "RedistributionDate": "2022-03-12T00:00:00",
                        "LawsuitAge": 60,
                        "ResponseDecisions": [
                            {
                                "DecisionContent": "culpado",
                                "DecisionDate": "2022-03-12T00:00:00"
                            }
                        ],
                        "ResponseParties": [
                            {
                                "Doc": "97179841072",
                                "IsPartyActive": "true",
                                "Name": "Maria Oliveira",
                                "Polarity": "passive",
                                "Type": "defendant",
                                "LastCaptureDate": "2021-10-02T23:42:23",
                                "PartyDetails": {
                                    "SpecificType": "reu"
                                }
                            }
                        ]
                    }
                ]
            }
        ]
    }
    return input6

@pytest.fixture
def outputValidation6():
    d = {"person_uuid": ["9619f6df-ca42-4979-b031-c8df9cb0cf82"],
         "document": ["01590738128"],        
         "name": ["denilson ramos junior"],
         "Number": ["00040272120168120013"],      
         "CourtType": ["criminal"],
         "MainSubject": ["ameaca"],             
         "PublicationDate": ["2018-08-14t00:00:00"],
         "NoticeDate": ["2016-12-08t00:00:00"],
         "RedistributionDate": ["0001-01-01t00:00:00"],
         "LawsuitAge": [2102],
         "Doc": ["01590738128"],
         "IsPartyActive": ["true"],
         "Name": ["denilson ramos junior"],
         "Polarity": ["passive"],
         "Type": ["defendant"],
         "LastCaptureDate": ["2018-08-15t03:26:54"],
         "SpecificType": ["reu"]}
    
    output6 = pd.DataFrame(data=d)
    
    return output6

@pytest.fixture
def inputValidation7():
    input7 = {
        "trucker": {
            "person_uuid": "9619f6df-ca42-4979-b031-c8df9cb0cf82",
            "document": "01590738128",
            "name": "denilson ramos junior",
            "process": [
                {
                    "Number": "00040272120168120013",
                    "CourtType": "criminal",
                    "MainSubject": "ameaca",
                    "PublicationDate": "2018-08-14T00:00:00",
                    "NoticeDate": "2016-12-08T00:00:00",
                    "RedistributionDate": "0001-01-01T00:00:00",
                    "LawsuitAge": 2102,
                    "ResponseParties": [
                        {
                            "Doc": "01590738128",
                            "IsPartyActive": "true",
                            "Name": "denilson ramos junior",
                            "Polarity": "passive",
                            "Type": "defendant",
                            "LastCaptureDate": "2018-08-15T03:26:54",
                            "PartyDetails": {
                                "SpecificType": "reu"
                            }
                        }
                    ]
                },
                {
                    "Number": "00008822020178120013",
                    "CourtType": "trabalhista",
                    "MainSubject": "xxx",
                    "PublicationDate": "2021-02-12T00:00:00",
                    "NoticeDate": "2017-03-23T00:00:00",
                    "RedistributionDate": "0001-01-01T00:00:00",
                    "LawsuitAge": 1997,
                    "ResponseParties": [
                        {
                            "Doc": "01590738128",
                            "IsPartyActive": "true",
                            "Name": "denilson ramos junior",
                            "Polarity": "passive",
                            "Type": "defendant",
                            "LastCaptureDate": "2021-02-13T14:03:26",
                            "PartyDetails": {
                                "SpecificType": "reu"
                            }
                        }
                    ]
                },
                {
                    "Number": "00013433120138120013",
                    "CourtType": "civel",
                    "MainSubject": "divorcio",
                    "PublicationDate": "2020-07-08T00:00:00",
                    "NoticeDate": "2010-10-22T00:00:00",
                    "RedistributionDate": "0001-01-01T00:00:00",
                    "LawsuitAge": 4341,
                    "ResponseParties": [
                        {
                            "Doc": "01590738128",
                            "IsPartyActive": "true",
                            "Name": "denilson ramos junior",
                            "Polarity": "passive",
                            "Type": "defendant",
                            "LastCaptureDate": "2020-07-09T15:29:10",
                            "PartyDetails": {
                                "SpecificType": "reu"
                            }
                        }
                    ]
                },
                {
                    "Number": "00022876720128120013",
                    "CourtType": "civel",
                    "MainSubject": "cnh",
                    "PublicationDate": "2020-08-12T00:00:00",
                    "NoticeDate": "2010-12-13T00:00:00",
                    "RedistributionDate": "0001-01-01T00:00:00",
                    "LawsuitAge": 4289,
                    "ResponseParties": [
                        {
                            "Doc": "01590738128",
                            "IsPartyActive": "true",
                            "Name": "denilson ramos junior",
                            "Polarity": "passive",
                            "Type": "defendant",
                            "LastCaptureDate": "2020-08-13T18:59:21",
                            "PartyDetails": {
                                "SpecificType": "reu"
                            }
                        }
                    ]
                },
                {
                    "Number": "00037991220178120013",
                    "CourtType": "criminal",
                    "MainSubject": "penhora",
                    "PublicationDate": "2021-12-03T00:00:00",
                    "NoticeDate": "2017-12-12T00:00:00",
                    "RedistributionDate": "0001-01-01T00:00:00",
                    "LawsuitAge": 1733,
                    "ResponseParties": [
                        {
                            "Doc": "01590738128",
                            "IsPartyActive": "true",
                            "Name": "denilson ramos junior",
                            "Polarity": "passive",
                            "Type": "defendant",
                            "LastCaptureDate": "2021-12-05T13:40:37",
                            "PartyDetails": {
                                "SpecificType": "reu"
                            }
                        }
                    ]
                }
            ]
        },
        "vehicle_owners": [
            {
                "person_uuid": "9619f6df-ca42-4979-b031-c8df9cb0cf82",
                "document": "97179841072",
                "name": "Maria Oliveira",
                "process": [
                    {
                        "Number": "456",
                        "CourtType": "Criminal",
                        "MainSubject": "Ameaca",
                        "PublicationDate": "2022-03-01T00:00:00",
                        "NoticeDate": "2022-03-10T00:00:00",
                        "RedistributionDate": "2022-03-12T00:00:00",
                        "LawsuitAge": 60,
                        "ResponseDecisions": [
                            {
                                "DecisionContent": "culpado",
                                "DecisionDate": "2022-03-12T00:00:00"
                            }
                        ],
                        "ResponseParties": [
                            {
                                "Doc": "97179841072",
                                "IsPartyActive": "true",
                                "Name": "Maria Oliveira",
                                "Polarity": "passive",
                                "Type": "defendant",
                                "LastCaptureDate": "2021-10-02T23:42:23",
                                "PartyDetails": {
                                    "SpecificType": "reu"
                                }
                            }
                        ]
                    }
                ]
            }
        ],
        "rntrc_owners": [
            {
                "person_uuid": "9619f6df-ca42-4979-b031-c8df9cb0cf82",
                "document": "97179841072",
                "name": "Maria Oliveira",
                "process": [
                    {
                        "Number": "456",
                        "CourtType": "Criminal",
                        "MainSubject": "Ameaca",
                        "PublicationDate": "2022-03-01T00:00:00",
                        "NoticeDate": "2022-03-10T00:00:00",
                        "RedistributionDate": "2022-03-12T00:00:00",
                        "LawsuitAge": 60,
                        "ResponseDecisions": [
                            {
                                "DecisionContent": "culpado",
                                "DecisionDate": "2022-03-12T00:00:00"
                            }
                        ],
                        "ResponseParties": [
                            {
                                "Doc": "97179841072",
                                "IsPartyActive": "true",
                                "Name": "Maria Oliveira",
                                "Polarity": "passive",
                                "Type": "defendant",
                                "LastCaptureDate": "2021-10-02T23:42:23",
                                "PartyDetails": {
                                    "SpecificType": "reu"
                                }
                            }
                        ]
                    }
                ]
            },
            {
                "person_uuid": "9619f6df-ca42-4979-b031-c8df9cb0cf82",
                "document": "97179841072",
                "name": "Maria Oliveira",
                "process": [
                    {
                        "Number": "456",
                        "CourtType": "Criminal",
                        "MainSubject": "Ameaca",
                        "PublicationDate": "2022-03-01T00:00:00",
                        "NoticeDate": "2022-03-10T00:00:00",
                        "RedistributionDate": "2022-03-12T00:00:00",
                        "LawsuitAge": 60,
                        "ResponseDecisions": [
                            {
                                "DecisionContent": "culpado",
                                "DecisionDate": "2022-03-12T00:00:00"
                            }
                        ],
                        "ResponseParties": [
                            {
                                "Doc": "97179841072",
                                "IsPartyActive": "true",
                                "Name": "Maria Oliveira",
                                "Polarity": "passive",
                                "Type": "defendant",
                                "LastCaptureDate": "2021-10-02T23:42:23",
                                "PartyDetails": {
                                    "SpecificType": "reu"
                                }
                            }
                        ]
                    }
                ]
            }
        ]
    }
    
    return input7
    
@pytest.fixture
def outputValidation7():
    d = {"person_uuid": ["9619f6df-ca42-4979-b031-c8df9cb0cf82"],
         "document": ["01590738128"],        
         "name": ["denilson ramos junior"],
         "Number": ["00040272120168120013"],      
         "CourtType": ["criminal"],
         "MainSubject": ["ameaca"],             
         "PublicationDate": ["2018-08-14t00:00:00"],
         "NoticeDate": ["2016-12-08t00:00:00"],
         "RedistributionDate": ["0001-01-01t00:00:00"],
         "LawsuitAge": [2102],
         "Doc": ["01590738128"],
         "IsPartyActive": ["true"],
         "Name": ["denilson ramos junior"],
         "Polarity": ["passive"],
         "Type": ["defendant"],
         "LastCaptureDate": ["2018-08-15t03:26:54"],
         "SpecificType": ["reu"]}

    output7 = pd.DataFrame(data=d)
    return output7

@pytest.fixture
def inputValidation8():
    input8 = {
        "trucker": {
            "person_uuid": "b614401f-7928-11ec-a361-02fb9b06c548",
            "document": "97179841072",
            "name": "Douglas Portela Fontella",
            "process": [
                {
                    "Number": "04283166520118217000",
                    "CourtType": "criminal",
                    "MainSubject": "trafico de drogas e condutas afins",
                    "PublicationDate": "2021-10-01T00:00:00",
                    "NoticeDate": "2011-09-09T00:00:00",
                    "RedistributionDate": "0001-01-01T00:00:00",
                    "LawsuitAge": 147,
                    "ResponseDecisions": [
                        {
                            "DecisionContent": "Decisão condenatória",
                            "DecisionDate": "2022-05-20T00:00:00"
                        }
                    ],
                    "ResponseParties": [
                        {
                            "Doc": "97179841072",
                            "IsPartyActive": "true",
                            "Name": "douglas portela fontella",
                            "Polarity": "passive",
                            "Type": "defendant",
                            "LastCaptureDate": "2021-10-02T23:51:18",
                            "PartyDetails": {
                                "SpecificType": "correu"
                            }
                        }
                    ]
                },
                {
                    "Number": "01658943820118217000",
                    "CourtType": "criminal",
                    "MainSubject": "trafico de drogas e condutas afins",
                    "PublicationDate": "2021-10-01T00:00:00",
                    "NoticeDate": "2011-04-19T00:00:00",
                    "RedistributionDate": "0001-01-01T00:00:00",
                    "LawsuitAge": 143,
                    "ResponseDecisions": [
                        {
                            "DecisionContent": "Decisão condenatória",
                            "DecisionDate": "2022-05-20T00:00:00"
                        }
                    ],
                    "ResponseParties": [
                        {
                            "Doc": "97179841072",
                            "IsPartyActive": "true",
                            "Name": "douglas portela fontella",
                            "Polarity": "passive",
                            "Type": "defendant",
                            "LastCaptureDate": "2021-10-02T23:49:09",
                            "PartyDetails": {
                                "SpecificType": "correu"
                            }
                        }
                    ]
                },
                {
                    "Number": "01482748120098217000",
                    "CourtType": "criminal",
                    "MainSubject": "trafico de drogas e condutas afins",
                    "PublicationDate": "2021-10-01T00:00:00",
                    "NoticeDate": "2009-10-19T00:00:00",
                    "RedistributionDate": "0001-01-01T00:00:00",
                    "LawsuitAge": 547,
                    "ResponseDecisions": [
                        {
                            "DecisionContent": "Decisão condenatória",
                            "DecisionDate": "2022-05-20T00:00:00"
                        }
                    ],
                    "ResponseParties": [
                        {
                            "Doc": "97179841072",
                            "IsPartyActive": "true",
                            "Name": "douglas portela fontella",
                            "Polarity": "passive",
                            "Type": "defendant",
                            "LastCaptureDate": "2021-10-02T23:45:53",
                            "PartyDetails": {
                                "SpecificType": "correu"
                            }
                        }
                    ]
                },
                {
                    "Number": "70027949056",
                    "CourtType": "criminal",
                    "MainSubject": "trafico de drogas e condutas afins",
                    "PublicationDate": "2021-10-01T00:00:00",
                    "NoticeDate": "2008-12-15T00:00:00",
                    "RedistributionDate": "0001-01-01T00:00:00",
                    "LawsuitAge": 121,
                    "ResponseDecisions": [
                        {
                            "DecisionContent": "Decisão condenatória",
                            "DecisionDate": "2022-05-20T00:00:00"
                        }
                    ],
                    "ResponseParties": [
                        {
                            "Doc": "97179841072",
                            "IsPartyActive": "true",
                            "Name": "douglas portela fontella",
                            "Polarity": "passive",
                            "Type": "defendant",
                            "LastCaptureDate": "2021-10-02T23:42:23",
                            "PartyDetails": {
                                "SpecificType": "correu"
                            }
                        }
                    ]
                }
            ]
        },
        "vehicle_owners": [
            {
                "person_uuid": "9619f6df-ca42-4979-b031-c8df9cb0cf82",
                "document": "97179841072",
                "name": "Maria Oliveira",
                "process": [
                    {
                        "Number": "456",
                        "CourtType": "Criminal",
                        "MainSubject": "Ameaca",
                        "PublicationDate": "2022-03-01T00:00:00",
                        "NoticeDate": "2022-03-10T00:00:00",
                        "RedistributionDate": "2022-03-12T00:00:00",
                        "LawsuitAge": 60,
                        "ResponseDecisions": [
                            {
                                "DecisionContent": "culpado",
                                "DecisionDate": "2022-03-12T00:00:00"
                            }
                        ],
                        "ResponseParties": [
                            {
                                "Doc": "97179841072",
                                "IsPartyActive": "true",
                                "Name": "Maria Oliveira",
                                "Polarity": "passive",
                                "Type": "defendant",
                                "LastCaptureDate": "2021-10-02T23:42:23",
                                "PartyDetails": {
                                    "SpecificType": "reu"
                                }
                            }
                        ]
                    }
                ]
            }
        ],
        "rntrc_owners": [
            {
                "person_uuid": "9619f6df-ca42-4979-b031-c8df9cb0cf82",
                "document": "97179841072",
                "name": "Maria Oliveira",
                "process": [
                    {
                        "Number": "456",
                        "CourtType": "Criminal",
                        "MainSubject": "Ameaca",
                        "PublicationDate": "2022-03-01T00:00:00",
                        "NoticeDate": "2022-03-10T00:00:00",
                        "RedistributionDate": "2022-03-12T00:00:00",
                        "LawsuitAge": 60,
                        "ResponseDecisions": [
                            {
                                "DecisionContent": "culpado",
                                "DecisionDate": "2022-03-12T00:00:00"
                            }
                        ],
                        "ResponseParties": [
                            {
                                "Doc": "97179841072",
                                "IsPartyActive": "true",
                                "Name": "Maria Oliveira",
                                "Polarity": "passive",
                                "Type": "defendant",
                                "LastCaptureDate": "2021-10-02T23:42:23",
                                "PartyDetails": {
                                    "SpecificType": "reu"
                                }
                            }
                        ]
                    }
                ]
            }
        ]
    }
    
    return input8

    
@pytest.fixture
def outputValidation8():
    d = {"person_uuid": ["b614401f-7928-11ec-a361-02fb9b06c548",
                        "b614401f-7928-11ec-a361-02fb9b06c548",
                        "b614401f-7928-11ec-a361-02fb9b06c548",
                        "b614401f-7928-11ec-a361-02fb9b06c548"],
         "MainSubject": ["trafico de drogas e condutas afins",
                 "trafico de drogas e condutas afins",
                 "trafico de drogas e condutas afins",
                 "trafico de drogas e condutas afins"],        
         "LawsuitAge": [147,143,547,121],
         "TimeDelta": [147,143,547,121],      
         "TimeDecay1": [0.961285, 0.962299, 0.869669, 0.967913],
         "TimeDecay2": [0.973853,0.974546,0.909166,0.978377],             
         "TimeDecay3": [0.980261,0.980787,0.930292,0.983695],
         "TimeDecay4": [0.984146,0.984571,0.943445,0.986913]}
    
    output8 = pd.DataFrame(data=d)
    
    return output8

@pytest.fixture
def inputValidation9():
    input9 = {
        "trucker": {
            "person_uuid": "b614401f-7928-11ec-a361-02fb9b06c548",
            "document": "97179841072",
            "name": "Douglas Portela Fontella",
            "process": [
                {
                    "Number": "04283166520118217000",
                    "CourtType": "criminal",
                    "MainSubject": "trafico de drogas e condutas afins",
                    "PublicationDate": "2021-10-01T00:00:00",
                    "NoticeDate": "2011-09-09T00:00:00",
                    "RedistributionDate": "0001-01-01T00:00:00",
                    "LawsuitAge": 147,
                    "ResponseDecisions": [
                        {
                            "DecisionContent": "Decisão condenatória",
                            "DecisionDate": "2022-05-20T00:00:00"
                        }
                    ],
                    "ResponseParties": [
                        {
                            "Doc": "97179841072",
                            "IsPartyActive": "true",
                            "Name": "douglas portela fontella",
                            "Polarity": "passive",
                            "Type": "defendant",
                            "LastCaptureDate": "2021-10-02T23:51:18",
                            "PartyDetails": {
                                "SpecificType": "correu"
                            }
                        }
                    ]
                },
                {
                    "Number": "01658943820118217000",
                    "CourtType": "criminal",
                    "MainSubject": "trafico de drogas e condutas afins",
                    "PublicationDate": "2021-10-01T00:00:00",
                    "NoticeDate": "2011-04-19T00:00:00",
                    "RedistributionDate": "0001-01-01T00:00:00",
                    "LawsuitAge": 143,
                    "ResponseDecisions": [
                        {
                            "DecisionContent": "Decisão condenatória",
                            "DecisionDate": "2022-05-20T00:00:00"
                        }
                    ],
                    "ResponseParties": [
                        {
                            "Doc": "97179841072",
                            "IsPartyActive": "true",
                            "Name": "douglas portela fontella",
                            "Polarity": "passive",
                            "Type": "defendant",
                            "LastCaptureDate": "2021-10-02T23:49:09",
                            "PartyDetails": {
                                "SpecificType": "correu"
                            }
                        }
                    ]
                },
                {
                    "Number": "01482748120098217000",
                    "CourtType": "criminal",
                    "MainSubject": "trafico de drogas e condutas afins",
                    "PublicationDate": "2021-10-01T00:00:00",
                    "NoticeDate": "2009-10-19T00:00:00",
                    "RedistributionDate": "0001-01-01T00:00:00",
                    "LawsuitAge": 547,
                    "ResponseDecisions": [
                        {
                            "DecisionContent": "Decisão condenatória",
                            "DecisionDate": "2022-05-20T00:00:00"
                        }
                    ],
                    "ResponseParties": [
                        {
                            "Doc": "97179841072",
                            "IsPartyActive": "true",
                            "Name": "douglas portela fontella",
                            "Polarity": "passive",
                            "Type": "defendant",
                            "LastCaptureDate": "2021-10-02T23:45:53",
                            "PartyDetails": {
                                "SpecificType": "correu"
                            }
                        }
                    ]
                },
                {
                    "Number": "70027949056",
                    "CourtType": "criminal",
                    "MainSubject": "trafico de drogas e condutas afins",
                    "PublicationDate": "2021-10-01T00:00:00",
                    "NoticeDate": "2008-12-15T00:00:00",
                    "RedistributionDate": "0001-01-01T00:00:00",
                    "LawsuitAge": 121,
                    "ResponseDecisions": [
                        {
                            "DecisionContent": "Decisão condenatória",
                            "DecisionDate": "2022-05-20T00:00:00"
                        }
                    ],
                    "ResponseParties": [
                        {
                            "Doc": "97179841072",
                            "IsPartyActive": "true",
                            "Name": "douglas portela fontella",
                            "Polarity": "passive",
                            "Type": "defendant",
                            "LastCaptureDate": "2021-10-02T23:42:23",
                            "PartyDetails": {
                                "SpecificType": "correu"
                            }
                        }
                    ]
                }
            ]
        },
        "vehicle_owners": [
            {
                "person_uuid": "9619f6df-ca42-4979-b031-c8df9cb0cf82",
                "document": "97179841072",
                "name": "Maria Oliveira",
                "process": [
                    {
                        "Number": "456",
                        "CourtType": "Criminal",
                        "MainSubject": "Ameaca",
                        "PublicationDate": "2022-03-01T00:00:00",
                        "NoticeDate": "2022-03-10T00:00:00",
                        "RedistributionDate": "2022-03-12T00:00:00",
                        "LawsuitAge": 60,
                        "ResponseDecisions": [
                            {
                                "DecisionContent": "culpado",
                                "DecisionDate": "2022-03-12T00:00:00"
                            }
                        ],
                        "ResponseParties": [
                            {
                                "Doc": "97179841072",
                                "IsPartyActive": "true",
                                "Name": "Maria Oliveira",
                                "Polarity": "passive",
                                "Type": "defendant",
                                "LastCaptureDate": "2021-10-02T23:42:23",
                                "PartyDetails": {
                                    "SpecificType": "reu"
                                }
                            }
                        ]
                    }
                ]
            }
        ],
        "rntrc_owners": [
            {
                "person_uuid": "9619f6df-ca42-4979-b031-c8df9cb0cf82",
                "document": "97179841072",
                "name": "Maria Oliveira",
                "process": [
                    {
                        "Number": "456",
                        "CourtType": "Criminal",
                        "MainSubject": "Ameaca",
                        "PublicationDate": "2022-03-01T00:00:00",
                        "NoticeDate": "2022-03-10T00:00:00",
                        "RedistributionDate": "2022-03-12T00:00:00",
                        "LawsuitAge": 60,
                        "ResponseDecisions": [
                            {
                                "DecisionContent": "culpado",
                                "DecisionDate": "2022-03-12T00:00:00"
                            }
                        ],
                        "ResponseParties": [
                            {
                                "Doc": "97179841072",
                                "IsPartyActive": "true",
                                "Name": "Maria Oliveira",
                                "Polarity": "passive",
                                "Type": "defendant",
                                "LastCaptureDate": "2021-10-02T23:42:23",
                                "PartyDetails": {
                                    "SpecificType": "reu"
                                }
                            }
                        ]
                    }
                ]
            }
        ]
    }
    
    return input9
    
@pytest.fixture
def outputValidation9():
    d = {'trucker_id': ['b614401f-7928-11ec-a361-02fb9b06c548',
          'b614401f-7928-11ec-a361-02fb9b06c548',
          'b614401f-7928-11ec-a361-02fb9b06c548',
          'b614401f-7928-11ec-a361-02fb9b06c548'],
         'LawsuitAge': [147, 143, 547, 121],
         'TimeDelta': [147, 143, 547, 121],
         'TimeDecay1': [0.9612852251777719,
          0.9622989717901397,
          0.8696688110555159,
          0.967913020418987],
         'TimeDecay2': [0.9738527214514408,
          0.9745461018155926,
          0.9091663899036865,
          0.9783774124374554],
         'TimeDecay3': [0.9802605075869478,
          0.9807873169420933,
          0.930291831273098,
          0.9836949198221265],
         'TimeDecay4': [0.9841458153580673,
          0.9845705653862753,
          0.9434449958643507,
          0.9869132597880165],
         'homicidio': [0, 0, 0, 0],
         'roubo': [0, 0, 0, 0],
         'furto': [0, 0, 0, 0],
         'lesao corporal': [0, 0, 0, 0],
         'ameaca': [0, 0, 0, 0],
         'contra a vida': [0, 0, 0, 0],
         'medidas protetivas': [0, 0, 0, 0],
         'pudor': [0, 0, 0, 0],
         'sistema nacional de armas': [0, 0, 0, 0],
         'porte ilegal de arma': [0, 0, 0, 0],
         'disparo de arma': [0, 0, 0, 0],
         'extorsao': [0, 0, 0, 0],
         'sequestro': [0, 0, 0, 0],
         'estupro': [0, 0, 0, 0],
         'violacao de domicilio': [0, 0, 0, 0],
         'violencia domestica': [0, 0, 0, 0],
         'esbulho': [0, 0, 0, 0],
         'turbacao': [0, 0, 0, 0],
         'trafico': [1, 1, 1, 1],
         'dano material': [0, 0, 0, 0],
         'infanticidio': [0, 0, 0, 0],
         'matar': [0, 0, 0, 0],
         'morte': [0, 0, 0, 0],
         'omissao de socorro': [0, 0, 0, 0],
         'carcere': [0, 0, 0, 0],
         'corrupcao': [0, 0, 0, 0],
         'corrupcao de menores': [0, 0, 0, 0],
         'feminicidio': [0, 0, 0, 0],
         'abuso de vulneravel': [0, 0, 0, 0],
         'maria da penha': [0, 0, 0, 0],
         'latrocinio': [0, 0, 0, 0],
         'organizacao criminosa': [0, 0, 0, 0],
         'terrorista': [0, 0, 0, 0],
         'associacao criminosa': [0, 0, 0, 0],
         'escravo': [0, 0, 0, 0],
         'transito': [0, 0, 0, 0],
         'veiculo': [0, 0, 0, 0],
         'embriaguez': [0, 0, 0, 0],
         'volante': [0, 0, 0, 0],
         'direcao': [0, 0, 0, 0],
         'velocidade': [0, 0, 0, 0],
         'transporte irregular': [0, 0, 0, 0],
         'acidente de transito': [0, 0, 0, 0],
         'cnh': [0, 0, 0, 0],
         'transporte de coisas': [0, 0, 0, 0],
         'influencia de alcool': [0, 0, 0, 0],
         'direcao perigosa': [0, 0, 0, 0],
         'disputar corrida': [0, 0, 0, 0],
         'manobra perigosa': [0, 0, 0, 0],
         'racha': [0, 0, 0, 0],
         'fraude': [0, 0, 0, 0],
         'lei antitoxicos': [0, 0, 0, 0],
         'quadrilha': [0, 0, 0, 0],
         'contrabando': [0, 0, 0, 0],
         'descaminho': [0, 0, 0, 0],
         'receptacao': [0, 0, 0, 0],
         'documento falso': [0, 0, 0, 0],
         'estelionato': [0, 0, 0, 0],
         'falsificacao': [0, 0, 0, 0],
         'falsidade ideologica': [0, 0, 0, 0],
         'enriquecimento': [0, 0, 0, 0],
         'fuga': [0, 0, 0, 0]}
    
    output9 = pd.DataFrame(data=d)
    
    return output9

@pytest.fixture
def inputValidation10():
    input10 = {
        "trucker": {
            "person_uuid": "b614401f-7928-11ec-a361-02fb9b06c548",
            "document": "97179841072",
            "name": "Douglas Portela Fontella",
            "process": [
                {
                    "Number": "04283166520118217000",
                    "CourtType": "criminal",
                    "MainSubject": "direcao de veiculo sob influencia de alcool",
                    "PublicationDate": "2021-10-01T00:00:00",
                    "NoticeDate": "2011-09-09T00:00:00",
                    "RedistributionDate": "0001-01-01T00:00:00",
                    "LawsuitAge": 147,
                    "ResponseDecisions": [
                        {
                            "DecisionContent": "Decisão condenatória",
                            "DecisionDate": "2022-05-20T00:00:00"
                        }
                    ],
                    "ResponseParties": [
                        {
                            "Doc": "97179841072",
                            "IsPartyActive": "true",
                            "Name": "douglas portela fontella",
                            "Polarity": "passive",
                            "Type": "defendant",
                            "LastCaptureDate": "2021-10-02T23:51:18",
                            "PartyDetails": {
                                "SpecificType": "correu"
                            }
                        }
                    ]
                },
                {
                    "Number": "01658943820118217000",
                    "CourtType": "criminal",
                    "MainSubject": "embriaguez ao volante",
                    "PublicationDate": "2021-10-01T00:00:00",
                    "NoticeDate": "2011-04-19T00:00:00",
                    "RedistributionDate": "0001-01-01T00:00:00",
                    "LawsuitAge": 143,
                    "ResponseDecisions": [
                        {
                            "DecisionContent": "Decisão condenatória",
                            "DecisionDate": "2022-05-20T00:00:00"
                        }
                    ],
                    "ResponseParties": [
                        {
                            "Doc": "97179841072",
                            "IsPartyActive": "true",
                            "Name": "douglas portela fontella",
                            "Polarity": "passive",
                            "Type": "defendant",
                            "LastCaptureDate": "2021-10-02T23:49:09",
                            "PartyDetails": {
                                "SpecificType": "correu"
                            }
                        }
                    ]
                },
                {
                    "Number": "01482748120098217000",
                    "CourtType": "criminal",
                    "MainSubject": "homicidio, crimes contra a vida",
                    "PublicationDate": "2021-10-01T00:00:00",
                    "NoticeDate": "2009-10-19T00:00:00",
                    "RedistributionDate": "0001-01-01T00:00:00",
                    "LawsuitAge": 547,
                    "ResponseDecisions": [
                        {
                            "DecisionContent": "Decisão condenatória",
                            "DecisionDate": "2022-05-20T00:00:00"
                        }
                    ],
                    "ResponseParties": [
                        {
                            "Doc": "97179841072",
                            "IsPartyActive": "true",
                            "Name": "douglas portela fontella",
                            "Polarity": "passive",
                            "Type": "defendant",
                            "LastCaptureDate": "2021-10-02T23:45:53",
                            "PartyDetails": {
                                "SpecificType": "correu"
                            }
                        }
                    ]
                },
                {
                    "Number": "70027949056",
                    "CourtType": "criminal",
                    "MainSubject": "contrabando / descaminho, acidente de transito",
                    "PublicationDate": "2021-10-01T00:00:00",
                    "NoticeDate": "2008-12-15T00:00:00",
                    "RedistributionDate": "0001-01-01T00:00:00",
                    "LawsuitAge": 121,
                    "ResponseDecisions": [
                        {
                            "DecisionContent": "Decisão condenatória",
                            "DecisionDate": "2022-05-20T00:00:00"
                        }
                    ],
                    "ResponseParties": [
                        {
                            "Doc": "97179841072",
                            "IsPartyActive": "true",
                            "Name": "douglas portela fontella",
                            "Polarity": "passive",
                            "Type": "defendant",
                            "LastCaptureDate": "2021-10-02T23:42:23",
                            "PartyDetails": {
                                "SpecificType": "correu"
                            }
                        }
                    ]
                }
            ]
        },
        "vehicle_owners": [
            {
                "person_uuid": "9619f6df-ca42-4979-b031-c8df9cb0cf82",
                "document": "97179841072",
                "name": "Maria Oliveira",
                "process": [
                    {
                        "Number": "456",
                        "CourtType": "Criminal",
                        "MainSubject": "Ameaca",
                        "PublicationDate": "2022-03-01T00:00:00",
                        "NoticeDate": "2022-03-10T00:00:00",
                        "RedistributionDate": "2022-03-12T00:00:00",
                        "LawsuitAge": 60,
                        "ResponseDecisions": [
                            {
                                "DecisionContent": "culpado",
                                "DecisionDate": "2022-03-12T00:00:00"
                            }
                        ],
                        "ResponseParties": [
                            {
                                "Doc": "97179841072",
                                "IsPartyActive": "true",
                                "Name": "Maria Oliveira",
                                "Polarity": "passive",
                                "Type": "defendant",
                                "LastCaptureDate": "2021-10-02T23:42:23",
                                "PartyDetails": {
                                    "SpecificType": "reu"
                                }
                            }
                        ]
                    }
                ]
            }
        ],
        "rntrc_owners": [
            {
                "person_uuid": "9619f6df-ca42-4979-b031-c8df9cb0cf82",
                "document": "97179841072",
                "name": "Maria Oliveira",
                "process": [
                    {
                        "Number": "456",
                        "CourtType": "Criminal",
                        "MainSubject": "Ameaca",
                        "PublicationDate": "2022-03-01T00:00:00",
                        "NoticeDate": "2022-03-10T00:00:00",
                        "RedistributionDate": "2022-03-12T00:00:00",
                        "LawsuitAge": 60,
                        "ResponseDecisions": [
                            {
                                "DecisionContent": "culpado",
                                "DecisionDate": "2022-03-12T00:00:00"
                            }
                        ],
                        "ResponseParties": [
                            {
                                "Doc": "97179841072",
                                "IsPartyActive": "true",
                                "Name": "Maria Oliveira",
                                "Polarity": "passive",
                                "Type": "defendant",
                                "LastCaptureDate": "2021-10-02T23:42:23",
                                "PartyDetails": {
                                    "SpecificType": "reu"
                                }
                            }
                        ]
                    }
                ]
            }
        ]
    }
    
    return input10

@pytest.fixture
def outputValidation10():
    d = {'trucker_id': ['b614401f-7928-11ec-a361-02fb9b06c548',
          'b614401f-7928-11ec-a361-02fb9b06c548',
          'b614401f-7928-11ec-a361-02fb9b06c548',
          'b614401f-7928-11ec-a361-02fb9b06c548'],
         'LawsuitAge': [147, 143, 547, 121],
         'TimeDelta': [147, 143, 547, 121],
         'TimeDecay1': [0.9612852251777719,
          0.9622989717901397,
          0.8696688110555159,
          0.967913020418987],
         'TimeDecay2': [0.9738527214514408,
          0.9745461018155926,
          0.9091663899036865,
          0.9783774124374554],
         'TimeDecay3': [0.9802605075869478,
          0.9807873169420933,
          0.930291831273098,
          0.9836949198221265],
         'TimeDecay4': [0.9841458153580673,
          0.9845705653862753,
          0.9434449958643507,
          0.9869132597880165],
         'homicidio': [0, 0, 1, 0],
         'roubo': [0, 0, 0, 0],
         'furto': [0, 0, 0, 0],
         'lesao corporal': [0, 0, 0, 0],
         'ameaca': [0, 0, 0, 0],
         'contra a vida': [0, 0, 0, 0],
         'medidas protetivas': [0, 0, 0, 0],
         'pudor': [0, 0, 0, 0],
         'sistema nacional de armas': [0, 0, 0, 0],
         'porte ilegal de arma': [0, 0, 0, 0],
         'disparo de arma': [0, 0, 0, 0],
         'extorsao': [0, 0, 0, 0],
         'sequestro': [0, 0, 0, 0],
         'estupro': [0, 0, 0, 0],
         'violacao de domicilio': [0, 0, 0, 0],
         'violencia domestica': [0, 0, 0, 0],
         'esbulho': [0, 0, 0, 0],
         'turbacao': [0, 0, 0, 0],
         'trafico': [0, 0, 0, 0],
         'dano material': [0, 0, 0, 0],
         'infanticidio': [0, 0, 0, 0],
         'matar': [0, 0, 0, 0],
         'morte': [0, 0, 0, 0],
         'omissao de socorro': [0, 0, 0, 0],
         'carcere': [0, 0, 0, 0],
         'corrupcao': [0, 0, 0, 0],
         'corrupcao de menores': [0, 0, 0, 0],
         'feminicidio': [0, 0, 0, 0],
         'abuso de vulneravel': [0, 0, 0, 0],
         'maria da penha': [0, 0, 0, 0],
         'latrocinio': [0, 0, 0, 0],
         'organizacao criminosa': [0, 0, 0, 0],
         'terrorista': [0, 0, 0, 0],
         'associacao criminosa': [0, 0, 0, 0],
         'escravo': [0, 0, 0, 0],
         'transito': [0, 0, 0, 0],
         'veiculo': [0, 0, 0, 0],
         'embriaguez': [0, 0, 0, 0],
         'volante': [0, 1, 0, 0],
         'direcao': [0, 0, 0, 0],
         'velocidade': [0, 0, 0, 0],
         'transporte irregular': [0, 0, 0, 0],
         'acidente de transito': [0, 0, 0, 1],
         'cnh': [0, 0, 0, 0],
         'transporte de coisas': [0, 0, 0, 0],
         'influencia de alcool': [1, 0, 0, 0],
         'direcao perigosa': [0, 0, 0, 0],
         'disputar corrida': [0, 0, 0, 0],
         'manobra perigosa': [0, 0, 0, 0],
         'racha': [0, 0, 0, 0],
         'fraude': [0, 0, 0, 0],
         'lei antitoxicos': [0, 0, 0, 0],
         'quadrilha': [0, 0, 0, 0],
         'contrabando': [0, 0, 0, 0],
         'descaminho': [0, 0, 0, 1],
         'receptacao': [0, 0, 0, 0],
         'documento falso': [0, 0, 0, 0],
         'estelionato': [0, 0, 0, 0],
         'falsificacao': [0, 0, 0, 0],
         'falsidade ideologica': [0, 0, 0, 0],
         'enriquecimento': [0, 0, 0, 0],
         'fuga': [0, 0, 0, 0]}
    
    output10 = pd.DataFrame(data=d)
    
    return output10

@pytest.fixture
def inputValidation11():
    input11 = {
        "trucker": {
            "person_uuid": "b614401f-7928-11ec-a361-02fb9b06c548",
            "document": "97179841072",
            "name": "Douglas Portela Fontella",
            "process": [
                {
                    "Number": "04283166520118217000",
                    "CourtType": "criminal",
                    "MainSubject": "homicidio, crimes de transito, crimes contra a vida",
                    "PublicationDate": "2021-10-01T00:00:00",
                    "NoticeDate": "2011-09-09T00:00:00",
                    "RedistributionDate": "0001-01-01T00:00:00",
                    "LawsuitAge": 147,
                    "ResponseDecisions": [
                        {
                            "DecisionContent": "Decisão condenatória",
                            "DecisionDate": "2022-05-20T00:00:00"
                        }
                    ],
                    "ResponseParties": [
                        {
                            "Doc": "97179841072",
                            "IsPartyActive": "true",
                            "Name": "douglas portela fontella",
                            "Polarity": "passive",
                            "Type": "defendant",
                            "LastCaptureDate": "2021-10-02T23:51:18",
                            "PartyDetails": {
                                "SpecificType": "correu"
                            }
                        }
                    ]
                },
                {
                    "Number": "01658943820118217000",
                    "CourtType": "criminal",
                    "MainSubject": "crimes de transito, lesao corporal na direção de veiculo",
                    "PublicationDate": "2021-10-01T00:00:00",
                    "NoticeDate": "2011-04-19T00:00:00",
                    "RedistributionDate": "0001-01-01T00:00:00",
                    "LawsuitAge": 143,
                    "ResponseDecisions": [
                        {
                            "DecisionContent": "Decisão condenatória",
                            "DecisionDate": "2022-05-20T00:00:00"
                        }
                    ],
                    "ResponseParties": [
                        {
                            "Doc": "97179841072",
                            "IsPartyActive": "true",
                            "Name": "douglas portela fontella",
                            "Polarity": "passive",
                            "Type": "defendant",
                            "LastCaptureDate": "2021-10-02T23:49:09",
                            "PartyDetails": {
                                "SpecificType": "correu"
                            }
                        }
                    ]
                },
                {
                    "Number": "01482748120098217000",
                    "CourtType": "criminal",
                    "MainSubject": "lesao corporal na direcao de veiculo",
                    "PublicationDate": "2021-10-01T00:00:00",
                    "NoticeDate": "2009-10-19T00:00:00",
                    "RedistributionDate": "0001-01-01T00:00:00",
                    "LawsuitAge": 547,
                    "ResponseDecisions": [
                        {
                            "DecisionContent": "Decisão condenatória",
                            "DecisionDate": "2022-05-20T00:00:00"
                        }
                    ],
                    "ResponseParties": [
                        {
                            "Doc": "97179841072",
                            "IsPartyActive": "true",
                            "Name": "douglas portela fontella",
                            "Polarity": "passive",
                            "Type": "defendant",
                            "LastCaptureDate": "2021-10-02T23:45:53",
                            "PartyDetails": {
                                "SpecificType": "correu"
                            }
                        }
                    ]
                },
                {
                    "Number": "70027949056",
                    "CourtType": "criminal",
                    "MainSubject": "furto / roubo de veiculo",
                    "PublicationDate": "2021-10-01T00:00:00",
                    "NoticeDate": "2008-12-15T00:00:00",
                    "RedistributionDate": "0001-01-01T00:00:00",
                    "LawsuitAge": 121,
                    "ResponseDecisions": [
                        {
                            "DecisionContent": "Decisão condenatória",
                            "DecisionDate": "2022-05-20T00:00:00"
                        }
                    ],
                    "ResponseParties": [
                        {
                            "Doc": "97179841072",
                            "IsPartyActive": "true",
                            "Name": "douglas portela fontella",
                            "Polarity": "passive",
                            "Type": "defendant",
                            "LastCaptureDate": "2021-10-02T23:42:23",
                            "PartyDetails": {
                                "SpecificType": "correu"
                            }
                        }
                    ]
                }
            ]
        },
        "vehicle_owners": [
            {
                "person_uuid": "9619f6df-ca42-4979-b031-c8df9cb0cf82",
                "document": "97179841072",
                "name": "Maria Oliveira",
                "process": [
                    {
                        "Number": "456",
                        "CourtType": "Criminal",
                        "MainSubject": "Ameaca",
                        "PublicationDate": "2022-03-01T00:00:00",
                        "NoticeDate": "2022-03-10T00:00:00",
                        "RedistributionDate": "2022-03-12T00:00:00",
                        "LawsuitAge": 60,
                        "ResponseDecisions": [
                            {
                                "DecisionContent": "culpado",
                                "DecisionDate": "2022-03-12T00:00:00"
                            }
                        ],
                        "ResponseParties": [
                            {
                                "Doc": "97179841072",
                                "IsPartyActive": "true",
                                "Name": "Maria Oliveira",
                                "Polarity": "passive",
                                "Type": "defendant",
                                "LastCaptureDate": "2021-10-02T23:42:23",
                                "PartyDetails": {
                                    "SpecificType": "reu"
                                }
                            }
                        ]
                    }
                ]
            }
        ],
        "rntrc_owners": [
            {
                "person_uuid": "9619f6df-ca42-4979-b031-c8df9cb0cf82",
                "document": "97179841072",
                "name": "Maria Oliveira",
                "process": [
                    {
                        "Number": "456",
                        "CourtType": "Criminal",
                        "MainSubject": "Ameaca",
                        "PublicationDate": "2022-03-01T00:00:00",
                        "NoticeDate": "2022-03-10T00:00:00",
                        "RedistributionDate": "2022-03-12T00:00:00",
                        "LawsuitAge": 60,
                        "ResponseDecisions": [
                            {
                                "DecisionContent": "culpado",
                                "DecisionDate": "2022-03-12T00:00:00"
                            }
                        ],
                        "ResponseParties": [
                            {
                                "Doc": "97179841072",
                                "IsPartyActive": "true",
                                "Name": "Maria Oliveira",
                                "Polarity": "passive",
                                "Type": "defendant",
                                "LastCaptureDate": "2021-10-02T23:42:23",
                                "PartyDetails": {
                                    "SpecificType": "reu"
                                }
                            }
                        ]
                    }
                ]
            }
        ]
    }
    
    return input11

@pytest.fixture
def outputValidation11():
    d = {'trucker_id': ['b614401f-7928-11ec-a361-02fb9b06c548',
          'b614401f-7928-11ec-a361-02fb9b06c548',
          'b614401f-7928-11ec-a361-02fb9b06c548',
          'b614401f-7928-11ec-a361-02fb9b06c548'],
         'LawsuitAge': [147, 143, 547, 121],
         'TimeDelta': [147, 143, 547, 121],
         'TimeDecay1': [0.9612852251777719,
          0.9622989717901397,
          0.8696688110555159,
          0.967913020418987],
         'TimeDecay2': [0.9738527214514408,
          0.9745461018155926,
          0.9091663899036865,
          0.9783774124374554],
         'TimeDecay3': [0.9802605075869478,
          0.9807873169420933,
          0.930291831273098,
          0.9836949198221265],
         'TimeDecay4': [0.9841458153580673,
          0.9845705653862753,
          0.9434449958643507,
          0.9869132597880165],
         'homicidio': [0, 0, 0, 0],
         'roubo': [0, 0, 0, 1],
         'furto': [0, 0, 0, 0],
         'lesao corporal': [0, 0, 0, 0],
         'ameaca': [0, 0, 0, 0],
         'contra a vida': [0, 0, 0, 0],
         'medidas protetivas': [0, 0, 0, 0],
         'pudor': [0, 0, 0, 0],
         'sistema nacional de armas': [0, 0, 0, 0],
         'porte ilegal de arma': [0, 0, 0, 0],
         'disparo de arma': [0, 0, 0, 0],
         'extorsao': [0, 0, 0, 0],
         'sequestro': [0, 0, 0, 0],
         'estupro': [0, 0, 0, 0],
         'violacao de domicilio': [0, 0, 0, 0],
         'violencia domestica': [0, 0, 0, 0],
         'esbulho': [0, 0, 0, 0],
         'turbacao': [0, 0, 0, 0],
         'trafico': [0, 0, 0, 0],
         'dano material': [0, 0, 0, 0],
         'infanticidio': [0, 0, 0, 0],
         'matar': [0, 0, 0, 0],
         'morte': [0, 0, 0, 0],
         'omissao de socorro': [0, 0, 0, 0],
         'carcere': [0, 0, 0, 0],
         'corrupcao': [0, 0, 0, 0],
         'corrupcao de menores': [0, 0, 0, 0],
         'feminicidio': [0, 0, 0, 0],
         'abuso de vulneravel': [0, 0, 0, 0],
         'maria da penha': [0, 0, 0, 0],
         'latrocinio': [0, 0, 0, 0],
         'organizacao criminosa': [0, 0, 0, 0],
         'terrorista': [0, 0, 0, 0],
         'associacao criminosa': [0, 0, 0, 0],
         'escravo': [0, 0, 0, 0],
         'transito': [1, 1, 0, 0],
         'veiculo': [0, 0, 1, 1],
         'embriaguez': [0, 0, 0, 0],
         'volante': [0, 0, 0, 0],
         'direcao': [0, 0, 0, 0],
         'velocidade': [0, 0, 0, 0],
         'transporte irregular': [0, 0, 0, 0],
         'acidente de transito': [0, 0, 0, 0],
         'cnh': [0, 0, 0, 0],
         'transporte de coisas': [0, 0, 0, 0],
         'influencia de alcool': [0, 0, 0, 0],
         'direcao perigosa': [0, 0, 0, 0],
         'disputar corrida': [0, 0, 0, 0],
         'manobra perigosa': [0, 0, 0, 0],
         'racha': [0, 0, 0, 0],
         'fraude': [0, 0, 0, 0],
         'lei antitoxicos': [0, 0, 0, 0],
         'quadrilha': [0, 0, 0, 0],
         'contrabando': [0, 0, 0, 0],
         'descaminho': [0, 0, 0, 0],
         'receptacao': [0, 0, 0, 0],
         'documento falso': [0, 0, 0, 0],
         'estelionato': [0, 0, 0, 0],
         'falsificacao': [0, 0, 0, 0],
         'falsidade ideologica': [0, 0, 0, 0],
         'enriquecimento': [0, 0, 0, 0],
         'fuga': [0, 0, 0, 0]}
    
    output11 = pd.DataFrame(data=d)
    
    return output11
    

@pytest.fixture
def inputValidation12():
    input12 = {"person_uuid": ["b614401f-7928-11ec-a361-02fb9b06c548"],
         "document": ["97179841072"],        
         "name": ["douglas portela fontella"],
         "Doc": ["6654444"],
         "Name": ["dougla portela fontella"]}
    
    return input12


@pytest.fixture
def outputValidation12():
    d = {"person_uuid": ["b614401f-7928-11ec-a361-02fb9b06c548"],
         "document": ["97179841072"],        
         "name": ["douglas portela fontella"],
         "Doc": ["6654444"],
         "Name": ["dougla portela fontella"],
         "token_set_ratio": 97.87234042553192}

    output12 = pd.DataFrame(data=d)
    return output12

@pytest.fixture
def inputValidation13():
    input13 = {
        "trucker": {
            "person_uuid": "b614401f-7928-11ec-a361-02fb9b06c548",
            "document": "97179841072",
            "name": "Douglas Portela Fontella",
            "process": [
                {
                    "Number": "04283166520118217000",
                    "CourtType": "criminal",
                    "MainSubject": "trafico de drogas e condutas afins",
                    "PublicationDate": "2021-10-01T00:00:00",
                    "NoticeDate": "2011-09-09T00:00:00",
                    "RedistributionDate": "0001-01-01T00:00:00",
                    "LawsuitAge": 147,
                    "ResponseDecisions": [
                        {
                            "DecisionContent": "Decisão condenatória",
                            "DecisionDate": "2022-05-20T00:00:00"
                        }
                    ],
                    "ResponseParties": [
                        {
                            "Doc": "97179841072",
                            "IsPartyActive": "true",
                            "Name": "douglas portela fontella",
                            "Polarity": "passive",
                            "Type": "defendant",
                            "LastCaptureDate": "2021-10-02T23:51:18",
                            "PartyDetails": {
                                "SpecificType": "correu"
                            }
                        }
                    ]
                },
                {
                    "Number": "01658943820118217000",
                    "CourtType": "criminal",
                    "MainSubject": "trafico de drogas e condutas afins",
                    "PublicationDate": "2021-10-01T00:00:00",
                    "NoticeDate": "2011-04-19T00:00:00",
                    "RedistributionDate": "0001-01-01T00:00:00",
                    "LawsuitAge": 143,
                    "ResponseDecisions": [
                        {
                            "DecisionContent": "Decisão condenatória",
                            "DecisionDate": "2022-05-20T00:00:00"
                        }
                    ],
                    "ResponseParties": [
                        {
                            "Doc": "97179841072",
                            "IsPartyActive": "true",
                            "Name": "douglas portela fontella",
                            "Polarity": "passive",
                            "Type": "defendant",
                            "LastCaptureDate": "2021-10-02T23:49:09",
                            "PartyDetails": {
                                "SpecificType": "correu"
                            }
                        }
                    ]
                },
                {
                    "Number": "01482748120098217000",
                    "CourtType": "criminal",
                    "MainSubject": "trafico de drogas e condutas afins",
                    "PublicationDate": "2021-10-01T00:00:00",
                    "NoticeDate": "2009-10-19T00:00:00",
                    "RedistributionDate": "0001-01-01T00:00:00",
                    "LawsuitAge": 547,
                    "ResponseDecisions": [
                        {
                            "DecisionContent": "Decisão condenatória",
                            "DecisionDate": "2022-05-20T00:00:00"
                        }
                    ],
                    "ResponseParties": [
                        {
                            "Doc": "97179841072",
                            "IsPartyActive": "true",
                            "Name": "douglas portela fontella",
                            "Polarity": "passive",
                            "Type": "defendant",
                            "LastCaptureDate": "2021-10-02T23:45:53",
                            "PartyDetails": {
                                "SpecificType": "correu"
                            }
                        }
                    ]
                },
                {
                    "Number": "70027949056",
                    "CourtType": "criminal",
                    "MainSubject": "trafico de drogas e condutas afins",
                    "PublicationDate": "2021-10-01T00:00:00",
                    "NoticeDate": "2008-12-15T00:00:00",
                    "RedistributionDate": "0001-01-01T00:00:00",
                    "LawsuitAge": 121,
                    "ResponseDecisions": [
                        {
                            "DecisionContent": "Decisão condenatória",
                            "DecisionDate": "2022-05-20T00:00:00"
                        }
                    ],
                    "ResponseParties": [
                        {
                            "Doc": "97179841072",
                            "IsPartyActive": "true",
                            "Name": "douglas portela fontella",
                            "Polarity": "passive",
                            "Type": "defendant",
                            "LastCaptureDate": "2021-10-02T23:42:23",
                            "PartyDetails": {
                                "SpecificType": "correu"
                            }
                        }
                    ]
                }
            ]
        },
        "vehicle_owners": [
            {
                "person_uuid": "9619f6df-ca42-4979-b031-c8df9cb0cf82",
                "document": "97179841072",
                "name": "Maria Oliveira",
                "process": [
                    {
                        "Number": "456",
                        "CourtType": "Criminal",
                        "MainSubject": "Ameaca",
                        "PublicationDate": "2022-03-01T00:00:00",
                        "NoticeDate": "2022-03-10T00:00:00",
                        "RedistributionDate": "2022-03-12T00:00:00",
                        "LawsuitAge": 60,
                        "ResponseDecisions": [
                            {
                                "DecisionContent": "culpado",
                                "DecisionDate": "2022-03-12T00:00:00"
                            }
                        ],
                        "ResponseParties": [
                            {
                                "Doc": "97179841072",
                                "IsPartyActive": "true",
                                "Name": "Maria Oliveira",
                                "Polarity": "passive",
                                "Type": "defendant",
                                "LastCaptureDate": "2021-10-02T23:42:23",
                                "PartyDetails": {
                                    "SpecificType": "reu"
                                }
                            }
                        ]
                    }
                ]
            }
        ],
        "rntrc_owners": [
            {
                "person_uuid": "9619f6df-ca42-4979-b031-c8df9cb0cf82",
                "document": "97179841072",
                "name": "Maria Oliveira",
                "process": [
                    {
                        "Number": "456",
                        "CourtType": "Criminal",
                        "MainSubject": "Ameaca",
                        "PublicationDate": "2022-03-01T00:00:00",
                        "NoticeDate": "2022-03-10T00:00:00",
                        "RedistributionDate": "2022-03-12T00:00:00",
                        "LawsuitAge": 60,
                        "ResponseDecisions": [
                            {
                                "DecisionContent": "culpado",
                                "DecisionDate": "2022-03-12T00:00:00"
                            }
                        ],
                        "ResponseParties": [
                            {
                                "Doc": "97179841072",
                                "IsPartyActive": "true",
                                "Name": "Maria Oliveira",
                                "Polarity": "passive",
                                "Type": "defendant",
                                "LastCaptureDate": "2021-10-02T23:42:23",
                                "PartyDetails": {
                                    "SpecificType": "reu"
                                }
                            }
                        ]
                    }
                ]
            }
        ]
    }
    
    return input13


@pytest.fixture
def outputValidation13():

    d = {'person_uuid': ['b614401f-7928-11ec-a361-02fb9b06c548',
      'b614401f-7928-11ec-a361-02fb9b06c548',
      'b614401f-7928-11ec-a361-02fb9b06c548',
      'b614401f-7928-11ec-a361-02fb9b06c548'],
     'LawsuitAge': [147, 143, 547, 121],
     'TimeDelta': [147, 143, 547, 121],
     'TimeDecay1': [0.9612852251777719,
      0.9622989717901397,
      0.8696688110555159,
      0.967913020418987],
     'TimeDecay2': [0.9738527214514408,
      0.9745461018155926,
      0.9091663899036865,
      0.9783774124374554],
     'TimeDecay3': [0.9802605075869478,
      0.9807873169420933,
      0.930291831273098,
      0.9836949198221265],
     'TimeDecay4': [0.9841458153580673,
      0.9845705653862753,
      0.9434449958643507,
      0.9869132597880165],
     'homicidio': [0, 0, 0, 0],
     'roubo': [0, 0, 0, 0],
     'furto': [0, 0, 0, 0],
     'lesao corporal': [0, 0, 0, 0],
     'ameaca': [0, 0, 0, 0],
     'contra a vida': [0, 0, 0, 0],
     'medidas protetivas': [0, 0, 0, 0],
     'pudor': [0, 0, 0, 0],
     'sistema nacional de armas': [0, 0, 0, 0],
     'porte ilegal de arma': [0, 0, 0, 0],
     'disparo de arma': [0, 0, 0, 0],
     'extorsao': [0, 0, 0, 0],
     'sequestro': [0, 0, 0, 0],
     'estupro': [0, 0, 0, 0],
     'violacao de domicilio': [0, 0, 0, 0],
     'violencia domestica': [0, 0, 0, 0],
     'esbulho': [0, 0, 0, 0],
     'turbacao': [0, 0, 0, 0],
     'trafico': [1, 1, 1, 1],
     'dano material': [0, 0, 0, 0],
     'infanticidio': [0, 0, 0, 0],
     'matar': [0, 0, 0, 0],
     'morte': [0, 0, 0, 0],
     'omissao de socorro': [0, 0, 0, 0],
     'carcere': [0, 0, 0, 0],
     'corrupcao': [0, 0, 0, 0],
     'corrupcao de menores': [0, 0, 0, 0],
     'feminicidio': [0, 0, 0, 0],
     'abuso de vulneravel': [0, 0, 0, 0],
     'maria da penha': [0, 0, 0, 0],
     'latrocinio': [0, 0, 0, 0],
     'organizacao criminosa': [0, 0, 0, 0],
     'terrorista': [0, 0, 0, 0],
     'associacao criminosa': [0, 0, 0, 0],
     'escravo': [0, 0, 0, 0],
     'transito': [0, 0, 0, 0],
     'veiculo': [0, 0, 0, 0],
     'embriaguez': [0, 0, 0, 0],
     'volante': [0, 0, 0, 0],
     'direcao': [0, 0, 0, 0],
     'velocidade': [0, 0, 0, 0],
     'transporte irregular': [0, 0, 0, 0],
     'acidente de transito': [0, 0, 0, 0],
     'cnh': [0, 0, 0, 0],
     'transporte de coisas': [0, 0, 0, 0],
     'influencia de alcool': [0, 0, 0, 0],
     'direcao perigosa': [0, 0, 0, 0],
     'disputar corrida': [0, 0, 0, 0],
     'manobra perigosa': [0, 0, 0, 0],
     'racha': [0, 0, 0, 0],
     'fraude': [0, 0, 0, 0],
     'lei antitoxicos': [0, 0, 0, 0],
     'quadrilha': [0, 0, 0, 0],
     'contrabando': [0, 0, 0, 0],
     'descaminho': [0, 0, 0, 0],
     'receptacao': [0, 0, 0, 0],
     'documento falso': [0, 0, 0, 0],
     'estelionato': [0, 0, 0, 0],
     'falsificacao': [0, 0, 0, 0],
     'falsidade ideologica': [0, 0, 0, 0],
     'enriquecimento': [0, 0, 0, 0],
     'fuga': [0, 0, 0, 0],
     'FinalValue': [4, 4, 4, 4],
     1: [0, 0, 0, 0],
     2: [0, 0, 0, 0],
     3: [0, 0, 0, 0],
     4: [1, 1, 1, 1]}

    output13 = pd.DataFrame(data=d)
    return output13

@pytest.fixture
def inputValidation14():
    input14 = {
        "trucker": {
            "person_uuid": "b614401f-7928-11ec-a361-02fb9b06c548",
            "document": "97179841072",
            "name": "Douglas Portela Fontella",
            "process": [
                {
                    "Number": "04283166520118217000",
                    "CourtType": "criminal",
                    "MainSubject": "dano material",
                    "PublicationDate": "2021-10-01T00:00:00",
                    "NoticeDate": "2011-09-09T00:00:00",
                    "RedistributionDate": "0001-01-01T00:00:00",
                    "LawsuitAge": 147,
                    "ResponseDecisions": [
                        {
                            "DecisionContent": "Decisão condenatória",
                            "DecisionDate": "2022-05-20T00:00:00"
                        }
                    ],
                    "ResponseParties": [
                        {
                            "Doc": "97179841072",
                            "IsPartyActive": "true",
                            "Name": "douglas portela fontella",
                            "Polarity": "passive",
                            "Type": "defendant",
                            "LastCaptureDate": "2021-10-02T23:51:18",
                            "PartyDetails": {
                                "SpecificType": "correu"
                            }
                        }
                    ]
                },
                {
                    "Number": "01658943820118217000",
                    "CourtType": "criminal",
                    "MainSubject": "violacao de domicilio",
                    "PublicationDate": "2021-10-01T00:00:00",
                    "NoticeDate": "2011-04-19T00:00:00",
                    "RedistributionDate": "0001-01-01T00:00:00",
                    "LawsuitAge": 143,
                    "ResponseDecisions": [
                        {
                            "DecisionContent": "Decisão condenatória",
                            "DecisionDate": "2022-05-20T00:00:00"
                        }
                    ],
                    "ResponseParties": [
                        {
                            "Doc": "97179841072",
                            "IsPartyActive": "true",
                            "Name": "douglas portela fontella",
                            "Polarity": "passive",
                            "Type": "defendant",
                            "LastCaptureDate": "2021-10-02T23:49:09",
                            "PartyDetails": {
                                "SpecificType": "correu"
                            }
                        }
                    ]
                },
                {
                    "Number": "01482748120098217000",
                    "CourtType": "criminal",
                    "MainSubject": "entregar direcao a pessoa nao habilitada",
                    "PublicationDate": "2021-10-01T00:00:00",
                    "NoticeDate": "2009-10-19T00:00:00",
                    "RedistributionDate": "0001-01-01T00:00:00",
                    "LawsuitAge": 547,
                    "ResponseDecisions": [
                        {
                            "DecisionContent": "Decisão condenatória",
                            "DecisionDate": "2022-05-20T00:00:00"
                        }
                    ],
                    "ResponseParties": [
                        {
                            "Doc": "97179841072",
                            "IsPartyActive": "true",
                            "Name": "douglas portela fontella",
                            "Polarity": "passive",
                            "Type": "defendant",
                            "LastCaptureDate": "2021-10-02T23:45:53",
                            "PartyDetails": {
                                "SpecificType": "correu"
                            }
                        }
                    ]
                },
                {
                    "Number": "70027949056",
                    "CourtType": "criminal",
                    "MainSubject": "trafico de drogas e condutas afins",
                    "PublicationDate": "2021-10-01T00:00:00",
                    "NoticeDate": "2008-12-15T00:00:00",
                    "RedistributionDate": "0001-01-01T00:00:00",
                    "LawsuitAge": 121,
                    "ResponseDecisions": [
                        {
                            "DecisionContent": "Decisão condenatória",
                            "DecisionDate": "2022-05-20T00:00:00"
                        }
                    ],
                    "ResponseParties": [
                        {
                            "Doc": "97179841072",
                            "IsPartyActive": "true",
                            "Name": "douglas portela fontella",
                            "Polarity": "passive",
                            "Type": "defendant",
                            "LastCaptureDate": "2021-10-02T23:42:23",
                            "PartyDetails": {
                                "SpecificType": "correu"
                            }
                        }
                    ]
                }
            ]
        },
        "vehicle_owners": [
            {
                "person_uuid": "9619f6df-ca42-4979-b031-c8df9cb0cf82",
                "document": "97179841072",
                "name": "Maria Oliveira",
                "process": [
                    {
                        "Number": "456",
                        "CourtType": "Criminal",
                        "MainSubject": "Ameaca",
                        "PublicationDate": "2022-03-01T00:00:00",
                        "NoticeDate": "2022-03-10T00:00:00",
                        "RedistributionDate": "2022-03-12T00:00:00",
                        "LawsuitAge": 60,
                        "ResponseDecisions": [
                            {
                                "DecisionContent": "culpado",
                                "DecisionDate": "2022-03-12T00:00:00"
                            }
                        ],
                        "ResponseParties": [
                            {
                                "Doc": "97179841072",
                                "IsPartyActive": "true",
                                "Name": "Maria Oliveira",
                                "Polarity": "passive",
                                "Type": "defendant",
                                "LastCaptureDate": "2021-10-02T23:42:23",
                                "PartyDetails": {
                                    "SpecificType": "reu"
                                }
                            }
                        ]
                    }
                ]
            }
        ],
        "rntrc_owners": [
            {
                "person_uuid": "9619f6df-ca42-4979-b031-c8df9cb0cf82",
                "document": "97179841072",
                "name": "Maria Oliveira",
                "process": [
                    {
                        "Number": "456",
                        "CourtType": "Criminal",
                        "MainSubject": "Ameaca",
                        "PublicationDate": "2022-03-01T00:00:00",
                        "NoticeDate": "2022-03-10T00:00:00",
                        "RedistributionDate": "2022-03-12T00:00:00",
                        "LawsuitAge": 60,
                        "ResponseDecisions": [
                            {
                                "DecisionContent": "culpado",
                                "DecisionDate": "2022-03-12T00:00:00"
                            }
                        ],
                        "ResponseParties": [
                            {
                                "Doc": "97179841072",
                                "IsPartyActive": "true",
                                "Name": "Maria Oliveira",
                                "Polarity": "passive",
                                "Type": "defendant",
                                "LastCaptureDate": "2021-10-02T23:42:23",
                                "PartyDetails": {
                                    "SpecificType": "reu"
                                }
                            }
                        ]
                    }
                ]
            }
        ]
    }
    
    return input14

@pytest.fixture
def outputValidation14():

    d = {'person_uuid': 'b614401f-7928-11ec-a361-02fb9b06c548',
         'ClassOne': 0.961285,
         'ClassTwo': 0.974546,
         'ClassThree': 0.930292,
         'ClassFour': 0.986913,
         'TotalFeatures': 4}
    
    output14 = pd.DataFrame(data=d, index=[0])
    return output14

@pytest.fixture
def inputValidation15():
    input15 = {
        "trucker": {
            "person_uuid": "b614401f-7928-11ec-a361-02fb9b06c548",
            "document": "97179841072",
            "name": "Douglas Portela Fontella",
            "process": [
                {
                    "Number": "04283166520118217000",
                    "CourtType": "criminal",
                    "MainSubject": "homicidio na conducao de veiculo, sistema nacional de armas, porte ilegal de arma",                
                    "PublicationDate": "2021-10-01T00:00:00",
                    "NoticeDate": "2011-09-09T00:00:00",
                    "RedistributionDate": "0001-01-01T00:00:00",
                    "LawsuitAge": 147,
                    "ResponseDecisions": [
                        {
                            "DecisionContent": "Decisão condenatória",
                            "DecisionDate": "2022-05-20T00:00:00"
                        }
                    ],
                    "ResponseParties": [
                        {
                            "Doc": "97179841072",
                            "IsPartyActive": "true",
                            "Name": "douglas portela fontella",
                            "Polarity": "passive",
                            "Type": "defendant",
                            "LastCaptureDate": "2021-10-02T23:51:18",
                            "PartyDetails": {
                                "SpecificType": "correu"
                            }
                        }
                    ]
                },
                {
                    "Number": "01658943820118217000",
                    "CourtType": "criminal",
                    "MainSubject": "homicidio no transito, furto de veiculo",
                    "PublicationDate": "2021-10-01T00:00:00",
                    "NoticeDate": "2011-04-19T00:00:00",
                    "RedistributionDate": "0001-01-01T00:00:00",
                    "LawsuitAge": 143,
                    "ResponseDecisions": [
                        {
                            "DecisionContent": "Decisão condenatória",
                            "DecisionDate": "2022-05-20T00:00:00"
                        }
                    ],
                    "ResponseParties": [
                        {
                            "Doc": "97179841072",
                            "IsPartyActive": "true",
                            "Name": "douglas portela fontella",
                            "Polarity": "passive",
                            "Type": "defendant",
                            "LastCaptureDate": "2021-10-02T23:49:09",
                            "PartyDetails": {
                                "SpecificType": "correu"
                            }
                        }
                    ]
                },
                {
                    "Number": "01482748120098217000",
                    "CourtType": "criminal",
                    "MainSubject": "crimes de transito, crimes contra a vida, corrupcao de menores",
                    "PublicationDate": "2021-10-01T00:00:00",
                    "NoticeDate": "2009-10-19T00:00:00",
                    "RedistributionDate": "0001-01-01T00:00:00",
                    "LawsuitAge": 547,
                    "ResponseDecisions": [
                        {
                            "DecisionContent": "Decisão condenatória",
                            "DecisionDate": "2022-05-20T00:00:00"
                        }
                    ],
                    "ResponseParties": [
                        {
                            "Doc": "97179841072",
                            "IsPartyActive": "true",
                            "Name": "douglas portela fontella",
                            "Polarity": "passive",
                            "Type": "defendant",
                            "LastCaptureDate": "2021-10-02T23:45:53",
                            "PartyDetails": {
                                "SpecificType": "correu"
                            }
                        }
                    ]
                },
                {
                    "Number": "70027949056",
                    "CourtType": "criminal",
                    "MainSubject": "lei antitoxicos, trafico, medidas protetivas, maria da penha",
                    "PublicationDate": "2021-10-01T00:00:00",
                    "NoticeDate": "2008-12-15T00:00:00",
                    "RedistributionDate": "0001-01-01T00:00:00",
                    "LawsuitAge": 121,
                    "ResponseDecisions": [
                        {
                            "DecisionContent": "Decisão condenatória",
                            "DecisionDate": "2022-05-20T00:00:00"
                        }
                    ],
                    "ResponseParties": [
                        {
                            "Doc": "97179841072",
                            "IsPartyActive": "true",
                            "Name": "douglas portela fontella",
                            "Polarity": "passive",
                            "Type": "defendant",
                            "LastCaptureDate": "2021-10-02T23:42:23",
                            "PartyDetails": {
                                "SpecificType": "correu"
                            }
                        }
                    ]
                }
            ]
        },
        "vehicle_owners": [
            {
                "person_uuid": "9619f6df-ca42-4979-b031-c8df9cb0cf82",
                "document": "97179841072",
                "name": "Maria Oliveira",
                "process": [
                    {
                        "Number": "456",
                        "CourtType": "Criminal",
                        "MainSubject": "Ameaca",
                        "PublicationDate": "2022-03-01T00:00:00",
                        "NoticeDate": "2022-03-10T00:00:00",
                        "RedistributionDate": "2022-03-12T00:00:00",
                        "LawsuitAge": 60,
                        "ResponseDecisions": [
                            {
                                "DecisionContent": "culpado",
                                "DecisionDate": "2022-03-12T00:00:00"
                            }
                        ],
                        "ResponseParties": [
                            {
                                "Doc": "97179841072",
                                "IsPartyActive": "true",
                                "Name": "Maria Oliveira",
                                "Polarity": "passive",
                                "Type": "defendant",
                                "LastCaptureDate": "2021-10-02T23:42:23",
                                "PartyDetails": {
                                    "SpecificType": "reu"
                                }
                            }
                        ]
                    }
                ]
            }
        ],
        "rntrc_owners": [
            {
                "person_uuid": "9619f6df-ca42-4979-b031-c8df9cb0cf82",
                "document": "97179841072",
                "name": "Maria Oliveira",
                "process": [
                    {
                        "Number": "456",
                        "CourtType": "Criminal",
                        "MainSubject": "Ameaca",
                        "PublicationDate": "2022-03-01T00:00:00",
                        "NoticeDate": "2022-03-10T00:00:00",
                        "RedistributionDate": "2022-03-12T00:00:00",
                        "LawsuitAge": 60,
                        "ResponseDecisions": [
                            {
                                "DecisionContent": "culpado",
                                "DecisionDate": "2022-03-12T00:00:00"
                            }
                        ],
                        "ResponseParties": [
                            {
                                "Doc": "97179841072",
                                "IsPartyActive": "true",
                                "Name": "Maria Oliveira",
                                "Polarity": "passive",
                                "Type": "defendant",
                                "LastCaptureDate": "2021-10-02T23:42:23",
                                "PartyDetails": {
                                    "SpecificType": "reu"
                                }
                            }
                        ]
                    }
                ]
            }
        ]
    }
    
    return input15

@pytest.fixture
def outputValidation15():
    d = {'trucker_id': ['b614401f-7928-11ec-a361-02fb9b06c548',
          'b614401f-7928-11ec-a361-02fb9b06c548',
          'b614401f-7928-11ec-a361-02fb9b06c548',
          'b614401f-7928-11ec-a361-02fb9b06c548'],
         'LawsuitAge': [147, 143, 547, 121],
         'TimeDelta': [147, 143, 547, 121],
         'TimeDecay1': [0.9612852251777719,
          0.9622989717901397,
          0.8696688110555159,
          0.967913020418987],
         'TimeDecay2': [0.9738527214514408,
          0.9745461018155926,
          0.9091663899036865,
          0.9783774124374554],
         'TimeDecay3': [0.9802605075869478,
          0.9807873169420933,
          0.930291831273098,
          0.9836949198221265],
         'TimeDecay4': [0.9841458153580673,
          0.9845705653862753,
          0.9434449958643507,
          0.9869132597880165],
         'homicidio': [1, 0, 0, 0],
         'roubo': [0, 0, 0, 0],
         'furto': [0, 1, 0, 0],
         'lesao corporal': [0, 0, 0, 0],
         'ameaca': [0, 0, 0, 0],
         'contra a vida': [0, 0, 0, 0],
         'medidas protetivas': [0, 0, 0, 0],
         'pudor': [0, 0, 0, 0],
         'sistema nacional de armas': [0, 0, 0, 0],
         'porte ilegal de arma': [1, 0, 0, 0],
         'disparo de arma': [0, 0, 0, 0],
         'extorsao': [0, 0, 0, 0],
         'sequestro': [0, 0, 0, 0],
         'estupro': [0, 0, 0, 0],
         'violacao de domicilio': [0, 0, 0, 0],
         'violencia domestica': [0, 0, 0, 0],
         'esbulho': [0, 0, 0, 0],
         'turbacao': [0, 0, 0, 0],
         'trafico': [0, 0, 0, 1],
         'dano material': [0, 0, 0, 0],
         'infanticidio': [0, 0, 0, 0],
         'matar': [0, 0, 0, 0],
         'morte': [0, 0, 0, 0],
         'omissao de socorro': [0, 0, 0, 0],
         'carcere': [0, 0, 0, 0],
         'corrupcao': [0, 0, 0, 0],
         'corrupcao de menores': [0, 0, 1, 0],
         'feminicidio': [0, 0, 0, 0],
         'abuso de vulneravel': [0, 0, 0, 0],
         'maria da penha': [0, 0, 0, 1],
         'latrocinio': [0, 0, 0, 0],
         'organizacao criminosa': [0, 0, 0, 0],
         'terrorista': [0, 0, 0, 0],
         'associacao criminosa': [0, 0, 0, 0],
         'escravo': [0, 0, 0, 0],
         'transito': [0, 1, 1, 0],
         'veiculo': [0, 0, 0, 0],
         'embriaguez': [0, 0, 0, 0],
         'volante': [0, 0, 0, 0],
         'direcao': [0, 0, 0, 0],
         'velocidade': [0, 0, 0, 0],
         'transporte irregular': [0, 0, 0, 0],
         'acidente de transito': [0, 0, 0, 0],
         'cnh': [0, 0, 0, 0],
         'transporte de coisas': [0, 0, 0, 0],
         'influencia de alcool': [0, 0, 0, 0],
         'direcao perigosa': [0, 0, 0, 0],
         'disputar corrida': [0, 0, 0, 0],
         'manobra perigosa': [0, 0, 0, 0],
         'racha': [0, 0, 0, 0],
         'fraude': [0, 0, 0, 0],
         'lei antitoxicos': [0, 0, 0, 0],
         'quadrilha': [0, 0, 0, 0],
         'contrabando': [0, 0, 0, 0],
         'descaminho': [0, 0, 0, 0],
         'receptacao': [0, 0, 0, 0],
         'documento falso': [0, 0, 0, 0],
         'estelionato': [0, 0, 0, 0],
         'falsificacao': [0, 0, 0, 0],
         'falsidade ideologica': [0, 0, 0, 0],
         'enriquecimento': [0, 0, 0, 0],
         'fuga': [0, 0, 0, 0]}
    
    output15 = pd.DataFrame(data=d)
    
    return output15

@pytest.fixture
def inputValidation16():
    d = {'trucker_id': 'b614401f-7928-11ec-a361-02fb9b06c548',
     'FinalValue': 10,
     'ClassOne': 0.0,
     'ClassTwo': 0.0,
     'ClassThree': 0.0,
     'ClassFour': 3.8990746363967097,
     'TotalFeatures': 4}
    
    input16 = pd.DataFrame(data=d, index=[0])
    
    return input16

@pytest.fixture
def outputValidation16():
    
    d = {'trucker_id': 'b614401f-7928-11ec-a361-02fb9b06c548',
         'FinalValue': 10,
         'ClassOne': 0.0,
         'ClassTwo': 0.0,
         'ClassThree': 0.0,
         'ClassFour': 3.8990746363967097,
         'TotalFeatures': 4,
         'FinalValueScore': 0.04995432622000529,
         'ClassOneScore': 0.0,
         'ClassTwoScore': 0.0,
         'ClassThreeScore': 0.0,
         'ClassFourScore': 0.30441407176366003,
         'TotalFeaturesScore': 0.21812413091933325,
         'Score': 0.5700000000000001}

    output16 = pd.DataFrame(data=d, index=[0])
    
    return output16

@pytest.fixture
def inputValidation17():
    input17 = {
        "trucker": {
            "person_uuid": "b614401f-7928-11ec-a361-02fb9b06c548",
            "document": "97179841072",
            "name": "Douglas Portela Fontella",
            "process": [
                {
                    "Number": "04283166520118217000",
                    "CourtType": "criminal",
                    "MainSubject": "dano material",
                    "PublicationDate": "2021-10-01T00:00:00",
                    "NoticeDate": "2011-09-09T00:00:00",
                    "RedistributionDate": "0001-01-01T00:00:00",
                    "LawsuitAge": 147,
                    "ResponseDecisions": [
                        {
                            "DecisionContent": "Decisão condenatória",
                            "DecisionDate": "2022-05-20T00:00:00"
                        }
                    ],
                    "ResponseParties": [
                        {
                            "Doc": "97179841072",
                            "IsPartyActive": "true",
                            "Name": "douglas portela fontella",
                            "Polarity": "passive",
                            "Type": "defendant",
                            "LastCaptureDate": "2021-10-02T23:51:18",
                            "PartyDetails": {
                                "SpecificType": "correu"
                            }
                        }
                    ]
                },
                {
                    "Number": "01658943820118217000",
                    "CourtType": "criminal",
                    "MainSubject": "violacao de domicilio",
                    "PublicationDate": "2021-10-01T00:00:00",
                    "NoticeDate": "2011-04-19T00:00:00",
                    "RedistributionDate": "0001-01-01T00:00:00",
                    "LawsuitAge": 143,
                    "ResponseDecisions": [
                        {
                            "DecisionContent": "Decisão condenatória",
                            "DecisionDate": "2022-05-20T00:00:00"
                        }
                    ],
                    "ResponseParties": [
                        {
                            "Doc": "97179841072",
                            "IsPartyActive": "true",
                            "Name": "douglas portela fontella",
                            "Polarity": "passive",
                            "Type": "defendant",
                            "LastCaptureDate": "2021-10-02T23:49:09",
                            "PartyDetails": {
                                "SpecificType": "correu"
                            }
                        }
                    ]
                },
                {
                    "Number": "01482748120098217000",
                    "CourtType": "criminal",
                    "MainSubject": "entregar direcao a pessoa nao habilitada",
                    "PublicationDate": "2021-10-01T00:00:00",
                    "NoticeDate": "2009-10-19T00:00:00",
                    "RedistributionDate": "0001-01-01T00:00:00",
                    "LawsuitAge": 547,
                    "ResponseDecisions": [
                        {
                            "DecisionContent": "Decisão condenatória",
                            "DecisionDate": "2022-05-20T00:00:00"
                        }
                    ],
                    "ResponseParties": [
                        {
                            "Doc": "97179841072",
                            "IsPartyActive": "true",
                            "Name": "douglas portela fontella",
                            "Polarity": "passive",
                            "Type": "defendant",
                            "LastCaptureDate": "2021-10-02T23:45:53",
                            "PartyDetails": {
                                "SpecificType": "correu"
                            }
                        }
                    ]
                },
                {
                    "Number": "70027949056",
                    "CourtType": "criminal",
                    "MainSubject": "trafico de drogas e condutas afins",
                    "PublicationDate": "2021-10-01T00:00:00",
                    "NoticeDate": "2008-12-15T00:00:00",
                    "RedistributionDate": "0001-01-01T00:00:00",
                    "LawsuitAge": 121,
                    "ResponseDecisions": [
                        {
                            "DecisionContent": "Decisão condenatória",
                            "DecisionDate": "2022-05-20T00:00:00"
                        }
                    ],
                    "ResponseParties": [
                        {
                            "Doc": "97179841072",
                            "IsPartyActive": "true",
                            "Name": "douglas portela fontella",
                            "Polarity": "passive",
                            "Type": "defendant",
                            "LastCaptureDate": "2021-10-02T23:42:23",
                            "PartyDetails": {
                                "SpecificType": "correu"
                            }
                        }
                    ]
                }
            ]
        },
        "vehicle_owners": [
            {
                "person_uuid": "9619f6df-ca42-4979-b031-c8df9cb0cf82",
                "document": "97179841072",
                "name": "Maria Oliveira",
                "process": [
                    {
                        "Number": "456",
                        "CourtType": "Criminal",
                        "MainSubject": "Ameaca",
                        "PublicationDate": "2022-03-01T00:00:00",
                        "NoticeDate": "2022-03-10T00:00:00",
                        "RedistributionDate": "2022-03-12T00:00:00",
                        "LawsuitAge": 60,
                        "ResponseDecisions": [
                            {
                                "DecisionContent": "culpado",
                                "DecisionDate": "2022-03-12T00:00:00"
                            }
                        ],
                        "ResponseParties": [
                            {
                                "Doc": "97179841072",
                                "IsPartyActive": "true",
                                "Name": "Maria Oliveira",
                                "Polarity": "passive",
                                "Type": "defendant",
                                "LastCaptureDate": "2021-10-02T23:42:23",
                                "PartyDetails": {
                                    "SpecificType": "reu"
                                }
                            }
                        ]
                    }
                ]
            }
        ],
        "rntrc_owners": [
            {
                "person_uuid": "9619f6df-ca42-4979-b031-c8df9cb0cf82",
                "document": "97179841072",
                "name": "Maria Oliveira",
                "process": [
                    {
                        "Number": "456",
                        "CourtType": "Criminal",
                        "MainSubject": "Ameaca",
                        "PublicationDate": "2022-03-01T00:00:00",
                        "NoticeDate": "2022-03-10T00:00:00",
                        "RedistributionDate": "2022-03-12T00:00:00",
                        "LawsuitAge": 60,
                        "ResponseDecisions": [
                            {
                                "DecisionContent": "culpado",
                                "DecisionDate": "2022-03-12T00:00:00"
                            }
                        ],
                        "ResponseParties": [
                            {
                                "Doc": "97179841072",
                                "IsPartyActive": "true",
                                "Name": "Maria Oliveira",
                                "Polarity": "passive",
                                "Type": "defendant",
                                "LastCaptureDate": "2021-10-02T23:42:23",
                                "PartyDetails": {
                                    "SpecificType": "reu"
                                }
                            }
                        ]
                    }
                ]
            }
        ]
    }

    return input17

@pytest.fixture
def outputValidation17():
    
    d = {'person_uuid': 'b614401f-7928-11ec-a361-02fb9b06c548',
         'ClassOne': 0.961285,
         'ClassTwo': 0.974546,
         'ClassThree': 0.930292,
         'ClassFour': 0.986913,
         'TotalFeatures': 4}
    
    input17 = pd.DataFrame(data=d, index=[0])
    
    return input17

@pytest.fixture
def inputValidation18():
    input18 = {
        "trucker_id": "b614401f-7928-11ec-a361-02fb9b06c548",
        "cpf": "97179841072",
        "name": "douglas portela fontella",
        "process": [
            {
                "Number": "04283166520118217000",
                "CourtType": "criminal",
                "MainSubject": "dano material",
                "PublicationDate": "2021-10-01T00:00:00",
                "NoticeDate": "2011-09-09T00:00:00",
                "RedistributionDate": "0001-01-01T00:00:00",
                "LawsuitAge": 147,
                "ResponseParties": {
                    "Doc": "97179841072",
                    "IsPartyActive": "true",
                    "Name": "douglas portela fontella",
                    "Polarity": "passive",
                    "Type": "defendant",
                    "LastCaptureDate": "2021-10-02T23:51:18",
                    "PartyDetails": {
                        "SpecificType": "correu"
                    }
                }
            },
            {
                "Number": "01658943820118217000",
                "CourtType": "criminal",
                "MainSubject": "violacao de domicilio",
                "PublicationDate": "2021-10-01T00:00:00",
                "NoticeDate": "2011-04-19T00:00:00",
                "RedistributionDate": "0001-01-01T00:00:00",
                "LawsuitAge": 143,
                "ResponseParties": {
                    "Doc": "97179841072",
                    "IsPartyActive": "true",
                    "Name": "douglas portela fontella",
                    "Polarity": "passive",
                    "Type": "defendant",
                    "LastCaptureDate": "2021-10-02T23:49:09",
                    "PartyDetails": {
                        "SpecificType": "correu"
                    }
                }
            },
            {
                "Number": "01482748120098217000",
                "CourtType": "criminal",
                "MainSubject": "entregar direcao a pessoa nao habilitada",
                "PublicationDate": "2021-10-01T00:00:00",
                "NoticeDate": "2009-10-19T00:00:00",
                "RedistributionDate": "0001-01-01T00:00:00",
                "LawsuitAge": 547,
                "ResponseParties": {
                    "Doc": "97179841072",
                    "IsPartyActive": "true",
                    "Name": "douglas portela fontella",
                    "Polarity": "passive",
                    "Type": "defendant",
                    "LastCaptureDate": "2021-10-02T23:45:53",
                    "PartyDetails": {
                        "SpecificType": "correu"
                    }
                }
            },
            {
                "Number": "70027949056",
                "CourtType": "criminal",
                "MainSubject": "trafico de drogas e condutas afins",
                "PublicationDate": "2021-10-01T00:00:00",
                "NoticeDate": "2008-12-15T00:00:00",
                "RedistributionDate": "0001-01-01T00:00:00",
                "LawsuitAge": 121,
                "ResponseParties": {
                    "Doc": "97179841072",
                    "IsPartyActive": "true",
                    "Name": "douglas portela fontella",
                    "Polarity": "passive",
                    "Type": "defendant",
                    "LastCaptureDate": "2021-10-02T23:42:23",
                    "PartyDetails": {
                        "SpecificType": "correu"
                    }
                }
            }
        ]
    }

    return input18

@pytest.fixture
def outputValidation18():
    
    input18 = {'trucker_id': 'b614401f-7928-11ec-a361-02fb9b06c548',
         'FinalValue': 10,
         'ClassOne': 0.9612852251777719,
         'ClassTwo': 0.9745461018155926,
         'ClassThree': 0.930291831273098,
         'ClassFour': 0.9869132597880165,
         'TotalFeatures': 4,
         'FinalValueScore': 0.04995432622000529,
         'ClassOneScore': 0.001570656960155997,
         'ClassTwoScore': 0.00768859920651829,
         'ClassThreeScore': 0.0271849223616839,
         'ClassFourScore': 0.09324206606780973,
         'TotalFeaturesScore': 0.21812413091933325,
         'Score': 0.4}

    return input18

@pytest.fixture
def input_legal_invalid():
    invalid_input = {
        "trucker_id": "b614401f-7928-11ec-a361-02fb9b06c548",
        "cpf": 97179841072,
        "name": 123,
        "process": [
            {
                "Number": "04283166520118217000",
                "CourtType": "criminal",
                "MainSubject": "trafico de drogas e condutas afins",
                "PublicationDate": "2021-10-01T00:00:00",
                "NoticeDate": "2011-09-09T00:00:00",
                "RedistributionDate": "0001-01-01T00:00:00",
                "LawsuitAge": "147",
                "ResponseParties": {
                    "Doc": "97179841072",
                    "IsPartyActive": "true",
                    "Name": "douglas portela fontella",
                    "Polarity": "passive",
                    "Type": "defendant",
                    "LastCaptureDate": "2021-10-02T23:51:18",
                    "PartyDetails": {
                        "SpecificType": "correu"
                    }
                }
            },
            {
                "Number": "01658943820118217000",
                "CourtType": "criminal",
                "MainSubject": "trafico de drogas e condutas afins",
                "PublicationDate": "2021-10-01T00:00:00",
                "NoticeDate": "2011-04-19T00:00:00",
                "RedistributionDate": "0001-01-01T00:00:00",
                "LawsuitAge": "143",
                "ResponseParties": {
                    "Doc": "97179841072",
                    "IsPartyActive": "true",
                    "Name": "douglas portela fontella",
                    "Polarity": "passive",
                    "Type": "defendant",
                    "LastCaptureDate": "2021-10-02T23:49:09",
                    "PartyDetails": {
                        "SpecificType": "correu"
                    }
                }
            },
            {
                "Number": "01482748120098217000",
                "CourtType": "criminal",
                "MainSubject": "trafico de drogas e condutas afins",
                "PublicationDate": "2021-10-01T00:00:00",
                "NoticeDate": "2009-10-19T00:00:00",
                "RedistributionDate": "0001-01-01T00:00:00",
                "LawsuitAge": "547",
                "ResponseParties": {
                    "Doc": "97179841072",
                    "IsPartyActive": "true",
                    "Name": "douglas portela fontella",
                    "Polarity": "passive",
                    "Type": "defendant",
                    "LastCaptureDate": "2021-10-02T23:45:53",
                    "PartyDetails": {
                        "SpecificType": "correu"
                    }
                }
            },
            {
                "Number": "70027949056",
                "CourtType": "criminal",
                "MainSubject": "trafico de drogas e condutas afins",
                "PublicationDate": "2021-10-01T00:00:00",
                "NoticeDate": "2008-12-15T00:00:00",
                "RedistributionDate": "0001-01-01T00:00:00",
                "LawsuitAge": "121",
                "ResponseParties": {
                    "Doc": "97179841072",
                    "IsPartyActive": "true",
                    "Name": "douglas portela fontella",
                    "Polarity": "passive",
                    "Type": "defendant",
                    "LastCaptureDate": "2021-10-02T23:42:23",
                    "PartyDetails": {
                        "SpecificType": "correu"
                    }
                }
            }
        ]
    }

    return invalid_input

@pytest.fixture
def inputValidation19():
    input19 = {
        "trucker": {
            "person_uuid": "b614401f-7928-11ec-a361-02fb9b06c548",
            "document": "97179841072",
            "name": "Douglas Portela Fontella",
            "process": [
                {
                    "Number": "01658943820118217000",
                    "CourtType": "trabalhista",
                    "MainSubject": "processo trabalhista",
                    "PublicationDate": "2021-10-01T00:00:00",
                    "NoticeDate": "2011-04-19T00:00:00",
                    "RedistributionDate": "0001-01-01T00:00:00",
                    "LawsuitAge": 143,
                    "ResponseDecisions": [
                        {
                            "DecisionContent": "Decisão condenatória",
                            "DecisionDate": "2022-05-20T00:00:00"
                        }
                    ],
                    "ResponseParties": [
                        {
                            "Doc": "97179841072",
                            "IsPartyActive": "true",
                            "Name": "douglas portela fontella",
                            "Polarity": "passive",
                            "Type": "defendant",
                            "LastCaptureDate": "2021-10-02T23:49:09",
                            "PartyDetails": {
                                "SpecificType": "correu"
                            }
                        }
                    ]
                }
            ]
        },
        "vehicle_owners": [
            {
                "person_uuid": "9619f6df-ca42-4979-b031-c8df9cb0cf82",
                "document": "97179841072",
                "name": "Maria Oliveira",
                "process": [
                    {
                        "Number": "456",
                        "CourtType": "Criminal",
                        "MainSubject": "Ameaca",
                        "PublicationDate": "2022-03-01T00:00:00",
                        "NoticeDate": "2022-03-10T00:00:00",
                        "RedistributionDate": "2022-03-12T00:00:00",
                        "LawsuitAge": 60,
                        "ResponseDecisions": [
                            {
                                "DecisionContent": "culpado",
                                "DecisionDate": "2022-03-12T00:00:00"
                            }
                        ],
                        "ResponseParties": [
                            {
                                "Doc": "97179841072",
                                "IsPartyActive": "true",
                                "Name": "Maria Oliveira",
                                "Polarity": "passive",
                                "Type": "defendant",
                                "LastCaptureDate": "2021-10-02T23:42:23",
                                "PartyDetails": {
                                    "SpecificType": "reu"
                                }
                            }
                        ]
                    }
                ]
            }
        ],
        "rntrc_owners": [
            {
                "person_uuid": "9619f6df-ca42-4979-b031-c8df9cb0cf82",
                "document": "97179841072",
                "name": "Maria Oliveira",
                "process": [
                    {
                        "Number": "456",
                        "CourtType": "Criminal",
                        "MainSubject": "Ameaca",
                        "PublicationDate": "2022-03-01T00:00:00",
                        "NoticeDate": "2022-03-10T00:00:00",
                        "RedistributionDate": "2022-03-12T00:00:00",
                        "LawsuitAge": 60,
                        "ResponseDecisions": [
                            {
                                "DecisionContent": "culpado",
                                "DecisionDate": "2022-03-12T00:00:00"
                            }
                        ],
                        "ResponseParties": [
                            {
                                "Doc": "97179841072",
                                "IsPartyActive": "true",
                                "Name": "Maria Oliveira",
                                "Polarity": "passive",
                                "Type": "defendant",
                                "LastCaptureDate": "2021-10-02T23:42:23",
                                "PartyDetails": {
                                    "SpecificType": "reu"
                                }
                            }
                        ]
                    }
                ]
            }
        ]
    }

    return input19

@pytest.fixture
def outputValidation19():

    d = {'person_uuid': 'b614401f-7928-11ec-a361-02fb9b06c548',
         'ClassOne': 0,
         'ClassTwo': 0,
         'ClassThree': 0,
         'ClassFour': 0,
         'TotalFeatures': 0}

    input19 = pd.DataFrame(data=d, index=[0])

    return input19

@pytest.fixture
def inputValidation20():
    input20 = {
        "trucker": {
            "person_uuid": "b614401f-7928-11ec-a361-02fb9b06c548",
            "document": "97179841072",
            "name": "Douglas Portela Fontella",
            "process": [
                {
                    "Number": "01658943820118217000",
                    "CourtType": "criminal",
                    "MainSubject": "furto qualificado",
                    "PublicationDate": "2021-10-01T00:00:00",
                    "NoticeDate": "2011-04-19T00:00:00",
                    "RedistributionDate": "0001-01-01T00:00:00",
                    "LawsuitAge": 143,
                    "ResponseDecisions": [
                        {
                            "DecisionContent": "Decisão condenatória",
                            "DecisionDate": "2022-05-20T00:00:00"
                        }
                    ],
                    "ResponseParties": [
                        {
                            "Doc": "97179841072",
                            "IsPartyActive": "true",
                            "Name": "douglas portela fontella",
                            "Polarity": "active",
                            "Type": "autor",
                            "LastCaptureDate": "2021-10-02T23:49:09",
                            "PartyDetails": {
                                "SpecificType": "autor"
                            }
                        }
                    ]
                }
            ]
        },
        "vehicle_owners": [
            {
                "person_uuid": "9619f6df-ca42-4979-b031-c8df9cb0cf82",
                "document": "97179841072",
                "name": "Maria Oliveira",
                "process": [
                    {
                        "Number": "456",
                        "CourtType": "Criminal",
                        "MainSubject": "Ameaca",
                        "PublicationDate": "2022-03-01T00:00:00",
                        "NoticeDate": "2022-03-10T00:00:00",
                        "RedistributionDate": "2022-03-12T00:00:00",
                        "LawsuitAge": 60,
                        "ResponseDecisions": [
                            {
                                "DecisionContent": "culpado",
                                "DecisionDate": "2022-03-12T00:00:00"
                            }
                        ],
                        "ResponseParties": [
                            {
                                "Doc": "97179841072",
                                "IsPartyActive": "true",
                                "Name": "Maria Oliveira",
                                "Polarity": "passive",
                                "Type": "defendant",
                                "LastCaptureDate": "2021-10-02T23:42:23",
                                "PartyDetails": {
                                    "SpecificType": "reu"
                                }
                            }
                        ]
                    }
                ]
            }
        ],
        "rntrc_owners": [
            {
                "person_uuid": "9619f6df-ca42-4979-b031-c8df9cb0cf82",
                "document": "97179841072",
                "name": "Maria Oliveira",
                "process": [
                    {
                        "Number": "456",
                        "CourtType": "Criminal",
                        "MainSubject": "Ameaca",
                        "PublicationDate": "2022-03-01T00:00:00",
                        "NoticeDate": "2022-03-10T00:00:00",
                        "RedistributionDate": "2022-03-12T00:00:00",
                        "LawsuitAge": 60,
                        "ResponseDecisions": [
                            {
                                "DecisionContent": "culpado",
                                "DecisionDate": "2022-03-12T00:00:00"
                            }
                        ],
                        "ResponseParties": [
                            {
                                "Doc": "97179841072",
                                "IsPartyActive": "true",
                                "Name": "Maria Oliveira",
                                "Polarity": "passive",
                                "Type": "defendant",
                                "LastCaptureDate": "2021-10-02T23:42:23",
                                "PartyDetails": {
                                    "SpecificType": "reu"
                                }
                            }
                        ]
                    }
                ]
            }
        ]
    }

    return input20

@pytest.fixture
def outputValidation20():

    d = {'person_uuid': 'b614401f-7928-11ec-a361-02fb9b06c548',
         'ClassOne': 0,
         'ClassTwo': 0,
         'ClassThree': 0,
         'ClassFour': 0,
         'TotalFeatures': 0}

    output20 = pd.DataFrame(data=d, index=[0])

    return output20

@pytest.fixture
def inputValidation21():
    input21 = {
        "trucker": {
            "person_uuid": "b614401f-7928-11ec-a361-02fb9b06c548",
            "document": "97179841072",
            "name": "Douglas Portela Fontella",
            "process": [
                {
                    "Number": "01658943820118217000",
                    "CourtType": "criminal",
                    "MainSubject": "furto qualificado",
                    "PublicationDate": "2021-10-01T00:00:00",
                    "NoticeDate": "2011-04-19T00:00:00",
                    "RedistributionDate": "0001-01-01T00:00:00",
                    "LawsuitAge": 143,
                    "ResponseDecisions": [
                        {
                            "DecisionContent": "Decisão condenatória",
                            "DecisionDate": "2022-05-20T00:00:00"
                        }
                    ],
                    "ResponseParties": [

                    ]
                }
            ]
        },
        "vehicle_owners": [
            {
                "person_uuid": "9619f6df-ca42-4979-b031-c8df9cb0cf82",
                "document": "97179841072",
                "name": "Maria Oliveira",
                "process": [
                    {
                        "Number": "456",
                        "CourtType": "Criminal",
                        "MainSubject": "Ameaca",
                        "PublicationDate": "2022-03-01T00:00:00",
                        "NoticeDate": "2022-03-10T00:00:00",
                        "RedistributionDate": "2022-03-12T00:00:00",
                        "LawsuitAge": 60,
                        "ResponseDecisions": [
                            {
                                "DecisionContent": "culpado",
                                "DecisionDate": "2022-03-12T00:00:00"
                            }
                        ],
                        "ResponseParties": [
                            {
                                "Doc": "97179841072",
                                "IsPartyActive": "true",
                                "Name": "Maria Oliveira",
                                "Polarity": "passive",
                                "Type": "defendant",
                                "LastCaptureDate": "2021-10-02T23:42:23",
                                "PartyDetails": {
                                    "SpecificType": "reu"
                                }
                            }
                        ]
                    }
                ]
            }
        ],
        "rntrc_owners": [
            {
                "person_uuid": "9619f6df-ca42-4979-b031-c8df9cb0cf82",
                "document": "97179841072",
                "name": "Maria Oliveira",
                "process": [
                    {
                        "Number": "456",
                        "CourtType": "Criminal",
                        "MainSubject": "Ameaca",
                        "PublicationDate": "2022-03-01T00:00:00",
                        "NoticeDate": "2022-03-10T00:00:00",
                        "RedistributionDate": "2022-03-12T00:00:00",
                        "LawsuitAge": 60,
                        "ResponseDecisions": [
                            {
                                "DecisionContent": "culpado",
                                "DecisionDate": "2022-03-12T00:00:00"
                            }
                        ],
                        "ResponseParties": [
                            {
                                "Doc": "97179841072",
                                "IsPartyActive": "true",
                                "Name": "Maria Oliveira",
                                "Polarity": "passive",
                                "Type": "defendant",
                                "LastCaptureDate": "2021-10-02T23:42:23",
                                "PartyDetails": {
                                    "SpecificType": "reu"
                                }
                            }
                        ]
                    }
                ]
            }
        ]
    }

    return input21

@pytest.fixture
def outputValidation21():

    d = {'person_uuid': 'b614401f-7928-11ec-a361-02fb9b06c548',
         'ClassOne': 0,
         'ClassTwo': 0,
         'ClassThree': 0,
         'ClassFour': 0,
         'TotalFeatures': 0}

    output21 = pd.DataFrame(data=d, index=[0])

    return output21

@pytest.fixture
def inputTestDataContract():
    test = {
        "trucker":{
            "person_uuid":"9723a439-3db3-4353-9841-cb8aceb5713f",
            "document":"35159161805",
            "name":"Fulano",
            "process": None
         },
         "vehicle_owners":[
            {
               "person_uuid":"",
               "document":"00407025022",
               "name":"HENRIQUE BALDISSERA",
               "process": None
            },
            {
               "person_uuid":"",
               "document":"11430844000199",
               "name":"HENRIQUE BALDISSERA",
               "process": None
            },
            {
               "person_uuid":"",
               "document":"09919398675",
               "name":"HENRIQUE BALDISSERA",
               "process": None
            },
            {
               "person_uuid":"",
               "document":"00567812103",
               "name":"JOAO PAULO SANTOS DE SOUZA",
               "process": None
            }
         ],
         "rntrc_owners":[
            {
               "person_uuid":"",
               "document":"00407025022",
               "name":"ABC TRANSPORTES E SERVICOS EIRELI",
               "process":None
            },
            {
               "person_uuid":"",
               "document":"35159161805",
               "name":"ABC TRANSPORTES E SERVICOS EIRELI",
               "process":None
            },
            {
               "person_uuid":"",
               "document":"01677966661",
               "name":"ABC TRANSPORTES E SERVICOS EIRELI",
               "process":None
            }
         ]
      }
    return test

# Permite simular API em operacao nos testes de predicao
@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client