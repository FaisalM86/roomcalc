
import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()

def execute_sql(conn, sql):
    """ Execute sql """
    try:
        c = conn.cursor()
        c.execute(sql)
    except Error as e:
        print(e)

def create_tables():
    """ Create tables in the SQLite database """
    database = "RoomCalc.db"

    sql_create_projects_table = """ CREATE TABLE IF NOT EXISTS projects (
                                        ProjectID INTEGER PRIMARY KEY,
                                        ProjectName TEXT NOT NULL,
                                        Client TEXT,
                                        Contract TEXT,
                                        SubContractor TEXT,
                                        DocumentNumber TEXT,
                                        Revision TEXT,
                                        RevisionDate TEXT,
                                        AmbientTempSummer REAL,
                                        AmbientTempWinter REAL,
                                        DefaultUValue REAL,
                                        Density REAL,
                                        HeatCapacity REAL
                                    ); """

    sql_create_rooms_table = """ CREATE TABLE IF NOT EXISTS rooms (
                                    RoomID INTEGER PRIMARY KEY,
                                    ProjectID INTEGER NOT NULL,
                                    RoomName TEXT NOT NULL,
                                    MinAirChangeRate REAL,
                                    MinVentilationPerArea REAL,
                                    MinVentilationPerPerson REAL,
                                    Remarks TEXT,
                                    FOREIGN KEY (ProjectID)
                                    REFERENCES projects (ProjectID)
                                ); """

    sql_create_surfaces_table = """ CREATE TABLE IF NOT EXISTS surfaces (
                                    SurfaceID INTEGER PRIMARY, 
                                    RoomID INTEGER NOT NULL,
                                    SurfaceType TEXT NOT NULL,
                                    Area REAL,
                                    UValue REAL,
                                    TemperatureOther REAL,
                                    FOREIGN KEY (RoomID)
                                    REFERENCES rooms (RoomID)
                                ); """

    sql_create_supply_systems_table = """ CREATE TABLE IF NOT EXISTS supply_systems (
                                            SupplySystemID INTEGER PRIMARY KEY,
                                            ProjectID INTEGER NOT NULL,
                                            SystemNo TEXT,
                                            SystemName TEXT,
                                            TempSupplyWinter REAL,
                                            TempSupplySummer REAL,
                                            CoolingEnthalpy REAL,
                                            FanHeat REAL,
                                            FOREIGN KEY (ProjectID)
                                            REFERENCES projects (ProjectID)
                                        ); """

    sql_create_room_supply_systems_table = """ CREATE TABLE IF NOT EXISTS room_supply_systems (
                                                RoomID INTEGER NOT NULL,
                                                SupplySystemID INTEGER NOT NULL,
                                                IncreaseDecrease REAL,
                                                RecircSystemName TEXT,
                                                ExtractSystemName TEXT,
                                                CoolAirTempSummer REAL,
                                                CoolAirTempWinter REAL,
                                                FOREIGN KEY (RoomID)
                                                REFERENCES rooms (RoomID),
                                                FOREIGN KEY (SupplySystemID)
                                                REFERENCES supply_systems (SupplySystemID)
                                            ); """

    sql_create_lights_table = """ CREATE TABLE IF NOT EXISTS lights (
                                    LightID INTEGER PRIMARY KEY,
                                    RoomID INTEGER NOT NULL,
                                    LightDescription TEXT,
                                    HeatLoadSummer REAL,
                                    HeatLoadWinter REAL,
                                    ApplySummer INTEGER,
                                    ApplyWinter INTEGER,
                                    FOREIGN KEY (RoomID)
                                    REFERENCES rooms (RoomID)
                                ); """

    sql_create_personnel_table = """ CREATE TABLE IF NOT EXISTS personnel (
                                        PersonnelID INTEGER PRIMARY KEY,
                                        RoomID INTEGER NOT NULL,
                                        Quantity INTEGER,
                                        HeatLoadPerPersonSummer REAL,
                                        HeatLoadPerPersonWinter REAL,
                                        ApplySummer INTEGER,
                                        ApplyWinter INTEGER,
                                        FOREIGN KEY (RoomID)
                                        REFERENCES rooms (RoomID)
                                    ); """

    sql_create_equipment_table = """ CREATE TABLE IF NOT EXISTS equipment (
                                        EquipmentID INTEGER PRIMARY KEY,
                                        RoomID INTEGER NOT NULL,
                                        EquipmentDescription TEXT,
                                        HeatLoadSummer REAL,
                                        HeatLoadWinter REAL,
                                        ApplySummer INTEGER,
                                        ApplyWinter INTEGER,
                                        FOREIGN KEY (RoomID)
                                        REFERENCES rooms (RoomID)
                                    ); """

    # create a database connection
    conn = sqlite3.connect(database)

    # create tables
    if conn is not None:
        execute_sql(conn, sql_create_projects_table)
        execute_sql(conn, sql_create_rooms_table)
        execute_sql(conn, sql_create_surfaces_table)
        execute_sql(conn, sql_create_supply_systems_table)
        execute_sql(conn, sql_create_room_supply_systems_table)
        execute_sql(conn, sql_create_lights_table)
        execute_sql(conn, sql_create_personnel_table)
        execute_sql(conn, sql_create_equipment_table)
        conn.commit()
    else:
        print("Error! cannot create the database connection.")

    conn.close()

if __name__ == '__main__':
    create_tables()
