import os
import xlwt
import logging

extracted_data_dot_net_0142=[]
extracted_data_dot_net_0142_to_remove_duplicates=[]
extracted_data_dot_net_0038=[]
count = 1

def log_validation_for_dot_net(dot_csv_file, file_name):
    try:
        logging.basicConfig(filename="Log_Validation_for_dot_net_logs.txt", level=logging.INFO, format="%(asctime)s %(message)s")

        logging.info('-----------------------------------------------------------------------------------------------------------------------------------------------')
        logging.info(file_name+'\n')
        #extrating http pattern using regex
        with open(dot_csv_file, 'r') as f:
            lines = f.readlines()
            for line in lines:
                global count

                if line.lower().strip().startswith('dotnet.0142'):

                    app_name = file_name

                    # print(line)
                    # print()

                    line = line.strip()[49:]
                    missing_object_index = line.find(' ')
                    missing_object = line[:missing_object_index]
                    # print(missing_object)
                    # print()
                    if ('test' in missing_object.lower()) or ('microsoft' in missing_object.lower()) or ('system' in missing_object.lower()):
                        continue

                    line = line[missing_object_index+9:]
                    version_index = line.find(' ')
                    version = line[:version_index]
                    # print(version)
                    # print()

                    missing_object_type = 'nuget package'

                    line = line[version_index+48:]
                    missing_object_referenced = line[:-17]
                    # print(missing_object_referenced)

                    
                    if (missing_object, version) not in extracted_data_dot_net_0142_to_remove_duplicates:
                        extracted_data_dot_net_0142_to_remove_duplicates.append((missing_object, version))

                        extracted_data_dot_net_0142.append([count, app_name, missing_object, version, missing_object_type, missing_object_referenced])
                        count += 1

                if line.lower().strip().startswith('"dotnet.0038'):

                    app_name = file_name

                    # print(line)
                    # print()

                    line = line.strip()[24:]
                    missing_object_index = line.find('not found for project')
                    missing_object = line[:missing_object_index]
                    # print(missing_object)

                    version = 'NA'

                    missing_object_type = 'PROJECT'

                    # print()
                    # print(line)
                    # print()
                    missing_object_referenced_index = line.lower().find('the analysis results may be incomplete.')
                    missing_object_referenced = line[missing_object_index+22 : missing_object_referenced_index]
                    # print(missing_object_referenced)

                    extracted_data_dot_net_0038.append([count, app_name, missing_object, version, missing_object_type, missing_object_referenced])
                    count += 1



    except Exception as e:
        print("Some Exception Occured !\n Please resolve or contact developers.\n"+str(e))

def remove_nested_duplicates(input_list):
    unique_list = []

    for sublist in input_list:
        if sublist not in unique_list:
            unique_list.append(sublist)

    return unique_list

def write_into_excel(out_put_path, extracted_data):

    try:
        Workbook = xlwt.Workbook()
        Log_Validation_Output = out_put_path+"\Log_Validation_Output.xls"
        sheet1 = Workbook.add_sheet("Log Validation")
        extracted_data.insert(0,('SL No', 'Application Name', 'Missing object', 'Version', 'Missing Object Type', 'Missing Object referenced in'))
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

        for i in range(len(extracted_data)):
            if i==0:
                sheet1.write(i, 5, extracted_data[i][5],style) 
            else:
                sheet1.write(i, 5, extracted_data[i][5])

        if os.path.exists(Log_Validation_Output):
            os.remove(Log_Validation_Output)
            Workbook.save(Log_Validation_Output)
            print(f"\nLog_Validation_for_dot_net_Output.xls is generated and availavle inside "+out_put_path)
        else:
            Workbook.save(Log_Validation_Output)
            print(f"\nLog_Validation_for_dot_net_Output.xls is generated and availavle inside "+out_put_path)

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
            log_validation_for_dot_net(subdir+'\\'+file, file_name)

out_put_path = input('\nplease enter the path where you want to store the excel output file : ')

extracted_data_dot_net_0142 = remove_nested_duplicates(extracted_data_dot_net_0142)

extracted_data=extracted_data_dot_net_0038 + extracted_data_dot_net_0142
write_into_excel(out_put_path, extracted_data)