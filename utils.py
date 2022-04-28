import os


def set_github_action_output(var_name, value):
    os.system(f'echo "::set-output name={var_name}::"{value}""')
