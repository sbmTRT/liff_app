from loguru import logger

from configs import log_config


logger.add(
    log_config.LOG_FILE_PATH,
    format=log_config.LOG_MSG_FORMAT,
    level=log_config.LOG_LEVEL,
    encoding="utf8")


# Informationログ出力用
def put_info(message: str):
    output = {}
    output["MESSAGE"] = message

    logger.info(output)


# Errorログ出力用
def put_error_info(file: str, method: str, line: str, code: str, message: str, other: str):
    output = {}
    output["CLASS"]   = file
    output["METHOD"]  = method
    output["LINE"]    = line
    output["CODE"]    = code
    output["MESSAGE"] = message
    output["OTHER"]   = other

    logger.error(output)


# Warningログ出力用
def put_warning_info(file: str, method: str, line: str, code: str, message: str, other: str):
    output = {}
    output["CLASS"]   = file
    output["METHOD"]  = method
    output["LINE"]    = line
    output["CODE"]    = code
    output["MESSAGE"] = message
    output["OTHER"]   = other

    logger.warning(output)


# Criticalログ出力用
def put_critical_info(file: str, method: str, line: str, code: str, message: str, other: str):
    output = {}
    output["CLASS"]   = file
    output["METHOD"]  = method
    output["LINE"]    = line
    output["CODE"]    = code
    output["MESSAGE"] = message
    output["OTHER"]   = other

    logger.error(output)
