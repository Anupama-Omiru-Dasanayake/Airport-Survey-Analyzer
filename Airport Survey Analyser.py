"""
****************************************************************************
Additional info
 1. I declare that my work contins no examples of misconduct, such as
 plagiarism, or collusion.
 2. Any code taken from other sources is referenced within my code solution.
 3. Student ID: 21820566 & w2182056     
 4. IIT Student ID: 20241811
 5. Date: 19/11/2025
****************************************************************************
"""
#____________________________ My Modifications ____________________________________________

# 1.after generating a histogram programme will wait until user close the histogram window
# 2.Added some error handling codes (check graphhics.py module is imported or in the correct disctory)
# 3.Added error handling.- Check wheather csv module is imported or not. 
# 4.Added file closed title with the file name before prompt to open another file
# 5.Customizable histogram (including light mode and dark mode) but I did not prompt for user inputs. inside code can chnage themes easily.
# 6.According to the way I understood, everything need to be appended even the programme close and run again. There was no any mention for reset the results.txt when again run the programme from the begining
#   So I appended everything. no reseting for each programme run. since this programme is written for survey group to make informed decisions, I thought all the data from previous programme run's are also needed.
# 7. According to our Tutorial lecturer I have used shedualed departure time for calculations. and I have used a 12 hour filter even though sheduled departure time is in 12 hour range
#-------------------------------------------------------------------------------------------

# I put "from graphics import *" in try except becuase when I try run the file without graphics.py module in the same directory it gave me an error
# But It will not stop the programme until user entered a airline code to generate a histogram. then it will show an error and end the program. 

try:
    graphics_module_error = None
    from graphics import *

except ModuleNotFoundError:
    print("\nError: Please put this file in the same directory as Graphics.py module")
    print("Error: Histrogram will not work, To generate the histogram try again after fixing that")
    graphics_module_error = True

import csv
import math

data_list = []   # data_list An empty list to load and hold data from csv file


def load_csv(CSV_chosen):
    """
    This function loads any csv file by name (set by the variable 'selected_data_file') into the list "data_list" 
    YOU DO NOT NEED TO CHANGE THIS BLOCK OF CODE --  I changed a bit :))
    """
    global csv_error
    global empty_csv
    csv_error = False
    empty_csv = False

    try:
        with open(CSV_chosen, 'r') as file:
            csvreader = csv.reader(file)
            header = next(csvreader)
            for row in csvreader:
                data_list.append(row)
    except NameError:
        print("\n---! Error You havent imported the csv module !!\n")
        print("--- Try again after fixing that -----\n")
        csv_error = True

    except StopIteration:  # This errors came to me when i entered a completely empty csv file
        pass

    if csv_error == False and len(data_list) == 0:     # Here I checked wheter entered csv file is empty or not
        print("\nError!: Entered csv file is empty")
        empty_csv = True
    

#************************************************************************************************************

# ----- The Plan ----- Algorithm ----

# 1. Start
# 2. store valid airport and IAIA codes 
# 3. prompt to enter airport code that in valid airport codes
# 4. prompt to enter year betwween 2000 and 2025
# 5. selcet the file using airport code and year. eg - LHR2025
# 6. load the selceted csv file data in to a list called "data_list"
# 7. calculate the flight details using that "data_list" list
#     7.1 Print them in the IDLE 
#     7.2 open "results.txt" file and write them in append mode
# 8. take valid airline for generate the histogram from the user
# 9. Generate the histogram and wait untill user close the histogram window
# 10. prompt "Do you want to select new data file: "
#     10.1 If user entered Y or YES repeat  step 2 to step 8
#     10.2 If user entered N or NO Display "Thank you for using this programme" and stop the programme
# 11. Stop

#*************************************************************************************************************


