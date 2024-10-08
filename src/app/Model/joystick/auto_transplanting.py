import time
from .joystick_mapper import JoystickMapper
import copy


class AutoTransplanting:
    
    def __init__(self,autonomus_plan):

        self.autonomus_plan = autonomus_plan
        self.num_of_parts = {1:3,2:2}
        # autonomus
        self.autonomus = 0
        #plan 1
        self.first_send = 1
        self.start_time = time.time()
        self.autonomus_list = []
        
        #plan 2
        self.current_pressure = 0.0
        self.pressure_at_prop = 0.0
        self.pressure_above_prop = 0.0 
        self.plan_part = 1   
        
        self.detected_square = 0 

    def increament(self):
        self.autonomus += 1
        self.autonomus %= self.num_of_parts[self.autonomus_plan]

        print(f'MODE : {self.autonomus}')
    
    def plan_1(self,values,signal):
        
        if self.autonomus == 1:
            # save values reversed
            rev_values = copy.deepcopy(values)

            for i in range(4):
                rev_values[i] = -1 * rev_values[i] if rev_values[i] else 0

            reversed_commands = str(JoystickMapper.map(rev_values))
            if len(self.autonomus_list) and self.autonomus_list[-1][0] == reversed_commands:
                self.autonomus_list[-1][1] = time.time() - self.start_time
            else:
                self.start_time = time.time()
                self.autonomus_list.append([reversed_commands, 0.0])

        elif self.autonomus == 2:
            # send saved values
            if len(self.autonomus_list) != 0:
                if self.first_send:
                    reversed_commands, _ = self.autonomus_list[-1]
                    signal.emit(
                        reversed_commands[1:len(reversed_commands) - 1].replace(", ", "").replace("'", "").encode())
                    self.first_send = 0
                    self.start_time = time.time()
                    
                if (time.time() - self.start_time >= self.autonomus_list[-1][1]):
                    self.autonomus_list.pop()
                    self.first_send = 1
            else:
                # open gripper
                print("arived at the desired position, opening the gripper")
                self.autonomus = 0


    def plan_2(self,signal):
        
        if self.autonomus == 1:  #Autonomus mode
            
            #part 1:keep ascending till we reach the required Pressure above the prop
            if self.plan_part == 1:
                if self.current_pressure < self.pressure_above_prop:
                    #self.send_commands("1550150015001500110O0S1",signal)
                    self.current_pressure += 1 
                    print("moving upward")                  
                elif self.current_pressure >= self.pressure_above_prop:
                    self.plan_part = 2
                    self.first_send = 1
            #part 2: keep moving forward and detecting squares till we find the square
            elif self.plan_part == 2:
                self.send_commands("1500150015501500110O0S1",signal)
                            
                '''
                    detect squaresssssssssssssssssssss from machineeee    
                '''       
                print("moving forward") 
                self.detected_square += 1
                if(self.detected_square >= 1000):
                    self.plan_part = 3
                    self.first_send = 1
            #part 3: The square is detected so we have to descend till we reach pressure at the red square
            elif self.plan_part == 3:
                if self.current_pressure > self.pressure_at_prop:
                    self.send_commands("1450150015001500110O0S1",signal)
                    self.current_pressure -= 1
                    print("moving down") 
                else:
                    self.send_commands("1500150015001500000O0S1",signal)
                    self.autonomus = 0    #return to normal mode
                    print("open gippers")
                
    def send_commands(self,command,signal):
        if self.first_send:
            signal.emit(command.encode())
            self.first_send = 0
                                   
    def do_plan(self,values,signal):
        if self.autonomus_plan == 1:
            self.plan_1(values,signal)
        elif self.autonomus_plan == 2:
            self.plan_2(signal)



