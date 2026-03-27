from enum import Enum

from pydantic import AnyUrl, BaseModel, Field, field_validator, model_validator


class MuscleGroup(str, Enum):
    chest = "chest"
    back = "back"
    shoulders = "shoulders"
    biceps = "biceps"
    triceps = "triceps"
    core = "core"
    glutes = "glutes"
    calves = "calves"
    forearms = "forearms"
    quadriceps = "quadriceps"
    hamstrings = "hamstrings"


class Equipment(str, Enum):
    bodyweight = "bodyweight"
    dumbbell = "dumbbell"
    barbell = "barbell"
    machine = "machine"
    cable = "cable"
    smith = "smith"


class Difficulty(str, Enum):
    beginner = "beginner"
    intermediate = "intermediate"
    advanced = "advanced"


class ExerciseBase(BaseModel):
    name: str
    primary_muscles: list[MuscleGroup] = Field(min_length=1)
    secondary_muscles: list[MuscleGroup] = Field(default_factory=list)
    equipment: Equipment
    difficulty: Difficulty
    instructions: str | None = None
    media_url: AnyUrl | None = None

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("name cannot be empty or whitespace-only")
        return value.strip()

    @model_validator(mode="after")
    def validate_muscle_overlap(self) -> "ExerciseBase":
        overlap = set(self.primary_muscles) & set(self.secondary_muscles)
        if overlap:
            raise ValueError("muscles cannot appear in both primary_muscles and secondary_muscles")
        return self


class ExerciseInput(ExerciseBase):
    pass


class Exercise(ExerciseBase):
    id: int
