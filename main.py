from tkinter import *
from pydexcom import Dexcom
from decouple import config
import threading
import time
import os
from sys import argv


def update_blood_sugar(dexcom: Dexcom, blood_sugar: Label) -> None:
    """_summary_
    
    Updates blood sugar label every 1 minute

    Args:
        dexcom (Dexcom): pydexcom object for API calls
        blood_sugar (Label): Tkinter label to be updated
        
    Returns:
        None
    """
    
    # Updates Blood Sugar Every Minute
    while True:
        
        curr_reading = dexcom.get_current_glucose_reading()
        
        if curr_reading is None:
            blood_sugar.after(0, blood_sugar.config, {"text": "Error: Trying Again in 1 Minute..."})
            time.sleep(60)
        
        else:
            blood_sugar.after(0, blood_sugar.config, {"text": str(curr_reading.mmol_l) + curr_reading.trend_arrow})
            time.sleep(60)


def main() -> None:
    """_summary_

    Initializes app and threading
    
    Returns:
        None
    """
    
    # Initialize pydexcom object using information in .env (See example.env)
    dexcom = Dexcom(username=config("EMAIL"), password=config("PASS"), region=config("REGION"))
    
    # Setup Tkinter
    window = Tk()
    window.title("Dexcom")
    window.geometry("225x225")
    abspath = os.path.abspath(argv[0])
    dname = os.path.dirname(abspath)
    os.chdir(dname)
    
    # Uncomment this if converting this to exe
    # window.iconphoto(True, PhotoImage(file=r"..\imgs\icon.png"))
    
    window.iconphoto(True, PhotoImage(file=r"imgs\icon.png"))
    
    window.configure(background='#dcdddd')

    curr_reading = dexcom.get_current_glucose_reading()
    
    if curr_reading is None:
        blood_sugar = Label(window, text="Error: Trying Again in 1 Minute...", bg='#dcdddd', fg='#3d3e3d', font=('SF Pro Text', 40, 'bold'))
        
    else:
        blood_sugar = Label(window, text=str(curr_reading.mmol_l) + curr_reading.trend_arrow, bg='#dcdddd',fg='#3d3e3d', font=('SF Pro Text', 40, 'bold'))
    
    blood_sugar.place(relx = 0.5, rely = 0.5, anchor = CENTER)

    # Setup Thread for Blood Sugar Updates
    thread = threading.Thread(target=update_blood_sugar, args=(dexcom, blood_sugar), daemon=True)
    
    # Start Window and Thread
    thread.start()
    window.mainloop()


if __name__ == "__main__":
    main()
