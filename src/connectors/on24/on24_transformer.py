from typing import Any


def flatten_event(event: dict[str, Any]) -> dict[str, Any]:
    return {
        "event_id": event.get("id"),
        "title": event.get("name"),
        "start_time": event.get("startTime"),
        "end_time": event.get("endTime"),
        "status": event.get("status"),
    }


def flatten_registrant(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "email": row.get("email"),
        "first_name": row.get("firstName"),
        "last_name": row.get("lastName"),
        "company": row.get("company"),
    }