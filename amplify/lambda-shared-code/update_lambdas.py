from pathlib import Path
import shutil

functions_that_dont_require_shared_lib = set([
])

lambdas_root = Path('../backend/function')
shared_lib_name = 'lambda_utils.py'

shared_lib_path = Path('.') / shared_lib_name

for function_dir in lambdas_root.iterdir():
    if function_dir.name not in functions_that_dont_require_shared_lib:
        destination = function_dir / 'src/' / shared_lib_name
        shutil.copyfile(shared_lib_path, destination)
        print(f'Updated {destination}')

print('NOTE: If you do not want shared libs in your functions, add its name to the list in this script')