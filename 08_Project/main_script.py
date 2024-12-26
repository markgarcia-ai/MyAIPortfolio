import os
import sys
import importlib
import time

"""
First we download the stock market data,we check the current data and download any updates required.
Current markets are Dow Jones, NASDAQ, S&P500 and S&P600.
Check stocks with higher increment % in the past months and less than $20 per share.


"""

# List of folders containing scripts
folders = ["scripts"]

# Dictionary specifying the functions to execute for each script with "Enable" or "Disable" options
functions_to_run = {
    "00_Test": [("function0", "Enable")],
    "01_download_data": [("function1", "Disable")],
    "02_Neural_Networks_Allstocks": [("function2", "Disable")],
    "02_Stock_changes": [("function2_1", "Disable")],    
    "03_ConvertToCSV": [("function3", "Disable")],
    "04_CompaniesData": [("function4", "Disable")],
    "05_Stock_selection": [("function5", "Disable")],
    "06_Automated_trading": [("function6", "Disable")]
}

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
    print("Welcome to the script runner.")
    if any([status == "Enable" for functions in functions_to_run.values() for _, status in functions]):  # Check if any functions are enabled
        print("\nStarting the execution of enabled functions...\n")
        run_specific_functions_with_timer(functions_to_run)
    else:
        print("No functions enabled for execution. Exiting.")