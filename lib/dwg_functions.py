import os, stat
import re
import sys
import ntpath
import math
import itertools

def delete_bak_files(nat_dir=""):
    rtn_list = []
    if len(nat_dir) > 0:
        files = os.listdir(nat_dir)
        for nf in files:
            if os.path.isdir(nat_dir + "/" + nf):
                continue
            nf_split = nf.split('.')
            nf_ext = nf_split[-1]
            if (nf_ext == "bak"):
                #rtn_list.append(nf)
                rel_path = nat_dir + "\\" + nf
                try:
                    os.chmod(rel_path, stat.S_IWRITE)
                    os.remove(rel_path)
                    rtn_list.append(rel_path)
                except Exception as e:
                    print(repr(e))
        return rtn_list        

def check_for_pdfs(nat_dir=""):
    rtn_list = []
    if len(nat_dir) > 0:
        files = os.listdir(nat_dir)
        pdfs = os.listdir(nat_dir + "/pdf")
        
        for nf in files:
            if os.path.isdir(nat_dir + "/" + nf):
                continue
            found = False
            nf_split = nf.split('.')
            nf_ext = nf_split[-1]
            nf_base = nf_split[0].upper()
            for pf in pdfs:
                pf_split = pf.split('.')
                pf_ext = pf_split[-1]
                pf_base = pf_split[0].upper()
                if pf_ext == "pdf" and nf_base == pf_base:
                    found = True
                    break
            if found == False:
                rtn_list.append(nf)
    return rtn_list

def check_for_old_pdfs(nat_dir=""):
    rtn_list = []
    if len(nat_dir) > 0:
        files = os.listdir(nat_dir)
        pdfs = os.listdir(nat_dir + "/pdf")
        
        for nf in files:
            if os.path.isdir(nat_dir + "/" + nf):
                continue
            found = False
            nf_split = nf.split('.')
            nf_ext = nf_split[-1]
            nf_base = nf_split[0].upper()
            for pf in pdfs:
                pf_split = pf.split('.')
                pf_ext = pf_split[-1]
                pf_base = pf_split[0].upper()
                if pf_ext == "pdf" and nf_base == pf_base:
                    nf_moddate = os.path.getmtime(nat_dir + "/" + nf)
                    pdf_moddate = os.path.getmtime(nat_dir + "/pdf/" + pf)
                    if pdf_moddate > (nf_moddate + 600):
                        rtn_list.append(pf)
                    break
    return rtn_list

def compare_new_revs(dir1="", dir2=""):
    #rtn_list = ["CA123456", "CA123457", "CA123458", "CA123459"]
    files = os.listdir(dir1)
    cfiles = os.listdir(dir2)
    rtn_list = []
    for file in files:
        try:
            fsp = file.split('.')
            dwg_ext = fsp[-1]
            dwg_fn = fsp[0].upper().split('_')
            dwg_no = "".join(dwg_fn[:-1])
            print(file)
            dwg_rev = dwg_fn[-1]
            if len(dwg_fn) == 1:
                dwg_rev = "-"
            for cfile in cfiles:
                cfsp = cfile.split('.')
                cdwg_ext = cfsp[-1]
                cdwg_fn = cfsp[0].upper().split('_')
                cdwg_no = "".join(cdwg_fn[:-1])
                cdwg_rev = cdwg_fn[-1]
                if len(cdwg_fn) == 1:
                    cdwg_rev = "-"
                if dwg_no == cdwg_no and dwg_ext == cdwg_ext and dwg_rev != cdwg_rev and min(dwg_rev,cdwg_rev) == cdwg_rev and not cfile in rtn_list:
                    rtn_list.append(file)
                    continue
        except Exception as e:
            print(repr(e) + '       ' + file)
            continue
    return rtn_list


def srch_superseded(srch_dir=""):
    files = os.listdir(srch_dir)
    rtn_list = []
    for file, cfile in itertools.combinations(files, 2):
    #compare(file, cfile)
    #for file in files:
        try:
            fsp = file.split('.')
            dwg_ext = fsp[-1]
            dwg_fn = fsp[0].upper().split('_')
            dwg_no = "".join(dwg_fn[:-1])
            dwg_rev = dwg_fn[-1]
            if len(dwg_fn) == 1:
                dwg_rev = "-"

            cfsp = cfile.split('.')
            cdwg_ext = cfsp[-1]
            cdwg_fn = cfsp[0].upper().split('_')
            cdwg_no = "".join(cdwg_fn[:-1])
            cdwg_rev = cdwg_fn[-1]
            if len(cdwg_fn) == 1:
                cdwg_rev = "-"

            if dwg_no == cdwg_no and dwg_ext == cdwg_ext and cdwg_rev != dwg_rev:
                if min(dwg_rev,cdwg_rev) == dwg_rev and not file in rtn_list:
                    rtn_list.append(file)
                elif min(dwg_rev,cdwg_rev) == cdwg_rev and not cfile in rtn_list:
                    rtn_list.append(cfile)
                #rtn_list.append( dwg_no + "_" + min(dwg_rev,cdwg_rev) + "." + str(dwg_ext))
                continue

        except Exception as e:
            print(repr(e) + '       ' + file)
            continue
    return rtn_list

def validate_CAE_filenames(srch_dir=""):
    files = os.listdir(srch_dir)
    rtn_list = []
    for f in files:
        if (not validate_CAE_filename(f)):
            rtn_list.append(f)
    return rtn_list

def validate_CAE_filename(file=""):
    # Desired format is SERIAL NUM | TAB NUM | TYPE | REV
    # e.g. MA399477_10_PL_A.pdf
    
    if len(file) == 0:
        raise Exception( 'No filename given' )
        
    valid_prefixes = ['CA','MA','PS','WD','TS','UD','MD','FP','ED','CD','PD']
    valid_filetypes = ['pdf','dgn','dwg','dxf','xls','xlsx']
    
    try:
        fsp = file.split('.')
        dwg_ext = fsp[1]
        dwg_no = fsp[0]
        dwg_sp = dwg_no.split('_')
        if len(dwg_sp) != 4:
            raise Exception( 'Failed to split dwg no' )
        dwg_type = dwg_sp[0][:2]
        dwg_ser_no = dwg_sp[0][2:]
        dwg_tab = dwg_sp[1]
        dwg_fd = dwg_sp[2]
        dwg_rev = dwg_sp[3]

        if dwg_sp[-1] == 'FD' or dwg_sp[-1] == 'PL':
            raise Exception( 'FD/PL appears at end of filename' )
        if not dwg_ext in valid_filetypes:
            raise Exception( 'Invalid filetype' )

        if not dwg_type in valid_prefixes:
            raise Exception( 'Invalid alpha prefix' )

        if not ((re.match("\d{6}", dwg_ser_no) and len(dwg_ser_no) == 6) or (re.match("\d{5}", dwg_ser_no) and len(dwg_ser_no) == 5)):
            raise Exception( 'Invalid serial no' ) 

        if not re.match("\d{2}", dwg_tab):
            raise Exception( 'Invalid tab' )

        if not(dwg_fd == 'FD' or dwg_fd == 'PL'):
            raise Exception( 'Invalid FD/PL' )

        if not (len(dwg_rev) == 1 or len(dwg_rev) == 2) or not (re.match("[A-Z]", dwg_rev) or re.match("[A-Z]{2}", dwg_rev) or dwg_rev == '-'):
            raise Exception( 'Invalid revision' )

        return True

    except Exception as e:
        print(repr(e) + '       ' + file)
        return False
