# MCP Server with Gradio Interface

This project provides an MCP (Model Context Protocol) server with a Gradio web interface for 14 functions.

## Overview

This MCP server exposes the following functions as tools that can be called by MCP clients:


### create_task

**Signature:** `create_task(title, description, priority)`

**Description:**
Create a new task in the system.

Args:
    title: The task title
    description: Detailed description of the task
    priority: Task priority (low, medium, high)
    
Returns:
    Success message with task ID

**Parameters:**
- `title` (str): Parameter description
- `description` (str): Parameter description
- `priority` (str): Parameter description

**Example Prompts:**
- 1.
- 2.
- 3.
- 4.
- 5.

---


### get_task

**Signature:** `get_task(task_id)`

**Description:**
Retrieve a specific task by ID.

Args:
    task_id: The unique identifier of the task
    
Returns:
    JSON representation of the task or error message

**Parameters:**
- `task_id` (int): Parameter description

**Example Prompts:**
- 1.
- 2.
- 3.
- 4.
- 5.

---


### list_tasks

**Signature:** `list_tasks(status)`

**Description:**
List all tasks, optionally filtered by status.

Args:
    status: Filter by status (all, todo, in_progress, done)
    
Returns:
    JSON list of tasks matching the criteria

**Parameters:**
- `status` (str): Parameter description

**Example Prompts:**
- 1.
- 2.
- 3.
- 4.
- ```json

---


### update_task_status

**Signature:** `update_task_status(task_id, status)`

**Description:**
Update the status of a specific task.

Args:
    task_id: The unique identifier of the task
    status: New status (todo, in_progress, done)
    
Returns:
    Success or error message

**Parameters:**
- `task_id` (int): Parameter description
- `status` (str): Parameter description

**Example Prompts:**
- 1) How can I change my project's current phase?
- 2) What should happen if I mark an internal review as 'done' next week?
- 3) Need help with updating our marketing campaign tasks based on recent feedback.
- 4) Can you assist me in finalizing some reports by setting their statuses correctly?
- **New prompt:** User wants assistance in changing completion state for multiple items at once so they could send it out collectively across various departments while ensuring tracking remains accurate.

---


### delete_task

**Signature:** `delete_task(task_id)`

**Description:**
Delete a task from the system.

Args:
    task_id: The unique identifier of the task to delete
    
Returns:
    Success or error message

**Parameters:**
- `task_id` (int): Parameter description

**Example Prompts:**
- 1.
- 2.
- 3.
- 4.
- 5.

---


### get_task_statistics

**Signature:** `get_task_statistics()`

**Description:**
Get comprehensive task statistics.

Returns:
    JSON with various task metrics and counts

**Parameters:**


**Example Prompts:**
- from asking for daily data, weekly summaries up until the last two weeks' performance stats.
- ```prompt
- Ask about my recent project progress or specific tasks completed over time?
- Provide historical insights on how much work I've done in past months?
- Need an overview of all outstanding projects along with their current status indicators?

---


### get_productivity_report

**Signature:** `get_productivity_report(days)`

**Description:**
Generate a productivity report for the specified time period.

Args:
    days: Number of days to analyze (default: 7)
    
Returns:
    JSON productivity report with insights and recommendations

**Parameters:**
- `days` (int): Parameter description

**Example Prompts:**
- 1.
- 2.
- 3.
- 4.
- Constraints:

---


### get_overdue_tasks

**Signature:** `get_overdue_tasks()`

**Description:**
Find tasks that have been in progress for more than 7 days.

Returns:
    JSON list of potentially overdue or stalled tasks

**Parameters:**


**Example Prompts:**
- 1) A task manager assistant who is very familiar with the tool's commands.
- 2) Someone learning how it works but not yet proficient at its advanced use cases (could require simpler phrasing).
- 3) Users unfamiliar with technical jargon, so they may phrase their request differently from those well-versed in technology terms.
- ```markdown table format? No - just plain text answers here```
- Here are five prompts:

---


### export_tasks_csv

**Signature:** `export_tasks_csv()`

**Description:**
Export all tasks in CSV format.

Returns:
    CSV-formatted string of all tasks

**Parameters:**


**Example Prompts:**
- some could be directed at exporting specific types of data, others just asking for the full list:
- 1.
- 2.
- 3.
- 4.

---


### search_tasks

**Signature:** `search_tasks(query)`

**Description:**
Search tasks by title or description using text matching.

Args:
    query: Search term to look for in task titles and descriptions
    
Returns:
    JSON list of tasks matching the search criteria

**Parameters:**
- `query` (str): Parameter description

**Example Prompts:**
- some could be simple keyword searches, while others may involve more complex queries like phrases with multiple keywords.
- Prompt should have proper use case context.
- 1. Looking for project management reports on client projects
- 2. I need help finding all software-related activities planned before March next year including testing phase specifics
- 3. Locate any documentation related to employee training sessions scheduled after July

---


### bulk_update_priority

**Signature:** `bulk_update_priority(task_ids, new_priority)`

**Description:**
Update priority for multiple tasks at once.

Args:
    task_ids: Comma-separated list of task IDs (e.g., "1,2,3")
    new_priority: New priority level (low, medium, high)
    
Returns:
    Summary of the bulk update operation

**Parameters:**
- `task_ids` (str): Parameter description
- `new_priority` (str): Parameter description