# ************************************************* STORE AIRPORT & AIRLINE CODES **************************************************  
# ------ All the airport codes and names ----------------
airport_codes = {
        "LHR" : "London Heathrow",
        "MAD" : "Madrid Adolfo Suárez-Barajas",
        "CDG" : "Charles De Gaulle International",
        "IST" : "Istanbul Airport International",
        "AMS" : "Amsterdam Schiphol",
        "LIS" : "Lisbon Portela",
        "FRA" : "Frankfurt Main",
        "FCO" : "Rome Fiumicino",
        "MUC" : "Munich International",
        "BCN" : "Barcelona International"
        }

# ----------- All IATA codes and names  --------------
IATA_codes = {
    "BA" : "British Airways",
    "AF" : "Air France",
    "AY" : "Finnair",
    "KL" : "KLM",
    "SK" : "Scandinavian Airlines",
    "TP" : "TAP Air Portugal",
    "TK" : "Turkish Airlines",
    "W6" : "Wizz Air",
    "U2" : "easyJet",
    "FR" : "Ryanair",
    "A3" : "Aegean Airlines",
    "SN" : "Brussels Airlines",
    "EK" : "Emirates",
    "QR" : "Qatar Airways",
    "IB" : "Iberia",
    "LH" : "Lufthansa"

}

# First I used global variables for evry variables in function. But Later I changed it because when importing these functions as modules using global variables will not work

# ************************************************* TAKE INPUTS --- TASK A **************************************************
def take_airport_code(): 
     """This function get airport code from the user and check its validity, if not valid show error message"""
    #  global airport_code
     first_prompt = True
     try:
        while True:
            if first_prompt == True:
                airport_code = input("\n\nPlease enter a three-letter Airport Code: ").strip().upper() # strip() ignore empty spaces from left and right
                
            elif len(airport_code) != 3:
                airport_code = input("\nWrong code lenght - Please enter a three-letter Airport Code: ").strip().upper() #upper() take evrething in capital
            elif not airport_code in airport_codes:
                airport_code = input("\nUnavailable city code - Please enter a valid Airport Code: ").strip().upper()
            elif len(airport_code) == 3 and airport_code in airport_codes:
                break  #exit the loop and return the entered airport code
            first_prompt = False
     except Exception as e:
         print("\nError: An error occured while taking Airport Code !",e)
     return airport_code


def take_year():
    """This function check if the year is valid or not and once valid year is entered return it"""
    # global year
    first_prompt = True

    try:

        while True:
            if first_prompt == True:
                year = input("\nPlease enter the year required in the format YYYY: ").strip()
                
            elif not(year.isdigit()): # .isdidgit() is used to check whether a string is containing a digit or not
                year = input("\nWrong data type - Please enter a four-digit year value: ").strip()
            elif year.isdigit():
                year = int(year)
                if not(year >= 2000 and year <= 2025):
                    year = input("\nOut of range - Please enter a year from 2000 to 2025: ").strip()
                elif year >= 2000 and year <= 2025:
                    year = str(year)  
                    break
            first_prompt = False
    except Exception as e:
        print("\nError: An error occured while taking the Year !", e)

    return year


def take_histogram_airline():
    """This function get the airline for generate the histogram"""
    # global histogram_airline
    first_prompt = True
    try:

        while True:
            if first_prompt == True:
                histogram_airline = input("Enter a two-character Airline code to plot a histogram: ").strip().upper()
            if histogram_airline not in IATA_codes:
                histogram_airline = input("\nUnavailable Airline code, Please try again: ").strip().upper()
            if histogram_airline in IATA_codes:
                break
            first_prompt = False
    except Exception as e:
        print("\nError: An error occured while taking Histogram Airline !",e)
    
    return histogram_airline
        

