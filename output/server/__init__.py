"""
MCP Server with Gradio Interface

This package contains 14 MCP function(s) with a Gradio interface.
"""

from .gradio_server import create_task, get_task, list_tasks, update_task_status, delete_task, get_task_statistics, get_productivity_report, get_overdue_tasks, export_tasks_csv, search_tasks, bulk_update_priority, filter_tasks_by_date, count_tasks_by_criteria, cleanup_completed_tasks

__all__ = ["create_task", "get_task", "list_tasks", "update_task_status", "delete_task", "get_task_statistics", "get_productivity_report", "get_overdue_tasks", "export_tasks_csv", "search_tasks", "bulk_update_priority", "filter_tasks_by_date", "count_tasks_by_criteria", "cleanup_completed_tasks"]