**Example Prompts:**
- e.g., they should include some repetition but also differ in context or specificity where needed.
- ```markdown
- ### Prompt Examples:
- **Example #1:**
- I have two tasks assigned with ID's '4' and '9'. I want to change their priorities from Medium to High immediately using your toolset.

---


### filter_tasks_by_date

**Signature:** `filter_tasks_by_date(date_filter, days)`

**Description:**
Filter tasks by creation or update date.

Args:
    date_filter: Filter type ('created_last', 'updated_last', 'created_before', 'updated_before')
    days: Number of days for the filter (default: 7)
    
Returns:
    JSON list of tasks matching the date criteria

**Parameters:**
- `date_filter` (str): Parameter description
- `days` (int): Parameter description

**Example Prompts:**
- they should cover various combinations of `date_filter` parameters with diverse task descriptions.
- Example prompt:
- Prompt 1: I need help filtering my overdue articles created last week from our publication pipeline before yesterday's deadline.
- ### Prompt Guidelines
- - Use clear instructions in sentence structure.

---


### count_tasks_by_criteria

**Signature:** `count_tasks_by_criteria(criteria, value)`

**Description:**
Count tasks matching specific criteria.

Args:
    criteria: What to count by ('status', 'priority', 'created_today', 'updated_today')
    value: Value to match (for status/priority) or ignored for date criteria
    
Returns:
    JSON with count information

**Parameters:**
- `criteria` (str): Parameter description
- `value` (str): Parameter description

**Example Prompts:**
- e.g., in-app queries from users working on an ongoing project management system; automated tests written using data-driven testing frameworks like pytest's yield_fixture pattern etc.
- ```markdown
- 1. As part of my daily review task list creation I need your help counting how many high priority issues are pending resolution as per the team guidelines. Can you provide me details?
- 2. Could you assist me by generating a report showing which all projects have their last updated activity falling within today’s timeframe? This will be helpful while assessing our recent progress updates at the end of each workday.
- 3. In order to better understand current resource allocation patterns across various departments we require understanding total number of outstanding 'not complete' critical category bugs created since yesterday afternoon until now specifically tagged under development phase only - is it possible?

---


### cleanup_completed_tasks

**Signature:** `cleanup_completed_tasks(days_old)`

**Description:**
Remove completed tasks older than specified days.

Args:
    days_old: Remove completed tasks older than this many days (default: 30)
    
Returns:
    Summary of cleanup operation

**Parameters:**
- `days_old` (int): Parameter description

**Example Prompts:**
- some could be about deleting old data, while others involve clearing out expired items or organizing archives.
- Example:
- * "How can I delete all the projects from last quarter?"
- **Prompt for 'cleanup_completed_tasks(90)'**
- 1.

---


## Installation

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Run the MCP server:
```bash
python server/mcp_server.py
```

3. Run the Gradio interface:
```bash
python server/gradio_interface.py
```

## Usage

### MCP Server

The MCP server can be used with any MCP client. The server exposes the following tools:

| Function | Description |
|----------|-------------|
| `create_task` | Create a new task in the system.

Args:
    title:... |
| `get_task` | Retrieve a specific task by ID.

Args:
    task_id... |
| `list_tasks` | List all tasks, optionally filtered by status.

Ar... |
| `update_task_status` | Update the status of a specific task.

Args:
    t... |
| `delete_task` | Delete a task from the system.

Args:
    task_id:... |
| `get_task_statistics` | Get comprehensive task statistics.

Returns:
    J... |
| `get_productivity_report` | Generate a productivity report for the specified t... |
| `get_overdue_tasks` | Find tasks that have been in progress for more tha... |
| `export_tasks_csv` | Export all tasks in CSV format.

Returns:
    CSV-... |
| `search_tasks` | Search tasks by title or description using text ma... |
| `bulk_update_priority` | Update priority for multiple tasks at once.

Args:... |
| `filter_tasks_by_date` | Filter tasks by creation or update date.

Args:
  ... |
| `count_tasks_by_criteria` | Count tasks matching specific criteria.

Args:
   ... |
| `cleanup_completed_tasks` | Remove completed tasks older than specified days.
... |


### Gradio Interface

The Gradio interface provides a web-based UI for testing the MCP functions:

- **Single Function**: If there's only one function, a simple interface is created
- **Multiple Functions**: If there are multiple functions, a tabbed interface is created

### Testing

Run the test client:
```bash
python client/test_client.py
```

Run unit tests:
```bash
pytest tests/
```

## Project Structure

```
output/
├── server/           # MCP server files
│   ├── mcp_server.py
│   ├── gradio_interface.py
│   └── __init__.py
├── client/           # Test client
│   ├── test_client.py
│   └── __init__.py
├── tests/            # Unit tests
│   ├── test_mcp_server.py
│   └── __init__.py
├── README.md         # This file
└── requirements.txt  # Python dependencies
```

## Configuration

The server can be configured using the following options:

- `--share`: Enable Gradio sharing
- `--model-endpoint`: Use an OpenAI-compatible model endpoint
- `--preserve-docstrings`: Keep original docstrings
- `--local-model`: Specify local Hugging Face model
- `--env-file`: Load environment variables from .env file

## Development

This project was generated using the Gradio MCP Server Builder tool.

## License

This generated project inherits the CC BY-NC 4.0 license from gradio-mcp-server-builder.

**You are free to:**
- Share — copy and redistribute the material in any medium or format
- Adapt — remix, transform, and build upon the material

**Under the following terms:**
- **Attribution** — You must give appropriate credit and indicate if changes were made
- **NonCommercial** — You may not use the material for commercial purposes

For more details, visit: https://creativecommons.org/licenses/by-nc/4.0/
