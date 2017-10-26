"""

     Base class for any vehicle model we implement


"""
import numpy as np

class MobileModel(object):
    def __init__(self, uid, name, num_config_dimensions,num_control_dimensions):
        """
        Initializer function

        :param uid: the unique id of this model
        :param name: the name of this modeltype
        :param num_config_dimensions: number of configuration dimensions
        :param num_control_dimensions: number of controllable dimensions
        :return:
        """
        # set the name and ID of this entity
        self.name= name
        self.id = uid

        # setup the arrays for config and control
        self.config = np.zeros(num_config_dimensions)
        self.control = np.zeros(num_control_dimensions)

        self.control_functions = []
        self.config_functions = []

    def Tick(self, delta_t):
        for function in self.control_functions:
            function(delta_t)

        for function in self.config_functions:
            function(delta_t)

    def ApplyControl(self, control_index, control_value):
        self.control[control_index] = control_value

    def ApplyControls(self, control_array):
        for index in range(len(control_array)):
            if index < self.control.shape[0]:
                self.ApplyControl(index,control_array[index])

    def AddControlFunction(self, fn):
        self.control_functions.append(fn)

    def AddConfigFunction(self, fn):
        self.control_functions.append(fn)

    def BasicInfoStr(self):
        return "(%d) %s: %d/%d" % (self.id, self.name, self.config.shape[0], self.control.shape[0])

    def ConfigFloatString(self, dimensions=None):
        if dimensions is None:
            config_string = "%0.3f " * self.config.shape[0]
            return config_string % tuple(self.config)

        config_string = "%0.3f " * len(dimensions)
        return config_string % tuple(self.config[dimensions])


class OmniModel(MobileModel):
    def __init__(self, uid):
        super(OmniModel, self).__init__(uid, "Omni", 2, 2)

        # controls in this model are applied directly to changes in position
        self.AddControlFunction(self.ApplyPositionChanges)

    def ApplyPositionChanges(self, delta_t):
        #
        self.config += self.control * delta_t

class OmniModelWithAccel(MobileModel):
    def __init__(self, uid, accel_rate, max_speed):
        super(OmniModelWithAccel, self).__init__(uid, "Omni-Accel", 4, 2)

        # set specific params
        self.accel_rate = accel_rate
        self.max_speed = max_speed

        # controls in this model are applied to velocity and acceleration
        self.AddControlFunction(self.ApplyAccelUpdates)

        # position updates happen from velocity updates in each dimension
        self.AddConfigFunction(self.ApplyPositionChanges)

    def ApplyAccelUpdates(self, delta_t):
        #apply acceleration to the velocities
        self.config[2:] += self.control * self.accel_rate * delta_t

        # limit the speeds
        for limited in [2,3]:
            if self.config[limited] > self.max_speed:
                self.config[limited] = self.max_speed


    def ApplyPositionChanges(self, delta_t):
        # apply the vels to the positions
        self.config[:2] += self.config[2:] * delta_t

class BicycleModel(MobileModel):
    def __init__(self, uid, length, max_steering=np.deg2rad(30)):
        super(BicycleModel, self).__init__(uid, "Bicycle", 3, 2)

        self.length = length
        self.max_steering = max_steering

        # controls in this model are applied to position and heading
        self.AddConfigFunction(self.ApplyPositionChanges)

    def ApplyPositionChanges(self, delta_t):
        # controls for the bike are steering and heading
        self.config[0] += np.cos(self.config[2]) * self.control[0] * delta_t
        self.config[1] += np.sin(self.config[2]) * self.control[0] * delta_t
        self.config[2] += np.tan(self.control[1] * self.max_steering) / self.length * delta_t * self.control[0]
        if self.config[2] > np.pi * 2:
            self.config[2] -= np.pi * 2
        elif self.config[2] < 0:
            self.config[2] += np.pi * 2

def TestOmniVehicles():
    models = []
    om = OmniModel(1)
    models.append(om)
    om = OmniModelWithAccel(2, 1, 1)
    models.append(om)

    for model in models:
        print("Info:", model.BasicInfoStr())
        model.ApplyControl(0,1)

    time = 0.0
    max_time = 5.0
    delta_t = 0.1

    while time < max_time:
        for model in models:
            if time % 0.25 == 0 or 1:
                print("    %d: %s" % (model.id, model.ConfigFloatString()))
            model.Tick(delta_t)
        time += delta_t

    time = 0

def TestBicycles():
    models = []
    by = BicycleModel(1, 1.0)
    models.append(by)

    # om = OmniModelWithAccel(2, 1, 1)
    # models.append(om)

    for model in models:
        print("Info:", model.BasicInfoStr())
        model.ApplyControl(0,0.5)
        model.ApplyControl(1, 1)


    time = 0.0
    max_time = 15.0
    delta_t = 0.1

    while time < max_time:
        for model in models:
            if time % 0.25 == 0 or 1:
                print("    %d: %s" % (model.id, model.ConfigFloatString()))
            model.Tick(delta_t)
        time += delta_t

    time = 0

if __name__ == "__main__":
    #TestOmniVehicles()
    TestBicycles()
