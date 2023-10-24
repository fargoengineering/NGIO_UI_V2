import time
from global_defines import *
from UserInterface.parse_excel import *
from UserInterface.generate_ui import *
from UserInterface.update_ui import *
from ethercat import *

start = time.time()
gd_obj = global_defines()

pe = parse_excel(gd_obj)
gu = generate_ui(gd_obj)
ui = update_ui(gd_obj)
ec = etherCAT(gd_obj)

pe.parse_excel()
gu.generate_spn_ui()
# gu.generate_setting_ui()
ec.run_ec()

# update_ui.py
def ui_update_thread():
    th1 = threading.Timer(0.01, ui_update_thread)
    th1.setDaemon(True)
    th1.start()  # 1 Second Read Thread

# set initial slot types from excel
time.sleep(3)
ec.set_types()

ui_update_thread()
ui.mainloop()

end = time.time()
boot_time = end - start
print("Boot Time = %s seconds" % boot_time)