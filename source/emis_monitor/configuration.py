import os
import tempfile


class Configuration:

    EMIS_RABBITMQ_DEFAULT_USER = os.environ.get("EMIS_RABBITMQ_DEFAULT_USER")
    EMIS_RABBITMQ_DEFAULT_PASS = os.environ.get("EMIS_RABBITMQ_DEFAULT_PASS")
    EMIS_RABBITMQ_DEFAULT_VHOST = os.environ.get("EMIS_RABBITMQ_DEFAULT_VHOST")
    # EMIS_PROPERTY_DATA = os.environ.get("EMIS_PROPERTY_DATA") or \
    #     tempfile.gettempdir()

    EMIS_AGGREGATE_QUERY_HOST = "emis_aggregate_query"
    EMIS_DOMAIN_HOST = "emis_domain"
    EMIS_LOG_HOST = "log"


    @staticmethod
    def init_app(
            app):
        pass


class DevelopmentConfiguration(Configuration):

    EMIS_AGGREGATE_QUERY_PORT = 5000
    EMIS_DOMAIN_PORT = 5000
    EMIS_LOG_PORT = 5000


class TestingConfiguration(Configuration):

    EMIS_AGGREGATE_QUERY_PORT = 5000
    EMIS_DOMAIN_PORT = 5000
    EMIS_LOG_PORT = 5000


class ProductionConfiguration(Configuration):

    EMIS_AGGREGATE_QUERY_PORT = 3031
    EMIS_DOMAIN_PORT = 3031
    EMIS_LOG_PORT = 3031


configuration = {
    "development": DevelopmentConfiguration,
    "testing": TestingConfiguration,
    "production": ProductionConfiguration
}
