import FlashXSS

func_table = {
    "Flash_XSS":FlashXSS.FlashXSS,
}



def ChooseFunc(PoC_Addr):
    if PoC_Addr in func_table.keys():
        return func_table[PoC_Addr]
