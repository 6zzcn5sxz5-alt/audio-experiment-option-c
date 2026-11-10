"""Execute this assignment notebook and embed outputs without a Jupyter server.

This small CPU-only runner captures printed text, audio players, and Matplotlib
plots into standard notebook output records. Using Jupyter 'Run All' gives the
same scientific calculations and saved results, and is the preferred UI route.
"""

from __future__ import annotations

import base64
import contextlib
import io
import json
import os
from pathlib import Path
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parent
NOTEBOOK_PATH = ROOT / "analysis.ipynb"


def execute() -> None:
    notebook = json.loads(NOTEBOOK_PATH.read_text(encoding="utf-8"))
    os.chdir(ROOT)
    scope = {"__name__": "__main__"}
    original_show = plt.show
    counter = 0

    for index, cell in enumerate(notebook["cells"]):
        if cell["cell_type"] != "code":
            continue

        counter += 1
        outputs: list[dict] = []
        outbuf, errbuf = io.StringIO(), io.StringIO()

        def flush_streams() -> None:
            for buf, name in ((outbuf, "stdout"), (errbuf, "stderr")):
                content = buf.getvalue()
                if content:
                    outputs.append({"output_type": "stream", "name": name, "text": content.splitlines(True)})
                    buf.seek(0)
                    buf.truncate(0)

        def capture_display(value) -> None:
            flush_streams()
            data = {"text/plain": repr(value)}
            repr_html = getattr(value, "_repr_html_", None)
            if callable(repr_html):
                html = repr_html()
                if html:
                    data["text/html"] = html
            outputs.append({"output_type": "display_data", "metadata": {}, "data": data})

        def capture_show(*_args, **_kwargs) -> None:
            flush_streams()
            for figure_id in plt.get_fignums():
                fig = plt.figure(figure_id)
                with io.BytesIO() as memory:
                    fig.savefig(memory, format="png", dpi=125, bbox_inches="tight")
                    image_b64 = base64.b64encode(memory.getvalue()).decode("ascii")
                outputs.append({
                    "output_type": "display_data",
                    "metadata": {},
                    "data": {"image/png": image_b64, "text/plain": "<Figure>"},
                })
                plt.close(fig)

        plt.show = capture_show
        try:
            with contextlib.redirect_stdout(outbuf), contextlib.redirect_stderr(errbuf):
                exec(compile("".join(cell["source"]), f"notebook cell {index}", "exec"), scope)
            flush_streams()
        except Exception as exception:
            flush_streams()
            outputs.append({
                "output_type": "error",
                "ename": type(exception).__name__,
                "evalue": str(exception),
                "traceback": [],
            })
            cell["outputs"] = outputs
            cell["execution_count"] = counter
            NOTEBOOK_PATH.write_text(json.dumps(notebook, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
            raise

        cell["outputs"] = outputs
        cell["execution_count"] = counter
        # First code cell imports IPython.display.display; use our capture for
        # subsequent cells. Keep the same actual Audio representation for replay.
        scope["display"] = capture_display

    plt.show = original_show
    notebook["metadata"]["language_info"]["version"] = ".".join(str(x) for x in sys.version_info[:3])
    NOTEBOOK_PATH.write_text(json.dumps(notebook, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Executed {counter} code cells with no errors: {NOTEBOOK_PATH}")
    for cell in notebook["cells"]:
        if cell["cell_type"] == "code":
            print(f"  cell {cell['execution_count']}: {len(cell['outputs'])} outputs")


if __name__ == "__main__":
    execute()
