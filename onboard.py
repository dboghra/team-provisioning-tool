from validate_data import validate_csv



#load .env
#load config file(represents each team)

#validate config data
valid_rows, error_rows = validate_csv("config.csv")


#call provisioner to create repo and add members

