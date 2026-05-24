from bson import ObjectId


def serialize_mongo_document(value):
    if isinstance(value, ObjectId):
        return str(value)

    if isinstance(value, list):
        return [serialize_mongo_document(item) for item in value]

    if isinstance(value, dict):
        return {key: serialize_mongo_document(item) for key, item in value.items()}

    return value


def map_tours_response(response: dict):
    return serialize_mongo_document(response)


def map_schedule_item(
    tour: dict,
    tour_date: dict,
):
    return serialize_mongo_document(
        {
            "tourId": tour["_id"],
            "slug": tour["slug"],
            "tour": tour.get("tour", ""),
            "dateStart": tour_date["date_start"],
            "dateEnd": tour_date["date_finish"],
            "spots": tour_date.get("spots"),
            "regions": tour.get("regions", []),
        }
    )


def map_tour_detail(
    tour: dict,
    dates: list[dict],
):
    return serialize_mongo_document(
        {
            **tour,
            "dates": dates,
        }
    )
