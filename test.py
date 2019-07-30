import os
import sys

def if_module_exist(module_name):
    folder_module = os.path.join(os.path.abspath(os.path.dirname(sys.argv[0])), "src" ,module_name)  # Полный путь до модуля, если это папка.
    init_in_folder_module = os.path.join(folder_module, "__init__.py")  # Полный путь до __init__.py в папке.
    root_module = folder_module + ".py"  # Полный путь до модуля, если он лежит в корне.

    # Проверим их наличие:
    if not os.path.exists(root_module) and not (os.path.isdir(folder_module) and os.path.exists(init_in_folder_module)):
        print(f"There is no module or package '{module_name}'.")
        return(False)
    else:
        return(True)

# Тестируем все ли модули на наличии:
print("----------------------------------------")
print("Testing the composition of the system...")
# Для начала проверяем наличие системынх модулей:
modules_for_test = ["flask", "matplotlib", "numpy", "pandas", "requests", "sklearn"]

print("----------------------------------------")
for one_module_name in modules_for_test:
    try:
        __import__(one_module_name)
        print(one_module_name.ljust(13) + " - ready.")
    except:
        print(one_module_name.ljust(13) + "is missing!")

print("----------------------------------------")
# Проверяем наличие разработанных модулей:
modules_for_test = ["constants", "db", "inet", "prediction", "utils"]

for one_module_name in modules_for_test:
    if if_module_exist(one_module_name):
        print(one_module_name.ljust(13) + " - ready.")
    else:
        print(one_module_name.ljust(13) + "is missing!")
print("----------------------------------------")