# ************************************************* CALCULATE FLIGHT DETAILS -- TASK B **************************************************
def flight_details(airport_code):
    """This function calculate all the required flight details"""
    # -- First make all the variables global --- (its easy than returning all of these) but then I remmbered it's not a good way when these functions imported from another programme
    # global total_flights
    # global departing_terminal_two
    # global departures_under_600
    # global air_france_flights
    # global departing_below_15d
    # global aver_british_per_hour
    # global british_departur_percentage
    # global delayed_air_france
    # global total_hours_rain
    # global least_common_destinations


    # ---- Create all the variables and assign them ---
    total_flights = 0
    departing_terminal_two = 0
    departures_under_600 = 0
    air_france_flights = 0
    departing_below_15d = 0
    aver_british_per_hour = 0
    british_departur_percentage = 0
    delayed_air_france = 0
    total_hours_rain = 0
    allready_counted = []
    air_france = 0
    all_airports = list(airport_codes.keys())
    all_airports.remove(airport_code)
    destination_counts = [] 
    least_common_destinations = []
    airport_count = 0
    done = False

    try:
    # -- Loops through all the flights in the csv file (data_list variable)
        for flight in range(len(data_list)):
            # -- Filter out only the 12 hour period 00:00 to 11:59 -- This filter is not required --- But I added because Tut Lecturer said it would be good
            if int(data_list[flight][2][:2]) <= 11 and int(data_list[flight][2][3:]) <= 59: #<<< ------- For ME -- Come here to change hours ----------- >>>

                # Total flights
                total_flights += 1
        
                # -- flights departing terminal two
                if data_list[flight][-3] == "2":
                    departing_terminal_two += 1

                # --- flights departing under 600 miles
                if int(data_list[flight][-6]) < 600:
                    departures_under_600 += 1

                # --- departres flights by AirFrance flights ---
                if data_list[flight][1][:2] == "AF":
                    air_france_flights += 1
        
                # --- flights departing in temp below 15 celcias
                # Here I have done something unique again 
                # I checked the temperature whether it's minus celsias or positive. 
                # This code can check up to -999 celcias and positive 1000 Celsias


                not_four_digit = False
                not_three_digit = False
                not_two_digit = False
                
                try:
                    degrees = int(data_list[flight][-1][:4])     # Here I have check if the temperature is 4 digit number
                except ValueError:
                    not_four_digit = True

                if not_four_digit == True:   # Here I have checked for 3 digit number if not 4 digit number
                    try:
                        degrees = int(data_list[flight][-1][:3])  
                    except ValueError:
                        not_three_digit = True

                    if not_three_digit == True:    # Here I have checked for 2 digit number if not 3 digit number
                        try:
                            degrees = int(data_list[flight][-1][:2])  
                        except ValueError:
                            not_two_digit = True

                    if not_two_digit == True:  # Here I have checked for one digit number if not 2 digit number
                        try:
                            degrees = int(data_list[flight][-1][:1]) 
                        except ValueError:
                            degrees = 0    # IF not one digit either I have assigned degree as 0 

                if int(degrees) < 15:   
                    departing_below_15d += 1
        
                # ---- british airways departures per hour 
                if data_list[flight][1][:2] == "BA":
                    aver_british_per_hour += 1
    

                # --- total departures british airways aircrafts
                if data_list[flight][1][:2] == "BA":
                    british_departur_percentage += 1
        

                # --- air france fights with delayed departure
                if data_list[flight][1][:2] == "AF":
                    air_france += 1
                    covert_to_minits_sheduled = int(data_list[flight][2][:2])*60 + int(data_list[flight][2][3:])
                    convert_to_minits_actual = int(data_list[flight][3][:2])*60 + int(data_list[flight][3][3:])
                    if convert_to_minits_actual > covert_to_minits_sheduled:  
                        delayed_air_france += 1
        

                # -- This calculate total number of hours of rain
                # select the last column (weather condition column)
                if data_list[flight][-1]:
                    # take weather condition all the words (heavy rain, rain ect)
                    weather = str(data_list[flight][-1]).lower().split(" ")
                    # take the hour
                    hour = data_list[flight][2][:2]
                    
                    # if word "rain" exist in anywhere doesnt matter heavy or normal rain, and that hour is not already counted , count one
                    if "rain" in weather and hour not in allready_counted: 
                        total_hours_rain += 1
                        # and append that hour to the allready counted list
                        allready_counted.append(hour)

        # -- This calculate the all the destination counts for each airport and append them with the airport name, and the count to a another list
        for i in range(len(all_airports)):
            # reset the count for every new airport
            airport_count = 0
            # check all the data_list for each airport 
            for flight in range(len(data_list)):
                # filter only for 00:00 to 12:00
                if int(data_list[flight][2][:2]) <= 11 and int(data_list[flight][2][3:]) <= 59:
                    if all_airports[i] == data_list[flight][4]:
                        airport_count += 1 
            if airport_count >= 1:
                destination_counts.append([airport_count,all_airports[i]]) 

        # This will sort all the airport counts minimum to maximum 
        # Even though it's not possiable to not to have any destination . But I have checked it
        if len(destination_counts) == 0:
            least_common_destinations = ["No destinations"] # If no any destinations display this
        else:
            destination_counts.sort() 
            # I assigned that variable to new variable called sorted 
            all_destinations_sorted = destination_counts 
            # append only the least count airport code to the least_common_destination list
            least_common_destinations.append(airport_codes[all_destinations_sorted[0][1]]) 
            

            # but if there are more distinations with the same count check it and append them too
            for i in range(1,len(all_destinations_sorted)-1):
                    if all_destinations_sorted[0][0] == all_destinations_sorted[i][0]: 
                        least_common_destinations.append(airport_codes[all_destinations_sorted[i][1]])
        

        # --- Average british departures per hour (rounded to two decimals)
        aver_british_per_hour = round(aver_british_per_hour/12,2)

        # -- british airways aircraft percentage
        british_departur_percentage = round(british_departur_percentage/total_flights*100,2)

        # -- percentage of delayed air france departures
        if air_france == 0:
            delayed_air_france = round(0,2)
        else:
            delayed_air_france = round(delayed_air_france/air_france*100,2)
    
        return total_flights, departing_terminal_two, departures_under_600, air_france_flights, departing_below_15d, aver_british_per_hour, british_departur_percentage, delayed_air_france,total_hours_rain,  least_common_destinations 
    
    except Exception as e:
        print("\nError!: An error occured while calculating required details ! [Location - def flight_details()]")
        print(f"Error!: {e}")

    
          

