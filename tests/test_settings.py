import sys
sys.dont_write_bytecode = True

# 添加 src 目录到 sys.path
src_path = "/Users/wumengsong/Code/Github/ToolAgent/src"
if src_path not in sys.path:
    sys.path.append(src_path)