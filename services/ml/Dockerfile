FROM tensorflow/serving:2.16.1

COPY models/ /models/
COPY models/models.config /models/models.config

ENV MODEL_NAME=cassava

CMD ["--model_config_file=/models/models.config", \
     "--model_config_file_poll_wait_seconds=60"]
