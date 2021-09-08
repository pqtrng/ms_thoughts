import jwt
from parse import parse
from datetime import datetime, timedelta
import logging
logger = logging.getLogger(__name__)


def encode_token(payload, private_key):
    return jwt.encode(payload, private_key, algorithm='RS256')


def decode_token(token, public_key):
    return jwt.decode(token, public_key, algorithms='RS256')


def generate_token_header(username, private_key):
    """Generate a token header base on the username. Sign using the private key

    Args:
        username (string): username
        private_key (string): private key to use
    """
    payload = {
        'username': username,
        'iat': datetime.utcnow(),
        'exp': datetime.utcnow() - timedelta(days=2)
    }

    token = encode_token(payload, private_key)
    token = token.decode('utf8')
    return f'Bearer {token}'


def validate_token_header(header, public_key):
    """Validate that a token header is correct
    If correct, it returns the username, it not, it returns None

    Args:
        header (string): header
        public_key (string): public key
    """
    if not header:
        logger.info("No header")
        return None

    # retrieve the bearer token
    parse_result = parse('Bearer {}', header)
    if not parse_result:
        logger.info(f'Wrong format for header "{header}"')
        return None

    token = parse_result[0]

    try:
        decoded_token = decode_token(token.encode('utf8'), public_key)
    except jwt.exceptions.DecodeError:
        logger.warning(
            f'Error decoding header "{header}". This may be key missmatch or wrong key')
        return None
    except jwt.exceptions.ExpiredSignatureError:
        logger.error(f'Authentication header has expired.')
        return None

    if 'exp' not in decoded_token:
        logger.warning('Token does not have expiry (exp).')
        return None

    if 'username' not in decoded_token:
        logger.warning('Token does not have username.')
        return None

    logger.info('Header successfully validated.')
    return decoded_token['username']
