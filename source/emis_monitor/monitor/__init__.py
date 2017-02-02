from datetime import datetime, timedelta
import os
import requests
import sys
import dateutil.parser
from starling import time_point


def route_uri(
        uri,
        route):
    return "{}/{}".format(uri, route.lstrip("/"))


def clear_expired_domain(
        domain_uri,
        domain):

    # Delete the dataset.
    pathname = domain["pathname"]

    if os.path.exists(pathname):
        os.remove(pathname)

    # Delete the resource.
    response = requests.delete(route_uri(domain_uri,
        domain["_links"]["self"]))

    if response.status_code != 200:
        sys.stderr.write("Could not delete domain : {}".format(response.text))


def clear_expired_aggregate_queries(
        aggregate_query_uri,
        domain_uri,
        now_time_point,
        expiration_period):

    # Delete aggregate queries older than the expiration period.
    response = requests.get(route_uri(aggregate_query_uri,
        "aggregate_queries"))

    if response.status_code != 200:
        sys.stderr.write("Could not get aggregate queries: {}"
            .format(response.text))

    queries = response.json()["aggregate_queries"]

    for query in queries:
        patched_at = query["patched_at"]
        patched_at_time_point = dateutil.parser.parse(patched_at)
        expiration_time_point = patched_at_time_point + expiration_period

        if expiration_time_point < now_time_point:

            # Delete all related data also.
            # - Uploaded domain
            # - Result dataset

            if "aggregate_query" in query["model"]:

                model = query["model"]["aggregate_query"]

                if "domain" in model:
                    response = requests.get(route_uri(domain_uri, model["domain"]))

                    if response.status_code != 200:
                        raise RuntimeError("Could not retrieve domain")

                    domain = response.json()["domain"]

                    clear_expired_domain(domain_uri, domain)

            if query["execute_status"] == "succeeded":

                query_id = query["id"]

                # TODO Don't make up the link. This should be provided by
                #      the query itself. If the query is executed successfuly,
                #      provide a link to the result.
                response = requests.get(route_uri(aggregate_query_uri,
                    "aggregate_query_results/{}".format(query_id)))


                if response.status_code != 200:
                    sys.stderr.write(
                        "Could not get aggregate query result: {}"
                            .format(response.text))

                # TODO Make it possible to determine the pathname of the
                #      dataset. We need it to delete the dataset. This is
                #      of no interest to public clients.



            # Delete the resource.
            response = requests.delete(route_uri(aggregate_query_uri,
                query["_links"]["self"]))

            if response.status_code != 200:
                sys.stderr.write("Could not delete aggregate query: {}"
                    .format(response.text))


def clear_expired_domains(
        domain_uri,
        now_time_point,
        expiration_period):

    # Delete domains older than the expiration period.
    # Delete both the domain resources and the associated dataset.
    response = requests.get(route_uri(domain_uri, "domains"))

    if response.status_code != 200:
        sys.stderr.write("Could not get domains : {}".format(response.text))

    domains = response.json()["domains"]

    for domain in domains:
        posted_at = domain["posted_at"]
        posted_at_time_point = dateutil.parser.parse(posted_at)
        expiration_time_point = posted_at_time_point + expiration_period

        if expiration_time_point < now_time_point:

            clear_expired_domain(domain_uri, domain)


def clear_expired_resource(
        aggregate_query_uri,
        domain_uri,
        expiration_period):
    """
    :param float expiration_period: Experation period in seconds, after
        which unused resources can be cleared
    """

    # Stuff to remove:
    # - domain dataset and resource
    #     - emis
    #         - Remove dataset in /upload folder
    #     - emis_domain
    #         - Remove resource (or mark resource as removed)
    # - aggregate query resource
    #     - emis_aggregate_query
    #         - Remove resource (or mark resource as removed)
    # - aggregate query result dataset and resource
    #     - emis
    #         - Remove dataset in /result folder
    #     - emis_domain
    #         - Remove resource (or mark resource as removed)


    # Time points are all in UTC time. No need to convert them to
    # local time.
    now_time_point = time_point.utc_now()
    expiration_period = timedelta(hours=expiration_period)


    clear_expired_aggregate_queries(aggregate_query_uri, domain_uri,
        now_time_point, expiration_period)
    clear_expired_domains(domain_uri, now_time_point, expiration_period)
