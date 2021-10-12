import rct229
from rct229.data import data
from rct229.data_fns.table_utils import find_osstd_table_entry

# This dictionary maps the VerticalFenestrationBuildingAreaType2019ASHRAE901 enumerations to
# the corresponding Baseline Building Gross Above-Grade-Wall Area in the OSSTD file
# ashrae_90_1_prm_2019.prm_wwr_bldg_type
BUILDING_AREA_TYPE_TO_VERTICAL_FENESTRATION_PERCENTAGE_MAP = {
    "GROCERY_STORE": "Grocery store",
    "HEALTHCARE_OUTPATIENT": "Healthcare (outpatient)",
    "HOSPITAL": "Hospital",
    # "HOTEL_MOTEL_SMALL": "Hotel/motel <= 75 rooms",
    "HOTEL_MOTEL_LARGE": "Hotel/motel > 75 rooms",
    "OFFICE_SMALL": "Office <= 5,000 sq ft",
    "OFFICE_MEDIUM": "Office 5,000 to 50,000 sq ft",
    "OFFICE_LARGE": "Office > 50,000 sq ft",
    "RESTAURANT_QUICK_SERVICE": "Restaurant (quick service)",
    "RESTAURANT_FULL_SERVICE": "Restaurant (full service)",
    "RETAIL_STAND_ALONE": "Retail (stand alone)",
    "RETAIL_STRIP_MALL": "Retail (strip mall)",
    "SCHOOL_PRIMARY": "School (primary)",
    "SCHOOL_SECONDARY_AND_UNIVERSITY": "School (secondary and university)",
    "WAREHOUSE_NONREFRIGERATED": "Warehouse (nonrefrigerated)",
}


def table_G3_1_1_1_lookup(building_area_type_enum_val):
    """Returns the baseline building vertical fenestration percentage for a building area type as
    required by ASHRAE 90.1 Table G3.1.1-1
    Parameters
    ----------
    building_area_type : str
        One of the VerticalFenestrationBuildingAreaType2019ASHRAE901 enumeration values
    Returns
    -------
    dict
        { wwr: float – The window to wall ratio given by Table G3.1.1-1 }

    """
    wwr_building_type = BUILDING_AREA_TYPE_TO_VERTICAL_FENESTRATION_PERCENTAGE_MAP[
        building_area_type_enum_val
    ]

    osstd_entry = find_osstd_table_entry(
        [("wwr_building_type", wwr_building_type)],
        osstd_table=data["ashrae_90_1_prm_2019.prm_wwr_bldg_type"],
    )
    wwr = osstd_entry["wwr"]

    return {"wwr": wwr}


# table_G3_1_1_1_lookup("GROCERY_STORE")
# table_G3_1_1_1_lookup("HEALTHCARE_OUTPATIENT")
