import itertools
from tkinter import ttk
import tkinter as tk
from tkinter import *
import subprocess


class global_defines:
    # testing with all hardware : 0, else 1
    # testing_active = 1
    # debug_mode = 0
    # debug_mode_button = 0

    # Create the master object
    master = tk.Tk()
    icon = tk.PhotoImage(file="img/fei_icon.png")
    master.iconphoto(True,icon)
    master.geometry("750x600")
    master.title("FEI_NGIO")
    mygreen = "#CEF743"
    red = "#B1CCE7"
    black = "#000000"

    style = ttk.Style()
    style.theme_create(
        "raspi",
        parent="alt",
        settings={
            "TNotebook": {"configure": {"tabmargins": [3, 5, 3, 0]}},
            "TNotebook.Tab": {
                "configure": {
                    "padding": [5, 1],
                    "background": "lightblue",
                    "foreground": black,
                },
                "map": {
                    "background": [("selected", "SteelBlue1")],
                    "expand": [("selected", [1, 1, 1, 0])],
                },
            },
        },
    )
    style.theme_use("raspi")
    
    tc = ttk.Notebook(master)

    # DIG I/P
    tc_dig_ip = ttk.Frame(tc)
    tc_dig_ip.pack(side="left")
    dig_ip_canvas = Canvas(
        tc_dig_ip, width=6, height=6, scrollregion=(0, 0, 1450, 1100)
    )
    dig_ip_canvas.config(width=6, height=6)
    dig_ip_canvas.pack(side=LEFT, expand=True, fill=BOTH)
    dig_ip_frame = Frame(dig_ip_canvas)
    dig_ip_canvas.create_window((0, 0), window=dig_ip_frame, anchor="nw")

    # DIG O/P
    tc_dig_op = ttk.Frame(tc)
    tc_dig_op.pack(side="left")
    dig_op_canvas = Canvas(
        tc_dig_op, width=6, height=6, scrollregion=(0, 0, 1450, 1100)
    )
    dig_op_canvas.config(width=6, height=6)
    dig_op_canvas.pack(side=LEFT, expand=True, fill=BOTH)
    dig_op_frame = Frame(dig_op_canvas)
    dig_op_canvas.create_window((0, 0), window=dig_op_frame, anchor="nw")

    # VOLTAGE in
    tc_vol_ip = ttk.Frame(tc)
    tc_vol_ip.pack(side="left")
    vol_ip_canvas = Canvas(
        tc_vol_ip, width=6, height=6, scrollregion=(0, 0, 1450, 1100)
    )
    vol_ip_canvas.config(width=6, height=6)
    vol_ip_canvas.pack(side=LEFT, expand=True, fill=BOTH)
    volt_ip_frame = Frame(vol_ip_canvas)
    vol_ip_canvas.create_window((0, 0), window=volt_ip_frame, anchor="nw")

    # VOLTAGE out
    tc_vol_op = ttk.Frame(tc)
    tc_vol_op.pack(side="left")
    vol_op_canvas = Canvas(
        tc_vol_op, width=6, height=6, scrollregion=(0, 0, 1450, 1100)
    )
    vol_op_canvas.config(width=6, height=6)
    vol_op_canvas.pack(side=LEFT, expand=True, fill=BOTH)
    volt_op_frame = Frame(vol_op_canvas)
    vol_op_canvas.create_window((0, 0), window=volt_op_frame, anchor="nw")

    # PWM I/P
    tc_pwm_ip = ttk.Frame(tc)
    tc_pwm_ip.pack(side="left")
    pwm_ip_canvas = Canvas(
        tc_pwm_ip, width=6, height=6, scrollregion=(0, 0, 1450, 1100)
    )
    pwm_ip_canvas.config(width=6, height=6)
    pwm_ip_canvas.pack(side=LEFT, expand=True, fill=BOTH)
    pwm_ip_frame = Frame(pwm_ip_canvas)
    pwm_ip_canvas.create_window((0, 0), window=pwm_ip_frame, anchor="nw")


    # Frequency
    tc_freq_op = ttk.Frame(tc)
    tc_freq_op.pack(side="left")
    freq_op_canvas = Canvas(
        tc_freq_op, width=6, height=6, scrollregion=(0, 0, 1450, 1100)
    )
    freq_op_canvas.config(width=6, height=6)
    freq_op_canvas.pack(side=LEFT, expand=True, fill=BOTH)
    freq_op_frame = Frame(freq_op_canvas)
    freq_op_canvas.create_window((0, 0), window=freq_op_frame, anchor="nw")

    # Settings
    tc_settings = ttk.Frame(tc)
    tc_settings.pack(side="left")
    settings_canvas = Canvas(
        tc_settings, width=6, height=6, scrollregion=(0, 0, 1450, 1100)
    )
    settings_canvas.config(width=6, height=6)
    settings_canvas.pack(side=LEFT, expand=True, fill=BOTH)
    setting_frame = Frame(settings_canvas)
    settings_canvas.create_window((0, 0), window=setting_frame, anchor="nw")
    
    
    tc.add(tc_dig_ip, text="DigitalIn")
    tc.add(tc_dig_op, text="DigitalOut")
    tc.add(tc_vol_ip, text="AnalogIn")
    tc.add(tc_vol_op, text="AnalogOut")
    tc.add(tc_pwm_ip, text="PWMIn")
    tc.add(tc_freq_op, text="FreqOut")
    tc.add(tc_settings, text="Settings")

    tc.pack(expand=1, fill="both")

    # Non-UI Variables:

    eng_spd = tk.StringVar()
    chopper_type = 1
    chopper_type_var = tk.StringVar()
    dig_ip_option_var = []
    open_option_var = []
    HHMC_gear = tk.StringVar()
    IC_gear = tk.StringVar()
    Aux_PTO_enabled_str = tk.StringVar()
    feeder_type = tk.StringVar()
    unload_rate = tk.StringVar()

    # general spn/widgets
    dropdown_relay_options = ["OpenCircuit","BatteryShort","GroundShort","Bypass"]
    toggle = 0  # Used for update_ui dictionary
    dig_ip_button = []  # Array of buttons listed on DIG I/P used to indicate input status (Green=HIGH,Red=LOW)
    dig_ip_update = []  # buttons to update digital input threshold
    dig_ip_entry = []   # entry to write digin threshold
    dig_ip_options = []  # Array of option menus listed on DIG I/P
    dig_op_button = []  # Array of buttons under DIG O/P
    dig_op_option = []
    open_option = []
    open_button = []
    open_mode = {}
    volt_ip_label = []
    volt_op_label = []
    volt_ip_option = []
    volt_op_option = []
    pwm_ip_option = []
    freq_op_option = []
    
    pwm_ip_label_freq = []
    pwm_ip_label_duty = []
    pwm_thresh_label = []
    freq_label_freq = []
    freq_label_duty = []
    duty_label = []
    pulse_label = []
    volt_ip_button = []
    volt_op_button = []

    dig_ip_mode = {}
    volt_ip_toggle = []  
    volt_op_toggle = []  
    relay_switch = []  # 1 for relay on, 0 for relay off

    pwm_ip_button = []
    pwm_ip_toggle = []
    freq_button = []
    freq_toggle = []
    button_pulse = []
    pulse_toggle = []
    brand = 0  # 0 = CIH, 1 = NH
    board_Num = 0  # 0 or Empty = Invalid Board.
    config_dict = {}

    # Create a list of all buttons and options for disabling at once.
    all_widgets = list(
        itertools.chain(
            dig_ip_button,
            dig_ip_options,
            dig_op_button,
            open_option,
            open_button,
            volt_ip_button,
            volt_ip_toggle,
            volt_op_button,
            volt_op_toggle,
            pwm_ip_button,
            pwm_ip_toggle,
            freq_button,
            freq_toggle,
            button_pulse,
            pulse_toggle,
        )
    )

    # Parse Strings
    dig_ip_str = "DigitalInput"
    dig_op_str = "DigitalOutput"
    vol_ip_str = "AnalogInput"
    vol_op_str = "AnalogOutput"
    pwm_ip_str = "PWMInput"
    fq_op_str = "FrequencyOutput"

    # Lists for Channel/Board
    ping_dict = {}  # Dictionary with Board Number : Boolean active value
    time_dict = {}  # Dictionary containing CAN timestamps
    board_dict = {}  # Dictionary with SPN : Board Number pairs
    
    # Lists for relays/CAN
    relay_board_dict = {}
    relay_channel_dict = {}
    relay_type_dict = {}
    relay_bool_dict = {}
    board_list = []
    channel_dict = {}  # Dictionary with SPN : relay(channel) pairs
    dig_state = {}  # Dictionary with SPN : default state of 0
    board_wid_dict = {}  # Dictionary with Board No : [list of widget] pairs
    volt_state = {}
    freq_state = {}
    pulse_state = {}
    pwm_state = {}
    ground_dict = {}  # Contains SPNs that are open to battery xor ground
    bool_both = {}  # Indicate if both Channel and Board number are listed
    # Indicate if all board, channel, and openTo(Ground or Board or Both) are listed
    bool_all = {}
    UI_dict = {}
    UI_spn = []
    button_list = []
    spn_list = []
    name_list = []
    dig_ip_spn = []
    dig_ip_option = []
    
    dig_op_spn = []
    vol_ip_spn = []
    vol_op_spn = []
    pwm_op_spn = []
    pwm_ip_spn = []
    fq_op_spn = []
    pulse_spn = []
    dig_ip_name = []
    dig_op_name = []
    vol_ip_name = []
    vol_op_name = []
    pwm_op_name = []
    pwm_ip_name = []
    fq_op_name = []
    pulse_name = []
    spare_list_1 = []
    spare_list_2 = []
    volt_op_string = []
    volt_ip_string = []
    pwm_ip_string = []
    freq_string = []
    pulse_string = []
    type_dict = {}


    # settings
    slot_num_box = tk.Entry
    aux_box = tk.Entry
    board_box = tk.Entry
    KeyIsON = 1
    Key_Button = 0
    fei_compatible = 0