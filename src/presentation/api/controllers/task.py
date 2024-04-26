from typing import Annotated
from uuid import UUID

from didiator import CommandMediator, Mediator, QueryMediator
from fastapi import APIRouter, Depends, Query, status, File, UploadFile as FUploadFile
from fastapi.responses import FileResponse, Response

from src.application.common.pagination.dto import Pagination, SortOrder
from src.application.task import dto
from src.application.task.commands import (
    CompleteTask,
    CheckTask,
    CreateTask,
    DelayTask,
    DeleteTask,
    RejectTask,
    UploadFile,
    ClearDatabase
)
from src.application.task.interfaces.persistence import GetTaskFilters
from src.application.task.queries import GetTaskByID, GetTaskByCode, GetTasks, GetFile
from src.domain.common.const import Empty
from src.presentation.api.controllers.responses.base import OkResponse
from src.presentation.api.providers.stub import Stub
from src.domain.task.value_objects import StatusState
from src.presentation.api.controllers.requests.task import CompleteTaskData

task_router = APIRouter(
    prefix="/tasks",
    tags=["tasks"],
)


@task_router.post(
    "/",
    responses={status.HTTP_201_CREATED: {"model": dto.Task}},
    status_code=status.HTTP_201_CREATED,
)
async def create_task(
    command: CreateTask,
    mediator: Annotated[Mediator, Depends(Stub(Mediator))],
) -> OkResponse[dto.TasksDTOs]:
    task_id = await mediator.send(command)
    task = await mediator.query(GetTaskByID(task_id=task_id))
    return OkResponse(result=task)


@task_router.get(
    "/@{code}",
    responses={status.HTTP_200_OK: {"model": dto.Task}}
)
async def get_task_by_code(
    code: str,
    mediator: Annotated[QueryMediator, Depends(Stub(QueryMediator))],
) -> OkResponse[dto.Task]:
    task = await mediator.query(GetTaskByCode(code=code))
    return OkResponse(result=task)


@task_router.get(
    "/{task_id}",
    responses={status.HTTP_200_OK: {"model": dto.TasksDTOs}}
)
async def get_task_by_id(
    task_id: UUID,
    mediator: Annotated[QueryMediator, Depends(Stub(QueryMediator))],
) -> OkResponse[dto.TasksDTOs]:
    task = await mediator.query(GetTaskByID(task_id=task_id))
    return OkResponse(result=task)


@task_router.get("/")
async def get_tasks(
    mediator: Annotated[QueryMediator, Depends(Stub(QueryMediator))],
    deleted: bool | None = None,
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=0, le=1000)] = 1000,
    order: SortOrder = SortOrder.ASC,
    condition: StatusState = StatusState.EXECUTING,
) -> OkResponse[dto.Tasks]:
    tasks = await mediator.query(
        GetTasks(
            filters=GetTaskFilters(deleted if deleted is not None else Empty.UNSET),
            pagination=Pagination(
                offset=offset,
                limit=limit,
                order=order,
            ),
            status=condition,
        )
    )
    return OkResponse(result=tasks)


@task_router.put("/{task_id}/complete")
async def complete_task(
    task_id: UUID,
    data: CompleteTaskData,
    mediator: Annotated[CommandMediator, Depends(Stub(CommandMediator))],
) -> OkResponse[None]:
    command = CompleteTask(
        task_id=task_id,
        near_photo_url=data.near_photo_url,
        far_photo_url=data.far_photo_url,
        current_indication=data.current_indication,
        previous_indication=data.previous_indication
    )
    await mediator.send(command)
    return OkResponse()


@task_router.put("/{tack_id}/check")
async def check_task(
    task_id: UUID,
    mediator: Annotated[CommandMediator, Depends(Stub(CommandMediator))],
) -> OkResponse[None]:
    await mediator.send(CheckTask(task_id=task_id))
    return OkResponse()


@task_router.put("/{tack_id}/reject")
async def reject_task(
    task_id: UUID,
    mediator: Annotated[CommandMediator, Depends(Stub(CommandMediator))],
) -> OkResponse[None]:
    await mediator.send(RejectTask(task_id=task_id))
    return OkResponse()


@task_router.put("/{tack_id}/delay")
async def delay_task(
    task_id: UUID,
    mediator: Annotated[CommandMediator, Depends(Stub(CommandMediator))],
) -> OkResponse[None]:
    await mediator.send(DelayTask(task_id=task_id))
    return OkResponse()


@task_router.delete("/{tack_id}/delete")
async def delete_task(
    task_id: UUID,
    mediator: Annotated[CommandMediator, Depends(Stub(CommandMediator))],
) -> OkResponse[None]:
    await mediator.send(DeleteTask(task_id=task_id))
    return OkResponse()


@task_router.post("/upload")
async def upload_task(
    mediator: Annotated[CommandMediator, Depends(Stub(CommandMediator))],
    file: FUploadFile = File(),
) -> OkResponse[None]:
    await mediator.send(UploadFile(file=file.file))
    return OkResponse()


@task_router.delete("/clear")
async def clear_database(
    mediator: Annotated[CommandMediator, Depends(Stub(CommandMediator))],
) -> OkResponse[None]:
    await mediator.send(ClearDatabase())
    return OkResponse()


@task_router.post("/download")
async def download(
    mediator: Annotated[QueryMediator, Depends(Stub(QueryMediator))],
    deleted: bool | None = None,
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=0, le=1000)] = 1000,
    order: SortOrder = SortOrder.ASC,
    condition: StatusState = StatusState.CHECKING,
) -> FileResponse:
    file = await mediator.query(
        GetFile(
            filters=GetTaskFilters(deleted if deleted is not None else Empty.UNSET),
            pagination=Pagination(
                offset=offset,
                limit=limit,
                order=order,
            ),
            status=condition,
        )
    )
    headers = {
        'Content-Disposition': 'attachment; filename="Report.xlsx"',
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Headers": "*",
        "Access-Control_Allow-Methods": "POST, GET, OPTIONS",
    }
    return Response(
        content=file.getvalue(),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;charset=utf-8",
        headers=headers
    )
