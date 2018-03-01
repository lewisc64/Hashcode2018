
def get_distance(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

class Vehicle:
    
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
        self.started = False
        self.ride = None
        self.rides = []
        self.wait = 0
    
    def getXY(self):
        return [self.x, self.y]
    
    def add_ride(self, i):
        self.started = False
        self.ride = i
        self.rides.append(i)
    
    def can_do(self, ride, city):
        """ if a ride can 'make it' """
        
        distance_to_start = get_distance(self.getXY(), ride.start)
        ride_distance = ride.get_distance()
        if city.steps_taken + distance_to_start >= ride.earliest_start:
            if city.steps_taken + distance_to_start + ride_distance < ride.latest_finish:
                return True
        return False
    
    def move(self, city):
        if self.ride is not None:
            ride = city.rides[self.ride]
            if self.x == ride.start[0] and self.y == ride.start[1]:
                self.started = True
            if self.started:
                x, y = ride.start
            else:
                x, y = ride.finish
            if self.x < x:
                self.x += 1
            elif self.x > x:
                self.x -= 1
            elif self.y > y:
                self.y -= 1
            elif self.y < y:
                self.y += 1
            if self.x == ride.finish[0] and self.y == ride.finish[1]:
                self.ride = None
    

class Ride:
    
    def __init__(self, start, finish, earliest_start, latest_finish):
        self.start = start
        self.finish = finish
        self.earliest_start = earliest_start
        self.latest_finish = latest_finish
        self.assigned = False

    def get_distance(self):
        return get_distance(self.start, self.finish)
        
class City:
    
    #def __init__(self, rows, columns, n_vehicles, n_rides, bonus, steps):
    def __init__(self, path):
        
        self.vehicles = []
        self.rides = []
        
        #file = open(input("file (.in): ") + ".in", "r")
        file = open(path, "r")
        
        for i, line in enumerate(file.read().splitlines()):
            
            values = list(map(int, line.split()))
            
            if i == 0:
                self.rows, self.columns, self.n_vehicles, self.n_rides, self.bonus, self.steps = values
            else:
                start = values[0:2]
                finish = values[2:4]
                earliest_start = values[4]
                latest_finish = values[5]
                
                self.rides.append(Ride(start, finish, earliest_start, latest_finish))
            
        file.close()
        
        for x in range(self.n_vehicles):
            self.vehicles.append(Vehicle())
        #self.grid = [[None for y in range(self.rows)] for x in range(self.columns)]
        self.steps_taken = 0
        
        print("{} steps".format(self.steps))
        print("{} vehicles".format(self.n_vehicles))
        print("{} rides".format(self.n_rides))
    
    def output(self, path):
        print("outputting...")
        lines = []
        for vehicle in self.vehicles:
            lines.append("{} {}".format(len(vehicle.rides), " ".join(map(str, vehicle.rides))).strip())
        out = "\n".join(lines)
        file = open(path, "w")
        file.write(out)
        file.close()
        return out
        
    
    def simulate(self):
        print("simulating...")
        for step in range(self.steps):
            print("step {}".format(step))
            #for v_i, vehicle in enumerate(self.vehicles):
            for vehicle in self.vehicles:
                if vehicle.ride is None:
                    if vehicle.wait > 0:
                        vehicle.wait -= 1
                    else:
                        assigned = False
                        next_ride = self.columns + self.rows
                        for i, ride in enumerate(self.rides):
                            time = abs(ride.earliest_start - self.steps_taken)
                            if time < next_ride:
                                next_ride = time
                            if not ride.assigned and vehicle.can_do(ride, self):
                                assigned = True
                                #print(" assigning ride {} to vehicle {}".format(i, v_i + 1))
                                vehicle.add_ride(i)
                                ride.assigned = True
                                break
                        if not assigned:
                            #print("set wait to {}".format(next_ride))
                            vehicle.wait = next_ride
            
            for i, vehicle in enumerate(self.vehicles):
                #print(" vehicle {} is assigned to {}".format(i + 1, vehicle.ride))
                if vehicle.ride is not None:
                    vehicle.move(self)
            self.steps_taken += 1

name = "a_example"
name = "b_should_be_easy"  
name = "c_no_hurry"   
#name = "d_metropolis"
name = "e_high_bonus"            
city = City(name + ".in")
city.simulate()
print(city.output(name + ".out"))