import pandas as pd
import os


class parse_excel:
    """
    This module is used to parse necessary data that has been configured in the Excel file: `Config_sheet.xlsx`

    Utilizes `pandas` python module to parse and read data from the CSV file, and converts said data into a pandas dataframe for manipulation.
    """

    global df, _pe

    def __init__(self, ob):
        """
        Module Initializing function.

        NOTE: may need to alter slash in path variable to match with OS file system...
        For windows, use backslash, for Unix, use forward slash.
        """
        path = os.path.dirname(__file__)
        path += "/Config_sheet.xlsx"
        # path += "/Config_sheet_old.xlsx"  #Legacy Config for backwards compatibility testing
        self.df = pd.read_excel(path, "SPN", header=1)
        self._pe = ob

    def parse_excel(self):
        """
        Opens the file specified by `path` variable, and parses data listed in SPN table.

        Tkinter will generate necessary components, based on the excel configuration.
        """
        for i in range(33):
            try:
                # use i when indexing excel columns, use spn when updating dictionaries
                spn = self.df.loc[i,"SPN"]
                self._pe.spn_list.append(spn)
                spn_data = self.df.loc[i, "type"]
                spn_type = str(spn_data)
                
                # Check for relay control
                relay_board = self.df.loc[i,"CANBoardNum"]
                relay_channel = self.df.loc[i,"CANChannel"]
                relay_type = self.df.loc[i,"IO_type"]
                
                if(str(relay_type) != "nan"):
                    self._pe.relay_bool_dict.update({spn:1})
                
                self._pe.relay_board_dict.update({spn:relay_board})
                self._pe.relay_channel_dict.update({spn:relay_channel})
                self._pe.relay_type_dict.update({spn:relay_type})

                # Check if 3 columns are configured:
                board_num = self.df.loc[i,"Board_Num"]
                channel = self.df.loc[i,"Channel"]
                self._pe.board_dict.update({spn:board_num})
                self._pe.channel_dict.update({spn:channel})
                # Only if type column has valid entries
                if (
                    (self._pe.dig_ip_str in spn_type)
                    or (self._pe.dig_op_str in spn_type)
                    or (self._pe.vol_ip_str in spn_type)
                    or (self._pe.vol_op_str in spn_type)
                    or (self._pe.pwm_ip_str in spn_type)
                    or (self._pe.fq_op_str in spn_type)
                ):
                    # required data
                    name = self.df.loc[i, "Name"]
                    self._pe.name_list.append(name)
                    self._pe.UI_spn.append(spn)
                    self._pe.UI_dict.update({spn: 0})
                    name_spn = "SPN" + str(spn)
                    self._pe.config_dict.update({spn: name})  # all data in dictionary
                
                    new_name = name_spn + " : " + name
                    if self._pe.dig_ip_str in spn_type:
                        self._pe.dig_ip_spn.append(spn)
                        self._pe.dig_ip_name.append(new_name)
                        self._pe.type_dict.update({spn: "digin"})

                    elif self._pe.dig_op_str in spn_type:
                        self._pe.dig_op_spn.append(spn)
                        self._pe.dig_op_name.append(new_name)
                        self._pe.type_dict.update({spn: "digout"})

                    elif self._pe.vol_ip_str in spn_type:
                        self._pe.vol_ip_spn.append(spn)
                        self._pe.vol_ip_name.append(new_name)
                        self._pe.type_dict.update({spn: "voltin"})
                    
                    elif self._pe.vol_op_str in spn_type:
                        self._pe.vol_op_spn.append(spn)
                        self._pe.vol_op_name.append(new_name)
                        self._pe.type_dict.update({spn: "voltout"})

                    elif self._pe.pwm_ip_str in spn_type:
                        self._pe.pwm_ip_spn.append(spn)
                        self._pe.pwm_ip_name.append(new_name)
                        self._pe.type_dict.update({spn: "pwmin"})

                    elif self._pe.fq_op_str in spn_type:
                        self._pe.fq_op_spn.append(spn)
                        self._pe.fq_op_name.append(new_name)
                        self._pe.type_dict.update({spn: "freqout"})
            except KeyError as e:
                print(e)