import boto3

from temporalio.client import Client, TLSConfig


def load_temporal_certificates():
    sm = boto3.client("secretsmanager")

    client_cert = sm.get_secret_value(
        SecretId="temporal-client-cert"
    )["SecretBinary"]

    client_key = sm.get_secret_value(
        SecretId="temporal-client-key"
    )["SecretBinary"]

    ca_cert = sm.get_secret_value(
        SecretId="temporal-ca-cert"
    )["SecretBinary"]

    return client_cert, client_key, ca_cert


async def get_temporal_client() -> Client:
    client_cert, client_key, ca_cert = load_temporal_certificates()

    return await Client.connect(
        "leads-data-load-prod.eroir.tmprl.cloud:7233",
        namespace="leads-data-load-prod.eroir",
        tls=TLSConfig(
            client_cert=client_cert,
            client_private_key=client_key,
        ),
    )