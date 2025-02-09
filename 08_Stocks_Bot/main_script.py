import os
import sys
import importlib
import time
from multiprocessing import Process
import subprocess

"""
01_download_data : First we download the stock market data,we check the current data and download any updates required.
Current markets are Dow Jones, NASDAQ, S&P500 and S&P600.
Check stocks with higher increment % in the past months and less than $20 per share.


"""

# List of folders containing scripts
folders = ["scripts"]

# Dictionary specifying the functions to execute for each script with "Enable" or "Disable" options
functions_to_run = {
    "Test": [("function0", "Disable")],
    "00_Generate_markets": [("function01", "Disable")],
    "01_Update_markets": [("function1", "Disable")],
    "02_Stock_changes": [("function2", "Disable")], 
    "03_Generate_portfolio": [("function3", "Disable")], 
    "04_Update_portfolio": [("function4", "Disable")], 
    "05_Compute_summary": [("function5", "Disable")]
}

def run_stock_bot():
    """Function to run the stock bot (main.py)."""
    subprocess.run(["python", "main.py"])

def run_web_app():
    """Function to run the Flask web application (app.py)."""
    subprocess.run(["python", "web_app/app.py"])



def run_specific_functions_with_timer(functions_to_run):
    for script_name, function_list in functions_to_run.items():
        # Filter for enabled functions
        enabled_functions = [func for func, status in function_list if status == "Enable"]
        if not enabled_functions:
            print(f"No functions enabled for {script_name}. Skipping.")
            continue
        
        try:
            # Add script folder to system path
            folder_path = os.path.abspath(folders[0])
            if folder_path not in sys.path:
                sys.path.append(folder_path)
            
            # Import the script dynamically
            module = importlib.import_module(script_name)
            
            # Execute each enabled function in the script with a timer
            for func_name in enabled_functions:
                try:
                    func = getattr(module, func_name)
                    print(f"Running {func_name} from {script_name}...")
                    
                    # Start timer
                    start_time = time.time()
                    func()
                    # End timer
                    end_time = time.time()
                    
                    elapsed_time = end_time - start_time
                    print(f"{func_name} completed in {elapsed_time:.4f} seconds.\n")
                except AttributeError:
                    print(f"Error: {func_name} not found in {script_name}.")
        except ModuleNotFoundError as e:
            print(f"Error: Module {script_name} not found. {e}")
        except Exception as e:
            print(f"Error while executing functions in {script_name}: {e}")

if __name__ == "__main__":
    """
    It runs the porfolio update and summary functions and then starts the stock bot and web app.
    Remember to enable functions to run for data stocks update
    Change enble_bot to False if you want to run only the functions.
    """

    enable_bot = True

    print("Welcome to the script runner.")
    if any([status == "Enable" for functions in functions_to_run.values() for _, status in functions]):  # Check if any functions are enabled
        print("\nStarting the execution of enabled functions...\n")
        run_specific_functions_with_timer(functions_to_run)
    else:
        print("No functions enabled for execution. Exiting.")

    if enable_bot:
        # Create processes
        stock_bot_process = Process(target=run_stock_bot)
        web_app_process = Process(target=run_web_app)

        # Start processes
        stock_bot_process.start()
        print("Stock bot started...")
        
        # Delay web app to ensure JSON data updates
        time.sleep(5)  # Wait for initial stock data update
        web_app_process.start()
        print("Web application started...")

        # Wait for processes to complete
        stock_bot_process.join()
        web_app_process.join()