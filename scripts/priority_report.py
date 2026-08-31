"""CLI: lê severidade por categoria de uma frota (JSON) e mostra o TOP N
veículos que precisam de manutenção primeiro.

Exemplo:
    python scripts/priority_report.py --input sample_data/frota_severidade.json --top 5
"""

import argparse
import json
import sys
from pathlib import Path

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from priority_score import rank_fleet


def build_arg_parser():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, help="JSON: veiculo -> {categoria: severidade 0-1}")
    parser.add_argument("--top", type=int, default=5)
    return parser


def run(args):
    with open(args.input, encoding="utf-8") as f:
        fleet_severities = json.load(f)

    ranking = rank_fleet(fleet_severities, top_n=args.top)

    print(f"TOP {args.top} — veículos que precisam de atenção agora:\n")
    for position, vehicle_score in enumerate(ranking, start=1):
        print(f"{position}. {vehicle_score.vehicle} — score {vehicle_score.score:.1f} "
              f"(pior categoria: {vehicle_score.worst_category})")
    return 0


if __name__ == "__main__":
    sys.exit(run(build_arg_parser().parse_args()))
