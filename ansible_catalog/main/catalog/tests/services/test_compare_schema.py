""" Test comparison of the two schemas """
import pytest

from ansible_catalog.main.catalog.tests.factories import (
    PortfolioItemFactory,
    ServicePlanFactory,
)
from ansible_catalog.main.inventory.tests.factories import (
    ServiceOfferingFactory,
    InventoryServicePlanFactory,
)
from ansible_catalog.main.catalog.services.compare_schema import (
    CompareSchema,
)


SCHEMA = {
    "schemaType": "emptySchema",
    "schema": {
        "fields": [
            {
                "component": "plain-text",
                "name": "empty-service-plan",
                "label": "This product requires no user input and is fully configured by the system.",
            }
        ]
    },
}


SCHEMA_1 = {
    "schemaType": "default",
    "schema": {
        "fields": [
            {
                "component": "plain-text",
                "name": "empty-service-plan",
                "label": "Empty Service plan configured by the system.",
                "helper_text": "The new added field",
            },
            {
                "label": "State",
                "name": "state",
                "initial_value": "",
                "helper_text": "The state where you live",
                "is_required": True,
                "component": "select-field",
                "options": [
                    {"label": "NJ", "value": "NJ"},
                    {"label": "PA", "value": "PA"},
                    {"label": "OK", "value": "OK"},
                ],
                "validate": [{"type": "required-validator"}],
            },
        ],
        "title": "",
        "description": "",
    },
}

SCHEMA_2 = {
    "schemaType": "default",
    "schema": {
        "fields": [
            {
                "component": "plain-text",
                "name": "empty-service-plan",
                "label": "Empty Service plan configured by the system.",
            },
            {
                "label": "Number of Job templates",
                "name": "dev_null",
                "initial_value": 8,
                "helper_text": "Number of Job templates on this workflow",
                "is_required": True,
                "component": "text-field",
                "type": "number",
                "data_type": "integer",
                "options": [{"label": "", "value": ""}],
                "validate": [
                    {"type": "required-validator"},
                    {"type": "min-number-value", "value": 0},
                    {"type": "max-number-value", "value": 100},
                ],
            },
        ],
        "title": "",
        "description": "",
    },
}


SCHEMA_3 = {
    "schemaType": "default",
    "schema": {
        "fields": [
            {
                "name": "empty-service-plan",
                "label": "Empty Service plan configured by the system.",
            },
            {
                "label": "Number of Job templates",
                "name": "dev_null",
                "initial_value": 8,
                "helper_text": "Number of Job templates on this workflow",
                "component": "text-field",
                "type": "number",
                "data_type": "integer",
                "options": [{"label": "", "value": ""}],
                "validate": [
                    {"type": "required-validator"},
                    {"type": "min-number-value", "value": 0},
                    {"type": "max-number-value", "value": 100},
                ],
            },
        ],
        "title": "",
        "description": "",
    },
}


def test_is_empty_schema():
    assert CompareSchema.is_empty_schema(None) is True
    assert CompareSchema.is_empty_schema(SCHEMA) is True
    assert CompareSchema.is_empty_schema(SCHEMA_1) is False
    assert CompareSchema.is_empty_schema(SCHEMA_2) is False


def test_compare_schema():
    changed_info = CompareSchema.compare_schema(SCHEMA, SCHEMA)

    assert changed_info == ""

    changed_info = CompareSchema.compare_schema(SCHEMA_1, SCHEMA_2)

    assert (
        changed_info
        == "Schema fields changes have been detected: fields added: ['dev_null']; fields removed: ['state']; fields changed: ['empty-service-plan']"
    )

    changed_info = CompareSchema.compare_schema(SCHEMA_3, SCHEMA_2)

    assert (
        changed_info
        == "Schema fields changes have been detected: fields changed: ['empty-service-plan', 'dev_null']"
    )
