"""Guard the coaching docs: each timeline/comms markdown exists, has an H1 and bullets."""
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
EXPECTED = [
    "timelines/Competitions.md",
    "timelines/Health_PT.md",
    "timelines/Training.md",
    "comms/Pipelines.md",
]


def test_docs_present_and_shaped():
    for rel in EXPECTED:
        p = ROOT / rel
        assert p.is_file(), rel
        lines = [l for l in p.read_text().splitlines() if l.strip()]
        assert lines and lines[0].startswith("# "), f"{rel}: missing H1"
        assert any(l.lstrip().startswith("- ") for l in lines), f"{rel}: no bullet items"


if __name__ == "__main__":
    test_docs_present_and_shaped()
    print("ok")
