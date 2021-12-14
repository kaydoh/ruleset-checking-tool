from rct229.data import data
from rct229.data_fns.table_utils import find_osstd_table_entry
from rct229.schema.config import ureg

# This dictionary maps the opaque surface types that are returned from get_opaque_surface_type()
# to the corresponding construction values in ashrae_90_1_prm_2019.construction_properties.json
OPAQUE_SURFACE_TYPE_TO_CONSTRUCTION_MAP = {
    "ABOVE-GRADE WALL": "PRM Steel Framed Exterior Wall",
}

# This dictionary maps surface conditioning categories as returned from get_surface_conditioning_category_dict()
# to the corresponding building category values in ashrae_90_1_prm_2019.construction_properties.json
SURFACE_CONDITIONING_CATEGORY_TO_BUILDING_CATEGORY_MAP = {
    "EXTERIOR RESIDENTIAL": "Residential",
    "EXTERIOR NON-RESIDENTIAL": "Nonresidential",
    "SEMI-EXTERIOR": "Semiheated",
}

# This dictionary maps the ClimateZone2019ASHRAE901 enumerations to
# the corresponding climate zone set values  in the OSSTD file ashrae_90_1_prm_2019.construction_properties.json
CLIMATE_ZONE_ENUMERATION_TO_CLIMATE_ZONE_SET_MAP = {
    "CZ0A": "ClimateZone 0",
    "CZ0B": "ClimateZone 0",
    "CZ1A": "ClimateZone 1",
    "CZ1B": "ClimateZone 1",
    "CZ2A": "ClimateZone 2",
    "CZ2B": "ClimateZone 2",
    "CZ3A": "ClimateZone 3",
    "CZ3B": "ClimateZone 3",
    "CZ3C": "ClimateZone 3",
    "CZ4A": "ClimateZone 4",
    "CZ4B": "ClimateZone 4",
    "CZ4C": "ClimateZone 4",
    "CZ5A": "ClimateZone 5",
    "CZ5B": "ClimateZone 5",
    "CZ5C": "ClimateZone 5",
    "CZ6A": "ClimateZone 6",
    "CZ6B": "ClimateZone 6",
    "CZ7": "ClimateZone 7",
    "CZ8": "ClimateZone 8",
}


def table_G34_lookup(climate_zone, surface_conditioning_category, opaque_surface_type):
    """Returns the assembly maxiumum values for a given climate zone, surface conditoning category
     and opaque sruface type as required by ASHRAE 90.1 Table G3.4-1 through G3.4-8

    Parameters
    ----------
    climate_zone : str
        One of the ClimateZone2019ASHRAE901 enumeration values
    surface_conditioning_category : str
        A surface conditioning category as returned by get_surface_conditioning_category_dict()
    opaque_surface_type : str
        An opaque surface type as returned by get_opaque_surfact_type()
    Returns
    -------
    dict
        { assembly_maximum_u_value: Quantity - The assembly maximum u value given by Table G3.4-1 }

    """
    climate_zone_set = CLIMATE_ZONE_ENUMERATION_TO_CLIMATE_ZONE_SET_MAP[climate_zone]
    building_category = SURFACE_CONDITIONING_CATEGORY_TO_BUILDING_CATEGORY_MAP[
        surface_conditioning_category
    ]
    construction = OPAQUE_SURFACE_TYPE_TO_CONSTRUCTION_MAP[opaque_surface_type]

    osstd_entry = find_osstd_table_entry(
        [
            ("climate_zone_set", climate_zone_set),
            ("building_category", building_category),
            ("construction", construction),
        ],
        osstd_table=data["ashrae_90_1_prm_2019.construction_properties"],
    )

    ip_u_value_units = osstd_entry["assembly_maximum_u_value"]
    u_value = ip_u_value_units * ureg("Btu / (hr * ft2 * delta_degF)")

    return {"u_value": u_value}
