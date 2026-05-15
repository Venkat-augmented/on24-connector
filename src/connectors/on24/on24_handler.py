import asyncio
from datetime import UTC, datetime, timedelta
from typing import Any

from src.connectors.on24.constants import DEFAULT_LOOKBACK_DAYS
from src.temporal.trigger_on24_workflow import trigger_on24_workflow
from src.utils.logger import get_logger

logger = get_logger(__name__)


class ON24Handler:
    def __init__(self, client: str):
        self.client = client

    def run(
        self,
        request_id: str,
        start_date: str | None = None,
        end_date: str | None = None,
        trigger_workflow: bool = True,
    ) -> dict[str, Any]:

        today = datetime.now(UTC)

        if not end_date:
            end_date = today.strftime("%Y-%m-%d")

        if not start_date:
            start_date = (
                today - timedelta(days=DEFAULT_LOOKBACK_DAYS)
            ).strftime("%Y-%m-%d")

        logger.info(
            f"Running ON24 connector "
            f"client={self.client} "
            f"start_date={start_date} "
            f"end_date={end_date}"
        )

        workflow_result = None

        if trigger_workflow:
            workflow_result = asyncio.run(
                trigger_on24_workflow(
                    client_name=self.client,
                    start_date=start_date,
                    end_date=end_date,
                    request_id=request_id,
                )
            )

        return {
            "status": "SUCCESS",
            "connector": "on24",
            "client": self.client,
            "start_date": start_date,
            "end_date": end_date,
            "workflow_triggered": trigger_workflow,
            "workflow_id": workflow_result["workflow_id"] if workflow_result else None,
            "workflow_run_id": workflow_result["run_id"] if workflow_result else None,
            "records_fetched": 0,
            "rows_inserted": 0,
        }