-- Создание пользовательского типа ENUM для типов контрольных точек
CREATE TYPE checkpoint_type AS ENUM ('entry', 'exit', 'intermediate');

-- Таблица сотрудников
CREATE TABLE Employee (
    ID INT PRIMARY KEY,
    Name VARCHAR(100) NOT NULL,
    RFID_Tag VARCHAR(50) UNIQUE NOT NULL
);

-- Таблица опасных зон
CREATE TABLE Hazardous_Area (
    ID INT PRIMARY KEY,
    Name VARCHAR(100) NOT NULL,
    Coordinates TEXT NOT NULL
);

-- Таблица контрольных точек
CREATE TABLE Checkpoint (
    ID INT PRIMARY KEY,
    Hazardous_Area_ID INT NOT NULL,
    Coordinates TEXT NOT NULL,
    Type checkpoint_type NOT NULL,
    FOREIGN KEY (Hazardous_Area_ID) REFERENCES Hazardous_Area(ID)
);

-- Таблица сессий мониторинга
CREATE TABLE Monitoring_Session (
    ID INT PRIMARY KEY,
    Employee_ID INT NOT NULL,
    Hazardous_Area_ID INT NOT NULL,
    Start_Time TIMESTAMP NOT NULL,
    End_Time TIMESTAMP,
    Violations_Count INT DEFAULT 0,
    Report_Link VARCHAR(255),
    FOREIGN KEY (Employee_ID) REFERENCES Employee(ID),
    FOREIGN KEY (Hazardous_Area_ID) REFERENCES Hazardous_Area(ID)
);

-- Таблица уведомлений
CREATE TABLE Notification (
    ID INT PRIMARY KEY,
    Monitoring_Session_ID INT NOT NULL,
    Timestamp TIMESTAMP NOT NULL,
    Violation_Type VARCHAR(50) NOT NULL,
    Description TEXT,
    FOREIGN KEY (Monitoring_Session_ID) REFERENCES Monitoring_Session(ID)
);