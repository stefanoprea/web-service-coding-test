import itertools


kpis = [
    {
        "id": 1,
        "name": "Runway",
        "description": "Runway is the number of months that a startup has until money runs out.",
        "parent_id": None
    },
    {
        "id": 2,
        "name": "Revenue",
        "description": "Revenue is the total monthly sales.",
        "parent_id": None
    },
    {
        "id": 3,
        "name": "Portfolio Runway",
        "description": "The runways for the seed investment portfolio",
        "parent_id": 1
    },
    {
        "id": 4,
        "name": "Portfolio Revenue",
        "description": "The total revenue for all portfolio companies",
        "parent_id": 2
    },
    {
        "id": 5,
        "name": "Company 1 Runway",
        "description": "This is the Company 1 Runway",
        "parent_id": 3
    },
    {
        "id": 6,
        "name": "Company 2 Runway",
        "description": "This is the Company 2 Runway",
        "parent_id": 3
    },
    {
        "id": 7,
        "name": "Company 3 Runway",
        "description": "This is the Company 3 Runway",
        "parent_id": 3
    },
    {
        "id": 8,
        "name": "Company 1 Revenue",
        "description": "This is the Company 1 Revenue",
        "parent_id": 4
    },
    {
        "id": 9,
        "name": "Company 2 Revenue",
        "description": "This is the Company 2 Revenue",
        "parent_id": 4
    },
    {
        "id": 10,
        "name": "Company 3 Revenue",
        "description": "This is the Company 3 Revenue",
        "parent_id": 4
    },
]


def make_values(*, start_id, start_month, kpi_id, value_format, values):
    return [
        {
            "id": start_id + i,
            "date": "2021-{:0>2d}-01".format(start_month + i),
            "value": value_format.format(values[i]),
            "kpi_id": kpi_id
        }
        for i in range(len(values))
    ]

company_1_runway_values = make_values(
    start_id=1,
    start_month=1,
    kpi_id=5,
    value_format="{} months",
    values=[12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
    )

company_2_runway_values = make_values(
    start_id=13,
    start_month=6,
    kpi_id=6,
    value_format="{} months",
    values=[24, 23, 22, 21, 20]
    )

company_3_runway_values = make_values(
    start_id=18,
    start_month=6,
    kpi_id=7,
    value_format="{} months",
    values=[12, 11, 10, 9, 8]
    )

portfolio_revenue = make_values(
    start_id=23,
    start_month=1,
    kpi_id=4,
    value_format="{:,} EUR",
    values=[12000, 10000, 9000, 12300, 12000]
    )

company_1_revenue = make_values(
    start_id=28,
    start_month=1,
    kpi_id=8,
    value_format="{:,} EUR",
    values=[6000, 4000, 3000, 6100, 9000]
    )

company_2_revenue = make_values(
    start_id=33,
    start_month=1,
    kpi_id=9,
    value_format="{:,} EUR",
    values=[3000, 4000, 3000, 4000, 2000]
    )

company_3_revenue = make_values(
    start_id=38,
    start_month=1,
    kpi_id=10,
    value_format="{:,} EUR",
    values=[3000, 2000, 3000, 2000, 1000]
    )

values = list(itertools.chain(
    company_1_runway_values,
    company_2_runway_values,
    company_3_runway_values,
    portfolio_revenue,
    company_1_revenue,
    company_2_revenue,
    company_3_revenue,
    ))