# ************************************************* PRINT & WRITE FLIGHT DETAILS --- TASK B  & TASK C **************************************************
# Here I have done something unique :) by using same function to write and print the details. 
# I put the keyword as a parameter, so I can change the keyword as I want when I call the function

def details(selected_title,total_flights , departing_terminal_two, departures_under_600, air_france_flights, departing_below_15d, aver_british_per_hour, british_departur_percentage, delayed_air_france,total_hours_rain,  least_common_destinations,key_word,new_line=""):
    """This function print and write all the airport details requested depending on the "key_word" parameters"""
    # I used variable called "new_line" to control writing lines and printing lines separately. for printing no need extra "\n" but for writing it requires to go to the next line
    try: 
        print()
        key_word(f"{selected_title}{new_line}")
        key_word(f"The total number of flights from this airport was {total_flights}{new_line}")
        key_word(f"The total number of flights departing Terminal Two was {departing_terminal_two}{new_line}")
        key_word(f"The total number of departing on flights under 600 miles was {departures_under_600}{new_line}")
        key_word(f"There were {air_france_flights} Air France flights from this airport{new_line}")
        key_word(f"There were {departing_below_15d} flights departing in temperatures below 15 degrees{new_line}")
        key_word(f"There was an average of {aver_british_per_hour} British Airways flights per hour from this airport{new_line}")
        key_word(f"British Airways planes made up {british_departur_percentage}% of all departures{new_line}")
        key_word(f"{delayed_air_france}% of Air France departures were delayed{new_line}")
        key_word(f"There were {total_hours_rain} hours which rain fell{new_line}")
        if len(least_common_destinations) == 1:
            key_word(f"The least common destination is {least_common_destinations}{new_line}{new_line}")
        else:
            key_word(f"The least common destinations are {least_common_destinations}{new_line}{new_line}")

    except Exception as e:
        print("\nError: An error occured while printing or writing required details !",e)


