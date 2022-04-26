from rct229.data.schema_enums import schema_enums
from rct229.ruleset_functions.get_surface_conditioning_category_dict import (
    get_surface_conditioning_category_dict,
    SurfaceConditioningCategory as SCC,
)
from rct229.utils.assertions import assert_required_fields, getattr_
from rct229.utils.jsonpath_utils import find_all

DOOR = schema_enums["SubsurfaceClassificationType"].DOOR.name

# Intended for internal use
GET_BUILDING_SCC_WINDOW_WALL_RATIO_DICT__REQUIRED_FIELDS = {
    "building": {
        "$..surfaces[*]": ["area"],
        "$..subsurfaces[*]": ["classification"],
    }
}


def get_building_scc_window_wall_ratios_dict(climate_zone, building):
    """Determines the window to wall ratio for each surface conditioning category
    in a building

    Parameters
    ----------
    climate_zone : str
        One of the ClimateZone2019ASHRAE901 enumerated values
    building : dict
        A dictionary representing a building as defined by the ASHRAE229 schema

    Returns
    -------
    dict
        A dictionary that maps each surface conditioning category to its average
        window to wall ratio
    """
    assert_required_fields(
        GET_BUILDING_SCC_WINDOW_WALL_RATIO_DICT__REQUIRED_FIELDS["building"], building
    )

    # Get the conditioning category for all the surfaces in the building
    scc_dict = get_surface_conditioning_category_dict(climate_zone, building)

    # Loop through all the surfaces in the building
    for surface in find_all("$..surfaces[*]", building):
        # surface conditioning category
        scc = scc_dict[surface["id"]]

        # Initialize total window areas
        total_res_window_area = ZERO.AREA
        total_nonres_window_area = ZERO.AREA
        total_mixed_window_area = ZERO.AREA
        total_semi_exterior_window_area = ZERO.AREA

        # Initialize total wall areas
        total_res_wall_area = ZERO.AREA
        total_nonres_wall_area = ZERO.AREA
        total_mixed_wall_area = ZERO.AREA
        total_semi_exterior_wall_area = ZERO.AREA

        if get_opaque_surface_type(surface) == OST.ABOVE_GRADE_WALL:
            surface_area = surface["area"]
            for subsurface in find_all("subsurfaces[*]", surface):
                glazed_area = subsurface.get("glazed_area", ZERO.AREA)
                opaque_area = subsurface.get("opaque_area", ZERO.AREA)
                window_area = (
                    glazed_area + opaque_area
                    if subsurface["classification"] != DOOR
                    or (glazed_area > opaque_area)
                    else ZERO.AREA
                )

            if scc == SCC.EXTERIOR_RESIDENTIAL:
                total_res_wall_area += surface_area
                toal_res_window_area += window_area
            elif scc == SCC.EXTERIOR_NON_RESIDENTIAL:
                total_nonres_wall_area += surface_area
                toal_nonres_window_area += window_area
            elif scc == SCC.EXTERIOR_MIXED:
                total_mixed_wall_area += surface_area
                toal_mixed_window_area += window_area
            elif scc == SCC.SEMI_EXTERIOR:
                total_semi_exterior_wall_area += surface_area
                toal_semi_exterior_window_area += window_area
            else:
                assert scc == SCC.UNREGULATED

    return {
        SCC.EXTERIOR_RESIDENTIAL: total_res_window_area / total_res_wall_area
        if total_res_wall_area > 0
        else 0,
        SCC.EXTERIOR_NON_RESIDENTIAL: total_nonres_window_area / total_nonres_wall_area
        if total_nonres_wall_area > 0
        else 0,
        SCC.EXTERIOR_MIXED: total_mixed_window_area / total_mixed_wall_area
        if total_mixed_wall_area > 0
        else 0,
        SCC.SEMI_EXTERIOR: total_semi_exterior_window_area
        / total_semi_exterior_wall_area
        if total_semi_exterior_wall_area > 0
        else 0,
    }
