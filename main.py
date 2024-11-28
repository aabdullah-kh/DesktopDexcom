from tkinter import *
from pydexcom import Dexcom
from decouple import config
import threading
import time
import os
from sys import argv


def update_blood_sugar(dexcom: Dexcom, blood_sugar: Label) -> None:
    """_summary_
    
    Updates Blood Sugar Label Every 5 seconds

    Args:
        dexcom (Dexcom): pydexcom object for API calls
        blood_sugar (Label): Tkinter label to be updated
        
    Returns:
        None
    """
    
    # Retrieves blood sugar every 5 seconds using pydexcom API
    while True:
        
        curr_reading = dexcom.get_current_glucose_reading()
        
        if curr_reading is None:
            # We should NOT get here
            blood_sugar.after(0, blood_sugar.config, {"text": "Error!"})
            time.sleep(5)
        
        else:
            blood_sugar.after(0, blood_sugar.config, {"text": str(curr_reading.mmol_l) + curr_reading.trend_arrow})
            time.sleep(5)


def main() -> None:
    """_summary_

    Initializes App
    
    Returns:
        None
    """
    
    # Initialize pydexcom object using information in .env (See example.env)
    
    try:
        dexcom = Dexcom(username=config("EMAIL"), password=config("PASS"), region=config("REGION"))
    
    except:
        print("=================================================================================")
        print("\n.env is not configured correctly OR Dexcom share is not configured correctly\n")
        print("See: https://gagebenne.github.io/pydexcom/pydexcom.html#frequently-asked-questions\n")
        print("=================================================================================")
        exit(1)
    
    # Setup Tkinter
    window = Tk()
    window.title("Dexcom")
    window.geometry("225x225")
    window.configure(background='#dcdddd')
    abspath = os.path.abspath(argv[0])
    dname = os.path.dirname(abspath)
    os.chdir(dname)
    
    # Uncomment this if converting .py to .exe using 'exe-compile-script.sh'
    # You WILL NEED 'Git Bash for Windows' to run it
    # The .exe NEEDS to stay in the created 'dist' directory, just make a shortcut to place it elsewhere
    
    # window.iconphoto(True, PhotoImage(file=r"..\imgs\icon.png"))
    
    # Comment this out if converting .py to .exe using 'exe-compile-script.sh'
    window.iconphoto(True, PhotoImage(file=r"imgs\icon.png"))

    curr_reading = dexcom.get_current_glucose_reading()
    
    if curr_reading is None:
        # We should NOT get here
        blood_sugar = Label(window, text="Error!", bg='#dcdddd', fg='#3d3e3d', font=('SF Pro Text', 40, 'bold'))
        
    else:
        blood_sugar = Label(window, text=str(curr_reading.mmol_l) + curr_reading.trend_arrow, bg='#dcdddd',fg='#3d3e3d', font=('SF Pro Text', 40, 'bold'))
        
    blood_sugar.place(relx = 0.5, rely = 0.5, anchor = CENTER)

    # Setup Thread for Dexcom API calls
    thread = threading.Thread(target=update_blood_sugar, args=(dexcom, blood_sugar), daemon=True)
    
    # Start Thread and App
    thread.start()
    window.mainloop()


if __name__ == "__main__":
    main()
