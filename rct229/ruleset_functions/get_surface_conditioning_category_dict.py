import pandas as pd

from rct229.ruleset_functions.get_zone_conditioning_category_dict import (
    ZoneConditioningCategory,
    get_zone_conditioning_category_dict,
)
from rct229.utils.jsonpath_utils import find_all

# Constants
# TODO: These should directly from the enumerations


# Intended for export and internal use
class SurfaceConditioningCategory:
    """Enumeration class for zone conditioning categories"""

    EXTERIOR: str = "EXTERIOR"
    GROUND: str = "GROUND"
    INTERIOR: str = "INTERIOR"
    # Surface conditioning categories (export these)
    EXTERIOR_MIXED: str = "EXTERIOR MIXED"
    EXTERIOR_NON_RESIDENTIAL: str = "EXTERIOR NON-RESIDENTIAL"
    EXTERIOR_RESIDENTIAL: str = "EXTERIOR RESIDENTIAL"
    SEMI_EXTERIOR: str = "SEMI-EXTERIOR"
    UNREGULATED: str = "UNREGULATED"


SCC_DATA_FRAME = pd.DataFrame(
    data={
        ZoneConditioningCategory.CONDITIONED_RESIDENTIAL: [
            SurfaceConditioningCategory.UNREGULATED,
            SurfaceConditioningCategory.UNREGULATED,
            SurfaceConditioningCategory.UNREGULATED,
            SurfaceConditioningCategory.SEMI_EXTERIOR,
            SurfaceConditioningCategory.EXTERIOR_RESIDENTIAL,
            SurfaceConditioningCategory.SEMI_EXTERIOR,
        ],
        ZoneConditioningCategory.CONDITIONED_NON_RESIDENTIAL: [
            SurfaceConditioningCategory.UNREGULATED,
            SurfaceConditioningCategory.UNREGULATED,
            SurfaceConditioningCategory.UNREGULATED,
            SurfaceConditioningCategory.SEMI_EXTERIOR,
            SurfaceConditioningCategory.EXTERIOR_NON_RESIDENTIAL,
            SurfaceConditioningCategory.SEMI_EXTERIOR,
        ],
        ZoneConditioningCategory.CONDITIONED_MIXED: [
            SurfaceConditioningCategory.UNREGULATED,
            SurfaceConditioningCategory.UNREGULATED,
            SurfaceConditioningCategory.UNREGULATED,
            SurfaceConditioningCategory.SEMI_EXTERIOR,
            SurfaceConditioningCategory.EXTERIOR_MIXED,
            SurfaceConditioningCategory.SEMI_EXTERIOR,
        ],
        ZoneConditioningCategory.SEMI_HEATED: [
            SurfaceConditioningCategory.SEMI_EXTERIOR,
            SurfaceConditioningCategory.SEMI_EXTERIOR,
            SurfaceConditioningCategory.SEMI_EXTERIOR,
            SurfaceConditioningCategory.UNREGULATED,
            SurfaceConditioningCategory.SEMI_EXTERIOR,
            SurfaceConditioningCategory.SEMI_EXTERIOR,
        ],
        ZoneConditioningCategory.UNENCLOSED: [
            SurfaceConditioningCategory.EXTERIOR_RESIDENTIAL,
            SurfaceConditioningCategory.EXTERIOR_NON_RESIDENTIAL,
            SurfaceConditioningCategory.EXTERIOR_MIXED,
            SurfaceConditioningCategory.SEMI_EXTERIOR,
            SurfaceConditioningCategory.UNREGULATED,
            SurfaceConditioningCategory.UNREGULATED,
        ],
        ZoneConditioningCategory.UNCONDITIONED: [
            SurfaceConditioningCategory.SEMI_EXTERIOR,
            SurfaceConditioningCategory.SEMI_EXTERIOR,
            SurfaceConditioningCategory.SEMI_EXTERIOR,
            SurfaceConditioningCategory.SEMI_EXTERIOR,
            SurfaceConditioningCategory.UNREGULATED,
            SurfaceConditioningCategory.UNREGULATED,
        ],
        SurfaceConditioningCategory.EXTERIOR: [
            SurfaceConditioningCategory.EXTERIOR_RESIDENTIAL,
            SurfaceConditioningCategory.EXTERIOR_NON_RESIDENTIAL,
            SurfaceConditioningCategory.EXTERIOR_MIXED,
            SurfaceConditioningCategory.SEMI_EXTERIOR,
            SurfaceConditioningCategory.UNREGULATED,
            SurfaceConditioningCategory.UNREGULATED,
        ],
        SurfaceConditioningCategory.GROUND: [
            SurfaceConditioningCategory.EXTERIOR_RESIDENTIAL,
            SurfaceConditioningCategory.EXTERIOR_NON_RESIDENTIAL,
            SurfaceConditioningCategory.EXTERIOR_MIXED,
            SurfaceConditioningCategory.SEMI_EXTERIOR,
            SurfaceConditioningCategory.UNREGULATED,
            SurfaceConditioningCategory.UNREGULATED,
        ],
    },
    index=[
        ZoneConditioningCategory.CONDITIONED_RESIDENTIAL,
        ZoneConditioningCategory.CONDITIONED_NON_RESIDENTIAL,
        ZoneConditioningCategory.CONDITIONED_MIXED,
        ZoneConditioningCategory.SEMI_HEATED,
        ZoneConditioningCategory.UNENCLOSED,
        ZoneConditioningCategory.UNCONDITIONED,
    ],
)


def get_surface_conditioning_category_dict(climate_zone, building):
    """Determines the surface conditioning category for every surface in a building

    Parameters
    ----------
    climate_zone : str
        One of the ClimateZone2019ASHRAE901 enumerated values
    building : dict
        A dictionary representing a building as defined by the ASHRAE229 schema
    Returns
    -------
    dict
        A dictionary that maps surfaces to one of the conditioning categories:
        EXTERIOR_RESIDENTIAL, EXTERIOR_NON_RESIDENTIAL, EXTERIOR_MIXED,
        SEMI_EXTERIOR, UNREGULATED
    """
    # The dictionary to be returned
    surface_conditioning_category_dict = {}

    # Get the conditioning category for all the zones in the building
    zcc_dict = get_zone_conditioning_category_dict(climate_zone, building)

    # Loop through all the zones in the building
    for zone in find_all("building_segments[*].zones[*]", building):
        # Zone conditioning category
        zcc = zcc_dict[zone["id"]]

        # Loop through all the surfaces in the zone
        for surface in zone["surfaces"]:
            surface_adjacent_to = surface["adjacent_to"]
            surface_conditioning_category_dict[surface["id"]] = SCC_DATA_FRAME.at[
                # row index
                zcc,
                # column index
                zcc_dict[surface["adjacent_zone"]]
                if surface_adjacent_to == SurfaceConditioningCategory.INTERIOR
                else surface_adjacent_to,
            ]

    return surface_conditioning_category_dict
