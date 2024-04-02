from datetime import datetime
from typing import cast

from src.application.common.exceptions import MappingError
from src.application.task import dto
from src.domain.task import value_objects as vo
from src.domain.task.entities import Task as TaskEntity
from src.infrastructure.database.models import Task as TaskModel


def convert_task_entity_to_db_model(task: TaskEntity) -> TaskModel:
    return TaskModel(
        task_id=task.task_id.to_raw(),
        code=task.code.to_raw(),
        name=task.name.to_raw(),
        address=task.address.to_raw(),
        current_indication=task.indication.current,
        previous_indication=task.indication.previous,
        implementer=task.implementer.to_raw(),
        latitude=task.coordinates.latitude,
        longitude=task.coordinates.longitude,
        comment=task.comment.to_raw(),
        status=task.status,
        near_photo_url=task.photo_url.near,
        far_photo_url=task.photo_url.far,
        completion_date=task.completion_date.to_raw(),
        deleted_at=task.deleted_at.to_raw(),
    )


def convert_db_model_to_task_entity(task: TaskModel) -> TaskEntity:
    indication = vo.Indication(current=task.current_indication, previous=task.previous_indication)
    coordinates = vo.Coordinates(longitude=task.longitude, latitude=task.latitude)
    photos = vo.PhotoURL(near=task.near_photo_url, far=task.far_photo_url)
    return TaskEntity(
        task_id=vo.TaskID(task.task_id),
        code=vo.Code(task.code),
        name=vo.Name(task.name),
        address=vo.Address(task.address),
        indication=indication,
        implementer=vo.Implementer(task.implementer),
        coordinates=coordinates,
        comment=vo.Comment(task.comment),
        status=vo.Status(task.status),
        photo_url=photos,
        completion_date=vo.CompletionDate(task.completion_date),
        deleted_at=vo.DeletionTime(task.deleted_at),
    )


def convert_db_model_to_active_task_dto(task: TaskModel) -> dto.Task:
    if task.deleted_at is not None:
        raise MappingError(f"Task {task} is deleted")

    return dto.Task(
        task_id=task.task_id,
        code=task.code,
        name=task.name,
        address=task.address,
        current_indication=task.current_indication,
        previous_indication=task.previous_indication,
        implementer=task.implementer,
        latitude=task.latitude,
        longitude=task.longitude,
        comment=task.comment,
        status=task.status,
        near_photo_url=task.near_photo_url,
        far_photo_url=task.far_photo_url,
        completion_date=task.completion_date,
    )


def convert_db_model_to_deleted_task_dto(task: TaskModel) -> dto.DeletedTask:
    return dto.DeletedTask(
        task_id=task.task_id,
        code=task.code,
        name=task.name,
        address=task.address,
        current_indication=task.current_indication,
        previous_indication=task.previous_indication,
        implementer=task.implementer,
        latitude=task.latitude,
        longitude=task.longitude,
        comment=task.comment,
        status=task.status,
        near_photo_url=task.near_photo_url,
        far_photo_url=task.far_photo_url,
        completion_date=task.completion_date,
        deleted_at=cast(datetime, task.deleted_at)
    )


def convert_db_model_to_task_dto(task: TaskModel) -> dto.TasksDTOs:
    match task:
        case TaskModel(deleted_at=None):
            return convert_db_model_to_active_task_dto(task)
        case TaskModel(deleted_at=True):
            return convert_db_model_to_deleted_task_dto(task)
        case _:
            raise MappingError(f"Task {task} is invalid")
