import random
import string

def generate_random_key(length=8):
    """
    生成指定长度的随机字符串。
    
    参数:
    length (int): 随机字符串的长度。默认值为10。
    
    返回:
    str: 生成的随机字符串。
    """
    # 定义字符串的所有可能字符
    characters = string.ascii_letters + string.digits + string.punctuation
    # 随机选择指定数量的字符并生成字符串
    random_key = ''.join(random.choice(characters) for i in range(length))
    return random_key

