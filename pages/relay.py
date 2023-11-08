from client import init_client
import dash
from dash import html, dcc, Input, Output, State, callback
import dash_bootstrap_components as dbc
from db import sql_engine, write_tables
from query import query_relay


dash.register_page(__name__, name="Query Relays")


client = init_client()


def layout():
    return dbc.Container(
        [
            dbc.Row(
                dbc.Col(
                    html.P(
                        "Query relays for more events. Events will be stored in local postgres and neo4j databases",
                        className="text-start",
                    ),
                    width={"size": 10, "offset": 2},
                ),
                className="mb-2",  # Adjust margin as needed
            ),
            dbc.Row(
                [
                    dbc.Col(html.Label("Enter npub:"), width=2),
                    dbc.Col(
                        dbc.Input(
                            id="input-npub", type="text", placeholder="Enter npub"
                        ),
                        width=10,
                    ),
                ],
                className="mb-3",
            ),
            dbc.Row(
                [
                    dbc.Col(html.Label("Enter Kind:"), width=2),
                    dbc.Col(
                        dbc.Input(
                            id="input-kind", type="text", placeholder="Enter Kind"
                        ),
                        width=10,
                    ),
                ],
                className="mb-3",
            ),
            dbc.Row(
                [
                    dbc.Col(html.Label("Enter Number of Days:"), width=2),
                    dbc.Col(
                        dbc.Input(
                            id="input-num-days",
                            type="number",
                            placeholder="Enter Number of Days",
                        ),
                        width=10,
                    ),
                ],
                className="mb-3",
            ),
            dbc.Row(
                [
                    dbc.Col(html.Label("Enter Number Limit:"), width=2),
                    dbc.Col(
                        dbc.Input(
                            id="input-num-limit",
                            type="number",
                            placeholder="Enter Number Limit",
                        ),
                        width=10,
                    ),
                ],
                className="mb-3",
            ),
            dbc.Row(
                [
                    dbc.Col(html.Label("Enter Timeout in Seconds:"), width=2),
                    dbc.Col(
                        dbc.Input(
                            id="input-timeout-secs",
                            type="number",
                            value=30,
                            placeholder="Enter Timeout in Seconds",
                        ),
                        width=10,
                    ),
                ],
                className="mb-3",
            ),
            dbc.Row(
                [
                    dbc.Col(width=2),
                    dbc.Col(
                        html.Button("Submit", id="submit-npub-button", n_clicks=0),
                        width=10,
                    ),
                ],
                className="mb-3",
            ),
            dcc.Loading(
                id="loading-1",
                type="default",
                children=html.Div(id="query-output"),
            ),
        ],
        fluid=True,
        style={"padding": "20px"},
    )


@callback(
    Output("query-output", "children"),
    Input("submit-npub-button", "n_clicks"),
    [
        State("input-npub", "value"),
        State("input-kind", "value"),
        State("input-num-days", "value"),
        State("input-num-limit", "value"),
        State("input-timeout-secs", "value"),
    ],
    prevent_initial_call=True,
)
def update_output(n_clicks, npub, kind, num_days, num_limit, timeout_secs):
    if kind is not None:
        kind = int(kind)
    df = query_relay(
        client=client,
        npub=npub,
        kind=kind,
        num_days=num_days,
        num_limit=num_limit,
        timeout_secs=timeout_secs,
    )
    write_tables(df, sql_engine)
    output_data = f"downloaded {len(df)} events, loaded into postgres and neo4j"
    return [
        output_data,
        html.Br(),
        html.A("Open Neo4j Browser", href="http://localhost:7474/", target="_blank"),
    ]
