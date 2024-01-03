from global_defines import *
from UserInterface.parse_excel import *
from UserInterface.generate_ui import *
from UserInterface.update_ui import *
from ethercat import *

gd_obj = global_defines()

ec = etherCAT(gd_obj)
pe = parse_excel(gd_obj)
gu = generate_ui(gd_obj,ec)
ui = update_ui(gd_obj)
uc = ui_callbacks(gd_obj,ec)

pe.parse_excel()
gu.generate_spn_ui()
gu.generate_setting_ui()
ec.run_ec()

# update_ui.py
def ui_update_thread():
    th1 = threading.Timer(0.01, ui_update_thread)
    th1.daemon = True
    th1.start()     
    

def default_thread():
    ec.set_types()  # Assuming this returns or yields control
    threading.Timer(10, default_thread).start()  # Reschedule after 2 seconds
    # time.sleep(10)

# Start the thread as a daemon:
# th = threading.Thread(target=default_thread)
# th.daemon = True
# th.start()


# Set defaults once and pause:
ec.set_types()
# ec.pause_pdo()

# Run UI
ui.mainloop()

# Close ethernet connection here, after UI is closed:
ec.close_ec()