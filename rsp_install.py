import shutil
import sysconfig
import os

# Имя расширения и его исходный путь
ext_file = "rsp.linux-amd64.so"

# Получаем путь к директории для установки расширений Python
ext_install_path = sysconfig.get_paths()["platlib"]

shutil.copy2(ext_file, os.path.join(
    ext_install_path, os.path.basename("rsp.so")))
