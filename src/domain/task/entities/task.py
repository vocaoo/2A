from dataclasses import dataclass, field
from datetime import datetime
from typing import Self

from src.domain.common.entities import AggregateRoot
from src.domain.task.exceptions import TaskIsDeleted
from src.domain.task.events import TaskCreated, TaskCompleted, TaskChecked, TaskRejected, TaskDelayed, TaskDeleted
from src.domain.task.value_objects import (
    TaskID,
    Code,
    Name,
    Address,
    Comment,
    CompletionDate,
    Coordinates,
    Implementer,
    Indication,
    PhotoURL,
    Status,
    StatusState,
    DeletionTime,
)


@dataclass
class Task(AggregateRoot):
    task_id: TaskID
    code: Code
    name: Name
    address: Address
    indication: Indication
    implementer: Implementer
    coordinates: Coordinates
    comment: Comment
    status: Status = field(default=StatusState.EXECUTING)
    photo_url: PhotoURL = field(default=PhotoURL(None, None))
    completion_date: CompletionDate = field(default=CompletionDate(None))
    deleted_at: DeletionTime = field(
        default=DeletionTime.create_not_deleted(), kw_only=True
    )

    @classmethod
    def create_task(
        cls,
        task_id: TaskID,
        code: Code,
        name: Name,
        address: Address,
        indication: Indication,
        implementer: Implementer,
        coordinates: Coordinates,
        comment: Comment
    ) -> Self:
        task = cls(
            task_id=task_id,
            code=code,
            name=name,
            address=address,
            indication=indication,
            implementer=implementer,
            coordinates=coordinates,
            comment=comment
        )
        task.record_event(
            TaskCreated(
                task_id=task_id.to_raw(),
                code=code.to_raw(),
                name=name.to_raw(),
                address=address.to_raw(),
                implementer=implementer.to_raw(),
                latitude=coordinates.latitude,
                longitude=coordinates.longitude,
                current_indication=indication.current,
                previous_indication=indication.previous,
                status=task.status,
            )
        )

        return task

    def complete_task(
        self,
        photo_url: PhotoURL,
        indication: Indication,
        coordinates: Coordinates,
        comment: Comment,
    ) -> None:
        self._validate_not_deleted()

        self.photo_url = photo_url
        self.coordinates = coordinates
        self.indication = indication
        self.comment = comment
        self.status = StatusState.CHECKING
        self.completion_date = CompletionDate(datetime.utcnow())
        self.record_event(
            TaskCompleted(
                task_id=self.task_id.to_raw(),
                near_photo_url=self.photo_url.near,
                far_photo_url=self.photo_url.far,
                latitude=self.coordinates.latitude,
                longitude=self.coordinates.longitude,
                current_indication=self.indication.current,
                previous_indication=self.indication.previous,
                status=self.status,
                comment=self.comment.to_raw(),
                completion_date=self.completion_date.to_raw(),
            )
        )

    def check_task(self) -> None:
        self._validate_not_deleted()

        self.status = StatusState.COMPLETED
        self.record_event(
            TaskChecked(
                task_id=self.task_id.to_raw(),
                status=self.status,
            )
        )

    def reject_task(self) -> None:
        self._validate_not_deleted()

        self.indication = Indication(self.indication.current, None)
        self.status = StatusState.EXECUTING
        self.record_event(
            TaskRejected(
                task_id=self.task_id.to_raw(),
                current_indication=self.indication.current,
                status=self.status,
            )
        )

    def delay_task(self) -> None:
        self._validate_not_deleted()

        self.status = StatusState.OVERDUE
        self.record_event(
            TaskDelayed(
                task_id=self.task_id.to_raw(),
                status=self.status,
            )
        )

    def delete_task(self) -> None:
        self._validate_not_deleted()
        self.status = StatusState.DELETED

        self.deleted_at.create_deleted()
        self.record_event(
            TaskDeleted(
                task_id=self.task_id.to_raw()
            )
        )

    def _validate_not_deleted(self) -> None:
        if self.deleted_at.is_deleted():
            raise TaskIsDeleted(self.task_id.to_raw())
