# Input Samples for Gradio MCP Server Builder

This directory contains sample input files to demonstrate different use cases of
the Gradio MCP Server Builder CLI tool.

## 📁 Sample Categories

### 🟢 Basic Example (`input-basic/`)

**Single file, single function** - Perfect for getting started

- **File**: `hello_world.py`
- **Functions**: 1 MCP tool function
- **Complexity**: Beginner
- **Use case**: Simple greeting service

```bash
# Test basic example
python main.py input-samples/input-basic/hello_world.py --preserve-docstrings

# Test basic example without test prompts (faster)
python main.py input-samples/input-basic/hello_world.py --preserve-docstrings --no-test-prompts
```

**Generated Interface**: Simple `gr.Interface` with one text input for the name
parameter.

### 🟡 Simple Example (`input-simple/`)

**Two files, four functions** - Demonstrates multi-file and tabbed interface

- **Files**:
  - `math_operations.py` (2 MCP functions)
  - `geometry.py` (2 MCP functions)
- **Functions**: 4 MCP tool functions total
- **Complexity**: Intermediate
- **Use case**: Math calculation services

```bash
# Test simple example
python main.py input-samples/input-simple/*.py --share --device mps
```

**Generated Interface**: `gr.TabbedInterface` with 4 tabs, each containing
different math operations.

### 🔴 Advanced Example (`input-advanced/`)

**Three files, comprehensive app** - Shows real-world application structure

- **Files**:
  - `task_storage.py` (5 MCP functions + 3 helper functions)
  - `task_analytics.py` (5 MCP functions + 2 helper functions)
  - `task_utilities.py` (6 MCP functions + 2 helper functions)
- **Functions**: 16 MCP tool functions + 7 non-tool helper functions
- **Complexity**: Advanced
- **Use case**: Complete task management system

```bash
# Test advanced example
python main.py input-samples/input-advanced/*.py --model-config config/examples/creative_model.json --log-config config/examples/debug_logging.json --log-file log/builds/task_build.log
```

**Generated Interface**: `gr.TabbedInterface` with 16 tabs covering complete
task management workflow.

## 🛠️ Function Breakdown

### Basic Example Functions

1. **`greet(name: str)`** - Simple greeting generator

### Simple Example Functions

1. **`add_numbers(a: float, b: float)`** - Addition operation
1. **`multiply_numbers(a: float, b: float)`** - Multiplication operation
1. **`circle_area(radius: float)`** - Circle area calculation
1. **`rectangle_area(width: float, height: float)`** - Rectangle area
   calculation

### Advanced Example Functions

#### Task Storage (`task_storage.py`)

1. **`create_task(title, description, priority)`** - Create new tasks
1. **`get_task(task_id)`** - Retrieve specific task
1. **`list_tasks(status)`** - List filtered tasks
1. **`update_task_status(task_id, status)`** - Update task status
1. **`delete_task(task_id)`** - Remove tasks

#### Task Analytics (`task_analytics.py`)

6. **`get_task_statistics()`** - Comprehensive task metrics
1. **`get_productivity_report(days)`** - Productivity analysis
1. **`get_overdue_tasks()`** - Find stalled tasks
1. **`export_tasks_csv()`** - Export to CSV format

#### Task Utilities (`task_utilities.py`)

10. **`search_tasks(query)`** - Text-based task search
1. ate_priority(task_ids, priority)\`\*\* - Batch priority updates
1. asks_by_date(date_filter, days)\`\*\* - Date-based filtering
1. ks_by_criteria(criteria, value)\`\*\* - Counting operations
1. ompleted_tasks(days_old)\`\*\* - Data cleanup

## 🎯 Testing Different Scenarios

### Single Function Interface

```bash
# Generates gr.Interface
python main.py input-samples/input-basic/hello_world.py
```

### Multi-Function Tabbed Interface

```bash
# Generates gr.TabbedInterface with gr.Blocks
python main.py input-samples/input-simple/*.py
python main.py input-samples/input-advanced/*.py
```

### With Custom Configuration

```bash
# Use OpenAI-compatible endpoint
python main.py input-samples/input-advanced/*.py --model-endpoint http://localhost:11434/v1 --preserve-docstrings

# Custom output directory
python main.py input-samples/input-simple/*.py --output-dir custom_math_server --share

# Full customization
python main.py input-samples/input-advanced/*.py \
  --device cuda \
  --model-config config/examples/precise_model.json \
  --log-config config/examples/production_logging.json \
  --log-file log/builds/$(date +%Y%m%d)_build.log \
  --output-dir production_task_server \
  --share
```

## 📊 Expected Outputs

Each sample will generate:

```
output/
├── server/
│   ├── gradio_server.py     # Main Gradio interface
│   └── __init__.py          # Package initialization
├── client/
│   └── mcp_client.py       # MCP client with examples
├── README.md                # Documentation
└── requirements.txt         # Dependencies
```

## 🚀 Quick Start

1. **Try the basic example first:**

   ```bash
   python main.py input-samples/input-basic/hello_world.py --preserve-docstrings
   ```

1. **Test the generated server:**

   ```bash
   cd output && python server/gradio_server.py
   ```

1. **Test the MCP client:**

   ```bash
   cd output && python client/mcp_client.py
   ```

1. **Scale up to more complex examples:**

   ```bash
   python main.py input-samples/input-advanced/*.py --share
   ```

## 💡 Tips

- Use `--preserve-docstrings` to keep original documentation while testing
- Try `--share` to make the Gradio interface publicly accessible
- Use `--no-test-prompts` to disable test prompt generation for faster builds
- Use different `--device` options (cpu, mps, cuda) based on your hardware
- Experiment with custom model and logging configurations from the
  `config/examples/` folder
- Check the generated log files to understand the build process
