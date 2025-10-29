import sys
import json
import subprocess
import os

class GuidantError(Exception):
    """Custom exception for Guidant errors."""
    def __init__(self, message, details=None):
        super().__init__(message)
        self.details = details

def take_screenshot():
    """Takes a screenshot and returns the path."""
    screenshot_path = os.path.join(os.getcwd(), 'screenshot.png')
    try:
        result = subprocess.run(
            ['xcrun', 'swift', 'main.swift', 'screenshot', screenshot_path],
            capture_output=True,
            text=True,
            check=True  # Raise an exception if the command fails
        )
        return {'message': 'Screenshot taken successfully', 'path': screenshot_path}
    except FileNotFoundError:
        raise GuidantError("The 'xcrun' command is not available in this environment.")
    except subprocess.CalledProcessError as e:
        raise GuidantError('Failed to take screenshot', details=e.stderr)

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

def main():
    """Main loop to read from stdin, process requests, and write to stdout."""
    for line in sys.stdin:
        request_id = None
        try:
            request = json.loads(line)
            request_id = request.get('id')
            method = request.get('method')
            params = request.get('params', {})

            if method == 'screenshot':
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
