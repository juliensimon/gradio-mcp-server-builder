"""
Task Utilities Module

Provides utility functions and batch operations for task management.
Includes search, filtering, bulk operations, and data management tools.
"""

import json
from datetime import datetime, timedelta

# Dummy task data for utilities
DUMMY_TASKS = [
    {
        "id": 1,
        "title": "Implement user authentication system",
        "description": "Add login and registration functionality with JWT tokens",
        "priority": "high",
        "status": "in_progress",
        "created_at": "2024-01-15T10:00:00",
        "updated_at": "2024-01-20T14:30:00",
    },
    {
        "id": 2,
        "title": "Fix navigation menu bug",
        "description": "Menu items not displaying correctly on mobile devices",
        "priority": "medium",
        "status": "done",
        "created_at": "2024-01-16T09:15:00",
        "updated_at": "2024-01-18T16:45:00",
    },
    {
        "id": 3,
        "title": "Create landing page design",
        "description": "Design mockups for new homepage with modern UI",
        "priority": "low",
        "status": "todo",
        "created_at": "2024-01-17T11:30:00",
        "updated_at": "2024-01-17T11:30:00",
    },
    {
        "id": 4,
        "title": "Setup CI/CD pipeline",
        "description": "Configure automated testing and deployment workflows",
        "priority": "high",
        "status": "done",
        "created_at": "2024-01-18T08:00:00",
        "updated_at": "2024-01-22T17:20:00",
    },
    {
        "id": 5,
        "title": "Add search functionality",
        "description": "Implement full-text search across the platform",
        "priority": "medium",
        "status": "in_progress",
        "created_at": "2024-01-19T13:45:00",
        "updated_at": "2024-01-25T10:15:00",
    },
    {
        "id": 6,
        "title": "Write unit tests for API",
        "description": "Increase test coverage to 80% for all API endpoints",
        "priority": "medium",
        "status": "todo",
        "created_at": "2024-01-20T15:20:00",
        "updated_at": "2024-01-20T15:20:00",
    },
    {
        "id": 7,
        "title": "Optimize image loading",
        "description": "Implement lazy loading for better performance",
        "priority": "low",
        "status": "done",
        "created_at": "2024-01-21T12:10:00",
        "updated_at": "2024-01-24T09:30:00",
    },
]


def validate_priority(priority: str) -> bool:
    """Validate that priority is one of the allowed values."""
    return priority.lower() in ["low", "medium", "high"]


def validate_status(status: str) -> bool:
    """Validate that status is one of the allowed values."""
    return status.lower() in ["todo", "in_progress", "done"]


@mcp.tool()
def search_tasks(query: str) -> str:
    """
    Search tasks by title or description using text matching.

    Args:
        query: Search term to look for in task titles and descriptions

    Returns:
        JSON list of tasks matching the search criteria
    """
    query_lower = query.lower()
    matching_tasks = []

    for task in DUMMY_TASKS:
        title = task.get("title", "").lower()
        description = task.get("description", "").lower()

        if query_lower in title or query_lower in description:
            matching_tasks.append(task)

    return json.dumps(matching_tasks, indent=2)


@mcp.tool()
def bulk_update_priority(task_ids: str, new_priority: str) -> str:
    """
    Update priority for multiple tasks at once.

    Args:
        task_ids: Comma-separated list of task IDs (e.g., "1,2,3")
        new_priority: New priority level (low, medium, high)

    Returns:
        Summary of the bulk update operation
    """
    if not validate_priority(new_priority):
        return f"Invalid priority '{new_priority}'. Must be: low, medium, or high"

    try:
        ids = [int(id_str.strip()) for id_str in task_ids.split(",")]
    except ValueError:
        return "Invalid task IDs format. Use comma-separated integers (e.g., '1,2,3')"

    # Simulate bulk update with dummy data
    updated_count = 0
    not_found = []

    for task_id in ids:
        if any(task.get("id") == task_id for task in DUMMY_TASKS):
            updated_count += 1
        else:
            not_found.append(task_id)

    result = {
        "updated_count": updated_count,
        "not_found_ids": not_found,
        "new_priority": new_priority,
    }

    return json.dumps(result, indent=2)


