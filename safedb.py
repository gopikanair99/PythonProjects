import sqlite3
import base64
import imageio
import cv2

#setting password for the safe
PASSWORD="gopika999"

connt=input("Enter your password for the safe!: ")

while connt != PASSWORD :
    connt=input("Please enter your password again! ")
    #if you want to quit 
    if connt=='q':
        break
    
if connt == PASSWORD:
    conn=sqlite3.connect('mysafe.db') #creating database that is mysafe
    try: #will create a database if no database is there
        conn.execute('''CREATE TABLE SAFE
                     (FULL_NAME TEXT PRIMARY KEY NOT NULL,
                     NAME TEXT NOT NULL,
                     EXTENSION TEXT NOT NULL
                     FILES TEXT NOT NULL);''') # Creating the safe database
        print("Your safe has been created now!!")
    except:
        print("Your safe is already created1 what would you like to do? ") # since its already created 
        
    while True:
        print("\n"+ "*"*15)
        print("Select from the commands on what you would like to do : ")
        print("q-> quit!")
        print("o-> open a file")
        print("s-> store a file")
        print("+"*15)
        your_choice=input(":")
        
        if your_choice=='q':
            break #exits 
        
        if your_choice=='o':
            #open the required file
            file_name=input("Enter your file name please : \n")
            file_type=input("Enter the extension type of your file: \n")
            FILE_=filename +"."+ file_type #format of the file
            cursor=conn.execute("SELECT * FROM SAFE WHERE FULL_NAME=" + '"' + FILE_ + '"' )
            file_string=""
            for row in cursor:
                file_string=row[3] #records name of the file that is FILE_
            with open(FILE_,'wb') as f_output:
                print(file_string)
                f_output.write(base64.b64decode(file_string)) #decodes the filename to binary
                
        if your_choice=='s':
            #store your file 
            PATH=input("Enter the path of the file that you want to store: \n")
            FILE_TYPES= {
                "txt":"TEXT",
                "java":"TEXT",
                "py":"TEXT",
                "doc":"TEXT",
                "jpg":"IMAGE",
                "png":"IMAGE",
                "jpeg":"IMAGE"
            }
            
            file_name=PATH.split('/') # splits the path by / and stores in a tuple
            file_name=file_name[len(file_name)-1]
            file_string=""
            
            NAME=file_name.split(".")[0]
            EXTENSION=file_name.split(".")[1]
            
            try:
                EXTENSION=FILE_TYPES[EXTENSION]
            except:
                Exception()
                
                
            if EXTENSION=="IMAGE":
                IMAGE=cv2.imread(PATH)
                file_string=base64.b64encode(cv2.imencode('.jpg',IMAGE)[1]).decode()
                
            elif EXTENSION=="TEXT":
                file_string=open(PATH,'r').read()      
                file_string=base64.b64encode(file_string)
                
            EXTENSION=file_name.split(".")
            
            command='INSER INTO SAFE (FULL_NAME,NAME,EXTENSION,FILES) VALUES (%S,%S,%S,%S);' %('"' + file_name +'"', '"' + NAME +'"', '"' + EXTENSION +'"', '"' + file_string +'"')
            conn.execute(command)
            conn.commit()
            
                 
                
            
            
    