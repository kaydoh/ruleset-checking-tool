import pytest

from rct229.data import data
from rct229.data.schema_enums import schema_enums
from rct229.data_fns.table_G3_8_fns import (
    lighting_space_enumeration_to_lpd_space_type_map,
    table_G3_8_lpd,
)
from rct229.data_fns.table_utils import (
    check_enumeration_to_osstd_match_field_value_map,
    find_osstd_table_entry,
)


# Testing table_G3_8_lpd() ------------------------------------------
def test__table_G3_8_lpd__automotive_facility():
    assert table_G3_8_lpd("AUTOMOTIVE_FACILITY") == 0.9


def test__table_G3_8_lpd__convention_center():
    assert table_G3_8_lpd("CONVENTION_CENTER") == 1.20


def test_t_able_G3_8_lpd__courthouse():
    assert table_G3_8_lpd("COURTHOUSE") == 1.20


def test__table_G3_8_lpd__workshop():
    assert table_G3_8_lpd("WORKSHOP") == 1.40


def test__table_G3_8_lpd__warehouse():
    assert table_G3_8_lpd("WAREHOUSE") == 0.80


def test__table_G3_8_lpd__courthouse():
    assert table_G3_8_lpd("COURTHOUSE") == 1.20


# Testing lighting_space_enumeration_to_lpd_space_type_map ----------
def test__lighting_space_enumeration_to_lpd_space_type_map():
    # check_enumeration_to_osstd_match_field_value_map() will throw exception(s)
    # when a check fails
    check_enumeration_to_osstd_match_field_value_map(
        match_field_name="lpd_space_type",
        enum_type="LightingSpaceType2019ASHRAE901T951TG38",
        osstd_table=data["ashrae_90_1_prm_2019.prm_interior_lighting"],
        enumeration_to_match_field_value_map=lighting_space_enumeration_to_lpd_space_type_map,
        exclude_enum_names=["NONE"],
    )