@mcp.tool()
def filter_tasks_by_date(date_filter: str, days: int = 7) -> str:
    """
    Filter tasks by creation or update date.

    Args:
        date_filter: Filter type ('created_last', 'updated_last', 'created_before', 'updated_before')
        days: Number of days for the filter (default: 7)

    Returns:
        JSON list of tasks matching the date criteria
    """
    cutoff_date = datetime.now() - timedelta(days=days)
    filtered_tasks = []

    for task in DUMMY_TASKS:
        try:
            if date_filter in ["created_last", "created_before"] and task.get(
                "created_at"
            ):
                task_date = datetime.fromisoformat(
                    task["created_at"].replace("Z", "+00:00")
                )
                if (date_filter == "created_last" and task_date >= cutoff_date) or (
                    date_filter == "created_before" and task_date < cutoff_date
                ):
                    filtered_tasks.append(task)

            elif date_filter in ["updated_last", "updated_before"] and task.get(
                "updated_at"
            ):
                task_date = datetime.fromisoformat(
                    task["updated_at"].replace("Z", "+00:00")
                )
                if (date_filter == "updated_last" and task_date >= cutoff_date) or (
                    date_filter == "updated_before" and task_date < cutoff_date
                ):
                    filtered_tasks.append(task)
        except BaseException:
            continue

    return json.dumps(filtered_tasks, indent=2)


@mcp.tool()
def count_tasks_by_criteria(criteria: str, value: str) -> str:
    """
    Count tasks matching specific criteria.

    Args:
        criteria: What to count by ('status', 'priority', 'created_today', 'updated_today')
        value: Value to match (for status/priority) or ignored for date criteria

    Returns:
        JSON with count information
    """
    count = 0
    total_tasks = len(DUMMY_TASKS)
    today = datetime.now().date()

    for task in DUMMY_TASKS:
        if criteria == "status" and task.get("status", "").lower() == value.lower():
            count += 1
        elif (
            criteria == "priority" and task.get("priority", "").lower() == value.lower()
        ):
            count += 1
        elif criteria == "created_today" and task.get("created_at"):
            try:
                task_date = datetime.fromisoformat(
                    task["created_at"].replace("Z", "+00:00")
                ).date()
                if task_date == today:
                    count += 1
            except BaseException:
                continue
        elif criteria == "updated_today" and task.get("updated_at"):
            try:
                task_date = datetime.fromisoformat(
                    task["updated_at"].replace("Z", "+00:00")
                ).date()
                if task_date == today:
                    count += 1
            except BaseException:
                continue

    result = {
        "criteria": criteria,
        "value": value if criteria in ["status", "priority"] else "today",
        "count": count,
        "total_tasks": total_tasks,
        "percentage": round((count / total_tasks * 100), 1) if total_tasks > 0 else 0,
    }

    return json.dumps(result, indent=2)


@mcp.tool()
def cleanup_completed_tasks(days_old: int = 30) -> str:
    """
    Remove completed tasks older than specified days.

    Args:
        days_old: Remove completed tasks older than this many days (default: 30)

    Returns:
        Summary of cleanup operation
    """
    cutoff_date = datetime.now() - timedelta(days=days_old)

    original_count = len(DUMMY_TASKS)
    removed_count = 0

    # Simulate cleanup by counting what would be removed
    for task in DUMMY_TASKS:
        if task.get("status") == "done" and task.get("updated_at"):
            try:
                updated_date = datetime.fromisoformat(
                    task["updated_at"].replace("Z", "+00:00")
                )
                if updated_date < cutoff_date:
                    removed_count += 1
            except BaseException:
                pass

    remaining_count = original_count - removed_count

    result = {
        "original_task_count": original_count,
        "removed_count": removed_count,
        "remaining_count": remaining_count,
        "cutoff_days": days_old,
    }

    return json.dumps(result, indent=2)