# ************************************************* GENERATE THE HISTOGRAM --- TASK D **************************************************
def histogram(histogram_airline,airport_code, year):
    """This function generate the histogram that shows total number of departing flights for the selected airline, for each hour of the twelve-hour survey"""
    
    try:

        # ------ Histogram Theme customizations ------------
        # By changing the theme_color variable I can change the theme of the hostogram easily 

        theme_color = "black"
        
        if theme_color.lower() == f"black" or theme_color.lower() == "dark" :
            arrow_color = "white"
            background_colour = f"black"
            text_colour = f"white"
            line_colour = f"white"
            text_font = f"helvetica"
            main_title_text = f"bold"
            bar_colour = f"{color_rgb(2, 208, 115)}"
            outline_color = f"black"
            line_width = 2

        elif theme_color.lower() == f"white" or theme_color.lower() == "light":
            arrow_color = "black"
            background_colour = f"white"
            text_colour = f"black"
            line_colour = f"black"
            text_font = f"helvetica"
            main_title_text = f"bold"
            bar_colour = f"{color_rgb(50, 102, 204)}"
            outline_color = f"black"
            line_width = 2

        # Create the window 
        window_width = 1300
        window_height = 900
        win = GraphWin(f"Histogram - {airport_code}{year}.csv - {histogram_airline}", window_width, window_height, autoflush=False ) # Here I set autoflush=False This will stop automatically drawing everthing until I update using win.update()
        
        win.setBackground(background_colour)

        # Add the grapgh main title
        title = f"Departures by hour for {IATA_codes[histogram_airline]} from {airport_codes[airport_code]} {year}"
        main_title = Text(Point(window_width/2,40),title)

        # make title fonts responsive according the title lenth
        if len(title) > 150: 
            main_title.setSize(13)
        else:
            main_title.setSize(16)

        main_title.setStyle(main_title_text)
        main_title.setTextColor(text_colour)
        main_title.setFace(text_font)
        main_title.draw(win)

        # A line after the main title
        line_title = Line(Point(0,80),Point(window_width,80))
        line_title.setFill(line_colour)
        line_title.draw(win)


        # ------------------------- Y Axsis ------------------------------

        # create the y axis line 
        y_line = Line(Point(150,150), Point(150,800))
        y_line.setFill(line_colour)
        y_line.setWidth(line_width)
        y_line.draw(win)


        # Y line tags (00 to 11)
        # Possiable working values for 
        #  start = 11 or 0
        #  end = -1 or 12
        #  step = -1 or 1
        # for reverse order = start = 0 , end = 12, step = 1
        start,end,step = 11,-1,-1
        tag_down_by_space = 201

        # Here I tried to make the bar graph responsive as possiable just by changing the start,end, and step variable values I can now change the order of display of bars 00 to 11 OR 11 to 00
        for i in range(start,end,step):
            if i == start:
                tag = Text(Point(132,tag_down_by_space),f"{i:02}")
                tag.setFace(text_font)
                tag.setStyle("bold")
                tag.setTextColor(text_colour)
                tag.draw(win)
            elif start == 0:
                if i > start:
                    tag = Text(Point(132,tag_down_by_space+51),f"{i:02}")  # Hear add bar height you choose to this y value
                    tag_down_by_space += 51
                    tag.setFace(text_font)
                    tag.setStyle("bold")
                    tag.setTextColor(text_colour)
                    tag.draw(win)
            elif start == 11:
                if i < start:
                    tag = Text(Point(132,tag_down_by_space+51),f"{i:02}")  # Hear add bar height you choose to this y value
                    tag_down_by_space += 51
                    tag.setFace(text_font)
                    tag.setStyle("bold")
                    tag.setTextColor(text_colour)
                    tag.draw(win)


        # Create the y Axixs Arrow head
        y_arrow = Polygon(Point(145,150),Point(155,150),Point(150,140))
        y_arrow.setFill(arrow_color)
        y_arrow.draw(win)

        # Add y axsis title
        y_title = Text(Point(70,475),"Hours\n00 to 12")
        y_title.setStyle("bold")
        y_title.setSize(11)
        y_title.setFace(text_font)
        y_title.setTextColor(text_colour)
        y_title.draw(win)

        # Box around y line title
        a_box_y_title = Rectangle(Point(30,445),Point(110,505))
        a_box_y_title.setOutline(line_colour)
        a_box_y_title.draw(win)  



        # ----------------------- X Axsis -------------------------

        # Create the x axis Line
        # x line contoller
        x_line_start = 150
        x_line_stop = 1250
        middle_of_xline = ((x_line_stop - x_line_start)/2) + x_line_start

        x_line = Line(Point(x_line_start,800),Point(x_line_stop,800))
        x_line.setFill(line_colour)
        x_line.setWidth(line_width)
        x_line.draw(win)

        # Create the x Axis arrow head
        x_arrow = Polygon(Point(x_line_stop,795),Point(x_line_stop,805),Point(1259,800))
        x_arrow.setFill(arrow_color)
        x_arrow.draw(win)

        # Add the x Axsis Title
        # take middle of x line to show the name of the x line
        x_title_name = "Number of Departures"
        x_title = Text(Point(middle_of_xline,850),x_title_name)
        x_title.setStyle("bold")
        x_title.setFace(text_font)
        x_title.setTextColor(text_colour)
        x_title.draw(win)

        # legend color 
        legend = Rectangle(Point(middle_of_xline-120,838),Point(middle_of_xline-100,858))
        legend.setFill(bar_colour)
        legend.setOutline(outline_color)
        legend.draw(win)

        box_x_title = Rectangle(Point(middle_of_xline-120-30,820),Point(middle_of_xline+110,875))
        box_x_title.setOutline(line_colour)
        box_x_title.draw(win)

        # ---------------------- Create Bars ------------------------------------------ 

        # Create bars 
        bar_height = 40
        bar_fixed_width = 150   #150 is the minimam value      
        space_between = 11
            
        number_of_departures = []
        number_of_departures.clear()
        hours = []
        all_hours = []

        # Take hours from 00 to 11 and append them to a list
        for i in range(12):
            hours.append(f"{i:02}") # formatted as two digits if only one digit add one zero to front

        # Take all the hours with in 00 to 11:59 that are similiar to user entered histogram airline  <<< ------- For ME -- Come here to change hours ----------- >>>
        for flight in range(len(data_list)):
            if int(data_list[flight][2][:2]) <= 11 and int(data_list[flight][2][3:]) <= 59:
                if data_list[flight][1][:2] == histogram_airline:   # get all the hours that are similiar to user entered airline
                    all_hours.append(data_list[flight][2][:2])

        all_hours.sort() # Sort all the hours in ascending order smaller to largest.
        
        # I have linked this to "change_order" variable from above so I can easily change the order
        for i in range(start,end,step):
            number_of_departures.append(all_hours.count(f"{i:02}")) # count how many times each hour in the "all_hours" list. and use formated string for i to get 0 when there is only one digit

            # eg - if [00,00,01,03,03,04,04,05,06,07,08,08,09,11] 
            # it will append each hour how many times appear in the list starting with 11, because I change the order not it shows 00 to 11 
            # eg - number_of_departues - [2,1,0,2,2,1,1,1,2,1,0,1] this way if the for loop range(0,12)
            #                             [1,0,1,2,1,1,1,2,2,0,1,2] This way now for loop change (-11,-1,-1)
            
            
        # Creating the responsive One Unit Marks in x Axsis --- Calculate the one point value 
        max_display_width = 1050
        copy_of_number_of_departues = number_of_departures.copy()      
        copy_of_number_of_departues.sort(reverse=True) # Sort them in Descending order
        highest_no = copy_of_number_of_departues[0]

        if highest_no == 0:  # Here I checked wether highest_no is 0 or not. because if zero it will casue ZeroDivisionError 
            one_point_value = 0
        else:
            one_point_value = max_display_width/highest_no

        # ---------------------------------------------
        
        # --- This code creates marks for each point in x axsis. I commented it - This marks becomes ugly when have too many data  --- but I kept the code :))
        # count = 1
        # while True:
        #     mark = Line(Point(150+count*one_point_value,797),Point(150+count*one_point_value,803))
        #     mark.setFill(line_colour)
        #     mark.setWidth(line_width)
        #     mark.draw(win)
        #     stop_mark = int(count*one_point_value)
        #     if stop_mark == max_display_width:
        #         break
        #     count+=1
        # ----------------------------------
            
        # --- Creating all the bars according to the OnePoint Value ---
        for i in range(0,12):
            one_bar = Rectangle(Point(150,180+i*bar_height+i*space_between), Point(150+one_point_value*number_of_departures[i], 180+i*space_between+(i+1)*bar_height))
            one_bar.setFill(bar_colour)
            one_bar.setOutline(outline_color)
            one_bar.setWidth(line_width)
            one_bar.draw(win)
        
            # This will create the bar tag infront of the bar 
            a_bar_tag = Text(Point(155+one_point_value*number_of_departures[i]+15,176+i*space_between+(i+1)*bar_height-15),f"{number_of_departures[i]}")
            a_bar_tag.setSize(11)
            a_bar_tag.setStyle("bold")
            a_bar_tag.setFace(text_font)
            a_bar_tag.setTextColor(text_colour)
            a_bar_tag.draw(win)
        
        # I just draw the Y line again because after creating the bars there are some gaps beacuse I matched the bar outline as same the bar colour.
        y_line = Line(Point(150,150), Point(150,800))
        y_line.setFill(line_colour)
        y_line.setWidth(line_width)
        y_line.draw(win)
        #---------------------------------------

        # ---- Extra design for user attraction Airplane Design ----
        # plane_body = Polygon(Point(860,840),Point(890,865),Point(990,820),Point(1010,830),Point(900,880),Point(865,870))
        # plane_body.draw(win)
        # plane_body.setFill("black")
        # plane = Polygon(Point(895,810),Point(900,840),Point(920,850),Point(960,850))
        # plane.setFill("black")
        # plane.draw(win)
        # --- I commented it, It feels like ugly ---
                
        # What I have done here is I pause the programme untill user close the histogram window to prompt to enter select new csv file
        win.update()
        print("\nSuccesfuly generated the Histogram !!\n")
        print("Close the histogram window to continue.")
        first_prompt = True 

        # I tried not to close the window to open new file but it juts crash in IDLE the windows keep Freezing. So I had no choice but to pause the program until user close it maualy.
        # This is how I did it. 
        while True:
            try:
                win.getMouse()
                if first_prompt == True:  
                    print("Waiting . . . . ")
                    first_prompt = False
            except:    # GrpahicsError comes when the window is closed manualy with having win.getMouse(). Here I did not catched the GraphicsError right away beacuse I want to display the file closed message by catching the GraphicsError from the down
                raise GraphicsError              # So I raised the GraphicsError  
            if GraphicsError == True:
                break
        
    except NameError as e:
        print(f"\n---!Error: Look like you haven't imported the Graphis.py module OR---")
        print("---!Error: Please put this file in the same directary as the Graphics.py module OR---")
        print(f"---!Error: {e}")
        print("! ------ Try Again after fixxing that --------- !\n")
    
    except GraphicsError: # Here I catch the GraphicsError raised earlier
        close_msg = f"File {airport_code}{year}.csv & Histogram closed."
        starline = "*"* len(close_msg)
        print(f"\n{starline}\n{close_msg}\n{starline}")
    
    except Exception as e:
        print("\nError: !",e)
    

