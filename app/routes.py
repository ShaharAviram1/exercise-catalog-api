from fastapi import APIRouter, Depends, HTTPException, Response, status

from app.models import Exercise, ExerciseCreateUpdate
from app.repository import ExerciseRepository

router = APIRouter(prefix="/exercises", tags=["exercises"])


def get_repository() -> ExerciseRepository:
    return exercise_repository


exercise_repository = ExerciseRepository()


@router.post("", response_model=Exercise, status_code=status.HTTP_201_CREATED)
def create_exercise(
    exercise_data: ExerciseCreateUpdate,
    repository: ExerciseRepository = Depends(get_repository),
) -> Exercise:
    return repository.create(exercise_data)


@router.get("", response_model=list[Exercise])
def list_exercises(
    repository: ExerciseRepository = Depends(get_repository),
) -> list[Exercise]:
    return repository.list_all()


@router.get("/{exercise_id}", response_model=Exercise)
def get_exercise(
    exercise_id: int,
    repository: ExerciseRepository = Depends(get_repository),
) -> Exercise:
    exercise = repository.get(exercise_id)
    if exercise is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Exercise not found")
    return exercise


@router.put("/{exercise_id}", response_model=Exercise)
def update_exercise(
    exercise_id: int,
    exercise_data: ExerciseCreateUpdate,
    repository: ExerciseRepository = Depends(get_repository),
) -> Exercise:
    exercise = repository.update(exercise_id, exercise_data)
    if exercise is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Exercise not found")
    return exercise


@router.delete("/{exercise_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_exercise(
    exercise_id: int,
    repository: ExerciseRepository = Depends(get_repository),
) -> Response:
    deleted = repository.delete(exercise_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Exercise not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
