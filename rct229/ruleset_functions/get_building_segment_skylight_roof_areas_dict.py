from rct229.utils.assertions import getattr_
from rct229.ruleset_functions.get_opaque_surface_type import OpaqueSurfaceType as OST
from rct229.ruleset_functions.get_opaque_surface_type import get_opaque_surface_type
from rct229.ruleset_functions.get_surface_conditioning_category_dict import (
    SurfaceConditioningCategory as SCC,
)
from rct229.ruleset_functions.get_surface_conditioning_category_dict import (
    get_surface_conditioning_category_dict,
)
from rct229.ruleset_functions.get_zone_conditioning_category_dict import (
    ZoneConditioningCategory as ZCC,
)
from rct229.ruleset_functions.get_zone_conditioning_category_dict import (
    get_zone_conditioning_category_dict,
)
from rct229.schema.config import ureg
from rct229.utils.assertions import assert_, assert_required_fields
from rct229.utils.jsonpath_utils import find_all
from rct229.utils.pint_utils import ZERO

# NOTE: There are no required fields at this function's level; the ruleset_functions
# called do have required fields

import pdb


def get_building_segment_skylight_roof_areas_dict(climate_zone, building):
    """Gets a dictionary mapping building segment id to a dictionary of (total area of
    skylights) and (total area of envelope roofs) for the building_segment

    Parameters
    ----------
    climate_zone : str
        One of the ClimateZone2019ASHRAE901 enumerated values
    building : dict
        A dictionary representing a building as defined by the ASHRAE229 schema

    Returns
    -------
    dict
        A dictionary of the form
        {
            <building segment id>: {
                "total_envelope_roof_area": <total roof area in the building segment>,
                "total_skylight_area": <total skylight area in the building segment>
            }
        }
    """
    print("Started get_building_segment_skylight_roof_areas_dict()")
    zcc_dict = get_zone_conditioning_category_dict(climate_zone, building)
    scc_dict = get_surface_conditioning_category_dict(climate_zone, building)
    # pdb.set_trace()
    building_segment_roof_areas_dict = {}

    for building_segment in find_all("building_segments[*]", building):
        building_segment_roof_areas_dict[
            building_segment["id"]
        ] = building_segment_roof_areas = {
            "total_envelope_roof_area": ZERO.AREA,
            "total_skylight_area": ZERO.AREA,
        }
        print(f"segment {building_segment['id']}")
        for zone in find_all("zones[*]", building_segment):
            if zcc_dict[zone["id"]] in [
                ZCC.CONDITIONED_RESIDENTIAL,
                ZCC.CONDITIONED_NON_RESIDENTIAL,
                ZCC.CONDITIONED_MIXED,
                ZCC.SEMI_HEATED,
            ]:
                print(f"zone {zone['id']}")
                for surface in find_all("surfaces[*]", zone):
                    print(f"surface {surface['id']}")
                    if get_opaque_surface_type(surface) == OST.ROOF and scc_dict[
                        surface["id"]
                    ] in [
                        SCC.EXTERIOR_RESIDENTIAL,
                        SCC.EXTERIOR_NON_RESIDENTIAL,
                        SCC.EXTERIOR_MIXED,
                        SCC.SEMI_EXTERIOR,
                    ]:

                        print(f"surface {surface['id']} is ROOF+")
                        building_segment_roof_areas[
                            "total_envelope_roof_area"
                        ] += getattr_(surface, "surface", "area")

                        building_segment_roof_areas["total_skylight_area"] += pint_sum(
                            find_all("subsurfaces[*].glazed_area"), surface
                        ) + pint_sum(find_all("subsurfaces[*].opaque_area", surface))

    # return building_segment_roof_areas_dict
