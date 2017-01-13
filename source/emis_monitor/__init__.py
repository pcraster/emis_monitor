import datetime
import json
import sys
import traceback
from flask import Config
import pika
from .configuration import configuration
# from .check import filesystem


class Monitor(object):

    def __init__(self):
        self.config = Config(__name__)


    def logs_uri(self,
            route):
        route = route.lstrip("/")
        return "http://{}:{}/{}".format(
            self.config["EMIS_LOG_HOST"],
            self.config["EMIS_LOG_PORT"],
            route)


    def log(self,
            message,
            priority="low",
            severity="non_critical"):

        try:

            payload = {
                "timestamp": datetime.datetime.utcnow().isoformat(),
                "priority": priority,
                "severity": severity,
                "message": message
            }

            # Post message in rabbitmq and be done with it.
            credentials = pika.PlainCredentials(
                current_app.config["EMIS_RABBITMQ_DEFAULT_USER"],
                current_app.config["EMIS_RABBITMQ_DEFAULT_PASS"]
            )

            connection = pika.BlockingConnection(
                pika.ConnectionParameters(
                    host="rabbitmq",
                    virtual_host=current_app.config[
                        "EMIS_RABBITMQ_DEFAULT_VHOST"],
                    credentials=credentials)
            )
            channel = connection.channel()

            properties = pika.BasicProperties()
            properties.content_type = "application/json"
            properties.durable = False

            channel.basic_publish(
                exchange="alerts",
                properties=properties,
                routing_key="{}.{}".format(priority, severity),
                body=json.dumps(payload)
            )
            connection.close()

        except Exception as exception:

            sys.stderr.write("Error while sending log message to broker\n")
            sys.stderr.write("Log message: {}\n".format(message))
            sys.stderr.write("Error message: {}\n".format(str(exception)))
            sys.stderr.write("{}\n".format(traceback.format_exc()))
            sys.stderr.flush()


    def on_message(self,
            channel,
            method_frame,
            header_frame,
            body):
        sys.stdout.write("received message: {}\n".format(body))
        sys.stdout.flush()

        try:
            body = body.decode("utf-8")

            self.log(body)

            data = json.loads(body)

            # uri = self.properties_uri("properties")
            # pathnames = data["pathnames"]
            # rewrite = data["rewrite"].split(":") if "rewrite" in data else None
            # assert rewrite is None or len(rewrite) == 2, rewrite

            # scan(uri, pathnames, rewrite)
            # filesystem.scan()

        except Exception as exception:

            sys.stderr.write("{}\n".format(traceback.format_exc()))
            sys.stderr.flush()


        channel.basic_ack(delivery_tag=method_frame.delivery_tag)


    def run(self,
            host):

        self.credentials = pika.PlainCredentials(
            self.config["EMIS_RABBITMQ_DEFAULT_USER"],
            self.config["EMIS_RABBITMQ_DEFAULT_PASS"]
        )
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(
            host="rabbitmq",
            virtual_host=self.config["EMIS_RABBITMQ_DEFAULT_VHOST"],
            credentials=self.credentials,
            # Keep trying for 8 minutes.
            connection_attempts=100,
            retry_delay=5  # Seconds
        ))
        self.channel = self.connection.channel()
        self.channel.queue_declare(
            queue="monitor")
        self.channel.basic_consume(
            self.on_message,
            queue="monitor")

        try:
            sys.stdout.write("Start consuming...\n")
            sys.stdout.flush()
            self.channel.start_consuming()
        except KeyboardInterrupt:
            self.channel.stop_consuming()

        sys.stdout.write("Close connection...\n")
        sys.stdout.flush()
        self.connection.close()


def create_app(
        configuration_name):

    app = Monitor()

    configuration_ = configuration[configuration_name]
    app.config.from_object(configuration_)
    configuration_.init_app(app)

    return app
