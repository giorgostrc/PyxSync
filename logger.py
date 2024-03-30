import logging

logger = logging.getLogger("PyxSync")
logger.setLevel(logging.DEBUG)

console = logging.StreamHandler()
console.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(asctime)s:%(name)s:%(levelname)s --> %(message)s", "%Y-%m-%d %H:%M")
console.setFormatter(formatter)

logger.addHandler(console)
