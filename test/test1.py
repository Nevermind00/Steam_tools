from loguru import logger

# logger.debug("Отладка")
# logger.info("Информация")
# logger.success("Успех!")
# logger.warning("Предупреждение")
# logger.error("Ошибка")

logger.add("file.log")
logger.error("")
