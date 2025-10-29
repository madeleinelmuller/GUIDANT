import AppKit
import Foundation

// Function to take a screenshot
func takeScreenshot(savePath: String) {
    if let image = CGDisplayCreateImage(CGMainDisplayID()) {
        let bitmapRep = NSBitmapImageRep(cgImage: image)
        if let data = bitmapRep.representation(using: .png, properties: [:]) {
            do {
                try data.write(to: URL(fileURLWithPath: savePath))
                print("Screenshot saved to \(savePath)")
            } catch {
                print("Error saving screenshot: \(error)")
            }
        }
    }
}

// Function to simulate a mouse click
func click(x: Double, y: Double) {
    let point = CGPoint(x: x, y: y)
    if let clickEvent = CGEvent(mouseEventSource: nil, mouseType: .leftMouseDown, mouseCursorPosition: point, mouseButton: .left) {
        clickEvent.post(tap: .cghidEventTap)
        if let releaseEvent = CGEvent(mouseEventSource: nil, mouseType: .leftMouseUp, mouseCursorPosition: point, mouseButton: .left) {
            releaseEvent.post(tap: .cghidEventTap)
            print("Clicked at (\(x), \(y))")
        }
    }
}

// Main execution
let arguments = CommandLine.arguments
if arguments.count > 1 {
    let command = arguments[1]
    switch command {
    case "screenshot":
        if arguments.count > 2 {
            takeScreenshot(savePath: arguments[2])
        } else {
            print("Usage: ./main screenshot <save_path>")
        }
    case "click":
        if arguments.count > 3 {
            if let x = Double(arguments[2]), let y = Double(arguments[3]) {
                click(x: x, y: y)
            } else {
                print("Invalid coordinates")
            }
        } else {
            print("Usage: ./main click <x> <y>")
        }
    default:
        print("Unknown command: \(command)")
    }
} else {
    print("Usage: ./main <command> [options]")
}
