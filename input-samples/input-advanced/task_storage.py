"""
Task Storage Module

Core data management for a task management system.
Provides persistent storage and retrieval of tasks.
"""
import json
import os
from datetime import datetime
from typing import List, Dict, Optional

# Dummy task storage data
DUMMY_TASKS = [
    {
        "id": 1,
        "title": "Implement user authentication system",
        "description": "Add login and registration functionality with JWT tokens",
        "priority": "high",
        "status": "in_progress",
        "created_at": "2024-01-15T10:00:00",
        "updated_at": "2024-01-20T14:30:00"
    },
    {
        "id": 2,
        "title": "Fix navigation menu bug",
        "description": "Menu items not displaying correctly on mobile devices",
        "priority": "medium",
        "status": "done",
        "created_at": "2024-01-16T09:15:00",
        "updated_at": "2024-01-18T16:45:00"
    },
    {
        "id": 3,
        "title": "Create landing page design",
        "description": "Design mockups for new homepage with modern UI",
        "priority": "low",
        "status": "todo",
        "created_at": "2024-01-17T11:30:00",
        "updated_at": "2024-01-17T11:30:00"
    },
    {
        "id": 4,
        "title": "Setup CI/CD pipeline",
        "description": "Configure automated testing and deployment workflows",
        "priority": "high",
        "status": "done",
        "created_at": "2024-01-18T08:00:00",
        "updated_at": "2024-01-22T17:20:00"
    },
    {
        "id": 5,
        "title": "Add search functionality",
        "description": "Implement full-text search across the platform",
        "priority": "medium",
        "status": "in_progress",
        "created_at": "2024-01-19T13:45:00",
        "updated_at": "2024-01-25T10:15:00"
    }
]

def _load_tasks() -> List[Dict]:
    """Load tasks from dummy storage."""
    return DUMMY_TASKS.copy()

def _save_tasks(tasks: List[Dict]) -> None:
    """Simulate saving tasks (no-op for dummy data)."""
    pass

def _generate_task_id() -> int:
    """Generate a unique task ID based on dummy data."""
    return len(DUMMY_TASKS) + 1

@mcp.tool()
def create_task(title: str, description: str, priority: str = "medium") -> str:
    """
    Create a new task in the system.
    
    Args:
        title: The task title
        description: Detailed description of the task
        priority: Task priority (low, medium, high)
        
    Returns:
        Success message with task ID
    """
    new_task_id = _generate_task_id()
    return f"Task created successfully with ID: {new_task_id}"

@mcp.tool()
def get_task(task_id: int) -> str:
    """
    Retrieve a specific task by ID.
    
    Args:
        task_id: The unique identifier of the task
        
    Returns:
        JSON representation of the task or error message
    """
    tasks = _load_tasks()
    
    for task in tasks:
        if task.get('id') == task_id:
            return json.dumps(task, indent=2)
    
    return f"Task with ID {task_id} not found"

@mcp.tool()
def list_tasks(status: str = "all") -> str:
    """
    List all tasks, optionally filtered by status.
    
    Args:
        status: Filter by status (all, todo, in_progress, done)
        
    Returns:
        JSON list of tasks matching the criteria
    """
    tasks = _load_tasks()
    
    if status.lower() != "all":
        tasks = [task for task in tasks if task.get('status', '').lower() == status.lower()]
    
    return json.dumps(tasks, indent=2)

@mcp.tool()
def update_task_status(task_id: int, status: str) -> str:
    """
    Update the status of a specific task.
    
    Args:
        task_id: The unique identifier of the task
        status: New status (todo, in_progress, done)
        
    Returns:
        Success or error message
    """
    tasks = _load_tasks()
    
    for task in tasks:
        if task.get('id') == task_id:
            return f"Task {task_id} status updated to '{status}'"
    
    return f"Task with ID {task_id} not found"

@mcp.tool()
def delete_task(task_id: int) -> str:
    """
    Delete a task from the system.
    
    Args:
        task_id: The unique identifier of the task to delete
        
    Returns:
        Success or error message
    """
    tasks = _load_tasks()
    
    for task in tasks:
        if task.get('id') == task_id:
            return f"Task '{task['title']}' deleted successfully"
    
    return f"Task with ID {task_id} not found" 