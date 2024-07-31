# calculations.py
# Contains the logic for performing thermal calculations for the RoomCalc application

from data_access import get_room_data, get_surface_data, get_supply_system_data, get_personnel_data, get_equipment_data, get_light_data, update_room_calculations
from models import Room, Surface, SupplySystem, Personnel, Equipment, Light

def calculate_heat_gain_from_surfaces(surfaces, room_temp_summer, ambient_temp_summer, room_temp_winter, ambient_temp_winter):
    """ Calculate total heat gain from all surfaces in a room for both summer and winter """
    total_heat_gain_summer = 0
    total_heat_gain_winter = 0
    for surface in surfaces:
        # Heat gain from a surface = Area * UValue * (TemperatureOther - RoomTemperature)
        heat_gain_summer = surface['Area'] * surface['UValue'] * (ambient_temp_summer - room_temp_summer)
        heat_gain_winter = surface['Area'] * surface['UValue'] * (ambient_temp_winter - room_temp_winter)
        total_heat_gain_summer += heat_gain_summer
        total_heat_gain_winter += heat_gain_winter
    return total_heat_gain_summer, total_heat_gain_winter

def calculate_heat_gain_from_personnel(personnel):
    """ Calculate total heat gain from personnel in a room """
    total_heat_gain = 0
    for person in personnel:
        # Total heat gain from one person = HeatLoadPerPersonSummer * Quantity
        heat_gain = person.HeatLoadPerPersonSummer * person.Quantity
        total_heat_gain += heat_gain
    return total_heat_gain

def calculate_heat_gain_from_equipment(equipment):
    """ Calculate total heat gain from equipment in a room """
    total_heat_gain = 0
    for equip in equipment:
        # Total heat gain from one equipment item = HeatLoadSummer * ApplySummer
        heat_gain = equip.HeatLoadSummer * (1 if equip.ApplySummer else 0)
        total_heat_gain += heat_gain
    return total_heat_gain

def calculate_heat_gain_from_lights(lights):
    """ Calculate total heat gain from lighting in a room """
    total_heat_gain = 0
    for light in lights:
        # Total heat gain from one light = HeatLoadSummer * ApplySummer
        heat_gain = light.HeatLoadSummer * (1 if light.ApplySummer else 0)
        total_heat_gain += heat_gain
    return total_heat_gain

def calculate_total_heat_gain(room_id):
    """ Calculate the total heat gain for a room """
    surfaces = get_surface_data(room_id)
    personnel = get_personnel_data(room_id)
    equipment = get_equipment_data(room_id)
    lights = get_light_data(room_id)

    heat_gain_surfaces = calculate_heat_gain_from_surfaces(surfaces)
    heat_gain_personnel = calculate_heat_gain_from_personnel(personnel)
    heat_gain_equipment = calculate_heat_gain_from_equipment(equipment)
    heat_gain_lights = calculate_heat_gain_from_lights(lights)

    total_heat_gain = heat_gain_surfaces + heat_gain_personnel + heat_gain_equipment + heat_gain_lights
    return total_heat_gain

def calculate_airflow_rates(room):
    """ Calculate the required airflow rates for a room based on minimum requirements """
    # Airflow rate calculations based on minimum air change rate, ventilation per area, and per person
    air_change_rate_flow = room.MinAirChangeRate * room.Volume  # Assuming room volume is calculated and stored in Room model
    ventilation_area_flow = room.MinVentilationPerArea * room.Area
    ventilation_person_flow = room.MinVentilationPerPerson * room.Occupancy  # Assuming Occupancy is calculated/stored

    required_airflow = max(air_change_rate_flow, ventilation_area_flow, ventilation_person_flow)
    return required_airflow

def calculate_room_parameters(room_id):
    """ Perform all calculations for a room and update the database with results """
    room = get_room_data(room_id)
    total_heat_gain = calculate_total_heat_gain(room_id)
    required_airflow = calculate_airflow_rates(room)

    # Update room with calculated values (this function should be implemented in data_access.py)
    update_room_calculations(room_id, total_heat_gain, required_airflow)

# Example usage
if __name__ == "__main__":
    room_id = 1  # Replace with actual room ID
    calculate_room_parameters(room_id)
