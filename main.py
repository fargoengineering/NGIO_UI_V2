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

# Set defaults once and pause:
ec.set_types()
# ec.pause_pdo()

# Run UI
ui.mainloop()

# Close ethernet connection here, after UI is closed:
ec.close_ec()