"""Transparent lifestyle *education*, separate from the ML model.

Rules are simple demo thresholds, NOT learned model explanations or clinical
risk cutoffs. No medical diagnosis, treatment, exercise prescription or
individualized health assessment is made here.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Suggestion:
    icon: str
    title: str
    description: str
    category: str
    tint: str


def _smokes(value: object) -> bool:
    return str(value).strip().lower() in {"yes", "true", "1", "y"}


def get_wellness_suggestions(values: dict) -> list[Suggestion]:
    """Return deterministic, non-diagnostic wellness ideas from four fields.

    The activity_index / nutrition_quality rules (<3 and <5) are illustrative
    dataset-scale prompts, not medical thresholds; the sleep reminder applies
    to the adults represented in the source dataset.
    """
    ideas: list[Suggestion] = []
    if float(values["sleep_hours"]) < 7:
        ideas.append(Suggestion("🌙", "Build a consistent sleep routine",
            "Consider consistent bedtimes and wake times. Many adults benefit from about 7–9 hours of sleep.",
            "Sleep", "violet"))
    if float(values["activity_index"]) < 3:
        ideas.append(Suggestion("🚶", "Add movement that works for you",
            "Consider small, sustainable activity breaks and gradually build toward more regular movement. The activity index is a dataset score, not minutes of exercise.",
            "Activity", "cyan"))
    if float(values["nutrition_quality"]) < 5:
        ideas.append(Suggestion("🥗", "Choose a variety of nourishing foods",
            "Consider more variety in meals, including fruits, vegetables and other nutritious foods when accessible. The nutrition score is from the dataset.",
            "Nutrition", "amber"))
    if _smokes(values["smokes"]):
        ideas.append(Suggestion("💚", "Explore support for quitting smoking",
            "Quitting tobacco can benefit long-term health. If you want to quit, a healthcare professional or local stop-smoking service can help.",
            "Smoking", "mint"))
    if not ideas:
        ideas.extend([
            Suggestion("✨", "Keep habits sustainable",
                "Maintain a sleep, meal and movement routine that fits your circumstances; the model prediction does not certify anyone's health.",
                "Wellbeing", "violet"),
            Suggestion("🧭", "Look beyond a model label",
                "Fitness is multifaceted. A binary educational model is not a substitute for medical or professional fitness assessment.",
                "Perspective", "cyan"),
        ])
    return ideas


RULE_EXPLANATION = (
    "These cards use simple example rules only: adult sleep under 7 hours, "
    "activity_index below 3, nutrition_quality below 5, and smoking = Yes. "
    "The activity and nutrition cutoffs are illustrative dataset-scale values, "
    "not validated medical thresholds. The suggestions are independent of the "
    "ML classifier and do not explain why its label was predicted."
)
