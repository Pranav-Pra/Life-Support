import pandas as pd

def get_hospital(filepath):
    df = pd.read_csv(filepath)

    # sort hospitals by closest
    df = df.sort_values('Distance (miles)')
    # dict for easy access
    hospital_dict = df.set_index('HospitalName').T.to_dict('list')

    df.set_index('HospitalName', inplace = True)

    return hospital_dict, df

def get_accident_types(filepath):
    df = pd.read_csv(filepath)
    accident_dict = df.set_index('Type').T.to_dict('list')
    df.set_index('Type', inplace = True)
    return accident_dict, df

'''
accident_requirements: type of accident and equipment/staff needed
patient_requirements: additional requirements selected by ambulance parademics
    ex: if pregnant and need obgyn then obgyn will be in this list
'''
def get_best_hospital(accident, hospital_df, accident_df, patient_requirements):
    # accident requirements + patient requirements
    requirements = accident_df.loc[accident, :]
    requirements = requirements[requirements>0].to_dict()
    patient_requirements.update(requirements)
    #print(patient_requirements)

    #hospitals = hospital_df.iloc[:, 0]
    check_next = 0
    for i in range(len(hospital_df.index)):
        hospital = hospital_df.iloc[[i]]
        #print(hospital.index[0])

        for req in patient_requirements:
            # check if requirements met
            if hospital[req][0] == 0:
                #print(req)
                check_next = 1
                break
        
        if (check_next):
            check_next = 0
            continue

        return hospital.index, 1
    
    # return closest if no hospitals meet requirements (change to be based on best fit in future)
    return (hospital_df.iloc[[0]]).index, 0
 
def main():
    hospital_dict, hospital_df = get_hospital("hospitals.csv")
    accident_dict, accident_df = get_accident_types("accident_types.csv")
    other_requirements = {'Ventilators': 1}
    result, is_best_fit = get_best_hospital('Overdose', hospital_df, accident_df, other_requirements)

    print(result[0], "is the best option")

# example
if __name__ == "__main__":
    main()
