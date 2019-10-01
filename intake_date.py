import datetime
import pandas as pd

#intake details
intake = {'09/12/2019': 9500, '09/13/2019': 9800, '09/14/2019': 9700}

#output details
output = {'09/12/2019': 2000, '09/13/2019': 9000, '09/14/2019': 3000, '09/15/2019': 900, '09/16/2019': 800, '09/17/2019': 9000, '09/20/2019': 4300}

min_intake_date_value = 1
min_output_date_value = 1
prod_plan = pd.DataFrame()

while min_intake_date_value>0:

    try:
        #get the min intake date with stone count > 0
        min_intake_date = min([datetime.datetime.strptime(date, "%m/%d/%Y") for date, value in intake.items() if value > 0])
        min_intake_date_st= min_intake_date.strftime("%m/%d/%Y")
        #the value of the min intake date
        min_intake_date_value = intake[min_intake_date_st]
        print("Intake Date: {} and intake value: {}" .format(min_intake_date, min_intake_date_value ))
        print(intake)
    except ValueError:
        print('All of planned intake has been plotted')
        print(intake)
        break
        
    try:
        #get the min output date with stone count > 0 and also if the output date is greater than or equal to the min intake date
        min_output_date = min([datetime.datetime.strptime(date, "%m/%d/%Y") for date, value in output.items() if value > 0 and datetime.datetime.strptime(date, "%m/%d/%Y") >= min_intake_date])
        min_output_date_st = min_output_date.strftime("%m/%d/%Y")
        #the value of the min output date
        min_output_date_value = output[min_output_date_st]
        print("Output Date: {} and Output value: {}" .format(min_output_date, min_output_date_value) )
        print(output)
    except ValueError:
        print('Planned Output is insufficient for the intake plan')
        print(output)
        break

    new_output_value = min(min_intake_date_value, min_output_date_value)
    print("New Output Number: {}" .format(new_output_value))
    intake[min_intake_date_st] = min_intake_date_value - new_output_value
    output[min_output_date_st] = min_output_date_value - new_output_value
    prod_plan = prod_plan.append({'intake_date': min_intake_date, 'output_date': min_output_date, 'stone_count': new_output_value}, ignore_index=True)
    print(prod_plan)
  