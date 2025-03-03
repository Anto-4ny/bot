import os from "os";
import { execSync } from "child_process";

try {
    if (os.platform() === "linux") {
        console.log("🔧 Running postinstall for Linux...");
        execSync(
            "apt-get update && apt-get install -y wget curl unzip chromium-driver python3 python3-pip && wget -q -O /tmp/chrome.deb https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && dpkg -i /tmp/chrome.deb || apt-get -fy install && rm /tmp/chrome.deb && pip3 install -r requirements.txt",
            { stdio: "inherit" }
        );
    } else if (os.platform() === "win32") {
        console.log("🔧 Running postinstall for Windows...");
        execSync("pip install -r requirements.txt", { stdio: "inherit" });
    } else {
        console.log("⚠️ OS not detected, skipping postinstall.");
    }
} catch (error) {
    console.error("❌ Postinstall script failed:", error);
    process.exit(1);
}
