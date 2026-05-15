import uuid

from temporalio.common import WorkflowIDReusePolicy

from src.temporal.temporal_client import get_temporal_client
from src.connectors.on24.constants import (
    ON24_TASK_QUEUE,
    WORKFLOW_NAME,
)


async def trigger_on24_workflow(
    *,
    client_name: str,
    start_date: str,
    end_date: str,
    request_id: str,
):

    client = await get_temporal_client()

    workflow_id = f"on24-{client_name}-{uuid.uuid4()}"

    handle = await client.start_workflow(
        WORKFLOW_NAME,
        {
            "client": client_name,
            "start_date": start_date,
            "end_date": end_date,
            "request_id": request_id,
        },
        id=workflow_id,
        task_queue=ON24_TASK_QUEUE,
        id_reuse_policy=WorkflowIDReusePolicy.ALLOW_DUPLICATE,
    )

    return {
        "workflow_id": workflow_id,
        "run_id": handle.result_run_id,
    }