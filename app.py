from flask import Flask, render_template
import psutil
import platform
import socket
import time

app = Flask(__name__)


@app.route("/")
def dashboard():
    uptime_seconds = time.time() - psutil.boot_time()

    days = int(uptime_seconds // 86400)
    hours = int((uptime_seconds % 86400) // 3600)
    minutes = int((uptime_seconds % 3600) // 60)

    cpu_usage = psutil.cpu_percent(interval=1)
    memory_usage = psutil.virtual_memory().percent
    disk_usage = psutil.disk_usage("/").percent

    if max(cpu_usage, memory_usage, disk_usage) >= 90:
        health_status = "Critical"

    elif max(cpu_usage, memory_usage, disk_usage) >= 70:
        health_status = "Warning"

    else:
        health_status = "Healthy"

    system_info = {
    "hostname": socket.gethostname(),
    "os": platform.system(),
    "release": platform.release(),
    "cpu": cpu_usage,
    "memory": memory_usage,
    "disk": disk_usage,
    "health": health_status,
    "uptime": f"{days}d {hours}h {minutes}m",
    "load": psutil.getloadavg(),
}

    return render_template("index.html", system=system_info)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
