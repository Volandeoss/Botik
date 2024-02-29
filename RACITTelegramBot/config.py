from environs import Env

env = Env()

env.read_env()


SERVICE_ACC_INFO = {
    "type": "service_account",
    "project_id": env.str("project_id"),
    "private_key_id": env.str("private_key_id"),
    "private_key": env.str("private_key"),
    "client_email": env.str("client_email"),
    "client_id": env.str("client_id"),
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": env.str("auth_provider_x509_cert_url"),
    "client_x509_cert_url": env.str("client_x509_cert_url"),
    "universe_domain": "googleapis.com",
}
