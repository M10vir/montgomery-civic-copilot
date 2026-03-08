INTENT_MAP = {
    "sanitation": {
        "targets": ["sanitation_schedule", "service_311"],
        "keywords": ["trash", "garbage", "pickup", "recycling", "waste", "bin", "missed pickup"],
    },
    "service_request_311": {
        "targets": ["service_311"],
        "keywords": ["311", "service request", "report issue", "complaint", "problem", "city issue"],
    },
    "code_violation": {
        "targets": ["code_violations", "service_311"],
        "keywords": ["code violation", "property complaint", "abandoned property", "unsafe property", "yard"],
    },
    "district_lookup": {
        "targets": ["address_lookup_district", "gis_viewer"],
        "keywords": ["district", "representative", "my address", "council district", "ward", "who represents me"],
    },
    "map_lookup": {
        "targets": ["gis_viewer"],
        "keywords": ["map", "gis", "location", "show on map"],
    },
    "parking": {
        "targets": ["downtown_parking", "m_transit"],
        "keywords": ["parking", "park downtown", "garage", "meter", "park"],
    },
    "transit": {
        "targets": ["m_transit", "downtown_parking"],
        "keywords": ["transit", "bus", "route", "public transport", "ride", "nearby bus"],
    },
    "traffic": {
        "targets": ["traffic_engineering", "service_311"],
        "keywords": ["traffic", "road", "signal", "intersection", "street issue", "traffic light"],
    },
}
