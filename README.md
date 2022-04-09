# Capstone Design1 - Video Summarizer Worker

## Stack

-   fetching message queue of Redis
-   key-value db(aws dynamodb)
-   YOLO v3, YOLO tiny v3

## To start

need .env file

- dynamodb_url
- redis_host
- redis_port
- redis_key
- detector_model : Literal["yolov3", "tinyYolov3"]
