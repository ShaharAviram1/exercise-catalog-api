from app.models import Exercise, ExerciseInput


class ExerciseRepository:
    def __init__(self) -> None:
        self._exercises: dict[int, Exercise] = {}
        self._next_id = 1

    def list_all(self) -> list[Exercise]:
        return [self._exercises[exercise_id] for exercise_id in sorted(self._exercises)]

    def get(self, exercise_id: int) -> Exercise | None:
        return self._exercises.get(exercise_id)

    def create(self, exercise_data: ExerciseInput) -> Exercise:
        exercise = Exercise(id=self._next_id, **exercise_data.model_dump())
        self._exercises[self._next_id] = exercise
        self._next_id += 1
        return exercise

    def update(self, exercise_id: int, exercise_data: ExerciseInput) -> Exercise | None:
        if exercise_id not in self._exercises:
            return None

        exercise = Exercise(id=exercise_id, **exercise_data.model_dump())
        self._exercises[exercise_id] = exercise
        return exercise

    def delete(self, exercise_id: int) -> bool:
        if exercise_id not in self._exercises:
            return False

        del self._exercises[exercise_id]
        return True
