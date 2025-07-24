import json
import requests
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, window, avg, stddev
from pyspark.sql.types import StructType, StructField, IntegerType, LongType, DoubleType

# Load Slack config
cfg = json.load(open('slack_config.json'))
webhook_url = cfg['webhook_url']

def alert_slack(message):
    requests.post(webhook_url, json={'text': message})

schema = StructType([
    StructField('sensor_id', IntegerType()),
    StructField('timestamp', LongType()),
    StructField('value', DoubleType()),
])

spark = SparkSession.builder.appName('AnomalyDetection').getOrCreate()

df = (spark.readStream
    .format('kafka')
    .option('kafka.bootstrap.servers', 'kafka:9092')
    .option('subscribe', 'sensor-data')
    .load()
)

parsed = df.select(from_json(col('value').cast('string'), schema).alias('data')).select('data.*')

stats = (parsed
    .withColumn('event_time', col('timestamp').cast('timestamp'))
    .groupBy(
        window(col('event_time'), '60 seconds', '30 seconds'),
        col('sensor_id')
    )
    .agg(
        avg('value').alias('mean_val'),
        stddev('value').alias('stddev_val')
    )
)

joined = parsed.join(stats,
    on=[
        parsed.sensor_id == stats.sensor_id,
        parsed.timestamp.cast('timestamp').between(stats.window.start, stats.window.end)
    ],
    how='inner'
).select(parsed.sensor_id, parsed.timestamp, parsed.value, stats.mean_val, stats.stddev_val)

anomalies = joined.filter(col('value') > col('mean_val') + 3 * col('stddev_val'))

def process_row(row):
    message = (f"Anomaly detected on sensor {row.sensor_id}: value={row.value:.2f} "
               f"(mean={row.mean_val:.2f}, stddev={row.stddev_val:.2f}) at {row.timestamp}")
    alert_slack(message)

query = (anomalies.writeStream
    .foreach(process_row)
    .outputMode('append')
    .start()
)

query.awaitTermination()
