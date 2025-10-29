import sys
import json
import subprocess
import os
import base64

class GuidantError(Exception):
    """Custom exception for Guidant errors."""
    def __init__(self, message, details=None):
        super().__init__(message)
        self.details = details

def take_screenshot():
    """Takes a screenshot and returns the path and base64 encoded image."""
    screenshot_path = os.path.join(os.getcwd(), 'screenshot.png')
    try:
        result = subprocess.run(
            ['xcrun', 'swift', 'main.swift', 'screenshot', screenshot_path],
            capture_output=True,
            text=True,
            check=True
        )
        
        # Read and encode the screenshot
        with open(screenshot_path, 'rb') as f:
            image_data = base64.b64encode(f.read()).decode('utf-8')
        
        return {
            'message': 'Screenshot taken successfully',
            'path': screenshot_path,
            'image_base64': image_data
        }
    except FileNotFoundError:
        raise GuidantError("The 'xcrun' command is not available in this environment.")
    except subprocess.CalledProcessError as e:
        raise GuidantError('Failed to take screenshot', details=e.stderr)
    except Exception as e:
        raise GuidantError('Failed to read screenshot', details=str(e))

def perform_click(x, y):
    """Performs a click at the given coordinates."""
    if x is None or y is None:
        raise GuidantError('x and y coordinates are required')
    try:
        result = subprocess.run(
            ['xcrun', 'swift', 'main.swift', 'click', str(x), str(y)],
            capture_output=True,
            text=True,
            check=True
        )
        return {'message': f'Clicked at ({x}, {y})'}
    except FileNotFoundError:
        raise GuidantError("The 'xcrun' command is not available in this environment.")
    except subprocess.CalledProcessError as e:
        raise GuidantError('Failed to perform click', details=e.stderr)

def handle_initialize(params):
    """Handle MCP initialize request."""
    return {
        'protocolVersion': '2024-11-05',
        'capabilities': {
            'tools': {}
        },
        'serverInfo': {
            'name': 'guidant',
            'version': '1.0.0'
        }
    }

def handle_tools_list():
    """Return the list of available tools."""
    return {
        'tools': [
            {
                'name': 'take_screenshot',
                'description': 'Takes a screenshot of the main display and returns it as base64 encoded PNG',
                'inputSchema': {
                    'type': 'object',
                    'properties': {},
                    'required': []
                }
            },
            {
                'name': 'click',
                'description': 'Simulates a left mouse click at the specified screen coordinates',
                'inputSchema': {
                    'type': 'object',
                    'properties': {
                        'x': {
                            'type': 'number',
                            'description': 'X coordinate for the click'
                        },
                        'y': {
                            'type': 'number',
                            'description': 'Y coordinate for the click'
                        }
                    },
                    'required': ['x', 'y']
                }
            }
        ]
    }

def handle_tools_call(name, arguments):
    """Handle tool execution."""
    if name == 'take_screenshot':
        return take_screenshot()
    elif name == 'click':
        x = arguments.get('x')
        y = arguments.get('y')
        return perform_click(x, y)
    else:
        raise GuidantError(f'Unknown tool: {name}')

def main():
    """Main loop to read from stdin, process requests, and write to stdout."""
    for line in sys.stdin:
        request_id = None
        try:
            request = json.loads(line)
            request_id = request.get('id')
            method = request.get('method')
            params = request.get('params', {})

            # Handle MCP protocol methods
            if method == 'initialize':
                result = handle_initialize(params)
            elif method == 'initialized':
                # Just acknowledge, no response needed for notifications
                continue
            elif method == 'tools/list':
                result = handle_tools_list()
            elif method == 'tools/call':
                tool_name = params.get('name')
                tool_arguments = params.get('arguments', {})
                result = {
                    'content': [
                        {
                            'type': 'text',
                            'text': json.dumps(handle_tools_call(tool_name, tool_arguments))
                        }
                    ]
                }
            # Legacy methods for backward compatibility
            elif method == 'screenshot':
                result = take_screenshot()
            elif method == 'click':
                x = params.get('x')
                y = params.get('y')
                result = perform_click(x, y)
            else:
                raise GuidantError(f'Unknown method: {method}')

            response = {
                'jsonrpc': '2.0',
                'id': request_id,
                'result': result
            }

        except json.JSONDecodeError:
            response = {
                'jsonrpc': '2.0',
                'id': None,
                'error': {'code': -32700, 'message': 'Parse error'}
            }
        except GuidantError as e:
            error_obj = {'code': -32000, 'message': str(e)}
            if e.details:
                error_obj['data'] = e.details
            response = {
                'jsonrpc': '2.0',
                'id': request_id,
                'error': error_obj
            }
        except Exception as e:
            response = {
                'jsonrpc': '2.0',
                'id': request_id,
                'error': {'code': -32603, 'message': f'Internal error: {e}'}
            }

        sys.stdout.write(json.dumps(response) + '\n')
        sys.stdout.flush()

if __name__ == '__main__':
    main()