# ************************************************* THE MAIN CODE **************************************************
def main():
    """This is the main function. This function contains the main code, inside this call functions"""

    # ---- TASK E ----- Looping until user enter N or No to open new data file prompt
    new_file =True 
    while new_file == True:
        airport_code = take_airport_code()
        year = take_year()
        
        file_found = None
        try:
            data_list.clear()
            selected_csv_file = f"{airport_code}{year}.csv"
            load_csv(selected_csv_file)
            selected_message = f"File {airport_code}{year}.csv selected - {airport_codes[airport_code]} {year}"
            starline = "*"* len(selected_message)
            selected_title = f"{starline}\n{selected_message}\n{starline}"
            file_found = True

        # If file not found print the error
        except FileNotFoundError:
            print(f"\nError!: File Not Found")

        # if accedentaly csv module not imported or that code is removed stop the programme
        if csv_error == True:
            break
        
        # if file is found succesfully and csv file is not empty and csv module is imported
        if file_found == True and csv_error == False and empty_csv == False:
            
            # Store all the flight details from the flight details function returns
            total_flights , departing_terminal_two, departures_under_600, air_france_flights, departing_below_15d, aver_british_per_hour, british_departur_percentage, delayed_air_france,total_hours_rain,  least_common_destinations = flight_details(airport_code)

            # Fist call the details functions using "print" keyword to print all the details in the IDLE
            details(selected_title,total_flights , departing_terminal_two, departures_under_600, air_france_flights, departing_below_15d, aver_british_per_hour, british_departur_percentage, delayed_air_france,total_hours_rain,  least_common_destinations,key_word=print)

            # According to the way I understood, everything need to be appended even the programme close and run again. There was no any mention for earse results.txt when again run the programme from the begining
            # So I appended everything. no reseting for each programme run. 
            current_results_file = open("results.txt","a")
            details(selected_title,total_flights , departing_terminal_two, departures_under_600, air_france_flights, departing_below_15d, aver_british_per_hour, british_departur_percentage, delayed_air_france,total_hours_rain,  least_common_destinations,key_word=current_results_file.write,new_line="\n")
            current_results_file.close()

            # Call the take_histogram_airline and store that function resturn value to a variable
            histogram_airline = take_histogram_airline()
            # Call the Histogram function with three arguments
            histogram(histogram_airline,airport_code, year)  # This could also write like this - histogram(take_histogram_airline(),airport_code, year) both do the same thing

        # if graphics.py module is not imported or The programme is not in the same directory as the graphics.py module stop the programme showing error msg
            if graphics_module_error == True:
                break

        # Ask for select a new data file 
        while True:
            new_file = input("\n\nDo you want to select a new data file? Y/N: ").strip().upper()
            if new_file in ["Y","YES"]:
                data_list.clear()
                new_file = True
                
                break
            elif new_file in ["N","NO"]:
                new_file = False
                print(f"\n-- Thank you for using this programme --\n")
                break
            else:
                print("Error!: Please enter YES or NO (Y/N)")


# ************************************************* CALL THE MAIN FUNCTION **************************************************
# if the file run is the main file run main function. if this file is imported as a module this will not work
if __name__ == "__main__":

    # ---- This code is written if the coursework is expecting to erase previous run written data for each new programme run (not the loop csv file open). to show that I know how to do that as well :)) ----
    # current_results_file = open("results.txt","w")
    # current_results_file.write("")
    # current_results_file.close()

    main()

#****************** End of the program ***************#
#  ___________________________________________________
# |                                                   |
# |  Developed By :- ©Anupama Omiru | @mr.dasanayake  |
# |  Contact      :- anupama.20241811@iit.ac.lk       |
# |___________________________________________________|
#
#*****************************************************#

    





    




