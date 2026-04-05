from __future__ import annotations

from pathlib import Path
import csv
import json

from .config import AppConfig
from .utils import ensure_dir, write_json


def _load_rows(app: AppConfig) -> list[dict]:
    rows: list[dict] = []
    if not app.paths.runs_dir.exists():
        return rows
    for benchmark_dir in sorted(app.paths.runs_dir.iterdir()):
        if not benchmark_dir.is_dir():
            continue
        for variant_dir in sorted(benchmark_dir.iterdir()):
            summary_path = variant_dir / "summary.json"
            if summary_path.exists():
                rows.append(json.loads(summary_path.read_text()))
    return rows


def _decorate_rows(rows: list[dict]) -> list[dict]:
    baseline_map: dict[str, dict] = {}
    for row in rows:
        row["pass_rate"] = (row["passed"] / row["total"]) if row["total"] else None
        if row["variant_id"] == "baseline":
            baseline_map[row["benchmark_id"]] = row
    for row in rows:
        baseline = baseline_map.get(row["benchmark_id"])
        if baseline and row["pass_rate"] is not None and baseline["pass_rate"] is not None:
            row["baseline_delta"] = row["pass_rate"] - baseline["pass_rate"]
        else:
            row["baseline_delta"] = None
    return rows


def _build_leaderboards(rows: list[dict]) -> dict:
    leaderboards: dict[str, list[dict]] = {}
    by_benchmark: dict[str, list[dict]] = {}
    for row in rows:
        by_benchmark.setdefault(row["benchmark_id"], []).append(row)
    for benchmark_id, items in by_benchmark.items():
        leaderboards[benchmark_id] = sorted(
            items,
            key=lambda item: (
                item["pass_rate"] is None,
                -(item["pass_rate"] or -1),
                -(item["baseline_delta"] or -999),
                item["variant_id"],
            ),
        )
    return leaderboards


def _write_csv(path: Path, rows: list[dict]) -> None:
    ensure_dir(path.parent)
    fields = [
        "benchmark_id",
        "variant_id",
        "total",
        "passed",
        "failed",
        "skipped",
        "pass_rate",
        "baseline_delta",
    ]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field) for field in fields})


def _markdown_summary(rows: list[dict], leaderboards: dict[str, list[dict]]) -> str:
    lines = ["# Skill Benchmark Summary", ""]
    for benchmark_id, items in sorted(leaderboards.items()):
        lines.append(f"## {benchmark_id}")
        lines.append("")
        lines.append("| Rank | Variant | Pass Rate | Delta vs Baseline | Passed | Failed | Skipped |")
        lines.append("| --- | --- | ---: | ---: | ---: | ---: | ---: |")
        for index, row in enumerate(items, start=1):
            pass_rate = "-" if row["pass_rate"] is None else f"{row['pass_rate'] * 100:.1f}%"
            delta = "-" if row["baseline_delta"] is None else f"{row['baseline_delta'] * 100:+.1f} pts"
            lines.append(
                f"| {index} | {row['variant_id']} | {pass_rate} | {delta} | "
                f"{row['passed']} | {row['failed']} | {row['skipped']} |"
            )
        lines.append("")
    lines.append("## Raw Runs")
    lines.append("")
    lines.append("| Benchmark | Variant | Total | Passed | Failed | Skipped |")
    lines.append("| --- | --- | ---: | ---: | ---: | ---: |")
    for row in sorted(rows, key=lambda item: (item["benchmark_id"], item["variant_id"])):
        lines.append(
            f"| {row['benchmark_id']} | {row['variant_id']} | {row['total']} | "
            f"{row['passed']} | {row['failed']} | {row['skipped']} |"
        )
    return "\n".join(lines) + "\n"


