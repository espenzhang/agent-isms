from __future__ import annotations

import argparse

from .benchmarks import get_benchmark_adapters
from .config import load_config
from .report import build_report
from .utils import ensure_dir


def _resolve_targets(value: str | None, all_ids: list[str]) -> list[str]:
    if not value:
        return all_ids
    wanted = [item.strip() for item in value.split(",") if item.strip()]
    return [item for item in all_ids if item in wanted]


def cmd_sample(args: argparse.Namespace) -> int:
    app = load_config(args.config)
    ensure_dir(app.paths.cache_dir)
    ensure_dir(app.paths.samples_dir)
    adapters = get_benchmark_adapters()
    benchmark_ids = _resolve_targets(args.benchmark, list(app.benchmarks))
    for benchmark_id in benchmark_ids:
        benchmark = app.benchmarks[benchmark_id]
        if not benchmark.enabled:
            continue
        adapters[benchmark_id].sample(app, benchmark)
    return 0


def cmd_run(args: argparse.Namespace) -> int:
    app = load_config(args.config)
    ensure_dir(app.paths.runs_dir)
    adapters = get_benchmark_adapters()
    benchmark_ids = _resolve_targets(args.benchmark, list(app.benchmarks))
    variant_ids = _resolve_targets(args.variant, [variant.id for variant in app.variants])
    for benchmark_id in benchmark_ids:
        benchmark = app.benchmarks[benchmark_id]
        if not benchmark.enabled:
            continue
        sample_path = app.paths.samples_dir / f"{benchmark_id}.jsonl"
        if not sample_path.exists():
            adapters[benchmark_id].sample(app, benchmark)
        for variant in app.variants:
            if variant.id not in variant_ids:
                continue
            adapters[benchmark_id].run_variant(app, benchmark, variant, sample_path)
    return 0


def cmd_report(args: argparse.Namespace) -> int:
    app = load_config(args.config)
    build_report(app)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="skill-bench")
    subparsers = parser.add_subparsers(dest="command", required=True)

    sample_parser = subparsers.add_parser("sample")
    sample_parser.add_argument("--config", required=True)
    sample_parser.add_argument("--benchmark")
    sample_parser.set_defaults(func=cmd_sample)

    run_parser = subparsers.add_parser("run")
    run_parser.add_argument("--config", required=True)
    run_parser.add_argument("--benchmark")
    run_parser.add_argument("--variant")
    run_parser.set_defaults(func=cmd_run)

    report_parser = subparsers.add_parser("report")
    report_parser.add_argument("--config", required=True)
    report_parser.set_defaults(func=cmd_report)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
