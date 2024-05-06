"""This script contains the basic logic of the bot."""
import json
from datetime import datetime, timedelta

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.command_cursor import CommandCursor

app: FastAPI = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
)
GROUP_TYPE_FORMATS: dict = {
    "month": "%Y-%m-01T00:00:00",
    "day":   "%Y-%m-%dT00:00:00",
    "hour":  "%Y-%m-%dT%H:00:00",
}


@app.get("/aggregate_payments/{dt_from}/{dt_upto}/{group_type}")
async def aggregate_payments(dt_from, dt_upto, group_type):
    """The function returns the amounts of salaries for a given period.

        The function accepts the date and time of the start and end of aggregation
        in ISO format, as well as the type of aggregation.
        And returns a list of amounts and date labels."""

    collection: Collection = MongoClient("mongo_db", 27017)["task"]["salary"]

    dt_from, dt_upto = datetime.fromisoformat(dt_from), datetime.fromisoformat(dt_upto)
    dt_format: str = GROUP_TYPE_FORMATS.get(group_type)

    aggregated_results: CommandCursor = collection.aggregate([
        {"$match": {"dt": {"$gte": dt_from, "$lte": dt_upto}}},
        {"$group": {
            "_id": {"$dateToString": {"format": dt_format, "date": "$dt"}},
            "total": {"$sum": "$value"},
        }},
        {"$sort": {"_id": 1}},
    ])

    if group_type == "hour":
        all_dates = [dt_from + timedelta(hours=x) for x in range(int((dt_upto-dt_from).total_seconds() // 3600 + 1))]
    else:
        all_dates = [dt_from + timedelta(days=x) for x in range((dt_upto-dt_from).days + 1)]

    salary_dict = {date.strftime(dt_format): 0 for date in all_dates}

    for result in aggregated_results:
        salary_dict[result["_id"]] = result["total"]

    dataset = list(salary_dict.values())
    labels = list(salary_dict.keys())

    result_dict = {"dataset": dataset, "labels": labels}
    return result_dict
