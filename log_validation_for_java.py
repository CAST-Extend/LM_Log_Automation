import os
import re
import xlwt
from xlwt import Workbook
from datetime import datetime
import logging

extracted_data=[]
count = 1

def extract_strings_with_single_quotes(line):
    pattern = r"'([^']+)'"
    matches = re.findall(pattern, line)
    return matches

def extract_data_between_first_and_second_single_quotes(line):
    pattern = r"[^']+'[^']*'([^']+)"
    match = re.search(pattern, line)
    
    if match:
        return match.group(1)
    else:
        return None

def log_validation(dot_csv_file, file_name):
    try:
        logging.basicConfig(filename="Log_Validation_Logs.txt", level=logging.INFO, format="%(asctime)s %(message)s")

        logging.info('-----------------------------------------------------------------------------------------------------------------------------------------------')
        logging.info(file_name+'\n')
        #extrating http pattern using regex
        with open(dot_csv_file, 'r') as f:
            lines = f.readlines()
            for line in lines:
                # code_pattern_list.append(1)
                # if 'lmig' in line.lower():
                result = extract_strings_with_single_quotes(line)
                # print(result)
                result_2 = extract_data_between_first_and_second_single_quotes(line)
                # print(result_2)
                if len(result) < 3 or result is None:
                    logging.info(line)
                else:
                    global count
                    app_name = file_name
                    missing_object = result[1]+'.'+result[0]
                    missing_object_full_name = result_2
                    missing_object_type = result[2]
                    # if 'lm' in missing_object.lower():
                    extracted_data.append([count, app_name, missing_object, missing_object_full_name, missing_object_type])
                    count += 1

    except Exception as e:
        print("Some Exception Occured !\n Please resolve or contact developers.\n"+str(e))


def write_into_excel(out_put_path):

    try:
        Workbook = xlwt.Workbook()
        Log_Validation_Output = out_put_path+"\Log_Validation_Output.xls"
        sheet1 = Workbook.add_sheet("Log Validation")
        extracted_data.insert(0,('SL No', 'Application Name', 'Missing object', 'Missing Object Type', 'Missing Object referenced in'))
        #write value into excel sheet one by one
        style = xlwt.easyxf('pattern: pattern solid, fore_colour light_green;' 'font: colour black, bold True;')
        
        for i in range(len(extracted_data)):
            if i==0:
                sheet1.write(i, 0, extracted_data[i][0],style) 
            else:
                sheet1.write(i, 0, extracted_data[i][0])

        for i in range(len(extracted_data)):
            if i==0:
                sheet1.write(i, 1, extracted_data[i][1],style) 
            else:
                sheet1.write(i, 1, extracted_data[i][1])

        for i in range(len(extracted_data)):
            if i==0:
                sheet1.write(i, 2, extracted_data[i][2],style) 
            else:
                sheet1.write(i, 2, extracted_data[i][2])

        for i in range(len(extracted_data)):
            if i==0:
                sheet1.write(i, 3, extracted_data[i][3],style) 
            else:
                sheet1.write(i, 3, extracted_data[i][3])

        for i in range(len(extracted_data)):
            if i==0:
                sheet1.write(i, 4, extracted_data[i][4],style) 
            else:
                sheet1.write(i, 4, extracted_data[i][4])

        if os.path.exists(Log_Validation_Output):
            os.remove(Log_Validation_Output)
            Workbook.save(Log_Validation_Output)
            print(f"\nLog_Validation_Output.xls is generated and availavle inside "+out_put_path)
        else:
            Workbook.save(Log_Validation_Output)
            print(f"\nLog_Validation_Output.xls is generated and availavle inside "+out_put_path)

    except Exception as e:
        print("Some Exception Occured !\n Please resolve or contact developers.\n"+str(e))



while True:
    try:
        #taking source code path as input from the user.
        dirLoc=input(r'Enter the input folder path: ').strip()
        break
    except FileNotFoundError as e:
        print("Incorrect Path!  Please enter the correct path.\n")
    except IndexError as e:
        print("Source code does not exist!  Please copy your source code to - "+ dirLoc +"\n")
    except Exception as e:
        print("Some Exception Occured !\n Please resolve them or contact developers.\n"+str(e))

for subdir, dirs, files in os.walk(dirLoc):
    for file in files:
        if file.endswith('.csv'):
            file_name = file[:-4]
            log_validation(subdir+'\\'+file, file_name)

out_put_path = input('\nplease enter the path where you want to store the excel output file : ')

# dateTimeObj = datetime.now()
# file_suffix = dateTimeObj.strftime("%d-%b-%Y(%H.%M.%S.%f)")
write_into_excel(out_put_path)
