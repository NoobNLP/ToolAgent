import os
import logging


def get_logger() -> logging.Logger:
    from toolagent import config # * 先有 config 再有 logger 避免循环引用
    # 实例化 主Logger 
    logger = logging.getLogger("ToolAgent")
    # 设置日志输出等级 
    logger.setLevel(logging.DEBUG)

    # 设置日志输出格式 
    # formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    basic_formatter = logging.Formatter(
        "[%(asctime)s - %(name)s:%(lineno)d - %(levelname)s] %(message)s"
    )

    # 如果日志输出文件夹不存在，则创建文件夹
    os.makedirs("TA_log/", exist_ok=True)

    # 1. 实例化写入日志文件的Handler
    file_handler = logging.FileHandler('TA_log/{}.log'.format(config.job_time))
    file_handler.setLevel(logging.INFO)
    file_formatter = logging.Formatter(
        "[%(asctime)s - %(name)s - %(levelname)s] %(pathname)s:%(lineno)d\n%(message)s\n\n"
    )
    file_handler.setFormatter(file_formatter)

    # 2. 实例化shell实时输出的Handler
    try:
        from rich.logging import RichHandler
        shell_handler = RichHandler(rich_tracebacks=True)
    except ImportError:
        shell_handler = logging.StreamHandler(stream=None)
        shell_handler.setFormatter(basic_formatter) 

    # 添加handler到logger 
    logger.addHandler(file_handler) 
    logger.addHandler(shell_handler)

    # 输出日志 
    # logger.debug('this is a debug message') 
    # logger.info('this is an info message') 
    # logger.warning('this is a warning message') 
    # logger.error('this is an error message') 
    # logger.critical('this is a critical message')
    return logger
