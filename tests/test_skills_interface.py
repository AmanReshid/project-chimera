"""
Central test file for all skill interfaces.

Purpose:
- Ensure every declared skill has interface.py
- Verify correct Input & Output model names
- Confirm they are valid Pydantic BaseModel subclasses
- Basic smoke checks (instantiation, required fields)

Run with: pytest tests/test_skills_interface.py -v
"""

import pytest
from pydantic import BaseModel, ValidationError
import importlib


# List of all skill folder names (snake_case)
SKILLS = [
    "trend_fetcher",
    "content_publish",
    "content_generate_image",
    # "wallet_check_balance",   # uncomment when you create this skill
    # Add new skills here when created
]


def get_interface_module(skill_name: str):
    """Import the interface module for a given skill."""
    module_name = f"skills.{skill_name}.interface"
    try:
        return importlib.import_module(module_name)
    except ImportError as e:
        pytest.fail(
            f"Cannot import {module_name} → "
            f"does skills/{skill_name}/interface.py exist?"
        )


def get_input_output_classes(module, skill_name: str):
    """Find Input and Output classes using correct naming pattern."""
    # Convert snake_case → CamelCase
    camel = ''.join(word.capitalize() for word in skill_name.split('_'))

    # Special case for skills that start with 'content_' or similar
    if skill_name.startswith("content_"):
        prefix = "Content" + camel[len("content_"):]
    else:
        prefix = camel

    input_name = f"{prefix}Input"
    output_name = f"{prefix}Output"

    input_cls = getattr(module, input_name, None)
    output_cls = getattr(module, output_name, None)

    if input_cls is None:
        pytest.fail(
            f"Skill '{skill_name}' missing expected Input class: {input_name}"
        )
    if output_cls is None:
        pytest.fail(
            f"Skill '{skill_name}' missing expected Output class: {output_name}"
        )

    assert issubclass(input_cls, BaseModel), f"{input_name} is not a Pydantic model"
    assert issubclass(output_cls, BaseModel), f"{output_name} is not a Pydantic model"

    return input_cls, output_cls


# ────────────────────────────────────────────────
# Core tests
# ────────────────────────────────────────────────

@pytest.mark.parametrize("skill_name", SKILLS)
def test_skill_has_valid_interface(skill_name):
    """Every skill must have interface.py + Input + Output models"""
    module = get_interface_module(skill_name)
    get_input_output_classes(module, skill_name)


@pytest.mark.parametrize("skill_name", SKILLS)
def test_skill_input_requires_fields(skill_name):
    """Instantiating Input with no args should fail (required fields enforced)"""
    module = get_interface_module(skill_name)
    InputModel, _ = get_input_output_classes(module, skill_name)

    with pytest.raises(ValidationError):
        InputModel()


@pytest.mark.parametrize("skill_name", SKILLS)
def test_skill_output_can_be_instantiated(skill_name):
    """Output model should at least accept success=False"""
    module = get_interface_module(skill_name)
    _, OutputModel = get_input_output_classes(module, skill_name)

    minimal = OutputModel(success=False)
    assert minimal.success is False

    success_case = OutputModel(success=True)
    assert success_case.success is True


# ────────────────────────────────────────────────
# Skill-specific extra checks (add more as needed)
# ────────────────────────────────────────────────

def test_content_generate_image_input_has_character_reference():
    module = get_interface_module("content_generate_image")
    InputModel, _ = get_input_output_classes(module, "content_generate_image")
    fields = InputModel.model_fields
    assert "character_reference_id" in fields, \
        "ImageGenerationInput must have character_reference_id"


def test_trend_fetcher_input_has_niche():
    module = get_interface_module("trend_fetcher")
    InputModel, _ = get_input_output_classes(module, "trend_fetcher")
    fields = InputModel.model_fields
    assert "niche" in fields
    assert "lookback_hours" in fields