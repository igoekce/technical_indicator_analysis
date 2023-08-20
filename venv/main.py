# main.py

import subprocess

# Execute the data_fetch_and_calc script
subprocess.run(['python', 'data_fetch_and_calc_stocks.py'])

# Execute the data_fetch_and_calc script
subprocess.run(['python', 'data_fetch_and_calc_indices.py'])

# Once the script is finished, proceed to execute the app.py script
subprocess.run(['streamlit', 'run', 'app.py'])