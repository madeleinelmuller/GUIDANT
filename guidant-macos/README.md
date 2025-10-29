# GUIDANT (Graphical User Interface Agent Navigation Tool)

GUIDANT is a macOS application that allows an AI agent to take screenshots and simulate mouse clicks on your machine. It consists of a Swift script for the core functionalities and a Python Flask server to expose these actions through API endpoints.

## Prerequisites

Before you begin, ensure you have the following installed:
- **Xcode Command Line Tools:** Provides the Swift compiler and other necessary tools. You can install it by running `xcode-select --install` in your terminal.
- **Python 3:** Required to run the Flask server.

## Setup Instructions

1.  **Install Dependencies:**
    -   Navigate to the `guidant-macos` directory and install the required Python packages:
        ```bash
        pip install -r requirements.txt
        ```

2.  **Grant macOS Permissions:**
    -   Follow the instructions in the `PERMISSIONS.md` file to grant the necessary permissions for screen recording and accessibility. This is a crucial step for the application to function correctly.

## Running the Server

1.  **Start the Server:**
    -   From the `guidant-macos` directory, run the following command to start the Flask server:
        ```bash
        python3 server.py
        ```
    -   The server will start on `http://127.0.0.1:5001`.

## API Endpoints

### Take a Screenshot

-   **Endpoint:** `/screenshot`
-   **Method:** `POST`
-   **Description:** Takes a screenshot of the main display and saves it as `screenshot.png` in the `guidant-macos` directory.
-   **Example:**
    ```bash
    curl -X POST http://127.0.0.1:5001/screenshot
    ```

### Simulate a Mouse Click

-   **Endpoint:** `/click`
-   **Method:** `POST`
-   **Description:** Simulates a left mouse click at the specified coordinates.
-   **Body (JSON):**
    ```json
    {
        "x": 100,
        "y": 200
    }
    ```
-   **Example:**
    ```bash
    curl -X POST -H "Content-Type: application/json" -d '{"x": 100, "y": 200}' http://127.0.0.1:5001/click
    ```
