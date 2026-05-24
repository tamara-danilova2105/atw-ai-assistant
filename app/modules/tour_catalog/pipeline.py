from datetime import UTC, datetime

MS_IN_DAY = 86400000

EXCHANGE_RATES = [
    {
        "currency": "₽",
        "rate": 0.0113,
    },
    {
        "currency": "€",
        "rate": 1.08,
    },
    {
        "currency": "$",
        "rate": 1,
    },
]


def build_tours_pipeline(
    filters: dict,
    sort: dict,
    page: int,
    limit: int | None,
):
    now = datetime.now(UTC)

    pipeline = [
        {
            "$match": {
                "isPublished": True,
            }
        },
        {
            "$lookup": {
                "from": "tourdates",
                "localField": "_id",
                "foreignField": "tourId",
                "as": "dates",
            }
        },
        {
            "$addFields": {
                "dates": {
                    "$ifNull": ["$dates", []],
                }
            }
        },
        {
            "$unwind": {
                "path": "$dates",
                "preserveNullAndEmptyArrays": False,
            }
        },
        {
            "$match": {
                "dates.date_start": {
                    "$gte": now,
                },
                "dates.status": {
                    "$ne": "canceled",
                },
            }
        },
    ]

    apply_date_range_filter(
        pipeline=pipeline,
        filters=filters,
    )

    apply_duration_filter(
        pipeline=pipeline,
        filters=filters,
    )

    apply_price_fields(pipeline)

    apply_price_filter(
        pipeline=pipeline,
        filters=filters,
    )

    pipeline.extend(
        [
            {
                "$sort": {
                    "dates.date_start": 1,
                }
            },
            {
                "$group": {
                    "_id": "$_id",
                    "tour": {
                        "$first": "$tour",
                    },
                    "slug": {
                        "$first": "$slug",
                    },
                    "cover": {
                        "$first": "$cover",
                    },
                    "discount": {
                        "$first": "$discount",
                    },
                    "regions": {
                        "$first": "$regions",
                    },
                    "createdAt": {
                        "$first": "$createdAt",
                    },
                    "isPublished": {
                        "$first": "$isPublished",
                    },
                    "dates": {
                        "$push": "$dates",
                    },
                    "minDatePriceUsd": {
                        "$min": "$datePriceUsd",
                    },
                    "maxDateDiscount": {
                        "$max": {
                            "$cond": [
                                {
                                    "$gt": [
                                        {
                                            "$ifNull": [
                                                "$dates.price.discount",
                                                0,
                                            ]
                                        },
                                        0,
                                    ]
                                },
                                "$dates.price.discount",
                                0,
                            ]
                        }
                    },
                }
            },
            {
                "$addFields": {
                    "validEarlyDiscount": {
                        "$cond": [
                            {
                                "$and": [
                                    {
                                        "$eq": [
                                            "$discount.enabled",
                                            True,
                                        ]
                                    },
                                    {
                                        "$gt": [
                                            "$discount.endDate",
                                            now,
                                        ]
                                    },
                                    {
                                        "$gt": [
                                            {
                                                "$ifNull": [
                                                    "$discount.percentage",
                                                    0,
                                                ]
                                            },
                                            0,
                                        ]
                                    },
                                ]
                            },
                            "$discount.percentage",
                            0,
                        ]
                    }
                }
            },
            {
                "$addFields": {
                    "hasEarlyDiscount": {
                        "$gt": [
                            "$validEarlyDiscount",
                            0,
                        ]
                    },
                    "hasDateDiscount": {
                        "$gt": [
                            "$maxDateDiscount",
                            0,
                        ]
                    },
                }
            },
        ]
    )

    apply_discount_filter(
        pipeline=pipeline,
        filters=filters,
    )

    pipeline.append(
        {
            "$addFields": {
                "maxDiscount": {
                    "$max": [
                        "$maxDateDiscount",
                        "$validEarlyDiscount",
                    ]
                }
            }
        }
    )

    pipeline.append(build_sort_stage(sort))

    pipeline.append(
        {
            "$project": {
                "_id": 1,
                "tour": 1,
                "slug": 1,
                "dates": 1,
                "cover": 1,
                "discount": 1,
                "regions": 1,
                "isPublished": 1,
            }
        }
    )

    if limit:
        skip = (page - 1) * limit

        pipeline.append(
            {
                "$facet": {
                    "tours": [
                        {
                            "$skip": skip,
                        },
                        {
                            "$limit": limit,
                        },
                    ],
                    "total": [
                        {
                            "$count": "count",
                        }
                    ],
                }
            }
        )

    return pipeline


