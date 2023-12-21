import time
from global_defines import *
from UserInterface.parse_excel import *
from UserInterface.generate_ui import *
from UserInterface.update_ui import *
from ethercat import *

start = time.time()
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
    
def slot_type_thread():
    # Make sure slots are always configured type, in the case that a slot is moved somewhere else.
    th1 = threading.Timer(25,ec.set_types)
    th1.daemon = True
    th1.start() # 10 second thread
    
# set initial slot types from excel
# Not sure this is working as expected...10/30
time.sleep(1)
ec.set_types()

ui_update_thread()

# slot_type_thread()

ui.mainloop()
end = time.time()
boot_time = end - start
print("Boot Time = %s seconds" % boot_time)

# Close ethernet connection here:
ec.close_ec()