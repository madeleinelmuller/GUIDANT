# macOS Permissions for GUIDANT

To allow GUIDANT to take screenshots and simulate mouse clicks, you need to grant the necessary permissions in your macOS System Settings. Specifically, you must enable **Accessibility** and **Screen Recording** for the terminal application you are using to run the agent.

## Steps to Grant Permissions:

1.  **Open System Settings:**
    *   Click the Apple icon in the top-left corner of your screen and select **System Settings**.

2.  **Navigate to Privacy & Security:**
    *   In the System Settings window, scroll down and click on **Privacy & Security**.

3.  **Enable Accessibility:**
    *   Under the **Privacy** section, find and click on **Accessibility**.
    *   Click the **+** button to add a new application.
    *   You will need to add your terminal application. Common terminal applications are located in `/Applications/Utilities/`. Select your terminal application (e.g., `Terminal.app`, `iTerm.app`).
    *   Ensure the toggle switch next to your terminal application is turned on.

4.  **Enable Screen Recording:**
    *   Go back to the **Privacy & Security** settings.
    *   Under the **Privacy** section, find and click on **Screen Recording**.
    *   Click the **+** button and add your terminal application if it's not already listed.
    *   Ensure the toggle switch next to your terminal application is turned on.

After completing these steps, you may be prompted to restart your terminal application for the changes to take effect. Once you've granted these permissions, the GUIDANT agent will be able to take screenshots and control your mouse.
