import logging
import os
def get_logger(name,path,func_name):
    # 创建 logger 对象
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # 创建文件 handler 和控制台 handler
    log_path = os.path.join(path, "log", f"{name}.log")
    os.makedirs(os.path.dirname(log_path), exist_ok=True)
    file_handler = logging.FileHandler(log_path,'w',encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # 创建 formatter
    formatter = logging.Formatter(f'%(asctime)s - %(levelname)s - {func_name}- %(message)s')

    # 设置 handler 的 formatter
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # 将 handler 添加到 logger 中
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger

def set_logger_format(logger, func_name):
    # 获取记录器的所有处理器
    handlers = logger.handlers
    new_format = f'%(asctime)s - %(levelname)s - {func_name}- %(message)s'
    # 为每个处理器设置新的格式化器
    for handler in handlers:
        formatter = logging.Formatter(new_format)
        handler.setFormatter(formatter)

def get_logger_path(logger):
    handlers = logger.handlers
    log_file_path = None
    for handler in handlers:
        if isinstance(handler, logging.FileHandler):
            log_file_path = handler.baseFilename
            break
    return log_file_path