from multiprocessing import Process
import subprocess
import time

def run_stock_bot():
    """Function to run the stock bot (main.py)."""
    subprocess.run(["python", "main.py"])

def run_web_app():
    """Function to run the Flask web application (app.py)."""
    subprocess.run(["python", "web_app/app.py"])

if __name__ == "__main__":
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
