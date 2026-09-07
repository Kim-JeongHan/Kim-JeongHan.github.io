"""KL divergence demo. Python owns the controls, calculations, and figure data."""

import numpy as np


CONTROLS = [
    {"name": "mu_q", "label": "μ_Q", "min": -3.5, "max": 3.5, "step": 0.05, "value": 0.0},
]

X = np.linspace(-6.0, 6.0, 601)
LOG_P = -0.5 * X**2 - 0.5 * np.log(2.0 * np.pi)
P = np.exp(LOG_P)


def compute(parameters: dict) -> dict:
    """Compare P = N(0, 1) and Q = N(mu_q, 1) with numerical integration."""
    mean_q = float(parameters["mu_q"])
    log_q = -0.5 * (X - mean_q) ** 2 - 0.5 * np.log(2.0 * np.pi)
    q = np.exp(log_q)
    # Subtract log densities directly to avoid bias from an epsilon in the ratio.
    contribution = P * (LOG_P - log_q)
    divergence = float(np.trapezoid(contribution, X))

    traces = [
        {
            "x": X.tolist(), "y": P.tolist(), "type": "scatter", "mode": "lines",
            "name": "P(x)", "line": {"color": "#2563eb", "width": 3},
            "hovertemplate": "x=%{x:.2f}<br>P(x)=%{y:.4f}<extra></extra>",
        },
        {
            "x": X.tolist(), "y": q.tolist(), "type": "scatter", "mode": "lines",
            "name": "Q(x)", "line": {"color": "#dc2626", "width": 3},
            "fill": "tozeroy", "fillcolor": "rgba(220, 38, 38, 0.12)",
            "hovertemplate": "x=%{x:.2f}<br>Q(x)=%{y:.4f}<extra></extra>",
        },
        {
            "x": X.tolist(), "y": contribution.tolist(), "type": "scatter", "mode": "lines",
            "name": "p(x) log(p(x) / q(x))", "line": {"color": "#0f766e", "width": 2.5},
            "fill": "tozeroy", "fillcolor": "rgba(15, 118, 110, 0.16)",
            "xaxis": "x2", "yaxis": "y2", "showlegend": False,
            "hovertemplate": "x=%{x:.2f}<br>contribution=%{y:.4f}<extra></extra>",
        },
    ]
    # Stack the two plots so the same figure fits narrow blog columns and phones.
    layout = {
        "xaxis": {"domain": [0, 1], "anchor": "y", "range": [-5, 5]},
        "yaxis": {
            "domain": [0.59, 1], "anchor": "x", "range": [0, 0.45],
            "title": {"text": "Probability density"},
        },
        "xaxis2": {"domain": [0, 1], "anchor": "y2", "range": [-5, 5], "title": {"text": "x"}},
        "yaxis2": {
            "domain": [0, 0.38], "anchor": "x2",
            "title": {"text": "KL contribution"},
            "range": [min(-0.1, float(contribution.min()) * 1.2), max(0.2, float(contribution.max()) * 1.2)],
        },
        "margin": {"l": 60, "r": 15, "t": 45, "b": 40},
        "legend": {"orientation": "h", "y": 1.13, "x": 0.5, "xanchor": "center"},
        "hovermode": "x unified",
        "uirevision": "kl-divergence",
        "annotations": [
            {
                "text": "p(x) log(p(x) / q(x))", "xref": "paper", "yref": "paper",
                "x": 0.5, "y": 0.46, "showarrow": False,
            },
        ],
    }
    return {
        "status": f"μ_Q = {mean_q:.2f}, D_KL(P || Q) ≈ {divergence:.3f}",
        "figure": {"data": traces, "layout": layout},
    }
