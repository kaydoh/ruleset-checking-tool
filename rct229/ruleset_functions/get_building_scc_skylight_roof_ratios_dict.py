from rct229.data.schema_enums import schema_enums
from rct229.ruleset_functions.get_opaque_surface_type import OpaqueSurfaceType as OST
from rct229.ruleset_functions.get_opaque_surface_type import get_opaque_surface_type
from rct229.ruleset_functions.get_surface_conditioning_category_dict import (
    SurfaceConditioningCategory as SCC,
)
from rct229.ruleset_functions.get_surface_conditioning_category_dict import (
    get_surface_conditioning_category_dict,
)
from rct229.utils.assertions import getattr_
from rct229.utils.jsonpath_utils import find_all
from rct229.utils.pint_utils import ZERO

DOOR = schema_enums["SubsurfaceClassificationType"].DOOR.name


def get_building_scc_skylight_roof_ratios_dict(climate_zone, building):
    # required fields for this function are coming from the nested functions
    scc_dictionary = get_surface_conditioning_category_dict(climate_zone, building)
    total_res_roof_area = ZERO.AREA
    total_res_skylight_area = ZERO.AREA
    total_nonres_roof_area = ZERO.AREA
    total_nonres_skylight_area = ZERO.AREA
    total_semiheated_roof_area = ZERO.AREA
    total_semiheated_skylight_area = ZERO.AREA

    for surface in find_all("building_segments[*].zones[*].surfaces[*]", building):
        floor_area = getattr_(surface, "surface", "area")
        skylight_area = _helper_calculate_skylight_area(surface)
        if get_opaque_surface_type(surface) == OST.ROOF:
            if scc_dictionary[surface["id"]] == SCC.EXTERIOR_RESIDENTIAL:
                total_res_roof_area += floor_area
                total_res_skylight_area += skylight_area
            elif scc_dictionary[surface["id"]] == SCC.EXTERIOR_NON_RESIDENTIAL:
                total_nonres_roof_area += floor_area
                total_nonres_skylight_area += skylight_area
            elif scc_dictionary[surface["id"]] == SCC.SEMI_EXTERIOR:
                total_semiheated_roof_area += floor_area
                total_semiheated_skylight_area += skylight_area

    srr_res = 0.0
    srr_nonres = 0.0
    srr_semiheated = 0.0
    if total_res_roof_area > ZERO.AREA:
        srr_res = total_res_skylight_area / total_res_roof_area
    if total_nonres_roof_area > ZERO.AREA:
        srr_nonres = total_nonres_skylight_area / total_nonres_roof_area
    if total_semiheated_roof_area > ZERO.AREA:
        srr_semiheated = total_semiheated_skylight_area / total_semiheated_roof_area

    return {
        SCC.EXTERIOR_RESIDENTIAL: srr_res,
        SCC.EXTERIOR_NON_RESIDENTIAL: srr_nonres,
        SCC.SEMI_EXTERIOR: srr_semiheated,
    }


def _helper_calculate_skylight_area(surface):
    total_glazed_area = ZERO.AREA
    for subsurface in find_all("subsurfaces[*]", surface):
        glazed_area = getattr_(subsurface, "subsurface", "glazed_area")
        opaque_area = getattr_(subsurface, "subsurface", "opaque_area")
        if getattr_(subsurface, "subsurface", "classification") == DOOR:
            if glazed_area > opaque_area:
                total_glazed_area += glazed_area + opaque_area
        else:
            total_glazed_area += glazed_area + opaque_area
    return total_glazed_area
