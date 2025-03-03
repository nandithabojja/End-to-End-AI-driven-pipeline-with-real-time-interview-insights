# %%

from datetime import datetime

import pandas as pd
from database.vector_store import VectorStore
from timescale_vector.client import uuid_from_time
import csv

# Initialize VectorStore
vec = VectorStore()

# Read the CSV file
#df = pd.read_csv("../data/output(1).csv", sep=";")
# df = pd.read_csv("../data/output(1).csv", sep=";", encoding="latin1")
df = pd.read_csv(
    "../data/output.csv",
    sep=";",
    encoding="latin1",
    on_bad_lines="skip",  # Skip bad lines
    quoting=csv.QUOTE_MINIMAL,  # Handle quoted fields
)

df.head()


# Prepare data for insertion
def prepare_record(row):
    """Prepare a record for insertion into the vector store.

    This function creates a record with a UUID version 1 as the ID, which captures
    the current time or a specified time.

    Note:
        - By default, this function uses the current time for the UUID.
        - To use a specific time:
          1. Import the datetime module.
          2. Create a datetime object for your desired time.
          3. Use uuid_from_time(your_datetime) instead of uuid_from_time(datetime.now()).

        Example:
            from datetime import datetime
            specific_time = datetime(2023, 1, 1, 12, 0, 0)
            id = str(uuid_from_time(specific_time))

        This is useful when your content already has an associated datetime.
    """
    content = f"Role: {row['JD_NAME']}\nJob Discription: {row['JD']}\nResume: {row['RESUME']}\nTAG: {row['TAG']}\nInterview: {row['Q_AND_A']}"
    #JD NAME	JD	RESUME	TAG	Q AND A
    embedding = vec.get_embedding(content)
    return pd.Series(
        {
            "id": str(uuid_from_time(datetime.now())),
            "metadata": {
                "category": row["category"],
                "created_at": datetime.now().isoformat(),
            },
            "contents": content,
            "embedding": embedding,
        }
    )


records_df = df.apply(prepare_record, axis=1)

# Create tables and insert data
vec.create_tables()
vec.create_index()  # DiskAnnIndex
vec.upsert(records_df)

# %%