def _dashboard_html(rows: list[dict], leaderboards: dict[str, list[dict]]) -> str:
    payload = {
        "rows": rows,
        "leaderboards": leaderboards,
    }
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Skill Benchmark Dashboard</title>
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
  <style>
    :root {{
      --bg: #f5f1e8;
      --card: #fffaf2;
      --ink: #1b1a17;
      --muted: #756b5f;
      --accent: #c5612f;
      --accent-2: #1e6f5c;
      --border: #d9ccb6;
    }}
    body {{
      margin: 0;
      font-family: Georgia, "Iowan Old Style", serif;
      color: var(--ink);
      background:
        radial-gradient(circle at top left, rgba(197,97,47,.18), transparent 30%),
        radial-gradient(circle at top right, rgba(30,111,92,.18), transparent 28%),
        var(--bg);
    }}
    .wrap {{
      max-width: 1200px;
      margin: 0 auto;
      padding: 32px 20px 64px;
    }}
    h1, h2 {{
      margin: 0 0 12px;
      letter-spacing: .02em;
    }}
    .lede {{
      color: var(--muted);
      margin-bottom: 24px;
    }}
    .grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
      gap: 18px;
    }}
    .card {{
      background: var(--card);
      border: 1px solid var(--border);
      border-radius: 18px;
      padding: 18px;
      box-shadow: 0 10px 30px rgba(27,26,23,.06);
    }}
    table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 14px;
    }}
    th, td {{
      border-bottom: 1px solid var(--border);
      padding: 8px 6px;
      text-align: left;
    }}
    th {{
      color: var(--muted);
      font-weight: 600;
    }}
    .delta-pos {{ color: var(--accent-2); font-weight: 700; }}
    .delta-neg {{ color: #a23b2b; font-weight: 700; }}
    .meta {{
      display: flex;
      gap: 12px;
      flex-wrap: wrap;
      margin-bottom: 18px;
      color: var(--muted);
      font-size: 14px;
    }}
    canvas {{
      width: 100% !important;
      height: 320px !important;
    }}
  </style>
</head>
<body>
  <div class="wrap">
    <h1>Skill Benchmark Dashboard</h1>
    <p class="lede">Leaderboard, pass rate, and delta-vs-baseline views across all completed benchmark runs.</p>
    <div class="meta">
      <div>Total runs: {len(rows)}</div>
      <div>Benchmarks: {len(leaderboards)}</div>
    </div>
    <div class="grid">
      <div class="card">
        <h2>Pass Rate</h2>
        <canvas id="passRateChart"></canvas>
      </div>
      <div class="card">
        <h2>Delta vs Baseline</h2>
        <canvas id="deltaChart"></canvas>
      </div>
    </div>
    {"".join(_dashboard_tables(leaderboards))}
  </div>
  <script>
    const payload = {json.dumps(payload, ensure_ascii=False)};
    const rows = payload.rows.filter(row => row.pass_rate !== null);
    const labels = rows.map(row => `${{row.benchmark_id}} / ${{row.variant_id}}`);
    const passRates = rows.map(row => +(row.pass_rate * 100).toFixed(2));
    const deltas = rows.map(row => row.baseline_delta === null ? null : +(row.baseline_delta * 100).toFixed(2));
    new Chart(document.getElementById('passRateChart'), {{
      type: 'bar',
      data: {{
        labels,
        datasets: [{{
          label: 'Pass rate (%)',
          data: passRates,
          backgroundColor: '#c5612f',
          borderRadius: 8,
        }}]
      }},
      options: {{
        responsive: true,
        plugins: {{ legend: {{ display: false }} }},
        scales: {{
          x: {{ ticks: {{ maxRotation: 75, minRotation: 45 }} }},
          y: {{ beginAtZero: true, max: 100 }}
        }}
      }}
    }});
    new Chart(document.getElementById('deltaChart'), {{
      type: 'bar',
      data: {{
        labels,
        datasets: [{{
          label: 'Delta vs baseline (points)',
          data: deltas,
          backgroundColor: deltas.map(v => v === null ? '#d9ccb6' : (v >= 0 ? '#1e6f5c' : '#a23b2b')),
          borderRadius: 8,
        }}]
      }},
      options: {{
        responsive: true,
        plugins: {{ legend: {{ display: false }} }},
        scales: {{
          x: {{ ticks: {{ maxRotation: 75, minRotation: 45 }} }},
          y: {{ beginAtZero: true }}
        }}
      }}
    }});
  </script>
</body>
</html>
"""


def _dashboard_tables(leaderboards: dict[str, list[dict]]) -> list[str]:
    sections: list[str] = []
    for benchmark_id, items in sorted(leaderboards.items()):
        rows = []
        for row in items:
            pass_rate = "-" if row["pass_rate"] is None else f"{row['pass_rate'] * 100:.1f}%"
            if row["baseline_delta"] is None:
                delta = "-"
                cls = ""
            else:
                cls = "delta-pos" if row["baseline_delta"] >= 0 else "delta-neg"
                delta = f"{row['baseline_delta'] * 100:+.1f} pts"
            rows.append(
                f"<tr><td>{row['variant_id']}</td><td>{pass_rate}</td>"
                f"<td class=\"{cls}\">{delta}</td><td>{row['passed']}</td>"
                f"<td>{row['failed']}</td><td>{row['skipped']}</td></tr>"
            )
        sections.append(
            f"""
    <div class="card" style="margin-top: 18px;">
      <h2>{benchmark_id}</h2>
      <table>
        <thead>
          <tr><th>Variant</th><th>Pass Rate</th><th>Delta vs Baseline</th><th>Passed</th><th>Failed</th><th>Skipped</th></tr>
        </thead>
        <tbody>
          {''.join(rows)}
        </tbody>
      </table>
    </div>
            """
        )
    return sections


def build_report(app: AppConfig) -> dict:
    rows = _decorate_rows(_load_rows(app))
    leaderboards = _build_leaderboards(rows)
    summary = {
        "benchmarks": {
            benchmark_id: {row["variant_id"]: row for row in items}
            for benchmark_id, items in leaderboards.items()
        },
        "totals": {
            "benchmark_count": len(leaderboards),
            "run_count": len(rows),
        },
    }
    ensure_dir(app.paths.reports_dir)
    write_json(app.paths.reports_dir / "summary.json", summary)
    _write_csv(app.paths.reports_dir / "leaderboard.csv", rows)
    (app.paths.reports_dir / "summary.md").write_text(
        _markdown_summary(rows, leaderboards),
        encoding="utf-8",
    )
    (app.paths.reports_dir / "dashboard.html").write_text(
        _dashboard_html(rows, leaderboards),
        encoding="utf-8",
    )
    return summary
