import json
import time
from pathlib import Path
from urllib.request import urlopen


PAGES = [
    ("homepage", "http://127.0.0.1:8000/"),
    ("club_list", "http://127.0.0.1:8000/clubs/"),
]


def fetch(url):
    started = time.perf_counter()
    with urlopen(url) as response:
        body = response.read()
        elapsed_ms = round((time.perf_counter() - started) * 1000, 2)
        return {
            "url": url,
            "status": response.status,
            "content_type": response.headers.get("Content-Type", ""),
            "bytes": len(body),
            "elapsed_ms": elapsed_ms,
        }


def main():
    results = []
    for label, url in PAGES:
        entry = fetch(url)
        entry["label"] = label
        results.append(entry)

    output = {
        "tool": "Local HTTP size/latency audit script",
        "generated_at": time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime()),
        "results": results,
    }
    target = Path("performance_audit.json")
    target.write_text(json.dumps(output, indent=2), encoding="utf-8")
    print(target.resolve())


if __name__ == "__main__":
    main()