def apply_date_range_filter(
    pipeline: list[dict],
    filters: dict,
):
    dates_filter = filters.get("dates") or {}

    start_date = dates_filter.get("startDate")
    end_date = dates_filter.get("endDate")

    if not start_date and not end_date:
        return

    conditions = []

    if end_date:
        conditions.append(
            {
                "$lte": [
                    "$dates.date_start",
                    parse_date(end_date),
                ]
            }
        )

    if start_date:
        conditions.append(
            {
                "$gte": [
                    "$dates.date_finish",
                    parse_date(start_date),
                ]
            }
        )

    pipeline.append(
        {
            "$match": {
                "$expr": {
                    "$and": conditions,
                }
            }
        }
    )


def apply_duration_filter(
    pipeline: list[dict],
    filters: dict,
):
    duration = filters.get("duration")

    if not isinstance(duration, list):
        return

    min_days = duration[0] if len(duration) > 0 else 0
    max_days = duration[1] if len(duration) > 1 else None

    duration_days_expr = {
        "$add": [
            {
                "$divide": [
                    {
                        "$subtract": [
                            "$dates.date_finish",
                            "$dates.date_start",
                        ]
                    },
                    MS_IN_DAY,
                ]
            },
            1,
        ]
    }

    conditions = [
        {
            "$gte": [
                duration_days_expr,
                int(min_days),
            ]
        }
    ]

    if max_days:
        conditions.append(
            {
                "$lte": [
                    duration_days_expr,
                    int(max_days),
                ]
            }
        )

    pipeline.append(
        {
            "$match": {
                "$expr": {
                    "$and": conditions,
                }
            }
        }
    )


def apply_price_fields(
    pipeline: list[dict],
):
    pipeline.append(
        {
            "$addFields": {
                "datePriceUsd": {
                    "$let": {
                        "vars": {
                            "amount": "$dates.price.amount",
                            "currency": "$dates.price.currency",
                        },
                        "in": {
                            "$multiply": [
                                "$$amount",
                                {
                                    "$switch": {
                                        "branches": [
                                            {
                                                "case": {
                                                    "$eq": [
                                                        "$$currency",
                                                        {
                                                            "$literal": rate["currency"],
                                                        },
                                                    ]
                                                },
                                                "then": rate["rate"],
                                            }
                                            for rate in EXCHANGE_RATES
                                        ],
                                        "default": 1,
                                    }
                                },
                            ]
                        },
                    }
                }
            }
        }
    )


def apply_price_filter(
    pipeline: list[dict],
    filters: dict,
):
    price = filters.get("price")

    if not isinstance(price, list):
        return

    min_rub = price[0] if len(price) > 0 else 0
    max_rub = price[1] if len(price) > 1 else None

    min_usd = rub_to_usd(min_rub or 0)
    max_usd = rub_to_usd(max_rub) if max_rub else None

    conditions = [
        {
            "$gte": [
                "$datePriceUsd",
                min_usd,
            ]
        }
    ]

    if max_usd:
        conditions.append(
            {
                "$lte": [
                    "$datePriceUsd",
                    max_usd,
                ]
            }
        )

    pipeline.append(
        {
            "$match": {
                "$expr": {
                    "$and": conditions,
                }
            }
        }
    )


def apply_discount_filter(
    pipeline: list[dict],
    filters: dict,
):
    discount = filters.get("discount") or {}

    early_discount_enabled = bool(discount.get("enabled"))

    date_discount_enabled = bool(discount.get("discount"))

    if early_discount_enabled and date_discount_enabled:
        pipeline.append(
            {
                "$match": {
                    "$or": [
                        {
                            "hasEarlyDiscount": True,
                        },
                        {
                            "hasDateDiscount": True,
                        },
                    ]
                }
            }
        )
        return

    if early_discount_enabled:
        pipeline.append(
            {
                "$match": {
                    "hasEarlyDiscount": True,
                }
            }
        )
        return

    if date_discount_enabled:
        pipeline.append(
            {
                "$match": {
                    "hasDateDiscount": True,
                }
            }
        )


def build_sort_stage(
    sort: dict,
):
    sort_option = sort.get("option") if sort else None

    if sort_option == "soon":
        return {
            "$sort": {
                "dates.0.date_start": 1,
            }
        }

    if sort_option == "cheaper":
        return {
            "$sort": {
                "minDatePriceUsd": 1,
            }
        }

    if sort_option == "expensively":
        return {
            "$sort": {
                "minDatePriceUsd": -1,
            }
        }

    if sort_option == "discount":
        return {
            "$sort": {
                "maxDiscount": -1,
                "minDatePriceUsd": 1,
                "dates.0.date_start": 1,
            }
        }

    return {
        "$sort": {
            "createdAt": -1,
        }
    }


def parse_date(
    value: str,
):
    if value.endswith("Z"):
        value = value.replace("Z", "+00:00")

    return datetime.fromisoformat(value)


def rub_to_usd(rub):
    return float(rub) * 0.0113
