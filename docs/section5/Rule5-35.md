
# Envelope - Rule 5-35  

**Rule ID:** 5-35  
**Rule Description:**  If the skylight area of the proposed design is greater than 3%, baseline skylight area shall be decreased by an identical percentage in all roof components in which skylights are located to reach 3%.  
**Rule Assertion:** B-RMR total (subsurface.glazed_area+subsurface.opaque_area) = expected value for each zone  
**Appendix G Section:** Section G3.1-5(e) Building Envelope Modeling Requirements for the Baseline building  
**Appendix G Section Reference:** None  

**Applicability:** All required data elements exist for B_RMR  
**Applicability Checks:**  None  

**Manual Check:** None  
**Evaluation Context:** Each Data Element  
**Data Lookup:** None  
**Function Call:**  

  1. get_building_segment_skylight_roof_areas()  
  2. match_data_element()

## Rule Logic:

- Get skylight roof areas dictionary for B_RMR: `skylight_roof_areas_dictionary_b = get_building_segment_skylight_roof_areas(B_RMR)`

- Get skylight roof areas dictionary for P_RMR: `skylight_roof_areas_dictionary_p = get_building_segment_skylight_roof_areas(P_RMR)`

- For each building segment in B_RMR: `for building_segment_b in B_RMR.building.building_segments:`

  - Calculate skylight roof ratio for building segment: `skylight_roof_ratio_b = skylight_roof_areas_dictionary_b[building_segment_b.id][0] / skylight_roof_areas_dictionary_b[building_segment_b.id][1]`

  - Get matching building segment in P_RMR: `building_segment_p = match_data_element(P_RMR, BuildingSegments, building_segment_b.id)`

    - Calculate skylight roof ratio for building segment in P_RMR: `skylight_roof_ratio_p = skylight_roof_areas_dictionary_p[building_segment_p.id][0] / skylight_roof_areas_dictionary_p[building_segment_p.id][1]`

      - Check if skylight roof ratio in P_RMR is greater than 3%: `if skylight_roof_ratio_p > 0.03:`

        **Rule Assertion:** 

        - Case 1: For each building segment in B_RMR, the skylight to roof ratio is equal to 3%: `if skylight_roof_ratio_b == 0.03: PASS`  

        - Case 2: Else: `Else: FAIL`

**[Back](../_toc.md)**
